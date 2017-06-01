"""
matchperipherals.py
Copyright 2017 Adam Greig
Licensed under the MIT and Apache 2.0 licenses.

Finds all peripherals that match the specified device.

Usage: python3 scripts/makeyaml.py peripherals/ devices/stm32f0x0.yaml
"""

import sys
import yaml
import fnmatch
import os.path
import argparse
import xml.etree.ElementTree as ET

import svdpatch


def process_device(device, ppath):
    # Load the SVD and process all modifications from the yaml
    # (but don't bother actually applying the enums/ranges).
    svdpath = svdpatch.abspath(device["_path"], device["_svd"])
    print("Loading SVD {} for {}".format(svdpath, device["_path"]))
    tree = ET.parse(svdpath)
    print("\nProcessing existing device peripherals")
    already_included = svdpatch.yaml_includes(device)
    for pspec in device:
        if not pspec.startswith("_"):
            device[pspec]["_path"] = device["_path"]
            svdpatch.process_peripheral(tree, pspec, device[pspec], False)

    # Now go through every YAML file we can find and see if they could be
    # matched against the device
    print("\nMatching against remaining peripherals")
    matches = []
    for root, dirnames, filenames in os.walk(ppath):
        for filename in fnmatch.filter(filenames, "*.yaml"):
            yamlpath = os.path.realpath(os.path.join(root, filename))
            if yamlpath in already_included:
                continue
            with open(yamlpath) as f:
                peripheral = yaml.load(f)
            peripheral["_path"] = yamlpath
            svdpatch.yaml_includes(peripheral)
            for pspec in peripheral:
                if not pspec.startswith("_"):
                    peripheral[pspec]["_path"] = peripheral["_path"]
                    try:
                        svdpatch.process_peripheral(
                            tree, pspec, peripheral[pspec], True)
                    except svdpatch.SvdPatchError as e:
                        print("Couldn't match {}: {}".format(yamlpath, e))
                        continue
                    else:
                        matches.append(yamlpath)
    return matches


def main(dpath, ppath, update):
    with open(dpath) as f:
        device = yaml.load(f)
    if "_svd" not in device:
        print("Could not find _svd in device YAML, cannot proceed.")
        return
    device["_path"] = dpath
    matches = process_device(device, ppath)
    if matches:
        absdpath = svdpatch.abspath(sys.argv[0], dpath)
        print(dpath)
        common = os.path.commonprefix([absdpath] + matches)
        matches = [" - ../" + match[len(common):] for match in matches]
        print("\nMatched these new peripherals:")
        print("\n".join(matches))
        if update:
            print("Updating device YAML")
            with open(dpath, "a") as f:
                f.write("\n".join(matches))
    else:
        print("\nNo new peripherals matched.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--update', action='store_true')
    parser.add_argument("peripherals")
    parser.add_argument("devices", nargs="*")
    args = parser.parse_args()
    for device in args.devices:
        main(device, args.peripherals, args.update)
