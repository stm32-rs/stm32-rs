"""
svdpatch.py

Copyright 2017 Adam Greig.
Licensed under the MIT and Apache 2.0 licenses. See LICENSE files for details.
"""

import yaml
import os.path
import argparse
import xml.etree.ElementTree as ET
from fnmatch import fnmatch
from collections import OrderedDict


# Set up pyyaml to use ordered dicts so we generate the same
# XML output each time
def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
yaml.add_constructor(_mapping_tag, dict_constructor)


def parseargs():
    """Parse our command line arguments, returns a Namespace of results."""
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml", help="Path to YAML file to load")
    args = parser.parse_args()
    return args


def matchname(name, spec):
    """Check if name matches against a specification."""
    return (
        (not name.startswith("_"))
        and any(fnmatch(subname, spec) for subname in name.split(",")))


def abspath(frompath, relpath):
    """Gets the absolute path of relpath from the point of view of frompath."""
    basepath = os.path.realpath(
        os.path.join(os.path.abspath(frompath), os.pardir))
    return os.path.normpath(os.path.join(basepath, relpath))


def update_dict(parent, child):
    """
    Recursively merge child.key into parent.key, with parent overriding.
    """
    for key in child:
        if key == "_path" or key == "_include":
            continue
        elif key in parent:
            if isinstance(parent[key], list):
                parent[key] += child[key]
            elif isinstance(parent[key], dict):
                update_dict(parent[key], child[key])
        else:
            parent[key] = child[key]


def yaml_includes(parent):
    """Recursively loads any included YAML files."""
    included = []
    for relpath in parent.get("_include", []):
        path = abspath(parent["_path"], relpath)
        if path in included:
            continue
        with open(path) as f:
            child = yaml.load(f)
        child["_path"] = path
        included.append(path)
        included += yaml_includes(child)
        update_dict(parent, child)
    return included


def make_write_constraint(wc_range):
    """Given a (min, max), returns a writeConstraint Element."""
    wc = ET.Element('writeConstraint')
    r = ET.SubElement(wc, 'range')
    minimum = ET.SubElement(r, 'minimum')
    minimum.text = str(wc_range[0])
    maximum = ET.SubElement(r, 'maximum')
    maximum.text = str(wc_range[1])
    wc.tail = "\r\n            "
    return wc


def make_enumerated_values(name, values):
    """
    Given a name and a dict of values which maps variant names to (value,
    description), returns an enumeratedValues Element.
    Optional _usage key in values specifies usage.
    """
    ev = ET.Element('enumeratedValues')
    ET.SubElement(ev, 'name').text = name
    if "_usage" in values:
        ET.SubElement(ev, 'usage').text = values["_usage"]
    for name in values:
        if name.startswith("_"):
            continue
        value, description = values[name]
        el = ET.SubElement(ev, 'enumeratedValue')
        ET.SubElement(el, 'name').text = name
        ET.SubElement(el, 'description').text = description
        ET.SubElement(el, 'value').text = str(value)
    ev.tail = "\r\n            "
    return ev


def make_derived_enumerated_values(name):
    """Returns an enumeratedValues Element which is derivedFrom name."""
    evd = ET.Element('enumeratedValues', {"derivedFrom": name})
    evd.tail = "\r\n            "
    return evd


def iter_peripherals(tree, pspec):
    """Iterates over all peripherals that match pspec."""
    for ptag in tree.iter('peripheral'):
        name = ptag.find('name').text
        if matchname(name, pspec) and "derivedFrom" not in ptag.attrib:
            yield ptag


def iter_registers(ptag, rspec):
    """
    Iterates over all registers that match rspec and live inside ptag.
    """
    for rtag in ptag.iter('register'):
        name = rtag.find('name').text
        if matchname(name, rspec):
            yield rtag


def iter_fields(rtag, fspec):
    """
    Iterates over all fields that match fspec and live inside rtag.
    """
    for ftag in rtag.find('fields').iter('field'):
        name = ftag.find('name').text
        if matchname(name, fspec):
            yield ftag


def process_device_modify(device, pspec, pmod):
    """Modify pspec inside device according to pmod."""
    for ptag in iter_peripherals(device, pspec):
        for (key, value) in pmod.items():
            ptag.find(key).text = value


def process_peripheral_modify(ptag, rspec, rmod):
    """Modify rspec inside ptag according to rmod."""
    for rtag in iter_registers(ptag, rspec):
        for (key, value) in rmod.items():
            rtag.find(key).text = value


def process_register_modify(rtag, fspec, fmod):
    """Modify fspec inside rtag according to fmod."""
    for ftag in iter_fields(rtag, fspec):
        for (key, value) in fmod.items():
            ftag.find(key).text = str(value)


def process_device_add(device, pname, padd):
    """Add pname given by padd to device."""
    parent = device.find('peripherals')
    pnew = ET.SubElement(parent, 'peripheral')
    ET.SubElement(pnew, 'name').text = pname
    for (key, value) in padd.items():
        if key == "registers":
            for rname in value:
                process_peripheral_add(pnew, rname, value[rname])
        elif key == "addressBlock":
            ab = ET.SubElement(pnew, 'addressBlock')
            for (ab_key, ab_value) in value:
                ET.SubElement(ab, ab_key).text = str(ab_value)
        else:
            ET.SubElement(pnew, key).text = str(value)


def process_peripheral_add(ptag, rname, radd):
    """Add rname given by radd to ptag."""
    parent = ptag.find('registers')
    rnew = ET.SubElement(parent, 'register')
    ET.SubElement(rnew, 'name').text = rname
    for (key, value) in radd.items():
        if key == "fields":
            for fname in value:
                process_register_add(rnew, fname, value[fname])
        else:
            ET.SubElement(rnew, key).text = str(value)


def process_register_add(rtag, fname, fadd):
    """Add fname given by fadd to rtag."""
    parent = rtag.find('fields')
    fnew = ET.SubElement(parent, 'field')
    ET.SubElement(fnew, 'name').text = fname
    for (key, value) in fadd.items():
        ET.SubElement(fnew, key).text = str(value)


class SvdPatchError(ValueError):
    pass


class RegisterMergeError(SvdPatchError):
    pass


class MissingFieldError(SvdPatchError):
    pass


class MissingRegisterError(SvdPatchError):
    pass


class MissingPeripheralError(SvdPatchError):
    pass


def process_register_merge(rtag, fspec):
    """Merge all fspec in rtag."""
    fields = list(iter_fields(rtag, fspec))
    if len(fields) == 0:
        rname = rtag.find('name').text
        raise RegisterMergeError("Could not find any fields to merge {}.{}"
                                 .format(rname, fspec))
    parent = rtag.find('fields')
    name = os.path.commonprefix([f.find('name').text for f in fields])
    desc = fields[0].find('description').text
    bitwidth = sum(int(f.find('bitWidth').text) for f in fields)
    bitoffset = min(int(f.find('bitOffset').text) for f in fields)
    for field in fields:
        parent.remove(field)
    fnew = ET.SubElement(parent, 'field')
    ET.SubElement(fnew, 'name').text = name
    ET.SubElement(fnew, 'description').text = desc
    ET.SubElement(fnew, 'bitOffset').text = str(bitoffset)
    ET.SubElement(fnew, 'bitWidth').text = str(bitwidth)


def process_field_enum(pname, rtag, fspec, field):
    """Add an enumeratedValues given by field to all fspec in rtag."""
    derived = None
    for ftag in iter_fields(rtag, fspec):
        name = ftag.find('name').text
        if derived is None:
            enum = make_enumerated_values(name, field)
            ftag.append(enum)
            derived = make_derived_enumerated_values(name)
        else:
            ftag.append(derived)
    if derived is None:
        rname = rtag.find('name').text
        raise MissingFieldError("Could not find {}:{}.{}"
                                .format(pname, rname, fspec))


def process_field_range(pname, rtag, fspec, field):
    """Add a writeConstraint range given by field to all fspec in rtag."""
    set_any = False
    for ftag in iter_fields(rtag, fspec):
        ftag.append(make_write_constraint(field))
        set_any = True
    if not set_any:
        rname = rtag.find('name').text
        raise MissingFieldError("Could not find {}:{}.{}"
                                .format(pname, rname, fspec))


def process_register_field(pname, rtag, fspec, field):
    """Work through a field, handling either an enum or a range."""
    if isinstance(field, dict):
        process_field_enum(pname, rtag, fspec, field)
    elif isinstance(field, list) and len(field) == 2:
        process_field_range(pname, rtag, fspec, field)


def process_peripheral_register(ptag, rspec, register, update_fields=True):
    """Work through a register, handling all fields."""
    # Find all registers that match the spec
    pname = ptag.find('name').text
    rcount = 0
    for rtag in iter_registers(ptag, rspec):
        rcount += 1
        # Handle modifications
        for fspec in register.get("_modify", []):
            fmod = register["_modify"][fspec]
            process_register_modify(rtag, fspec, fmod)
        # Handle additions
        for fname in register.get("_add", []):
            fadd = register["_add"][fname]
            process_register_add(rtag, fname, fadd)
        # Handle merges
        for fspec in register.get("_merge", []):
            process_register_merge(rtag, fspec)
        # Handle fields
        if update_fields:
            for fspec in register:
                if not fspec.startswith("_"):
                    field = register[fspec]
                    process_register_field(pname, rtag, fspec, field)
    if rcount == 0:
        raise MissingRegisterError("Could not find {}:{}"
                                   .format(pname, rspec))


def process_peripheral(svd, pspec, peripheral, update_fields=True):
    """Work through a peripheral, handling all fields."""
    # Handle includes
    yaml_includes(peripheral)

    # Find all peripherals that match the spec
    pcount = 0
    for ptag in iter_peripherals(svd, pspec):
        pcount += 1
        # Handle modifications
        for rspec in peripheral.get("_modify", []):
            rmod = peripheral["_modify"][rspec]
            process_peripheral_modify(ptag, rspec, rmod)
        # Handle additions
        for rname in peripheral.get("_add", []):
            radd = peripheral["_add"][rname]
            process_peripheral_add(ptag, rname, radd)
        # Handle registers
        for rspec in peripheral:
            if not rspec.startswith("_"):
                register = peripheral[rspec]
                process_peripheral_register(ptag, rspec, register,
                                            update_fields)
    if pcount == 0:
        raise MissingPeripheralError("Could not find {}".format(pspec))


def main():
    # Load the specified YAML root file
    args = parseargs()
    with open(args.yaml) as f:
        root = yaml.load(f)
        root["_path"] = args.yaml

    # Load the specified SVD file
    if "_svd" not in root:
        raise RuntimeError("You must have an svd key in the root YAML file")
    svdpath = abspath(args.yaml, root["_svd"])
    svdpath_out = svdpath + ".patched"
    svd = ET.parse(svdpath)

    # Load all included YAML files
    yaml_includes(root)

    # Handle any peripheral modifications
    for pspec in root.get("_modify", []):
        pmod = root["_modify"][pspec]
        process_device_modify(svd, pspec, pmod)

    # Handle any new peripherals (!)
    for pname in root.get("_add", []):
        padd = root["_add"][pname]
        process_device_add(root, pname, padd)

    # Now process all peripherals
    for periphspec in root:
        if not periphspec.startswith("_"):
            root[periphspec]["_path"] = root["_path"]
            process_peripheral(svd, periphspec, root[periphspec])

    # SVD should now be updated, write it out
    svd.write(svdpath_out)


if __name__ == "__main__":
    main()
