from FieldClass import Field

f = Field(-400,400,-400,400)
'''
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
'''
f.clearGoals()
f.clearObstacles()
f.addGoal(370,0) # green flag
f.addObstacle(-100,-100)
'''

f.setupMap4Ls()
#f.setupMapRotatedBoxes()

#f.calculateFields()

f.fastCalculate()

print f.getFast(297, 50), f.getFast(300, 50), f.getFast(303, 50)
print f.getFast(-297, 50), f.getFast(-300, 50), f.getFast(-303, 50)
f.drawFast(True, True, True)

f.goToHome(True)
print f.getFast(297, 50), f.getFast(300, 50), f.getFast(303, 50)
print f.getFast(-297, 50), f.getFast(-300, 50), f.getFast(-303, 50)
f.drawFast(True, True, True)
#
#f.setupMapRotatedBoxes()
#f.fastCalculate()
#f.drawFast(True, True, True)


#print f.queryPosition(0, 100)

#f.visualize(True, True, True) # all fields
#f.visualize(True, False, False) # attractive only
#f.visualize(False, True, False) # repulsive only
#f.visualize(False, False, True) # tangential only
