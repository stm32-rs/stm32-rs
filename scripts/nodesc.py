import os.path
import argparse
import xml.etree.ElementTree as ET

def parseargs():
    """Parse our command line arguments, returns a Namespace of results."""
    parser = argparse.ArgumentParser()
    parser.add_argument("svd", help="Path to SVD file to load")
    parser.add_argument("out", help="Path to SVD file to save")
    args = parser.parse_args()
    return args

def recursive_xml(root):
    if root.getchildren() is not None:
        for child in root.getchildren():
            if child.tag in ('description', 'writeConstraint', 'enumeratedValues'):
                root.remove(child)
            else:
                recursive_xml(child)

def sort_svd(pp, down=True):
    for p in pp.iter("peripheral"):
        print("\t"+p.findtext("name"))
        if 'derivedFrom' in p.attrib:
            continue
        rr = p.find("registers")
        sort_registers(rr)
        
        for r in rr.iter("register"):
            ff = r.find("fields")
            sort_fields(ff, down)
        
        for c in rr.iter("cluster"):
            #sort_registers(c)
            for r in c.iter("register"):
                ff = r.find("fields")
                sort_fields(ff, down)

def sort_fields(ff, down=True):
    if ff:
        fields = []
        for f in ff:
            key = int(f.findtext("bitOffset"))
            fields.append((key, f))
        if down:
            fields.sort(reverse=True, key=lambda x: x[0])
        else:
            fields.sort(key=lambda x: x[0])
        ff[:] = [item[-1] for item in fields]

def sort_registers(rr):
    if rr:
        registers = []
        for r in rr:
            txt = r.findtext("addressOffset")
            key = int(txt, 16)
            registers.append((key, r))
        registers.sort(key=lambda x: x[0])
        rr[:] = [item[-1] for item in registers]

def main():
    # Load the specified YAML root file
    args = parseargs()
    with open(args.svd) as f:
        svd = ET.parse(f)

    pp = svd.find('peripherals')
    recursive_xml(pp)
    sort_svd(pp)

    # SVD should now be updated, write it out
    svd.write(args.out)

if __name__ == "__main__":
    main()
