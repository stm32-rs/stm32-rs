"""
makejson.py
Copyright 2017 Adam Greig
Licensed under the MIT and Apache 2.0 licenses.

Transforms the given SVD files into a JSON format more suited for
web pages.
"""

import os.path
import argparse
import xml.etree.ElementTree as ET
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader('makehtml', ''),
                  autoescape=select_autoescape(['html']))


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
            # peripherals[pname] = {"name": pname, "base": pbase}
            # peripherals[pname]["derivedFrom"] = ptag.attrib["derivedFrom"]
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
            roffset = int(rtag.find('addressOffset').text, 0)
            for ftag in rtag.iter('field'):
                register_fields_total += 1
                fname = ftag.find('name').text
                fdesc = ftag.find('description').text
                foffset = int(ftag.find('bitOffset').text, 0)
                fwidth = int(ftag.find('bitWidth').text, 0)
                enum = ftag.find('enumeratedValues')
                if enum is not None:
                    register_fields_documented += 1
                fields[fname] = {"name": fname, "offset": foffset,
                                 "width": fwidth, "description": fdesc}
            registers[rname] = {"name": rname, "offset": roffset,
                                "description": rdesc, "resetValue": rrstv,
                                "access": raccs, "fields": fields,
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
    for svdfile in args.svdfiles:
        print("Processing", svdfile)
        device = parse_device(svdfile)
        page = generate_device_page(device)
        pagename = "{}.html".format(device["name"])
        with open(os.path.join(args.htmldir, pagename), "w") as f:
            f.write(page)
