import argparse
import xml.etree.ElementTree as ET
import pprint

from collections import defaultdict

from svdtools import patch


def main(svdfile):
    tree = ET.parse(svdfile)
    field_tims = defaultdict(set)
    for ptag in patch.iter_peripherals(tree, "TIM*"):
        pname = ptag.find('name').text
        for rtag in patch.iter_registers(ptag, "*"):
            rname = rtag.find('name').text
            for ftag in patch.iter_fields(rtag, "*"):
                fname = ftag.find('name').text
                rfname = "{}.{}".format(rname, fname)
                field_tims[rfname].add(pname)
    for ptag in tree.iter('peripheral'):
        pname = ptag.find('name').text
        if patch.matchname(pname, "TIM*"):
            if "derivedFrom" in ptag.attrib:
                derives = ptag.attrib["derivedFrom"]
                for _, tims in field_tims.items():
                    if derives in tims:
                        tims.add(pname)
    tims_field = defaultdict(lambda: defaultdict(list))
    for field, timers in field_tims.items():
        rname, fname = field.split(".")
        tims = list(timers)
        tims.sort(key=lambda x: int(x[3:]))
        tims_field[tuple(tims)][rname].append(fname)
    tf = list(tims_field.items())
    tf.sort(key=lambda x: len(x[0]))
    for tims, regs in tf:
        print("\n" + ", ".join(tims) + ":")
        for reg in sorted(list(regs.keys())):
            print("   ", reg + ":", " ".join(sorted(regs[reg])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("svdfile")
    args = parser.parse_args()
    main(args.svdfile)
