import math, sys, numpy
from CustomFieldClass import Field

f = Field(-5,5,-5,5)
occupancyGrid = numpy.array( [ (0,0,0,0,0,0,0,0,0,0 ), 
                              (0,0,0,0,0,0,0,0,0,0), 
                              (0,0,1,1,1,0,0,0,0,0), 
                              (0,0,1,1,1,0,0,0,0,0),
                              (0,0,0,0,0,0,0,0,0,0),
                              (0,0,0,0,0,1,1,1,0,0),
                              (0,0,0,0,0,1,1,1,0,0),
                              (0,0,0,0,0,0,0,0,0,0),
                              (0,0,0,0,0,0,0,0,0,0) ] )

AoccupancyGrid = numpy.array( [ (0,0,0,0,0,0,0,0,0,0 ), 
                              (0,0,0,0,0,0,0,0,0,0), 
                              (0,0,0,0,0,0,0,0,0,0), 
                              (0,0,0,0,1,0,0,0,0,0),
                              (0,0,0,0,0,0,0,0,0,0),
                              (0,0,0,0,0,0,0,0,0,0),
                              (0,0,0,0,0,0,0,0,0,0),
                              (0,0,0,0,0,0,0,0,0,0),
                              (0,0,0,0,0,0,0,0,0,0) ] )

print occupancyGrid

threshhold = 1
resolution = 1
row = 0
column = 0
obstacles = []

for y in occupancyGrid:
    first = 0
    firstPair = False
    if row % resolution == 0:
        for x in y:
            if x >= threshhold and column == len(occupancyGrid[1]):
                obstacles.append([column-1-5,5-row])
                if firstPair:
                    obstacles.append([first-5, 5-row])
                    first = False
                #print ('appended right edge [{},{}]').format(row, first)
            elif x >= threshhold:
                if not firstPair:
                    first = column
                    firstPair = True
                    #print ('appended left obstacle [{},{}]').format(row, first)
            else:
                if column != 0 and firstPair:
                    obstacles.append([first-5, 5-row])
                    obstacles.append([column-1-5, 5-row])
                    firstPair = False
                    #print ('appended right obstacle [{},{}]').format(row, first)
            column = column + 1   
    column = 0
    row = row + 1
row = 0

print obstacles

f.setupMap(obstacles)
#f.setupMapRotatedBoxes()

#f.calculateFields()

f.fastCalculate()

#f.visualize(False, True, False)
f.drawFast(False, True, False)
