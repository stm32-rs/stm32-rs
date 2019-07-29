import os
import argparse
import xml.etree.ElementTree as ET


def parse_device(svdfile):
    interrupts = {}
    tree = ET.parse(svdfile)
    dname = tree.find("name").text
    for ptag in tree.iter('peripheral'):
        pname = ptag.find('name').text
        for itag in ptag.iter('interrupt'):
            name = itag.find('name').text
            value = itag.find('value').text
            desc = itag.find('description').text.replace("\n", " ")
            interrupts[int(value)] = {"name": name,
                                      "desc": desc,
                                      "pname": pname}
    return dname, interrupts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("outdir", help="directory to write files to")
    parser.add_argument("svdfiles", nargs="*", help="List of SVD files")
    args = parser.parse_args()
    devices = {}
    for f in args.svdfiles:
        name, interrupts = parse_device(f)
        devices[name] = interrupts
        missing = set()
        with open(os.path.join(args.outdir, name), "w") as f:
            lastint = -1
            for val in sorted(interrupts.keys()):
                for v in range(lastint+1, val):
                    missing.add(v)
                lastint = val
                i = interrupts[val]
                f.write("{} {}: {} (in {})\n".format(
                    val, i["name"], i["desc"], i["pname"]))
            f.write("\nGaps: {}\n"
                    .format(", ".join(str(x) for x in sorted(missing))))


if __name__ == "__main__":
    main()
