"""
makehtml.py
Copyright 2017, 2018 Adam Greig
Licensed under the MIT and Apache 2.0 licenses.

Generates a webpage for a given SVD file containing details on every
peripheral and register and their level of coverage.
"""

import os.path
import argparse
import xml.etree.ElementTree as ET
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('makehtml', ''))


def generate_index_page(devices):
    template = env.get_template('makehtml.index.template.html')
    return template.render(devices=devices)


def generate_device_page(device):
    template = env.get_template('makehtml.template.html')
    return template.render(device=device)


def parse_device(svdfile):
    tree = ET.parse(svdfile)
    dname = tree.find('name').text
    peripherals = {}
    device_fields_total = 0
    device_fields_documented = 0
    for ptag in tree.iter('peripheral'):
        registers = {}
        peripheral_fields_total = 0
        peripheral_fields_documented = 0
        pname = ptag.find('name').text
        pbase = ptag.find('baseAddress').text
        if 'derivedFrom' in ptag.attrib:
            dfname = ptag.attrib['derivedFrom']
            dffrom = tree.findall(".//peripheral/[name='" + dfname + "']")
            if dffrom:
                ptag = dffrom[0]
            else:
                print("Can't find derivedFrom={} for {}"
                      .format(dfname, pname))
                continue
        pdesc = ptag.find('description').text
        for rtag in ptag.iter('register'):
            fields = {}
            register_fields_total = 0
            register_fields_documented = 0
            rname = rtag.find('name').text
            rdesc = rtag.find('description').text
            rrstv = rtag.find('resetValue').text
            raccs = rtag.find('access')
            if raccs is not None:
                raccs = raccs.text
            else:
                raccs = "Unspecified"
            roffset = int(rtag.find('addressOffset').text, 16)
            for ftag in rtag.iter('field'):
                register_fields_total += 1
                fname = ftag.find('name').text
                fdesc = ftag.find('description').text
                foffset = int(ftag.find('bitOffset').text)
                fwidth = int(ftag.find('bitWidth').text)
                enum = ftag.find('enumeratedValues')
                wc = ftag.find('writeConstraint')
                doc = False
                if enum is not None or wc is not None or raccs == "read-only":
                    register_fields_documented += 1
                    if enum is not None:
                        doc = "Allowed values:<br>"
                        if 'derivedFrom' in enum.attrib:
                            dfname = enum.attrib['derivedFrom']
                            dffrom = rtag.findall(
                                ".//enumeratedValues/[name='" + dfname + "']")
                            if dffrom:
                                enum = dffrom[0]
                        for value in enum.iter('enumeratedValue'):
                            doc += "<strong>"
                            doc += value.find('value').text
                            doc += ": "
                            doc += value.find('name').text
                            doc += "</strong>: "
                            doc += value.find('description').text
                            doc += "<br>"
                    elif wc is not None:
                        wcrange = wc.find('range')
                        if wcrange is not None:
                            mn = wcrange.find('minimum').text
                            mx = wcrange.find('maximum').text
                            doc = "Allowed values: {}-{}".format(mn, mx)
                fields[foffset] = {"name": fname, "offset": foffset,
                                   "width": fwidth, "description": fdesc,
                                   "doc": doc}
            table = [[{"name": "", "width": 1, "doc": False}
                      for _ in range(16)] for _ in range(2)]
            for foffset in reversed(sorted(fields.keys())):
                fwidth = fields[foffset]['width']
                fname = fields[foffset]['name']
                fdoc = bool(fields[foffset]['doc'])
                for idx in range(foffset, foffset + fwidth):
                    trowidx = (31 - idx)//16
                    tcolidx = 15 - (idx % 16)
                    table[trowidx][tcolidx]['name'] = fname
                    table[trowidx][tcolidx]['doc'] = fdoc
            for trow in table:
                idx = 0
                while idx < len(trow)-1:
                    if trow[idx]['name'] == trow[idx+1]['name']:
                        trow[idx]['width'] += 1
                        del trow[idx+1]
                        continue
                    idx += 1
            table = [
                {"headers": reversed(list(range(16, 32))), "fields": table[0]},
                {"headers": reversed(list(range(0, 16))), "fields": table[1]}]
            # Bodge to prevent /0 when there are no fields in a register
            if register_fields_total == 0:
                register_fields_total = 1
            registers[roffset] = {"name": rname, "offset": hex(roffset),
                                  "description": rdesc, "resetValue": rrstv,
                                  "access": raccs, "fields": fields,
                                  "table": table,
                                  "fields_total": register_fields_total,
                                  "fields_documented":
                                      register_fields_documented}
            peripheral_fields_total += register_fields_total
            peripheral_fields_documented += register_fields_documented
        peripherals[pname] = {"name": pname, "base": pbase,
                              "description": pdesc, "registers": registers,
                              "fields_total": peripheral_fields_total,
                              "fields_documented":
                                  peripheral_fields_documented}
        device_fields_total += peripheral_fields_total
        device_fields_documented += peripheral_fields_documented
    return {"name": dname, "peripherals": peripherals,
            "fields_total": device_fields_total,
            "fields_documented": device_fields_documented}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("htmldir", help="Path to write HTML files to")
    parser.add_argument("svdfiles", help="Path to patched SVD files",
                        nargs="*")
    args = parser.parse_args()
    devices = {}
    for svdfile in args.svdfiles:
        print("Processing", svdfile)
        device = parse_device(svdfile)
        devices[device['name']] = device
        page = generate_device_page(device)
        pagename = "{}.html".format(device["name"])
        with open(os.path.join(args.htmldir, pagename), "w") as f:
            f.write(page)
    index_page = generate_index_page(devices)
    with open(os.path.join(args.htmldir, "index.html"), "w") as f:
        f.write(index_page)
