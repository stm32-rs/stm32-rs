import argparse
import os.path
import xml.etree.ElementTree as ET


def iter_peripherals(tree):
    for ptag in tree.iter('peripheral'):
        yield ptag


def iter_registers(ptag):
    for rtag in ptag.iter('register'):
        yield rtag


def iter_fields(rtag):
    for ftag in rtag.iter('field'):
        yield ftag


def parse(svdfile):
    tree = ET.parse(svdfile)
    peripherals = {}
    for ptag in iter_peripherals(tree):
        registers = {}
        pname = ptag.find('name').text
        pbase = int(ptag.find('baseAddress').text, 0)
        for rtag in iter_registers(ptag):
            fields = {}
            rname = rtag.find('name').text
            roffset = int(rtag.find('addressOffset').text, 0)
            for ftag in iter_fields(rtag):
                fname = ftag.find('name').text
                foffset = int(ftag.find('bitOffset').text, 0)
                fwidth = int(ftag.find('bitWidth').text, 0)
                fields[fname] = {"name": fname, "offset": foffset,
                                 "width": fwidth}
            registers[rname] = {"name": rname, "offset": roffset,
                                "fields": fields}
        peripherals[pname] = {"name": pname, "base": pbase,
                              "registers": registers}
        if 'derivedFrom' in ptag.attrib:
            peripherals[pname]["derives"] = ptag.attrib["derivedFrom"]
    for pname, periph in list(peripherals.items()):
        if 'derives' in periph:
            peripherals[pname]['registers'] = \
                peripherals[periph['derives']]['registers']
    return {"name": svdfile.split(".")[0], "peripherals": peripherals}


def who_has_what_peripherals(parts):
    peripherals = {}
    for part in parts:
        for pname, periph in part['peripherals'].items():
            name = (pname, periph['base'])
            if name not in peripherals:
                peripherals[name] = []
            peripherals[name].append(part['name'])
    return peripherals


def who_has_what_peripheral_registers(parts, peripheral):
    registers = {}
    for part in parts:
        for pname, periph in part['peripherals'].items():
            if pname != peripheral[0] or periph['base'] != peripheral[1]:
                continue
            for rname, reg in periph['registers'].items():
                name = (reg['offset'], rname)
                if name not in registers:
                    registers[name] = []
                registers[name].append(part['name'])
    return registers


def who_has_what_register_fields(parts, peripheral, register):
    fields = {}
    for part in parts:
        for pname, periph in part['peripherals'].items():
            if pname != peripheral[0] or periph['base'] != peripheral[1]:
                continue
            for rname, reg in periph['registers'].items():
                if rname != register[1] or reg['offset'] != register[0]:
                    continue
                for fname, field in reg['fields'].items():
                    name = (field['offset'], field['width'], fname)
                    if name not in fields:
                        fields[name] = []
                    fields[name].append(part['name'])
    return fields

def html_page(title, table):
    out = ["""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">"""]
    out.append('<title>{}</title>'.format(title))
    out.append("""</head>
<style>
table thead tr th {
    position: sticky;
    top: 0;
    z-index: 6;
    background: white;
}
td:first-child {
    position: sticky;
    left: 0;
    z-index: 5;
    background: white;
}
</style>
<body>""")
    out.append('<h1>{}</h1>'.format(title))
    out.append(table)
    out.append("</body></html>")
    return "\n".join(out)

def html_table_peripherals(parts, peripherals):
    out=[]
    out.append("<table><thead><tr><th>Peripheral</th><th>Address</th>")
    for part in parts:
        out.append("<th>{}</th>".format(part['name'].replace('svd/', '')))
    out.append("</thead><tbody>")
    for periph in sorted(peripherals.keys()):
        name, base = periph
        base = "0x{:08X}".format(base)
        periph_parts = peripherals[periph]
        link = '<a href="{}_{}.html">{}</a>'.format(name, base, name)
        out.append("<tr><td>{}</td><td>{}</td>".format(link, base))
        for part in parts:
            if part['name'] in periph_parts:
                out.append('<td align=center bgcolor="#ccffcc">&#10004;</td>')
            else:
                out.append('<td align=center bgcolor="#ffcccc">&#10008;</td>')
        out.append("</tr>")
    out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def html_table_registers(parts, peripheral, registers):
    out = ["<table><thead><tr><th>Register</th><th>Offset</th>"]
    for part in parts:
        out.append("<th>{}</th>".format(part['name'].replace('svd/', '')))
    out.append("</thead><tbody>")
    for reg in sorted(registers.keys()):
        offset, name = reg
        offset = "0x{:04X}".format(offset)
        reg_parts = registers[reg]
        link = '<a href="{}_0x{:08X}_{}_{}.html">{}</a>'.format(
            peripheral[0], peripheral[1], name, offset, name)
        out.append("<tr><td>{}</td><td>{}</td>".format(link, offset))
        for part in parts:
            if part['name'] in reg_parts:
                out.append('<td align=center bgcolor="#ccffcc">&#10004;</td>')
            else:
                out.append('<td align=center bgcolor="#ffcccc">&#10008;</td>')
        out.append("</tr>")
    out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def html_table_fields(parts, peripheral, register, fields):
    out = ["<table><thead><tr><th>Field</th><th>Offset</th><th>Width</th>"]
    for part in parts:
        out.append("<th>{}</th>".format(part['name'].replace('svd/', '')))
    out.append("</thead><tbody>")
    for field in reversed(sorted(fields.keys())):
        offset, width, name = field
        field_parts = fields[field]
        out.append("<tr><td>{}</td><td>{}</td><td>{}</td>"
                   .format(name, offset, width))
        for part in parts:
            if part['name'] in field_parts:
                out.append('<td align=center bgcolor="#ccffcc">&#10004;</td>')
            else:
                out.append('<td align=center bgcolor="#ffcccc">&#10008;</td>')
        out.append("</tr>")
    out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def html_tables(parts):
    peripherals = who_has_what_peripherals(parts)
    files = {}
    peripheral_table = html_table_peripherals(parts, peripherals)
    peripheral_title = "Compare peripherals"
    files["index.html"] = html_page(peripheral_title, peripheral_table)
    for pname in peripherals:
        registers = who_has_what_peripheral_registers(parts, pname)
        register_table = html_table_registers(parts, pname, registers)
        register_title = "Registers In {} 0x{:08X}".format(*pname)
        filename = "{}_0x{:08X}.html".format(pname[0], pname[1])
        files[filename] = html_page(register_title, register_table)
        for rname in registers:
            fields = who_has_what_register_fields(parts, pname, rname)
            field_table = html_table_fields(parts, pname, rname, fields)
            field_title = "Fields In {}_{} (0x{:08X}, 0x{:04X})".format(
                pname[0], rname[1], pname[1], rname[0])
            filename = "{}_0x{:08X}_{}_0x{:04X}.html".format(
                pname[0], pname[1], rname[1], rname[0])
            files[filename] = html_page(field_title, field_table)
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("htmldir", help="Path to write HTML files to")
    parser.add_argument("svdfiles", help="Path to patched SVD files", nargs="*")
    args = parser.parse_args()

    parts = [parse(svdfile) for svdfile in args.svdfiles]
    files = html_tables(parts)
    for fn in files:
        with open(os.path.join(args.htmldir, fn), "w") as f:
            f.write(files[fn])

if __name__ == "__main__":
    main()
