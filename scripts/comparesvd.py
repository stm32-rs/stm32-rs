import sys
import xml.etree.ElementTree as ET

s1 = ET.parse(sys.argv[1])
s2 = ET.parse(sys.argv[2])


def getregs(s):
    regs = {}
    for peripheral in s.iter('peripheral'):
        pname = peripheral.find('name').text
        base = int(peripheral.find('baseAddress').text, 0)
        for register in peripheral.iter('register'):
            rname = register.find('name').text
            name = pname + "_" + rname
            offset = int(register.find('addressOffset').text, 0)
            regs[name] = hex(base+offset)
    return regs

r1 = getregs(s1)
r2 = getregs(s2)

for reg in r1:
    if reg not in r2:
        print("+A", reg, r1[reg])
    else:
        if r1[reg] != r2[reg]:
            print("X ", reg, r1[reg], r2[reg])
for reg in r2:
    if reg not in r1:
        print("+B", reg, r2[reg])
