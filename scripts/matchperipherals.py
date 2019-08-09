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


def process_yamlfile(svd, yamlpath, quiet):
    with open(yamlpath, encoding='utf-8') as f:
        peripheral = yaml.safe_load(f)
    peripheral["_path"] = yamlpath
    svdpatch.yaml_includes(peripheral)
    matched = True
    for pspec in peripheral:
        if not pspec.startswith("_"):
            peripheral[pspec]["_path"] = peripheral["_path"]
            try:
                svdpatch.process_peripheral(
                    svd, pspec, peripheral[pspec], True)
            except svdpatch.SvdPatchError as e:
                if not quiet:
                    print("Couldn't match {}: {}".format(yamlpath, e))
                matched = False
                continue
    return matched


def process_device(device, ppath, quiet):
    # Load the SVD and process all modifications from the yaml
    # (but don't bother actually applying the enums/ranges).
    svdpath = svdpatch.abspath(device["_path"], device["_svd"])
    if not quiet:
        print("Loading SVD {} for {}".format(svdpath, device["_path"]))
    tree = ET.parse(svdpath)
    if not quiet:
        print("Processing existing device peripherals")
    already_included = svdpatch.yaml_includes(device)
    svdpatch.process_device(tree, device, False)

    # Now go through every YAML file we can find and see if they could be
    # matched against the device
    if not quiet:
        print("Matching against remaining peripherals")
    matches = []
    if os.path.isfile(ppath):
        yamlpath = os.path.realpath(ppath)
        if yamlpath not in already_included:
            if process_yamlfile(tree, ppath, quiet):
                matches.append(ppath)
    else:
        for root, dirnames, filenames in os.walk(ppath):
            for filename in fnmatch.filter(filenames, "*.yaml"):
                yamlpath = os.path.realpath(os.path.join(root, filename))
                if yamlpath in already_included:
                    continue
                if process_yamlfile(tree, yamlpath, quiet):
                    matches.append(yamlpath)
    return matches


def main(dpath, ppath, update, quiet):
    with open(dpath, encoding='utf-8') as f:
        device = yaml.safe_load(f)
    if "_svd" not in device:
        print("Could not find _svd in device YAML, cannot proceed.")
        return
    device["_path"] = dpath
    matches = process_device(device, ppath, quiet)
    if matches:
        absdpath = svdpatch.abspath(sys.argv[0], dpath)
        common = os.path.commonprefix([absdpath] + matches)
        matches = [" - ../" + match[len(common):] for match in matches]
        if not quiet:
            print("\nMatched these new peripherals:")
            print("\n".join(matches))
        else:
            print(dpath)
            print("\n".join(matches))
        if update:
            print("Updating device YAML")
            with open(dpath, "a") as f:
                f.write("\n".join(matches))
                f.write("\n")
        print()
    else:
        if not quiet:
            print("No new peripherals matched.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument("peripherals")
    parser.add_argument("devices", nargs="*")
    args = parser.parse_args()
    for device in args.devices:
        main(device, args.peripherals, args.update, args.quiet)
