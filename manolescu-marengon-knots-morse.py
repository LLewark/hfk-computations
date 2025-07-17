#!/usr/bin/python3
# For Morse code format, see documentation at
# https://cbz20.raspberryip.com/code/khtpp/docs/Input.html

import subprocess, os

def morse2PD(m):
    result = subprocess.run(['./morse2pd.py', m], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')[:-1]

import sys

assert(len(sys.argv) == 2)
strands = int(sys.argv[1])
assert (strands >= 1)

s = ""
for i in range(2 * strands):
    s += ("l" if (i%4) in [0,3] else "r") + str(i) + "."
for i in range(strands - 1):
    s += "y" + str(2*i+1) + "."
for i in range(strands):
    s += ("l" if (i%2) == 0 else "r") + str(2*i+1) + ".y" + str(2*i) + ".y" + str(2*i + 2) + ".u" + str(2*i+1) + "."
t = "";
for i in range(2*strands - 1):
    t += "y" + str(i) + "."
s += t * (2*strands)
for i in range(2*strands):
    s += "u" + str(2*strands - i - 1) + "."
s = s[:-1] + ","

print(s)
print(morse2PD(s))
