"""
periphtemplate.py
Copyright 2018 Adam Greig
Licensed under the MIT and Apache 2.0 licenses.

Generates a YAML template for describing fields in a peripheral's registers
from a provided SVD file.
"""

import argparse
import xml.etree.ElementTree as ET


def parse_periph(svdfile, pname):
    tree = ET.parse(svdfile)
    ptag = tree.find(".//peripheral/[name='" + pname + "']")
    if not ptag:
        print("Can't find peripheral {} in device".format(pname))
        return
    if 'derivedFrom' in ptag.attrib:
        dfname = ptag.attrib['derivedFrom']
        dffrom = tree.find(".//peripheral/[name='" + dfname + "']")
        if dffrom:
            ptag = dffrom
        else:
            print("Can't find derivedFrom={} for {}".format(dfname, pname))
            return
    registers = {}
    for rtag in ptag.iter('register'):
        fields = {}
        rname = rtag.find('name').text
        roffset = int(rtag.find('addressOffset').text, 0)
        for ftag in rtag.iter('field'):
            fname = ftag.find('name').text
            foffset = int(ftag.find('bitOffset').text, 0)
            fwidth = int(ftag.find('bitWidth').text, 0)
            fields[foffset] = {"name": fname, "width": fwidth}
        registers[roffset] = {"name": rname, "fields": fields}
    return registers


def make_template(pname, registers):
    out = ["", '"{}":'.format(pname)]
    for roffset in sorted(registers.keys()):
        register = registers[roffset]
        rname = register['name']
        out.append("  {}:".format(rname))
        for foffset in reversed(sorted(register['fields'].keys())):
            field = register['fields'][foffset]
            fname = field['name']
            fwidth = field['width']
            out.append("    {}:".format(fname))
            if fwidth == 1 and fname.endswith("E"):
                out.append('      Disabled: [0, ""]')
                out.append('      Enabled: [1, ""]')
            elif fwidth == 1 and fname.endswith("D"):
                out.append('      Enabled: [0, ""]')
                out.append('      Disabled: [1, ""]')
        out.append("")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("svdfile", help="Path to read SVD file from")
    parser.add_argument("peripheral", help="Name of peripheral to template")
    parser.add_argument("yamlfile", help="YAML file to write out")
    args = parser.parse_args()
    registers = parse_periph(args.svdfile, args.peripheral)
    if not registers:
        print("Parsing device failed")
        return
    tpl = make_template(args.peripheral, registers)
    with open(args.yamlfile, "w") as f:
        f.write(tpl)


if __name__ == "__main__":
    main()
