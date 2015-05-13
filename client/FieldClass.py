import numpy as np
import matplotlib.pyplot as plt

class Field:
    'Container for all potential fields with related methods'
    
    #set default weights for potential field types
    wAttractive = 1
    wRepulsive = 0.2
    wTangential = 0.5
    
    x_min = -10
    x_max = 10
    y_min = -10
    y_max = 10
    
    range_x = (x_max - x_min) + 1
    range_y = (y_max - y_min) + 1
    
    radiusAttractive = 1
    radiusRepulsive = 1
    radiusTangential = 1
    
    spreadAttractive = 1
    spreadRepulsive = 1
    spreadTangential = 1
    
    home = [0,0]
    homeIsGoal = False
    
    def __init__(self, minX, maxX, minY, maxY):
        print "Field initializing ..."
        self.wAttractive = 1
        self.wRepulsive = 0.2
        self.wTangential = 0.5
        self.x_min = minX
        self.x_max = maxX
        self.y_min = minY
        self.y_max = maxY
        self.range_x = (self.x_max - self.x_min) + 1
        self.range_y = (self.y_max - self.y_min) + 1
        self.radiusAttractive = 1
        self.radiusRepulsive = 1
        self.radiusTangential = 1
        self.spreadAttractive = 1
        self.spreadRepulsive = 1
        self.spreadTangential = 1
        
        self.homeIsGoal = False
        
        # setup matrices
        self.clearFields()
        self.clearGoals()
        self.clearObstacles()
    
    def clearFields(self):
        self.a_x = np.zeros((self.range_x, self.range_y))
        self.a_y = np.zeros((self.range_x, self.range_y))
        self.h_x = np.zeros((self.range_x, self.range_y))
        self.h_y = np.zeros((self.range_x, self.range_y))
        self.r_x = np.zeros((self.range_x, self.range_y))
        self.r_y = np.zeros((self.range_x, self.range_y))
        self.t_x = np.zeros((self.range_x, self.range_y))
        self.t_y = np.zeros((self.range_x, self.range_y))
        self.potential_x = np.zeros((self.range_x, self.range_y))
        self.potential_y = np.zeros((self.range_x, self.range_y))
        
    def getMaxAttraction(self):
        return (self.wAttractive * self.spreadAttractive)
    
    def setAttractionWeight(self, weight):
        self.wAttractive = weight
        
    def setRepulsionWeight(self, weight):
        self.wRepulsive = weight
        
    def setTangentialWeight(self, weight):
        self.wTangential = weight
        
    def setAttractionRadius(self, radius):
        self.radiusAttractive = radius
    
    def setRepulsionRadius(self, radius):
        self.radiusRepulsive = radius
        
    def setTangentialRadius(self, radius):
        self.radiusTangential = radius    
        
    def setAttractionSpread(self, spread):
        self.spreadAttractive = spread
    
    def setRepulsionSpread(self, spread):
        self.spreadRepulsive = spread
        
    def setTangentialSpread(self, spread):
        self.spreadTangential = spread    
    
    def clearGoals(self):
        self.goals = []
        
    def clearObstacles(self):
        self.obstacles = []
    
    def addGoal(self, goalX, goalY):
        self.goals.append([goalX, goalY])
        # print self.goals
        
    def setHomeBase(self, homeX, homeY):
        self.home = [homeX, homeY]
        
    def switchToHome(self, goalIsHome):
        self.homeIsGoal = goalIsHome
        if (self.homeIsGoal):
            self.potential_x = self.h_x + self.r_x + self.t_x
            self.potential_y = self.h_y + self.r_y + self.t_y
        else:
            self.potential_x = self.a_x + self.r_x + self.t_x
            self.potential_y = self.a_y + self.r_y + self.t_y
        
    def addObstacle(self, obstacleX, obstacleY):
        if ([obstacleX, obstacleY] not in self.obstacles):
            self.obstacles.append([obstacleX, obstacleY])
            # print "Obstacle added"
        
    def setupMap4Ls(self):
        self.clearFields()
        self.clearGoals()
        self.clearObstacles()
        self.addObstacle(150, 150); self.addObstacle(150, 90); self.addObstacle(90, 90); self.addObstacle(90.0, 150.0)
        self.addObstacle(150.0,210.0); self.addObstacle(150.0,150.0); self.addObstacle(90.0, 150.0); self.addObstacle(90.0, 210.0)
        self.addObstacle(210.0, 150.0); self.addObstacle(210.0, 90.0); self.addObstacle(150.0, 90.0); self.addObstacle(150.0, 150.0)
        self.addObstacle(150.0, -90.0); self.addObstacle(150.0, -150.0); self.addObstacle(90.0, -150.0); self.addObstacle(90.0, -90.0)
        self.addObstacle(210.0, -90.0); self.addObstacle(210.0, -150.0); self.addObstacle(150.0, -150.0); self.addObstacle(150.0, -90.0)
        self.addObstacle(150.0, -150.0); self.addObstacle(150.0, -210.0); self.addObstacle(90.0, -210.0); self.addObstacle(90.0, -150.0)
        self.addObstacle(-90.0, -90.0); self.addObstacle(-90.0, -150.0); self.addObstacle(-150.0, -150.0); self.addObstacle(-150.0, -90.0)
        self.addObstacle(-90.0, -150.0); self.addObstacle(-90.0, -210.0); self.addObstacle(-150.0, -210.0); self.addObstacle(-150.0, -150.0)
        self.addObstacle(-150.0, -90.0); self.addObstacle(-150.0, -150.0); self.addObstacle(-210.0, -150.0); self.addObstacle(-210.0, -90.0)
        self.addObstacle(-90.0, 150.0); self.addObstacle(-90.0, 90.0); self.addObstacle(-150.0, 90.0); self.addObstacle(-150.0, 150.0)
        self.addObstacle(-90.0, 210.0); self.addObstacle(-90.0, 150.0); self.addObstacle(-150.0, 150.0); self.addObstacle(-150.0, 210.0)
        self.addObstacle(-150.0, 150.0); self.addObstacle(-150.0, 90.0); self.addObstacle(-210.0, 90.0); self.addObstacle(-210.0, 150.0)
        self.addObstacle(10.0,60.0);self.addObstacle(10.0,-60.0);self.addObstacle(-10.0, -60.0);self.addObstacle(-10.0, 60.0)
        self.addObstacle(10, 20); self.addObstacle(10, -20); self.addObstacle(-10.0, -20.0);self.addObstacle(-10.0, 20.0)
        self.addGoal(370,0)
        self.setHomeBase(-370, 0)
        
    def setupMapRotatedBoxes(self):
        self.clearFields()
        self.clearGoals()
        self.clearObstacles()
        self.addObstacle(100.0, 42.4264068712); self.addObstacle(142.426406871, 0.0); self.addObstacle(100.0, -42.4264068712); self.addObstacle(57.5735931288, 0)
        self.addObstacle(-100.0, 42.4264068712); self.addObstacle(-57.5735931288, 0.0); self.addObstacle(-100.0, -42.4264068712); self.addObstacle(-142.426406871, 0)
        self.addObstacle(0, 142.426406871); self.addObstacle(42.4264068712, 100.0); self.addObstacle(0, 57.5735931288); self.addObstacle(-42.4264068712, 100.0)
        self.addObstacle(0, -57.5735931288); self.addObstacle(42.4264068712, -100.0); self.addObstacle(0, -142.426406871); self.addObstacle(-42.4264068712, -100.0);
        self.addGoal(-370,0)
        self.setHomeBase(370, 0)

    def distance(self, p1, p2):
        return np.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )
        
    def calculateFields(self):
        maxrepx = 0
        maxrepy = 0
        print "Calculating fields ..."
        for i in range(self.range_x):
            for j in range(self.range_y):
                xPos = self.x_min + i
                yPos = self.y_min + j
                # calculate attraction
                # iterate through each goal
                for g in self.goals:
                    # calculate distance from goal
                    dist = self.distance((xPos, yPos), g)
                    theta = np.arctan2(g[1] - yPos, g[0] - xPos)
                    # theta = np.arctan2(yPos -g[1], xPos - g[0])
                    # print '( {0:d}, {1:d} ) = {2:.2f} @ {3:.1f}' . format(xPos, yPos, dist, np.degrees(theta))
                    # evaluate cases and store in matrix
                    if (dist < self.radiusAttractive):
                        self.a_x[j][i] += 0
                        self.a_y[j][i] += 0
                    elif ((self.radiusAttractive <= dist) and (dist <= (self.radiusAttractive + self.spreadAttractive))):
                        self.a_x[j][i] += self.wAttractive * ( (dist - self.radiusAttractive)*np.cos(theta) )
                        self.a_y[j][i] += self.wAttractive * ( (dist - self.radiusAttractive)*np.sin(theta) )
                    elif (dist > (self.radiusAttractive + self.spreadAttractive)):
                        self.a_x[j][i] += self.wAttractive * self.spreadAttractive * np.cos(theta)
                        self.a_y[j][i] += self.wAttractive * self.spreadAttractive * np.sin(theta)
                
                # calculate for home base
                dist = self.distance((xPos, yPos), self.home)
                theta = np.arctan2(self.home[1] - yPos, self.home[0] - xPos) 
                if (dist < self.radiusAttractive):
                    self.h_x[j][i] += 0
                    self.h_y[j][i] += 0
                elif ((self.radiusAttractive <= dist) and (dist <= (self.radiusAttractive + self.spreadAttractive))):
                    self.h_x[j][i] += self.wAttractive * ( (dist - self.radiusAttractive)*np.cos(theta) )
                    self.h_y[j][i] += self.wAttractive * ( (dist - self.radiusAttractive)*np.sin(theta) )
                elif (dist > (self.radiusAttractive + self.spreadAttractive)):
                    self.h_x[j][i] += self.wAttractive * self.spreadAttractive * np.cos(theta)
                    self.h_y[j][i] += self.wAttractive * self.spreadAttractive * np.sin(theta)   
                
                for o in self.obstacles:
                    dist = self.distance((xPos, yPos), o)
                    theta = np.arctan2(o[1] - yPos, o[0] - xPos)
                    repx = 0
                    repy = 0
                    if (dist < self.radiusRepulsive):
                        repx = (-np.sign(np.cos(theta)) * 1) # set to zero? tank cannot be inside
                        repy = (-np.sign(np.sin(theta)) * 1) # set to zero? tank cannot be inside
                    elif ((self.radiusRepulsive <= dist) and (dist <= (self.radiusRepulsive + self.spreadRepulsive))):
                        repx = -self.wRepulsive * ( (self.spreadRepulsive + self.radiusRepulsive - dist) * np.cos(theta))
                        repy = -self.wRepulsive * ( (self.spreadRepulsive + self.radiusRepulsive - dist) * np.sin(theta))
                    elif (dist > (self.radiusRepulsive + self.spreadRepulsive)):    
                        repx = 0
                        repy = 0
                    self.r_x[j][i] += repx
                    self.r_y[j][i] += repy
                    
                    #if (np.abs(repx) > maxrepx):
                    #    maxrepx = np.abs(repx)
                    #    print 'new max X at %s, %s of %s' % (self.x_min+i,self.y_min+j,maxrepx)
                    #if (np.abs(repy) > maxrepy):
                    #    maxrepy = np.abs(repy)
                    #    print 'new max Y at %s, %s of %s' % (self.x_min+i,self.y_min+j,maxrepy)
                    # calculate tangents
                    
                    clockwise = theta - (np.pi / 2)
                    c_clockwise = theta + (np.pi / 2)

                    # TO-DO: pick clockwise / counter-clockwise based on position of point in relation to the goal
                    # TO-DO: adjust magnitude based on % parallel to angle from obstacle to goal    
                    if ((self.radiusTangential <= dist) and (dist <= (self.radiusTangential + self.spreadTangential))):
                        self.t_x[j][i] += -self.wTangential * 1 * np.cos(clockwise)
                        self.t_y[j][i] += -self.wTangential * 1 * np.sin(clockwise)

        # combine
        self.potential_x = self.a_x + self.r_x + self.t_x
        self.potential_y = self.a_y + self.r_y + self.t_y

    
    def queryPosition(self, posX, posY):
        x = min(max(np.round(posX, 0), self.x_min), self.x_max) - self.x_min
        y = min(max(np.round(posY, 0), self.y_min), self.y_max) - self.y_min
        # print x, y
        return [self.potential_x[y][x], self.potential_y[y][x]]
    
    def visualize(self, attractive, repulsive, tangential):
        print "Preparing viz export ..."
        
        viz_x = np.zeros((self.range_x, self.range_y))
        viz_y = np.zeros((self.range_x, self.range_y))
        
        if (attractive):
            viz_x += self.a_x
            viz_y += self.a_y
        if (repulsive):
            viz_x += self.r_x
            viz_y += self.r_y
        if (tangential):
            viz_x += self.t_x
            viz_y += self.t_y
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        segments = 50
        spacebetween = (self.x_max - self.x_min) / segments
        
        starting = spacebetween / 2
        x = np.linspace(self.x_min, self.x_max, segments)
        y = np.linspace(self.y_min, self.y_max, segments)
        x,y = np.meshgrid(x,y)
        sampled_x = np.zeros(np.shape(x))
        sampled_y = np.zeros(np.shape(y))
        for i in range(0,segments,1):
            for j in range(0,segments,1):
                sampled_x[j][i] = viz_x[starting + j * spacebetween][starting + i * spacebetween]
                sampled_y[j][i] = viz_y[starting + j * spacebetween][starting + i * spacebetween]
        # print np.sum(sampled_x)
        ax.quiver(x, y, sampled_x, sampled_y, pivot='mid', color='r', headlength=6, headwidth=4, units='inches')
        '''
        x = np.linspace(self.x_min, self.x_max)
        y = np.linspace(self.y_min, self.y_max)
        ax.quiver(x[::10, ::10], y[::10, ::10], viz_x[::10, ::10], viz_y[::10, ::10], pivot='mid', color='r')
        '''
        for g in self.goals:
            fig.gca().add_artist(plt.Circle(g, radius=self.radiusAttractive, color='g', fill=False))
        for o in self.obstacles:
            fig.gca().add_artist(plt.Circle(o, radius=self.radiusRepulsive, color='black', fill=False))
        plt.show()
    

