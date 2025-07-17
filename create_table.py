#!/usr/bin/python

print("Reads in output file from computehfk, creates table. One argument: the filename.")

import sys

assert(len(sys.argv) == 2)
filename = sys.argv[1]

lines = []
with open(filename) as my_file:
    lines = my_file.readlines()

# Remove empty lines
lines = [x for x in lines if len(x) > 2]
# Remove header and footer of computehfk output
lines = lines[4:-7]

homology = dict()
alex_support = set()
maslov_support = set()
for l in lines:
    t1 = l.split(" ")
    rank = int(t1[0])
    t2 = t1[3].split(",")
    alex = int(t2[0][1:])
    alex_support.add(alex)
    maslov = int(t2[1][:-2])
    maslov_support.add(maslov)
    assert(not (alex,maslov) in homology)
    homology[alex,maslov] = rank


alex_min = min(alex_support)
alex_max = max(alex_support)
maslov_min = min(maslov_support)
maslov_max = max(maslov_support)

# Add axes
for m in range(maslov_min, maslov_max + 1):
    homology[alex_min - 1, m] = m
for a in range(alex_min, alex_max + 1):
    homology[a, maslov_min - 1] = a


print('\\begin{tblr}[b]{hlines={0.7pt, solid}, vlines={0.7pt, solid}, hline{3-Y} = {0.3pt, dashed}, vline{3-Y} = {0.3pt, dashed}, rowspec={*{' + str(2 + maslov_max - maslov_min) + '}c}, rows={9mm}, columns={9mm}, rowsep=0mm, colsep=0mm}')
#print("\\begin{tabular}{|*" + str(alex_max - alex_min + 2) + "{c|}}\\hline")
#print("\\begin{TAB}(e,8mm,8mm){c|" + "c." * (alex_max - alex_min) + "c}{c|" + "c." * (maslov_max - maslov_min) + "c}")
for m in range(maslov_min - 1, maslov_max + 1):
    s = ''
    for a in range(alex_min - 1, alex_max + 1):
        s += '$' + str(homology[a,m]) + '$' if (a,m) in homology else ' '
        s += '\t& '
    s = s[:-2] + '\\\\'
    print(s)
#print("\\end{TAB}")
print("\\end{tblr}")
