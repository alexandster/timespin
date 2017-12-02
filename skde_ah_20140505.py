import math

hs = 750                          # spatial bandwidth (in meters)
ht = 5                            # temporal bandwidth (in days)

inFile = open("AllCases2010.txt", "r")
outFile = open("AllCases2010_stkde.txt", "w")
##inFile = [1,2,3]
inFile2 = inFile
inList = []
for record in inFile:
    inList.append(record)
inList2 = inList
n = len(inList)

# 3D Kernel density estimation formula (see Nakaya & Yano, 2010 in Transactions in GIS)
def densityF(x, y, t, xi, yi, ti, n, hs, ht):
    u = (x-xi) / hs
    v = (y-yi) / hs
    w = (t-ti) / ht
    if  pow(u, 2) + pow(v, 2) < 1 and pow(w, 2) < 1:
        constantTerm = pow(10.0, 10) / (n * pow(hs, 2) * ht)
        Ks = (2 / math.pi) * (1 - pow(u, 2) - pow(v, 2))
        Kt = 0.75 * (1 - pow(w, 2))
        spaceTimeKDE = constantTerm * Ks * Kt
    else: spaceTimeKDE = 0
    return spaceTimeKDE

for line in inList:
    xCoord = float(line.split("\t")[0])
    yCoord = float(line.split("\t")[1])
    tCoord = float(line.split("\t")[2])

    density = 0.0
    
    for line2 in inList2:
        xiCoord = float(line2.split("\t")[0])
        yiCoord = float(line2.split("\t")[1])
        tiCoord = float(line2.split("\t")[2])
        
        nList = []

        if hs >= math.sqrt(pow(xCoord - xiCoord, 2) + pow(yCoord - yiCoord, 2)):
            if ht >= math.fabs(tCoord - tiCoord):
                density += densityF(xCoord, yCoord, tCoord, xiCoord, yiCoord, tiCoord, n, hs, ht)
            else:
                pass
        else:
            pass
        
    resultsSTKDE = str(xCoord) + "\t" + str(yCoord) + "\t" + str(tCoord) + "\t" + str(density) +"\n"

    outFile.write(resultsSTKDE)
    
outFile.close()

          
            
        
        

        
        
