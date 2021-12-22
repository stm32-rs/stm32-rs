"""
makehtml.py
Copyright 2017, 2018 Adam Greig
Licensed under the MIT and Apache 2.0 licenses.

Generates a webpage for a given SVD file containing details on every
peripheral and register and their level of coverage.
"""

import shutil
import copy
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


def iter_clusters(ptag):
    registers = ptag.find("registers")
    if registers is None:
        return []
    else:
        return registers.findall("cluster")


def iter_registers(ptag):
    registers = ptag.find("registers")
    if registers is None:
        return []
    else:
        return registers.findall("register")


def iter_fields(rtag):
    fields = rtag.find("fields")
    if fields is None:
        return []
    else:
        return fields.findall("field")


def get_string(node, tag, default=None):
    text = node.findtext(tag, default=default)
    if text == default:
        return text
    return " ".join(text.split())


def get_int(node, tag, default=None):
    text = get_string(node, tag, default=default)
    if text == default:
        return text
    text = text.lower().strip()
    if text == "true":
        return 1
    elif text == "false":
        return 0
    elif text[:2] == "0x":
        return int(text[2:], 16)
    elif text[:2] == "0b":
        return int(text[2:], 2)
    else:
        return int(text, 10)


def expand_dim(node, field=False):
    """
    Given a node (a cluster, a register or a field) which may have a `dim` child,
    returns an expanded list of all such nodes with '%s' in the name replaced
    by the appropriate index. If there is no `dim` child, a list containing
    just the original node is returned.
    """
    dim = node.findtext("dim")
    if dim is None:
        return [node]
    inc = get_int(node, "dimIncrement")
    idxs = get_string(node, "dimIndex")
    if idxs is None:
        idxs = list(range(int(dim, 0)))
    else:
        if len(idxs) == 1:
            pass
        elif "," in idxs:
            idxs = idxs.split(",")
        elif "-" in idxs:
            li, ri = idxs.split("-")
            idxs = list(range(int(li), int(ri) + 1))
        else:
            raise ValueError(f"Unknown dimIndex: '{idxs}'")
    nodes = []
    for cnt, idx in enumerate(idxs):
        name = get_string(node, "name").replace("%s", f"[{idx}]")
        description = get_string(node, "description").replace("%s", str(idx))
        dim_node = copy.deepcopy(node)
        dim_node.find("name").text = name
        dim_node.find("description").text = description
        if field:
            offset = get_int(dim_node, "bitOffset") + cnt * inc
            dim_node.find("bitOffset").text = f"{offset}"
        else:
            addr = get_int(dim_node, "addressOffset") + cnt * inc
            dim_node.find("addressOffset").text = f"0x{addr:08x}"
        dim_node.attrib["dim_index"] = str(idx)
        nodes.append(dim_node)
    return nodes


def expand_cluster(node):
    """
    Given a cluster, returns a list of all registers inside the cluster,
    with their names updated to include the cluster index and their address
    offsets updated to include the cluster address offset.
    The returned register nodes are as though they were never in a cluster.
    """
    if node.attrib.get("dim_index") is None:
        raise ValueError("Can't process cluster without dim_index")
    cluster_idx = node.attrib["dim_index"]
    cluster_addr = get_int(node, "addressOffset")
    nodes = []
    for rtag in node.findall("register"):
        addr = cluster_addr + get_int(rtag, "addressOffset")
        name = f"{get_string(rtag, 'name')} [{cluster_idx}]"
        new_rtag = copy.deepcopy(rtag)
        new_rtag.find("addressOffset").text = f"0x{addr:08x}"
        new_rtag.find("name").text = name
        nodes.append(new_rtag)
    return nodes


def parse_register(rtag):
    fields = {}
    register_fields_total = 0
    register_fields_documented = 0
    rname = get_string(rtag, 'name')
    rdesc = get_string(rtag, 'description')
    rrstv = get_string(rtag, 'resetValue')
    raccs = get_string(rtag, 'access') or "Unspecified"
    roffset = get_int(rtag, 'addressOffset')
    for ftag in iter_fields(rtag):
        register_fields_total += 1
        fname = get_string(ftag, 'name')
        fdesc = get_string(ftag, 'description')
        # Some svd files will specify a bitRange rather than
        # bitOffset and bitWidth
        frange = get_string(ftag, 'bitRange')
        if frange:
            parts = frange[1:-1].split(':')
            end = int(parts[0], 0)
            start = int(parts[1], 0)
            foffset = start
            fwidth = end - start + 1
        else:
            foffset = get_int(ftag, 'bitOffset')
            fwidth = get_int(ftag, 'bitWidth')
        faccs = get_string(ftag, 'access') or raccs
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
                    doc += get_string(value, 'value')
                    doc += ": "
                    doc += get_string(value, 'name')
                    doc += "</strong>: "
                    doc += get_string(value, 'description')
                    doc += "<br>"
            elif wc is not None:
                wcrange = wc.find('range')
                if wcrange is not None:
                    mn = hex(get_int(wcrange, 'minimum'))
                    mx = hex(get_int(wcrange, 'maximum'))
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
    return (roffset, rname), {
        "name": rname,
        "offset": hex(roffset),
        "description": rdesc,
        "resetValue": rrstv,
        "access": raccs,
        "fields": fields,
        "table": table,
        "fields_total": register_fields_total,
        "fields_documented": register_fields_documented
    }


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
        pname = get_string(ptag, 'name')
        pbase = hex(get_int(ptag, 'baseAddress'))
        if 'derivedFrom' in ptag.attrib:
            dfname = ptag.attrib['derivedFrom']
            dffrom = tree.findall(".//peripheral/[name='" + dfname + "']")
            if dffrom:
                ptag = dffrom[0]
            else:
                print("Can't find derivedFrom={} for {}"
                      .format(dfname, pname))
                continue
        pdesc = get_string(ptag, 'description')
        for ctag in iter_clusters(ptag):
            for ctag in expand_dim(ctag):
                for rtag in expand_cluster(ctag):
                    key, register = parse_register(rtag)
                    registers[key] = register
                    peripheral_fields_total += register['fields_total']
                    peripheral_fields_documented += register['fields_documented']
        for rtag in iter_registers(ptag):
            for rtag in expand_dim(rtag):
                key, register = parse_register(rtag)
                registers[key] = register
                peripheral_fields_total += register['fields_total']
                peripheral_fields_documented += register['fields_documented']
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


def generate_if_newer(arg):
    device, htmldir = arg
    pagename = "{}.html".format(device["name"])
    filename = os.path.join(htmldir, pagename)
    isfile = os.path.isfile(filename)
    if not isfile or os.stat(filename).st_mtime < device['last-modified']:
        page = generate_device_page(device)
        print("Generating", pagename)
        with open(filename, "w", encoding='utf-8') as f:
            f.write(page)
        shutil.copy(device["svdfile"], htmldir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("htmldir", help="Path to write HTML files to")
    parser.add_argument("svdfiles", help="Path to patched SVD files", nargs="*")
    args = parser.parse_args()
    devices = {}
    with multiprocessing.pool.ThreadPool() if sys.platform == 'win32' else multiprocessing.Pool() as p:
        devices = p.map(process_svd, args.svdfiles)
        p.map(generate_if_newer, [(device, args.htmldir) for device in devices])
    devices = {d['name']: d for d in devices}
    index_page = generate_index_page(devices)
    with open(os.path.join(args.htmldir, "index.html"), "w", encoding='utf-8') as f:
        f.write(index_page)
