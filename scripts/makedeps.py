"""
makedeps.py
Copyright 2017 Adam Greig
Licensed under the MIT and Apache 2.0 licenses.

Generate make dependency file for each device.
"""

import yaml
import os.path
import argparse
import svdpatch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("devices", nargs="*")
    args = parser.parse_args()
    for dpath in args.devices:
        with open(dpath, encoding='utf-8') as f:
            device = yaml.safe_load(f)
        device["_path"] = dpath
        deps = svdpatch.yaml_includes(device)
        depname = ".deps/{}.d".format(
            os.path.splitext(os.path.basename(dpath))[0])
        svdname = "svd/{}.svd.patched".format(
            os.path.splitext(os.path.basename(dpath))[0])
        print("{} {}: {}".format(svdname, depname, " ".join(deps)))

if __name__ == "__main__":
    main()
