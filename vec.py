#!/usr/bin/env python

import os
import numpy
from numpy import reshape
from os.path import splitext
from os.path import abspath

#***************************************************************
# IMPORTANT!!
# All indeces saved (eg. in flagged) are the ATOM INDEX, not the
# line number. Everything has to be normalized to the ATOM INDEX.
#***************************************************************

# NOTE:
# The .xyz file nees an empty line at the end of the data set.
# The vec.dat file can not have an empty line at the end of the data.
# Make sure '+1'/'+0' is chosen correctly.


# AUTOMATE:
# - 'babel' call to generate .xyz file
# - Renaming of 'babel' output (ads '1' inside file name)
# - 'vec.dat' file generation from 'forcets.out' file

# IMPROVE:
# - Opportunities for 'numpy.array' methods, ie. 'ravel', 'reshape', ...?
# - 'filter' instead of 'is in' condition

# Write the normal mode corresponding to imaginary frequency
# into .dat file.  
data = open('vec7.dat', 'r')
value = data.readlines()


# Script then calculates the absolute value of the normal
# mode for every atom:
# [x1**2 + y1**2 + z1**2, x2**2 + y2**2 + z2**2, ..., xn**2 + yn**2 + zn**2]
comp = [eval(value[i])**2 + eval(value[i+1])**2 + eval(value[i+2])**2 for i in range(0, len(value), 3)] 

# Printing the absolute values of the normal mode for every atom
# in the order they were flagged '+1':
# comp[0] = absolute value of normal mode on first '+1' atom, ...
print 'absolut values of vector:', [str(i) for i in comp]

# Sorting by decreasing absolute value
comp.sort(reverse=True)

# Printing the absolute value of the normal mode for every atom
# from largest to lowest. Find the same value in the above print,
# then in the '.mop' file this atom can be identified.
print 'sorted values:', [str(i) for i in comp] 

def getConstAtoms(mopfile):
    # Get the atom identifier for which flag +1 is set in FORCETS
    # As a guideline, if the last job was a TS search, then
    # the value has to be set to the flag of the majority of flags.
    mopdata = open(mopfile, 'r')
    mopvalue = mopdata.readlines() 
    for i in range(len(mopvalue)):
        if mopvalue[i] == '':
            pass
        # Not really sure how this is working.
        if '+0' in mopvalue[i]:
            flagged.append(i-2)

def getVecComponents(vecfile):
    vecdata = open(vecfile, 'r')
    vecvalue = vecdata.readlines() 

    # Try numpy.reshape, numpy.ravel, ...
    # Starting point:
    # return reshape(numpy.array(vecvalue), (len(vecvalue)/3,3))
    # Still needs to strip the '\n' and whitespace.
    return [[vecvalue[i].strip(), vecvalue[i+1].strip(), vecvalue[i+2].strip()] for i in range(len(vecvalue)/3)]





# Approach:
# First add '0.0 0.0 0.0' to all but 1., 2. and last line.
# Then add the vector components.
def getXYZVibFile(xyzfile):
    # Open the '.xyz' file (generated by BABEL)
    # Automize '.xyz' file generation
    xyzdata = open(xyzfile, 'r') 
    xyzvalue = xyzdata.readlines() 
        
    # How does splitext() work?
    xyzvib = open(abspath(splitext(xyzfile)[0]) + '-vib.xyz', 'w')
    xyzvib.write('')
    xyzvib.close()

    xyzvib = open(abspath(splitext(xyzfile)[0]) + '-vib.xyz', 'w')

    # Add '0.0 0.0 0.0' to all atoms. 
    for i in range(len(xyzvalue)):
        if i == 0 or i == 1 or i == len(xyzvalue)-1:
            xyzvib.write(xyzvalue[i])
        else:
            xyzvib.write(xyzvalue[i][:-1] + '    ' + '0.0 0.0 0.0\n') 
    xyzvib.close()

    # Get flagged atoms.
    xyzvib = open(abspath(splitext(xyzfile)[0]) + '-vib.xyz', 'w')
    counter = 0
    for i in range(len(xyzvalue)):
        if i == 0 or i == 1 or i == len(xyzvalue)-1:
            xyzvib.write(xyzvalue[i])
        elif i-1 in flagged:
            #print i, xyzvalue[i][:-1], '    ', '    '.join(vec[counter])
            xyzvib.write(xyzvalue[i][:-1] + '    ' + '    '.join(vec[counter]) + '\n') 
            counter += 1
        else:
            #print i, xyzvalue[i][:-1], '    ' + '0.0 0.0 0.0'
            xyzvib.write(xyzvalue[i][:-1] + '    ' + '0.0 0.0 0.0\n')

        

    





flagged = []
# Provide file with flags.
mopfile = '3-wt-ts7-inv.mop'

# Needs to be written by the user.
vecfile = 'vec7.dat'

# Use 'babel'.
xyzfile = '3-wt-ts7-inv.xyz'

getConstAtoms(mopfile)
print 'flagged', flagged

vec = getVecComponents(vecfile)
print 'vec', vec

getXYZVibFile(xyzfile)



