"""
svdpatch.py

Copyright 2017-2019 Adam Greig.
Licensed under the MIT and Apache 2.0 licenses. See LICENSE files for details.
"""

import copy
import yaml
import os.path
import argparse
import xml.etree.ElementTree as ET
from fnmatch import fnmatch
from collections import OrderedDict

DEVICE_CHILDREN = [
    "vendor", "vendorID", "name", "series", "version", "description",
    "licenseText", "headerSystemFilename", "headerDefinitionsPrefix",
    "addressUnitBits", "width", "size", "access", "protection", "resetValue",
    "resetMask"]


# Set up pyyaml to use ordered dicts so we generate the same
# XML output each time
def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))


_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
yaml.add_constructor(_mapping_tag, dict_constructor, yaml.SafeLoader)


def parseargs():
    """Parse our command line arguments, returns a Namespace of results."""
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml", help="Path to YAML file to load")
    args = parser.parse_args()
    return args


def matchname(name, spec):
    """Check if name matches against a specification."""
    return (
        (not spec.startswith("_")) and
        any(fnmatch(name, subspec) for subspec in spec.split(",")))


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
        with open(path, encoding='utf-8') as f:
            child = yaml.safe_load(f)
        child["_path"] = path
        included.append(path)
        # Process any peripheral-level includes in child
        for pspec in child:
            if not pspec.startswith("_") and "_include" in child[pspec]:
                child[pspec]["_path"] = path
                included += yaml_includes(child[pspec])
        # Process any top-level includes in child
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
    wc.tail = "\n            "
    return wc


def make_enumerated_values(name, values, usage="read-write"):
    """
    Given a name and a dict of values which maps variant names to (value,
    description), returns an enumeratedValues Element.
    """
    ev = ET.Element('enumeratedValues')
    usagekey = {
        "read": "R",
        "write": "W",
    }.get(usage, "")
    ET.SubElement(ev, 'name').text = name + usagekey
    ET.SubElement(ev, 'usage').text = usage
    if len(set(v[0] for v in values.values())) != len(values):
        raise ValueError("enumeratedValue {}: can't have duplicate values"
                         .format(name))
    if name[0] in "0123456789":
        raise ValueError("enumeratedValue {}: can't start with a number"
                         .format(name))
    for vname in values:
        if vname.startswith("_"):
            continue
        if vname[0] in "0123456789":
            raise ValueError("enumeratedValue {}.{}: can't start with a number"
                             .format(name, vname))
        value, description = values[vname]
        if not description:
            raise ValueError("enumeratedValue {}: can't have empty description"
                             " for value {}".format(name, value))
        el = ET.SubElement(ev, 'enumeratedValue')
        ET.SubElement(el, 'name').text = vname
        ET.SubElement(el, 'description').text = description
        ET.SubElement(el, 'value').text = str(value)
    ev.tail = "\n            "
    return ev


def make_derived_enumerated_values(name):
    """Returns an enumeratedValues Element which is derivedFrom name."""
    evd = ET.Element('enumeratedValues', {"derivedFrom": name})
    evd.tail = "\n            "
    return evd


def spec_ind(spec):
    """
    Find left and right indices of enumeration token in specification string.
    """
    li1 = spec.find("*")
    li2 = spec.find("?")
    li3 = spec.find("[")
    li = li1 if li1 > -1 else li2 if li2 > -1 else li3 if li3 > -1 else None
    ri1 = spec[::-1].find("*")
    ri2 = spec[::-1].find("?")
    ri3 = spec[::-1].find("]")
    ri = ri1 if ri1 > -1 else ri2 if ri2 > -1 else ri3 if ri3 > -1 else None
    return li, ri


def check_offsets(offsets, dimIncrement):
    for o1, o2 in zip(offsets[:-1], offsets[1:]):
        if o2-o1 != dimIncrement:
            return False
    return True


def check_bitmasks(masks, mask):
    for m in masks:
        if m != mask:
            return False
    return True


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


class Device:
    """Class collecting methods for processing device contents"""
    def __init__(self, device):
        self.device = device

    def iter_peripherals(self, pspec, check_derived=True):
        """Iterates over all peripherals that match pspec."""
        for ptag in self.device.iter('peripheral'):
            name = ptag.find('name').text
            if matchname(name, pspec):
                if check_derived and "derivedFrom" in ptag.attrib:
                    continue
                yield ptag

    def modify_child(self, key, val):
        """Modify key inside device and set it to val."""
        for child in self.device.findall(key):
            child.text = str(val)

    def modify_cpu(self, mod):
        """Modify the `cpu` node inside `device` according to `mod`."""
        cpu = self.device.find('cpu')
        for key, val in mod.items():
            field = cpu.find(key)
            if field is not None:
                field.text = str(val)
            else:
                field = ET.SubElement(cpu, key)
                field.text = str(val)

    def modify_peripheral(self, pspec, pmod):
        """Modify pspec inside device according to pmod."""
        for ptag in self.iter_peripherals(pspec):
            for (key, value) in pmod.items():
                ptag.find(key).text = str(value)

    def add_peripheral(self, pname, padd):
        """Add pname given by padd to device."""
        parent = self.device.find('peripherals')
        for ptag in parent.iter('peripheral'):
            if ptag.find('name').text == pname:
                raise SvdPatchError('device already has a peripheral {}'
                                    .format(pname))
        if "derivedFrom" in padd:
            derived = padd["derivedFrom"]
            pnew = ET.SubElement(parent, 'peripheral',
                                 {"derivedFrom": derived})
        else:
            pnew = ET.SubElement(parent, 'peripheral')
        ET.SubElement(pnew, 'name').text = pname
        for (key, value) in padd.items():
            if key == "registers":
                ET.SubElement(pnew, 'registers')
                for rname in value:
                    Peripheral(pnew).add_register(rname, value[rname])
            elif key == "interrupts":
                for iname in value:
                    Peripheral(pnew).add_interrupt(iname, value[iname])
            elif key == "addressBlock":
                ab = ET.SubElement(pnew, 'addressBlock')
                for (ab_key, ab_value) in value.items():
                    ET.SubElement(ab, ab_key).text = str(ab_value)
            elif key != "derivedFrom":
                ET.SubElement(pnew, key).text = str(value)
        pnew.tail = "\n    "

    def delete_peripheral(self, pspec):
        """Delete registers matched by rspec inside ptag."""
        for ptag in list(self.iter_peripherals(pspec, check_derived=False)):
            self.device.find('peripherals').remove(ptag)

    def derive_peripheral(self, pname, pderive):
        """
        Remove registers from pname and mark it as derivedFrom pderive.
        Update all derivedFrom referencing pname.
        """
        parent = self.device.find('peripherals')
        ptag = parent.find('./peripheral[name=\'{}\']'.format(pname))
        derived = parent.find('./peripheral[name=\'{}\']'.format(pderive))
        if ptag is None:
            raise SvdPatchError('peripheral {} not found'.format(pname))
        if derived is None:
            raise SvdPatchError('peripheral {} not found'.format(pderive))
        for (value) in list(ptag):
            if value.tag in ('name', 'baseAddress', 'interrupt'):
                continue
            ptag.remove(value)
        for value in ptag:
            last = value
        last.tail = "\n    "
        ptag.set('derivedFrom', pderive)
        for p in parent.findall(
                './peripheral[@derivedFrom=\'{}\']'.format(pname)):
            p.set('derivedFrom', pderive)

    def copy_peripheral(self, pname, pmod):
        """
        Create copy of peripheral
        """
        parent = self.device.find('peripherals')
        ptag = parent.find('./peripheral[name=\'{}\']'.format(pname))
        pcopyname = pmod['from']
        pcopy = copy.deepcopy(
            parent.find('./peripheral[name=\'{}\']'.format(pcopyname)))
        if pcopy is None:
            raise SvdPatchError('peripheral {} not found'.format(pcopy))
        if ptag is None:
            pcopy.find("name").text = pname
            raise SvdPatchError('unimplemented')
        else:
            for value in list(ptag):
                if value.tag in ('name', 'baseAddress', 'interrupt'):
                    tag = pcopy.find(value.tag)
                    if tag is not None:
                        pcopy.remove(tag)
                    pcopy.append(value)
        parent.remove(ptag)
        parent.append(pcopy)

    def rebase_peripheral(self, pnew, pold):
        """
        Move registers from pold to pnew.
        Update all derivedFrom referencing pold.
        """
        parent = self.device.find('peripherals')
        old = parent.find('./peripheral[name=\'{}\']'.format(pold))
        new = parent.find('./peripheral[name=\'{}\']'.format(pnew))
        if old is None:
            raise SvdPatchError('peripheral {} not found'.format(pold))
        if new is None:
            raise SvdPatchError('peripheral {} not found'.format(pnew))
        for value in new:
            last = value
        last.tail = "\n      "
        for (value) in list(old):
            if value.tag in ('name', 'baseAddress', 'interrupt'):
                continue
            old.remove(value)
            new.append(value)
        for value in old:
            last = value
        last.tail = "\n    "
        del new.attrib['derivedFrom']
        old.set('derivedFrom', pnew)
        for p in parent.findall(
                './peripheral[@derivedFrom=\'{}\']'.format(pold)):
            p.set('derivedFrom', pnew)

    def process_peripheral(self, pspec, peripheral, update_fields=True):
        """Work through a peripheral, handling all registers."""
        # Find all peripherals that match the spec
        pcount = 0
        for ptag in self.iter_peripherals(pspec):
            pcount += 1
            # Handle deletions
            p = Peripheral(ptag)
            deletions = peripheral.get("_delete", [])
            if isinstance(deletions, list):
                for rspec in deletions:
                    p.delete_register(rspec)
            elif isinstance(deletions, dict):
                for rspec in deletions:
                    if rspec == "_registers":
                        for rspec in deletions[rspec]:
                            p.delete_register(rspec)
                    elif rspec == "_interrupts":
                        for ispec in deletions[rspec]:
                            p.delete_interrupt(ispec)
                    else:
                        p.delete_register(rspec)
            # Handle modifications
            for rspec in peripheral.get("_modify", {}):
                rmod = peripheral["_modify"][rspec]
                if rspec == "_registers":
                    for rspec in rmod:
                        p.modify_register(rspec, rmod[rspec])
                elif rspec == "_interrupts":
                    for ispec in rmod:
                        p.modify_interrupt(ispec, rmod[ispec])
                else:
                    p.modify_register(rspec, rmod)
            # Handle strips
            for prefix in peripheral.get("_strip", []):
                p.strip_prefix(prefix)
            # Handle additions
            for rname in peripheral.get("_add", {}):
                radd = peripheral["_add"][rname]
                if rname == "_registers":
                    for rname in radd:
                        p.add_register(rname, radd[rname])
                elif rname == "_interrupts":
                    for iname in radd:
                        p.add_interrupt(iname, radd[iname])
                else:
                    p.add_register(rname, radd)
            # Handle registers
            for rspec in peripheral:
                if not rspec.startswith("_"):
                    register = peripheral[rspec]
                    p.process_register(rspec, register, update_fields)
            # Handle register arrays
            for rspec in peripheral.get("_array", {}):
                rmod = peripheral["_array"][rspec]
                p.collect_in_array(rspec, rmod)
            # Handle clusters
            for cname in peripheral.get("_cluster", {}):
                cmod = peripheral["_cluster"][cname]
                p.collect_in_cluster(cname, cmod)
        if pcount == 0:
            raise MissingPeripheralError("Could not find {}".format(pspec))


class Peripheral:
    """Class collecting methods for processing peripheral contents"""
    def __init__(self, ptag):
        self.ptag = ptag

    def iter_registers(self, rspec):
        """
        Iterates over all registers that match rspec and live inside ptag.
        """
        for rtag in self.ptag.iter('register'):
            name = rtag.find('name').text
            if matchname(name, rspec):
                yield rtag

    def iter_interrupts(self, ispec):
        """Iterates over all interrupts matching ispec"""
        for itag in self.ptag.iter('interrupt'):
            name = itag.find('name').text
            if matchname(name, ispec):
                yield itag

    def add_interrupt(self, iname, iadd):
        """Add iname given by iadd to ptag."""
        for itag in self.ptag.iter('interrupt'):
            if itag.find('name').text == iname:
                raise SvdPatchError(
                    'peripheral {} already has an interrupt {}'
                    .format(self.ptag.find('name').text, iname))
        inew = ET.SubElement(self.ptag, 'interrupt')
        ET.SubElement(inew, 'name').text = iname
        for key, val in iadd.items():
            ET.SubElement(inew, key).text = str(val)
        inew.tail = "\n    "

    def modify_interrupt(self, ispec, imod):
        """Modify ispec according to imod"""
        for itag in self.iter_interrupts(ispec):
            for (key, value) in imod.items():
                tag = itag.find(key)
                if value == "":
                    itag.remove(tag)
                else:
                    tag.text = str(value)

    def delete_interrupt(self, ispec):
        """Delete interrupts matched by ispec"""
        for itag in list(self.iter_interrupts(ispec)):
            self.ptag.remove(itag)

    def modify_register(self, rspec, rmod):
        """Modify rspec inside ptag according to rmod."""
        for rtag in self.iter_registers(rspec):
            for (key, value) in rmod.items():
                tag = rtag.find(key)
                if value == "":
                    rtag.remove(tag)
                else:
                    tag.text = value

    def add_register(self, rname, radd):
        """Add rname given by radd to ptag."""
        parent = self.ptag.find('registers')
        for rtag in parent.iter('register'):
            if rtag.find('name').text == rname:
                raise SvdPatchError(
                    'peripheral {} already has a register {}'
                    .format(self.ptag.find('name').text, rname))
        rnew = ET.SubElement(parent, 'register')
        ET.SubElement(rnew, 'name').text = rname
        ET.SubElement(rnew, 'fields')
        for (key, value) in radd.items():
            if key == "fields":
                for fname in value:
                    Register(rnew).add_field(fname, value[fname])
            else:
                ET.SubElement(rnew, key).text = str(value)
        rnew.tail = "\n        "

    def delete_register(self, rspec):
        """Delete registers matched by rspec inside ptag."""
        for rtag in list(self.iter_registers(rspec)):
            self.ptag.find('registers').remove(rtag)

    def strip_prefix(self, prefix):
        """Delete prefix in register names inside ptag."""
        for rtag in self.ptag.iter('register'):
            nametag = rtag.find('name')
            name = nametag.text
            if name.startswith(prefix):
                nametag.text = name[len(prefix):]
                dnametag = rtag.find('displayName')
                dname = dnametag.text
                if dname.startswith(prefix):
                    dnametag.text = dname[len(prefix):]

    def collect_in_array(self, rspec, rmod):
        """Collect same registers in peripheral into register array."""
        registers = []
        li, ri = spec_ind(rspec)
        for rtag in list(self.iter_registers(rspec)):
            rname = rtag.findtext('name')
            registers.append([rtag, rname[li:len(rname)-ri],
                              int(rtag.findtext('addressOffset'), 0)])
        dim = len(registers)
        if dim == 0:
            raise SvdPatchError("{}: registers {} not found"
                                .format(self.ptag.findtext('name'), rspec))
        registers = sorted(registers, key=lambda r: r[2])

        if rmod.get('_start_from_zero', ""):
            dimIndex = ",".join([str(i) for i in range(dim)])
        else:
            if dim == 1:
                dimIndex = "{0}-{0}".format(registers[0][1])
            else:
                dimIndex = ",".join(r[1] for r in registers)
        offsets = [r[2] for r in registers]
        bitmasks = [Register(r[0]).get_bitmask() for r in registers]
        dimIncrement = 0
        if dim > 1:
            dimIncrement = offsets[1]-offsets[0]

        if not (
                check_offsets(offsets, dimIncrement) and
                check_bitmasks(bitmasks, bitmasks[0])):
            raise SvdPatchError(
                "{}: registers cannot be collected into {} array"
                .format(self.ptag.findtext('name'), rspec))
        for rtag, _, _ in registers[1:]:
            self.ptag.find('registers').remove(rtag)
        rtag = registers[0][0]
        if 'name' in rmod:
            name = rmod['name']
        else:
            name = rspec[:li]+"%s"+rspec[len(rspec)-ri:]
        rtag.find('name').text = name
        self.process_register(name, rmod)
        ET.SubElement(rtag, 'dim').text = str(dim)
        ET.SubElement(rtag, 'dimIndex').text = dimIndex
        ET.SubElement(rtag, 'dimIncrement').text = hex(dimIncrement)

    def collect_in_cluster(self, cname, cmod):
        """Collect registers in peripheral into clusters."""
        rdict = {}
        first = True
        check = True
        rspecs = [r for r in cmod if r != "description"]
        for rspec in rspecs:
            registers = []
            li, ri = spec_ind(rspec)
            for rtag in list(self.iter_registers(rspec)):
                rname = rtag.findtext('name')
                registers.append([rtag, rname[li:len(rname)-ri],
                                  int(rtag.findtext('addressOffset'), 0)])
            registers = sorted(registers, key=lambda r: r[2])
            rdict[rspec] = registers
            bitmasks = [Register(r[0]).get_bitmask() for r in registers]
            if first:
                dim = len(registers)
                if dim == 0:
                    check = False
                    break
                dimIndex = ",".join([r[1] for r in registers])
                offsets = [r[2] for r in registers]
                dimIncrement = 0
                if dim > 1:
                    dimIncrement = offsets[1]-offsets[0]
                if not (
                        check_offsets(offsets, dimIncrement) and
                        check_bitmasks(bitmasks, bitmasks[0])):
                    check = False
                    break
            else:
                if (
                        (dim != len(registers)) or
                        (dimIndex != ",".join([r[1] for r in registers])) or
                        (not check_offsets(offsets, dimIncrement)) or
                        (not check_bitmasks(bitmasks, bitmasks[0]))
                   ):
                    check = False
                    break
            first = False
        if not check:
            raise SvdPatchError(
                "{}: registers cannot be collected into {} cluster"
                .format(self.ptag.findtext('name'), cname))
        ctag = ET.SubElement(self.ptag.find('registers'), 'cluster')
        addressOffset = min(
            [registers[0][2] for _, registers in rdict.items()])
        ET.SubElement(ctag, 'name').text = cname
        if 'description' in cmod:
            description = cmod['description']
        else:
            description = ("Cluster {}, containing {}"
                           .format(cname, ", ".join(rspecs)))
        ET.SubElement(ctag, 'description').text = description
        ET.SubElement(ctag, 'addressOffset').text = hex(addressOffset)
        for rspec, registers in rdict.items():
            for rtag, _, _ in registers[1:]:
                self.ptag.find('registers').remove(rtag)
            rtag = registers[0][0]
            rmod = cmod[rspec]
            self.process_register(rspec, rmod)
            new_rtag = copy.deepcopy(rtag)
            self.ptag.find('registers').remove(rtag)
            if 'name' in rmod:
                name = rmod['name']
            else:
                li, ri = spec_ind(rspec)
                name = rspec[:li]+rspec[len(rspec)-ri:]
            new_rtag.find('name').text = name
            offset = new_rtag.find('addressOffset')
            offset.text = hex(int(offset.text, 0)-addressOffset)
            ctag.append(new_rtag)
        ET.SubElement(ctag, 'dim').text = str(dim)
        ET.SubElement(ctag, 'dimIndex').text = dimIndex
        ET.SubElement(ctag, 'dimIncrement').text = hex(dimIncrement)

    def process_register(self, rspec, register, update_fields=True):
        """Work through a register, handling all fields."""
        # Find all registers that match the spec
        pname = self.ptag.find('name').text
        rcount = 0
        for rtag in self.iter_registers(rspec):
            r = Register(rtag)
            rcount += 1
            # Handle deletions
            for fspec in register.get("_delete", []):
                r.delete(fspec)
            # Handle modifications
            for fspec in register.get("_modify", []):
                fmod = register["_modify"][fspec]
                r.modify_field(fspec, fmod)
            # Handle additions
            for fname in register.get("_add", []):
                fadd = register["_add"][fname]
                r.add_field(fname, fadd)
            # Handle merges
            for fspec in register.get("_merge", []):
                r.merge_fields(fspec)
            # Handle splits
            for fspec in register.get("_split", []):
                r.split_fields(fspec)
            # Handle fields
            if update_fields:
                for fspec in register:
                    if not fspec.startswith("_"):
                        field = register[fspec]
                        r.process_field(pname, fspec, field)
        if rcount == 0:
            raise MissingRegisterError("Could not find {}:{}"
                                       .format(pname, rspec))


class Register:
    """Class collecting methods for processing register contents"""
    def __init__(self, rtag):
        self.rtag = rtag

    def iter_fields(self, fspec):
        """
        Iterates over all fields that match fspec and live inside rtag.
        """
        for ftag in self.rtag.find('fields').iter('field'):
            name = ftag.find('name').text
            if matchname(name, fspec):
                yield ftag

    def modify_field(self, fspec, fmod):
        """Modify fspec inside rtag according to fmod."""
        for ftag in self.iter_fields(fspec):
            for (key, value) in fmod.items():
                try:
                    ftag.find(key).text = str(value)
                except AttributeError:
                    raise SvdPatchError(
                        'invalid attribute {!r} for register {}, field {}'
                        .format(key, self.rtag.find('name').text,
                                ftag.find('name').text))

    def add_field(self, fname, fadd):
        """Add fname given by fadd to rtag."""
        parent = self.rtag.find('fields')
        for ftag in parent.iter('field'):
            if ftag.find('name').text == fname:
                raise SvdPatchError(
                    'register {} already has a field {}'
                    .format(self.rtag.find('name').text, fname))
        fnew = ET.SubElement(parent, 'field')
        ET.SubElement(fnew, 'name').text = fname
        for (key, value) in fadd.items():
            ET.SubElement(fnew, key).text = str(value)
        fnew.tail = "\n            "

    def delete(self, fspec):
        """Delete fields matched by fspec inside rtag."""
        for ftag in list(self.iter_fields(fspec)):
            self.rtag.find('fields').remove(ftag)

    def merge_fields(self, fspec):
        """Merge all fspec in rtag."""
        fields = list(self.iter_fields(fspec))
        if len(fields) == 0:
            rname = self.rtag.find('name').text
            raise RegisterMergeError("Could not find any fields to merge {}.{}"
                                     .format(rname, fspec))
        parent = self.rtag.find('fields')
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

    def split_fields(self, fspec):
        """split all fspec in rtag."""
        fields = list(self.iter_fields(fspec))
        if len(fields) == 0:
            rname = self.rtag.find('name').text
            raise RegisterMergeError("Could not find any fields to split {}.{}"
                                     .format(rname, fspec))
        parent = self.rtag.find('fields')
        name = os.path.commonprefix([f.find('name').text for f in fields])
        desc = fields[0].find('description').text
        bitwidth = sum(int(f.find('bitWidth').text) for f in fields)
        parent.remove(fields[0])
        for i in range(bitwidth):
            fnew = ET.SubElement(parent, 'field')
            ET.SubElement(fnew, 'name').text = name + str(i)
            ET.SubElement(fnew, 'description').text = desc
            ET.SubElement(fnew, 'bitOffset').text = str(i)
            ET.SubElement(fnew, 'bitWidth').text = str(1)

    def process_field(self, pname, fspec, field):
        """Work through a field, handling either an enum or a range."""
        if isinstance(field, dict):
            usages = ("_read", "_write")

            if not any(u in field for u in usages):
                self.process_field_enum(pname, fspec, field)

            for usage in (u for u in usages if u in field):
                self.process_field_enum(pname, fspec, field[usage],
                                        usage=usage.replace("_", ""))

        elif isinstance(field, list) and len(field) == 2:
            self.process_field_range(pname, fspec, field)

    def process_field_enum(self, pname, fspec, field, usage="read-write"):
        """Add an enumeratedValues given by field to all fspec in rtag."""
        derived = None
        for ftag in self.iter_fields(fspec):
            name = ftag.find('name').text
            if derived is None:
                enum = make_enumerated_values(name, field, usage=usage)
                enum_name = enum.find('name').text
                enum_usage = enum.find('usage').text
                for ev in ftag.iter('enumeratedValues'):
                    ev_usage = ev.find('usage').text
                    if ev_usage == enum_usage or ev_usage == "read-write":
                        print(pname, fspec, field)
                        raise SvdPatchError(
                            "{}: field {} already has enumeratedValues for {}"
                            .format(pname, name, ev_usage))
                ftag.append(enum)
                derived = make_derived_enumerated_values(enum_name)
            else:
                ftag.append(derived)
        if derived is None:
            rname = self.rtag.find('name').text
            raise MissingFieldError("Could not find {}:{}.{}"
                                    .format(pname, rname, fspec))

    def process_field_range(self, pname, fspec, field):
        """Add a writeConstraint range given by field to all fspec in rtag."""
        set_any = False
        for ftag in self.iter_fields(fspec):
            ftag.append(make_write_constraint(field))
            set_any = True
        if not set_any:
            rname = self.rtag.find('name').text
            raise MissingFieldError("Could not find {}:{}.{}"
                                    .format(pname, rname, fspec))

    def get_bitmask(self):
        """Calculate filling of register"""
        mask = 0x0
        for ftag in self.iter_fields("*"):
            foffset = int(ftag.findtext("bitOffset"), 0)
            fwidth = int(ftag.findtext("bitWidth"), 0)
            mask |= (0xffffffff >> (32-fwidth)) << foffset
        return mask


def process_device(svd, device, update_fields=True):
    """Work through a device, handling all peripherals"""

    d = Device(svd)
    # Handle any deletions
    for pspec in device.get("_delete", []):
        d.delete_peripheral(pspec)

    # Handle any copied peripherals
    for pname in device.get("_copy", {}):
        val = device["_copy"][pname]
        d.copy_peripheral(pname, val)

    # Handle any modifications
    for key in device.get("_modify", {}):
        val = device["_modify"][key]
        if key == "cpu":
            d.modify_cpu(val)
        elif key == "_peripherals":
            for pspec in val:
                pmod = device['_modify']['_peripherals'][pspec]
                d.modify_peripheral(pspec, pmod)
        elif key in DEVICE_CHILDREN:
            d.modify_child(key, val)
        else:
            d.modify_peripheral(key, val)

    # Handle any new peripherals (!)
    for pname in device.get("_add", []):
        padd = device["_add"][pname]
        d.add_peripheral(pname, padd)

    # Handle any derived peripherals
    for pname in device.get("_derive", []):
        pderive = device["_derive"][pname]
        d.derive_peripheral(pname, pderive)

    # Handle any rebased peripherals
    for pname in device.get("_rebase", []):
        pold = device["_rebase"][pname]
        d.rebase_peripheral(pname, pold)

    # Now process all peripherals
    for periphspec in device:
        if not periphspec.startswith("_"):
            device[periphspec]["_path"] = device["_path"]
            d.process_peripheral(periphspec, device[periphspec],
                                 update_fields)


def main():
    # Load the specified YAML root file
    args = parseargs()
    with open(args.yaml, encoding='utf-8') as f:
        root = yaml.safe_load(f)
        root["_path"] = args.yaml

    # Load the specified SVD file
    if "_svd" not in root:
        raise RuntimeError("You must have an svd key in the root YAML file")
    svdpath = abspath(args.yaml, root["_svd"])
    svdpath_out = svdpath + ".patched"
    svd = ET.parse(svdpath)

    # Load all included YAML files
    yaml_includes(root)

    # Process device
    process_device(svd, root)

    # SVD should now be updated, write it out
    svd.write(svdpath_out)


if __name__ == "__main__":
    main()
