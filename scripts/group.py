"""
Generate sets of devices with peripherals in common.
"""

import os
import glob
import yaml
import json
import argparse
import xml.etree.ElementTree as ET

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x: x

from svdtools import patch


def main(devices, output):
    print("Stage 1: Enumerating all fields in all devices")
    peripherals = {}
    for device_path in tqdm(glob.glob(os.path.join(devices, "*.yaml"))):
        device_name = os.path.splitext(os.path.basename(device_path))[0]
        with open(device_path, encoding='utf-8') as f:
            device = yaml.safe_load(f)
            device["_path"] = device_path
        if "_svd" not in device:
            raise RuntimeError("You must have an _svd key in the YAML file")
        svdpath = patch.abspath(device_path, device["_svd"])
        svd = ET.parse(svdpath)
        patch.process_device(svd, device)
        for ptag in svd.iter('peripheral'):
            if "derivedFrom" in ptag.attrib:
                continue
            pname = ptag.find('name').text
            device_members = []

            for rtag in ptag.iter('register'):
                rname = rtag.find('name').text
                roffset = rtag.find('addressOffset').text
                for ftag in rtag.iter('field'):
                    fname = ftag.find('name').text
                    foffset = ftag.find('bitOffset').text
                    fwidth = ftag.find('bitWidth').text
                    device_members.append(
                        "{}__{}_{}__{}_{}_{}".format(
                            pname, roffset, rname, foffset, fwidth, fname
                        )
                    )

            if pname not in peripherals:
                peripherals[pname] = {}
            peripherals[pname][device_name] = device_members

    print("Stage 2: Inverting to find all devices for each field and merging")
    fields = {}
    merged_fields = {}
    for pname, devices in tqdm(peripherals.items()):
        fields[pname] = {}
        for device, device_fields in devices.items():
            for fname in device_fields:
                if fname not in fields[pname]:
                    fields[pname][fname] = set()
                fields[pname][fname].add(device)
        merged_fields[pname] = {}
        skip_fields = set()
        for field, devices in fields[pname].items():
            if field in skip_fields:
                continue
            merged_key = [field]
            for field2, devices2 in fields[pname].items():
                if field != field2 and devices == devices2:
                    merged_key.append(field2)
                    skip_fields.add(field2)
            merged_fields[pname][",".join(sorted(merged_key))] = devices

    print("Stage 3: Building tree of subsets")
    field_tree = {}
    for pname in tqdm(merged_fields):
        field_tree[pname] = {}

        # Build our dict of tree nodes
        for fieldset, devices in merged_fields[pname].items():
            field_tree[pname][fieldset] = (devices, {})

        # Function to take a given (fieldset: (devices, children))
        # and dictionary of its siblings (including itself),
        # then move all siblings inside itself and recurse,
        # returning the list of all siblings moved inside itself.
        def treeify(fieldset, devices, children, siblings):
            # First find all subsets and move them into our children
            moved_siblings = []
            for fieldset2, (devices2, children2) in siblings.items():
                if fieldset2 != fieldset and devices2 < devices:
                    children[fieldset2] = (devices2, children2)
                    moved_siblings.append(fieldset2)

            # Remove all our new children from the parent list
            for fieldset2 in moved_siblings:
                del siblings[fieldset2]

            # Now treeify each new child
            moved_children = []
            for fieldset2 in moved_siblings:
                if fieldset2 in moved_children:
                    continue
                devices2, children2 = children[fieldset2]
                moved_children += treeify(fieldset2, devices2, children2, children)

            return moved_siblings

        # Form the tree of all these fieldsets
        fieldsets = list(field_tree[pname].keys())
        moved_fieldsets = []
        for fieldset in fieldsets:
            if fieldset in moved_fieldsets:
                continue
            devices, children = field_tree[pname][fieldset]
            moved_fieldsets += treeify(fieldset, devices, children, field_tree[pname])

        # Now strip the device names from all but the leaves
        def strip_devices(siblings):
            fieldsets = list(siblings.keys())
            for fieldset in fieldsets:
                devices, children = siblings[fieldset]
                if children:
                    strip_devices(children)
                    siblings[fieldset] = children
                else:
                    siblings[fieldset] = list(devices)

        strip_devices(field_tree[pname])

    print("Stage 4: Writing results JSON")
    with open(output, "w") as f:
        json.dump(field_tree, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("devices", help="Path to folder of device YAML files")
    parser.add_argument("output", help="Path to write output to")
    args = parser.parse_args()

    main(args.devices, args.output)
