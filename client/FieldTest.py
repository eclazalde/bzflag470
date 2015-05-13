from FieldClass import Field

f = Field(-400,400,-400,400)

f.setAttractionWeight(1)
f.setAttractionRadius(5)
f.setAttractionSpread(1132)

f.setRepulsionWeight(.5)
f.setRepulsionRadius(2)
f.setRepulsionSpread(50)

f.setTangentialWeight(2)
f.setTangentialRadius(10)
f.setTangentialSpread(12)

'''
f.clearGoals()
f.clearObstacles()
f.addGoal(370,0) # green flag
f.addObstacle(-100,-100)
'''

#f.setupMap4Ls()
f.setupMapRotatedBoxes()

f.calculateFields()

#print f.queryPosition(0, 100)

f.visualize(True, True, True) # all fields
#f.visualize(True, False, False) # attractive only
#f.visualize(False, True, False) # repulsive only
#f.visualize(False, False, True) # tangential only
