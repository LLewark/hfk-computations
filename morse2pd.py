#!/usr/bin/python3

# Takes one command line parameter, which represents a tangle in Morse code.
# For Morse code format, see documentation at
# https://cbz20.raspberryip.com/code/khtpp/docs/Input.html
# Outputs PD code of the tangle, see documentation at
# http://katlas.org/wiki/Planar_Diagrams

# Example:
# ./morse2pd.py l0.r1.y3.y2.y4.y3.x1.x0.x2.x1.y3.y2.y4.y3.u1.u0.l1.y2.y0.u1,0,1
# should output
# PD[X[[8,1,9,2]],X[[19,3,20,2]],X[[7,27,8,26]],X[[20,25,21,26]],X[[3,19,4,18]],X[[4,9,5,10]],X[[24,17,25,18]],X[[23,11,24,10]],X[[16,21,17,22]],X[[11,23,12,22]],X[[15,7,16,6]],X[[12,5,13,6]],X[[29,14,30,15]],X[[13,28,14,29]]
#
# Crossingless components (circles) of the diagram are ignored.

debug = 0

def pdebug(*args):
    # Uncomment the next line to get debugging messages
    # print(args)
    return

def goacross(i):
    global types
    if types[i // 4] in ['x','y']:
        diffs = [2, 2, -2, -2]
        return i + diffs[i % 4]
    if types[i // 4] in ['l','r']:
        diffs = ['error', 'error', 1, -1]
        return i + diffs[i % 4]
    diffs = [1, -1, 'error', 'error']
    return i + diffs[i % 4]

from sys import argv
m, topOrientations = argv[1].split(",",1)
if topOrientations == '':
    topOrientations = []
else:
    pdebug(topOrientations)
    topOrientations = [int(x) for x in topOrientations.split(",")]
pdebug("Top orientations:", topOrientations)

strands = [int(x[1:]) for x in m.split(".")]
# x, y, l, r or u
types = [x[0] for x in m.split(".")]
height = len(strands)
pdebug(height)

# Each entry in strands/types stands for one critical point.
# Each critical point has four "ends", ordered NE, NW, SW, SE (counterclockwise starting upper right)
# The ends are enumerated globally
# connections saves for each end which other end it is connected to, or to the top or bottom (if it is a loose end).
connections = ['to be done' for i in range(4 * height)]
maxStrand = max(strands) + 1
bottomStrands = []
for i in range(height):
    if types[i] == 'u':
        connections[4*i + 2] = 'nonexistent'
        connections[4*i + 3] = 'nonexistent'
        continue
    if types[i] in ['l', 'r']:
        connections[4*i] = 'nonexistent'
        connections[4*i + 1] = 'nonexistent'
    for j in [2,3]:
        pointX = strands[i] + j - 2
        pointY = i + 1
        pdebug("Starting at ", pointX, pointY)
        while True:
            if pointY == height:
                connections[4*i + j] = ['bottom', pointX]
                pdebug("Reached bottom at ", pointX)
                if len(bottomStrands) <= pointX:
                    bottomStrands += ['to be defined'] * (pointX - len(bottomStrands) + 1)
                bottomStrands[pointX] = 4*i + j
                break
            Xdiff = strands[pointY] - pointX
            if (Xdiff in [0, -1]) and types[pointY] in ['x','y','u']:
                thisIdx = 4*i + j
                otherIdx = 4*pointY  + (Xdiff + 1)
                pdebug("Hit a crossing or cup. Connecting ", thisIdx, otherIdx)
                connections[thisIdx] = otherIdx
                assert(connections[otherIdx] == 'to be done')
                connections[otherIdx] = thisIdx
                break
            if (Xdiff <= 0) and (types[pointY] == 'u'):
                pointX -= 2
                pdebug("It's a cup. Evading to ", pointX, pointY)
            if (Xdiff <= 0) and (types[pointY] in ['l', 'r']):
                pointX += 2
                pdebug("It's a cap. Evading to ", pointX, pointY)
            pointY += 1
            pdebug("Advancing to ", pointX, pointY)

topStrands = []
for i in range(maxStrand):
    for j in range(height):
        if (strands[j] != i):
            continue
        for k in [1,0]:
            if connections[4*j + k] == 'to be done':
                connections[4*j + k] = ['top', len(topStrands)]
                topStrands.append(4*j + k)

pdebug("Strands on top: ", topStrands, "Strands on bottom: ", bottomStrands)

pdebug("Now enumerate components.")
topComponents = ['to be done' for i in topStrands]
bottomComponents = ['to be done' for i in bottomStrands]
components = ['to be done' if connections[i] != 'nonexistent' else 'nonexistent' for i in range(4 * height)]

componentStart = []
componentEnd = []

currentComponent = 0
while True:
    i = -1
    if 'to be done' in topComponents:
        j = topComponents.index('to be done')
        i = topStrands[j]
        topComponents[j] = currentComponent
        switchOrientation = (topOrientations[j] == 1)
    elif 'to be done' in bottomComponents:
        j = bottomComponents.index('to be done')
        i = bottomStrands[j]
        bottomComponents[j] = currentComponent
        switchOrientation = "unclear"
    elif 'to be done' in components:
        i = components.index('to be done')
        switchOrientation = "unclear"
    else:
        break
    pdebug("Starting at", i)
    componentStart += [i]
    oldI = i
    while (type(i) != list) and (components[i] == 'to be done'):
        components[i] = currentComponent
        if types[i // 4] in ['l', 'r']:
            b = (((i % 4) == 2) and types[i // 4] == 'l') or (((i % 4) == 3) and types[i // 4] == 'r')
            assert(switchOrientation in ["unclear", b])
            switchOrientation = b
        pdebug("Setting component of ", i, "to", currentComponent, "and going across.")
        i = goacross(i)
        pdebug("Now at", i)
        components[i] = currentComponent
        pdebug("Setting component of ", i, "to", currentComponent, "and connecting.")
        oldI = i
        i = connections[i]
        pdebug("Now at", i)
    if (type(i) == list):
        if i[0] == 'top':
            topComponents[i[1]] = currentComponent
            b = (topOrientations[i[1]] == 0) 
            assert(switchOrientation in ["unclear", b])
            switchOrientation = b
            pdebug("Set top Component", i[1])
        else:
            bottomComponents[i[1]] = currentComponent
            pdebug("Set bottom Component", i[1])
    if (switchOrientation):
        componentEnd += [componentStart[-1]]
        componentStart[-1] = oldI
    else:
        componentEnd += [oldI]
    pdebug("Orientation needs to be switched:", switchOrientation)        
    pdebug("Done with component", currentComponent)
    pdebug("Top components", topComponents)
    pdebug("Bottom components", bottomComponents)
    pdebug("Components", components)
    currentComponent += 1

pdebug("Top components", topComponents)
pdebug("Bottom components", bottomComponents)
pdebug("Components and start and end points", components, componentStart, componentEnd)

pdebug("Now get PD code.")
pdIdx = 0
# Order in crossingcode same as for connections (NOT the same as for the final PD code result)
crossingcode = [["todo" for j in range(4)] if types[i] in ["x","y"] else "nocrossing" for i in range(len(types))]
crossingIncomingLower = ["todo" if types[i] in ["x","y"] else "nocrossing" for i in range(len(types))]
for i in range(len(componentStart)):
    j = componentStart[i]
    pdebug("Starting at", j)
    firstPdIdx = pdIdx
    lastsetJ = -1
    while True:
        oldJ = j
        j = goacross(j)
        pdebug("Going across to ", j)
        if types[j // 4] in ["x","y"]:
            if (types[j // 4] == "x" and ((oldJ % 4) in [0,2])) or (types[j // 4] == "y" and ((oldJ % 4) in [1,3])):
                crossingIncomingLower[j // 4] = oldJ % 4
            crossingcode[j // 4][oldJ % 4] = pdIdx
            pdebug("Set crossing code ", j//4, oldJ % 4, " to ", pdIdx)
            pdIdx += 1
            crossingcode[j // 4][j % 4] = pdIdx
            pdebug("And set crossing code ", j//4, j % 4, " to ", pdIdx)
            lastsetJ = j
            if (j == componentEnd[i]) and (type(connections[j]) == list):
                pdIdx += 1
        if j == componentEnd[i]:
            break
        j = connections[j]
        pdebug("Connecting to ", j)
    if (not type(connections[j]) == list):
        assert(lastsetJ != -1)
        crossingcode[lastsetJ // 4][lastsetJ % 4] = firstPdIdx
        pdebug("Set crossing code ", lastsetJ, " to first idx ", firstPdIdx)

pdebug("Now reordering according to the PD rule (lower incoming strand first, then counterclockwise.")
pdResult = []
for i in range(len(crossingcode)):
    x = crossingcode[i]
    assert(x != "todo")
    if x == "nocrossing":
        continue
    s = crossingIncomingLower[i]
    pdResult.append([x[s], x[(s + 1) % 4], x[(s + 2) % 4], x[(s + 3) % 4]])

print("PD[" + ",".join(["X" + str([y + 1 for y in x]).replace(" ","") for x in pdResult]) + "]")
