from FieldClass import Field

f = Field(-400,400,-400,400)

f.setAttractionWeight(1)
f.setAttractionRadius(5)
f.setAttractionSpread(1132)

f.setRepulsionWeight(.5)
f.setRepulsionRadius(10)
f.setRepulsionSpread(100)

f.setTangentialWeight(2)
f.setTangentialRadius(10)
f.setTangentialSpread(30)

f.clearGoals()
f.clearObstacles()
f.addGoal(380,0)
f.addObstacle(-100,-100)
f.calculateFields()

print f.queryPosition(0, 100)

f.visualize()

