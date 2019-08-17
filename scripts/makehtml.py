"""
makehtml.py
Copyright 2017, 2018 Adam Greig
Licensed under the MIT and Apache 2.0 licenses.

Generates a webpage for a given SVD file containing details on every
peripheral and register and their level of coverage.
"""

import shutil
import sys
import os.path
import argparse
if sys.platform == 'win32':
    import multiprocessing.pool
else:
    import multiprocessing
import xml.etree.ElementTree as ET
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('makehtml', ''))


def generate_index_page(devices):
    print("Generating Index")
    template = env.get_template('makehtml.index.template.html')
    return template.render(devices=devices)


def generate_device_page(device):
    template = env.get_template('makehtml.template.html')
    return template.render(device=device)


def short_access(accs):
    return {
        "read-write": "rw", "read-only": "r", "write-only": "w"
    }.get(accs, "N/A")


def parse_device(svdfile):
    tree = ET.parse(svdfile)
    temp = os.stat(svdfile).st_mtime
    dname = tree.findtext('name')
    peripherals = {}
    device_fields_total = 0
    device_fields_documented = 0
    for ptag in tree.iter('peripheral'):
        registers = {}
        peripheral_fields_total = 0
        peripheral_fields_documented = 0
        pname = ptag.findtext('name')
        pbase = ptag.findtext('baseAddress')
        if 'derivedFrom' in ptag.attrib:
            dfname = ptag.attrib['derivedFrom']
            dffrom = tree.findall(".//peripheral/[name='" + dfname + "']")
            if dffrom:
                ptag = dffrom[0]
            else:
                print("Can't find derivedFrom={} for {}"
                      .format(dfname, pname))
                continue
        pdesc = ptag.findtext('description')
        for rtag in ptag.iter('register'):
            fields = {}
            register_fields_total = 0
            register_fields_documented = 0
            rname = rtag.findtext('name')
            rdesc = rtag.findtext('description')
            rrstv = rtag.findtext('resetValue')
            raccs = rtag.findtext('access') or "Unspecified"
            roffset = int(rtag.findtext('addressOffset'), 16)
            for ftag in rtag.iter('field'):
                register_fields_total += 1
                fname = ftag.findtext('name')
                fdesc = ftag.findtext('description')
                # Some svd files will specify a bitRange rather than
                # bitOffset and bitWidth
                frange = ftag.findtext('bitRange')
                if frange:
                    parts = frange[1:-1].split(':')
                    end = int(parts[0])
                    start = int(parts[1])
                    foffset = start
                    fwidth = end - start + 1
                else:
                    foffset = int(ftag.findtext('bitOffset'))
                    fwidth = int(ftag.findtext('bitWidth'))
                faccs = ftag.findtext('access') or raccs
                enum = ftag.find('enumeratedValues')
                wc = ftag.find('writeConstraint')
                doc = False
                if enum is not None or wc is not None or faccs == "read-only":
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
                            doc += value.findtext('value')
                            doc += ": "
                            doc += value.findtext('name')
                            doc += "</strong>: "
                            doc += value.findtext('description')
                            doc += "<br>"
                    elif wc is not None:
                        wcrange = wc.find('range')
                        if wcrange is not None:
                            mn = wcrange.findtext('minimum')
                            mx = wcrange.findtext('maximum')
                            doc = "Allowed values: {}-{}".format(mn, mx)
                fields[foffset] = {"name": fname, "offset": foffset,
                                   "width": fwidth, "description": fdesc,
                                   "doc": doc, "access": faccs}
            table = [[{"name": "", "width": 1, "doc": False}
                      for _ in range(16)] for _ in range(2)]
            for foffset in reversed(sorted(fields.keys())):
                fwidth = fields[foffset]['width']
                fname = fields[foffset]['name']
                fdoc = bool(fields[foffset]['doc'])
                faccs = fields[foffset]['access']
                for idx in range(foffset, foffset + fwidth):
                    trowidx = (31 - idx)//16
                    tcolidx = 15 - (idx % 16)
                    tcell = table[trowidx][tcolidx]
                    tcell['name'] = fname
                    tcell['doc'] = fdoc
                    tcell['access'] = short_access(faccs)
                    tcell['separated'] = foffset < 16 and foffset + fwidth > 16
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
            registers[roffset] = {"name": rname,
                                  "offset": "0x{:X}".format(roffset),
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
            "fields_documented": device_fields_documented,
            "last-modified": temp, "svdfile": svdfile}


def process_svd(svdfile):
    print("Processing", svdfile)
    device = parse_device(svdfile)
    return device


def generate_if_newer(device):
    pagename = "{}.html".format(device["name"])
    filename = os.path.join(args.htmldir, pagename)
    isfile = os.path.isfile(filename)
    if not isfile or os.stat(filename).st_mtime < device['last-modified']:
        page = generate_device_page(device)
        print("Generating", pagename)
        with open(filename, "w") as f:
            f.write(page)
        shutil.copy(device["svdfile"], args.htmldir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("htmldir", help="Path to write HTML files to")
    parser.add_argument("svdfiles", help="Path to patched SVD files", nargs="*")
    args = parser.parse_args()
    devices = {}

    with multiprocessing.pool.ThreadPool() if sys.platform == 'win32' else multiprocessing.Pool() as p:
        devices = p.map(process_svd, args.svdfiles)
        p.map(generate_if_newer, devices)
    devices = {d['name']: d for d in devices}
    index_page = generate_index_page(devices)
    with open(os.path.join(args.htmldir, "index.html"), "w") as f:
        f.write(index_page)
