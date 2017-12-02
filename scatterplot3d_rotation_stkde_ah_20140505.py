from mayavi.mlab import *
import os
import math
import inspect

# Dear user, please specify the parameters below. If you don't do as instructed, the python will eat you!
#=========================================================================================================
range1 = 45             # Upper temporal boundary of disease phase 1 (emergence). Must be higher than 3. Hint: 45          
range2 = 65             # Upper temporal boundary of disease phase 2 (dominance). Hint: 65
range3 = 130            # Upper temporal boundary of disease phase 3 (decrease). Hint: 130   

p = 1                   # Exponential factor p            
yr = 880000             # Rotation axis

inFilePath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + os.sep + "AllCases2010_stkde.txt"   # Specify input file containing coordinates of points
#=========================================================================================================

inFile = open(inFilePath, "r")

# define empty lists
inX, inY, inT, inC, inA, inY2, inT2 = [], [], [], [], [], [], []

# loop through input file (rows) and append values to lists
for record in inFile:

    inX.append(float(record.split("\t")[0]))                # x-coordinate
    inY.append(float(record.split("\t")[1]))                # y-coordinate
    inT.append(float(record.split("\t")[2]))                # t-coordinate
    inC.append(pow(float(record.split("\t")[3]), 2) * 2)    # color

inFile.close()

# define counters
p1, p2, p3, p4 = 0, 0, 0, 0

# loop through list of t-coordinates and, depending on which phase 
# the value belongs to calculate angle and append it to list.
for T in inT:
    
    if T <= range1:
        inA.append(pow(T/(range1), p) * 120)
        p1 = p1 + 1
    elif T <= range2:
        inA.append(pow(T/(range2), p) * 240)
        p2 = p2 + 1
    elif T <= range3:
        inA.append(pow(T/(range3), p) * 360)
        p3 = p3 + 1
    else:
        inA.append(359)
        p4 = p4 + 1
    
    
# loop though lists of y and t coordinates and angles. Calculate new position of point.
# depending angle, formula changes (sectors).    
for y1, t1, a1 in zip(inY, inT, inA):
    
    if a1 <= 90:
        inY2.append(yr - math.cos(math.radians(a1)) * (yr - y1))
        inT2.append(t1 + math.sin(math.radians(a1)) * (yr - y1))
    elif a1 <= 180:
        inY2.append(yr + math.cos(math.radians(180 - a1)) * (yr - y1))
        inT2.append(t1 + math.sin(math.radians(180 - a1)) * (yr - y1))
    elif a1 <= 270:
        inY2.append(yr + math.cos(math.radians(a1 - 180)) * (yr - y1))            
        inT2.append(t1 - math.sin(math.radians(a1 - 180)) * (yr - y1))
    else:
        inY2.append(yr - math.cos(math.radians(360 - a1)) * (yr - y1))            
        inT2.append(t1 - math.sin(math.radians(360 - a1)) * (yr - y1))         


# display the plot using MayaVi
points3d(inX, inY2, inT2, inC, opacity=.5, colormap="copper", scale_factor=40.0)

print(p1)
print(p2)
print(p3)
print(p4)
