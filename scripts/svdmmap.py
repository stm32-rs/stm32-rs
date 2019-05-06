"""
svdmmap.py

Copyright 2019 Adam Greig.
Licensed under the MIT and Apache 2.0 licenses. See LICENSE files for details.
"""

import sys
import copy
import xml.etree.ElementTree as ET


def iter_clusters(ptag):
    registers = ptag.find('registers')
    if registers is None:
        return []
    else:
        return registers.findall('cluster')


def iter_registers(ptag):
    registers = ptag.find('registers')
    if registers is None:
        return []
    else:
        return registers.findall('register')


def iter_fields(rtag):
    fields = rtag.find('fields')
    if fields is None:
        return []
    else:
        return fields.findall('field')


ACCESS = {
    "read-only": "ro",
    "read-write": "rw",
    "write-only": "wo",
}


def get_access(tag):
    """
    Reads and formats the access attribute of the tag.
    If possible it is shortened to ro/rw/wo, and then
    returned inside brackets with a leading space.
    """
    access = get_string(tag, 'access')
    if access is not None:
        return " (" + ACCESS.get(access, access) + ")"
    else:
        return ""


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


def expand_dim(node):
    """
    Given a node (a cluster or a register) which may have a `dim` child,
    returns an expanded list of all such nodes with '%s' in the name replaced
    by the appropriate index. If there is no `dim` child, a list containing
    just the original node is returned.
    """
    dim = node.findtext('dim')
    if dim is None:
        return [node]
    inc = get_int(node, 'dimIncrement')
    idxs = get_string(node, 'dimIndex')
    if idxs is None:
        idxs = list(range(dim))
    else:
        if "," in idxs:
            idxs = idxs.split(",")
        elif "-" in idxs:
            li, ri = idxs.split("-")
            idxs = list(range(int(li), int(ri)+1))
        else:
            raise ValueError(f"Unknown dimIndex: '{idxs}'")
    nodes = []
    for cnt, idx in enumerate(idxs):
        name = get_string(node, 'name').replace("%s", str(idx))
        dim_node = copy.deepcopy(node)
        dim_node.find('name').text = name
        addr = get_int(dim_node, 'addressOffset') + cnt * inc
        dim_node.find('addressOffset').text = f"0x{addr:08x}"
        dim_node.attrib['dim_index'] = idx
        nodes.append(dim_node)
    return nodes


def expand_cluster(node):
    """
    Given a cluster, returns a list of all registers inside the cluster,
    with their names updated to include the cluster index and their address
    offsets updated to include the cluster address offset.
    The returned register nodes are as though they were never in a cluster.
    """
    if node.attrib.get('dim_index') is None:
        raise ValueError("Can't process cluster without dim_index")
    cluster_idx = node.attrib['dim_index']
    cluster_addr = get_int(node, 'addressOffset')
    nodes = []
    for rtag in node.findall('register'):
        addr = cluster_addr + get_int(rtag, 'addressOffset')
        name = get_string(rtag, 'name') + str(cluster_idx)
        new_rtag = copy.deepcopy(rtag)
        new_rtag.find('addressOffset').text = f"0x{addr:08x}"
        new_rtag.find('name').text = name
        nodes.append(new_rtag)
    return nodes


def parse_register(rtag):
    """
    Extract register and field information from a register node into a dict.
    """
    fields = {}
    rname = get_string(rtag, 'name')
    rdesc = get_string(rtag, 'description')
    raccess = get_access(rtag)
    roffset = get_int(rtag, 'addressOffset')
    for ftag in iter_fields(rtag):
        fname = get_string(ftag, 'name')
        foffset = get_int(ftag, 'bitOffset')
        fwidth = get_int(ftag, 'bitWidth')
        fdesc = get_string(ftag, 'description')
        faccess = get_access(ftag)
        fields[fname] = {"name": fname, "offset": foffset,
                         "width": fwidth, "description": fdesc,
                         "access": faccess}
    return {"name": rname, "offset": roffset, "description": rdesc,
            "access": raccess, "fields": fields}


def parse(svdfile):
    """
    Parse SVD file into dict of peripherals, registers, and fields.
    """
    tree = ET.parse(svdfile)
    peripherals = {}
    device_interrupts = {}
    for ptag in tree.find('peripherals').findall('peripheral'):
        interrupts = {}
        registers = {}
        clusters = {}
        pname = get_string(ptag, 'name')
        pbase = get_int(ptag, 'baseAddress')
        for itag in ptag.findall('interrupt'):
            iname = get_string(itag, 'name')
            idesc = get_string(itag, 'description')
            ival = get_int(itag, 'value')
            interrupt = {"name": iname, "description": idesc, "value": ival,
                         "pname": pname}
            interrupts[iname] = device_interrupts[ival] = interrupt
        for ctag in iter_clusters(ptag):
            for ctag in expand_dim(ctag):
                cname = get_string(ctag, 'name')
                cdesc = get_string(ctag, 'description')
                coff = get_int(ctag, 'addressOffset')
                for rtag in expand_cluster(ctag):
                    register = parse_register(rtag)
                    registers[register['name']] = register
                clusters[cname] = {"name": cname, "description": cdesc,
                                   "offset": coff}
        for rtag in iter_registers(ptag):
            for rtag in expand_dim(rtag):
                register = parse_register(rtag)
                registers[register['name']] = register
        peripherals[pname] = {"name": pname, "base": pbase,
                              "interrupts": interrupts, "registers": registers,
                              "clusters": clusters}
        if 'derivedFrom' in ptag.attrib:
            peripherals[pname]["derives"] = ptag.attrib["derivedFrom"]
    for pname, periph in list(peripherals.items()):
        if 'derives' in periph:
            peripherals[pname]['registers'] = \
                peripherals[periph['derives']]['registers']
    return {"name": svdfile.split(".")[0], "peripherals": peripherals,
            "interrupts": device_interrupts}


def to_text(device):
    """
    Output sorted text of every peripheral, register, field, and interrupt
    in the device, such that automated diffing is possible.
    """
    mmap = []
    for i in device['interrupts'].values():
        mmap.append(f"INTERRUPT {i['value']:03d}: "
                    + f"{i['name']} ({i['pname']}): {i['description']}")
    for p in device['peripherals'].values():
        mmap.append(f"0x{p['base']:08X} A PERIPHERAL {p['name']}")
        for c in p['clusters'].values():
            addr = p['base'] + c['offset']
            mmap.append(f"0x{addr:08X} B  CLUSTER {c['name']}: "
                        + f"{c['description']}")
        for r in p['registers'].values():
            addr = p['base'] + r['offset']
            mmap.append(f"0x{addr:08X} B  REGISTER {r['name']}{r['access']}: "
                        + f"{r['description']}")
            for f in r['fields'].values():
                offset, width = f['offset'], f['width']
                mmap.append(f"0x{addr:08X} C   FIELD {offset:02d}w{width:02d} "
                            + f"{f['name']}{f['access']}: "
                            + f"{f['description']}")
    return "\n".join(sorted(mmap))


def main():
    device = parse(sys.argv[1])
    print(to_text(device))


if __name__ == "__main__":
    main()
