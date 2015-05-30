import numpy as np
import matplotlib.pyplot as plt

class Field:
    'Container for all potential fields with related methods'
    
    #set default weights for potential field types
    wAttractive = 0
    wRepulsive = 0
    wTangential = 0
    
    radiusAttractive = 0
    radiusRepulsive = 0
    radiusTangential = 0
    
    spreadAttractive = 0
    spreadRepulsive = 0
    spreadTangential = 0
    
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    
    range_x = (x_max - x_min) + 1
    range_y = (y_max - y_min) + 1
    
    home = [0,0]
    homeIsGoal = False
    
    def __init__(self, minX, maxX, minY, maxY):
        #print "Field initializing ..."
        self.wAttractive = 0
        self.wRepulsive = 0
        self.wTangential = 0
        self.radiusAttractive = 0
        self.radiusRepulsive = 0
        self.radiusTangential = 0
        self.spreadAttractive = 0
        self.spreadRepulsive = 0
        self.spreadTangential = 0
        self.x_min = minX
        self.x_max = maxX
        self.y_min = minY
        self.y_max = maxY
        self.range_x = (self.x_max - self.x_min) + 1
        self.range_y = (self.y_max - self.y_min) + 1
        
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
        
    def setupConstants(self):
        self.setRepulsionWeight(2)
        self.setRepulsionSpread(5)
        self.setRepulsionRadius(1)
        
        self.setTangentialWeight(3)
        self.setTangentialSpread(10)
        self.setTangentialRadius(1)
        
        self.setAttractionWeight(8)
        self.setAttractionSpread(15)
        self.setAttractionRadius(1)
        
    def setupMap(self, obstacles, goal):
        self.clearFields()
        self.clearGoals()
        self.clearObstacles()
        for o in obstacles:
            self.addObstacle(o[0], o[1])
        self.addGoal(goal[0], goal[1])
        self.setupConstants()
        self.fastCalculate()
        
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
        
    def addObstacle(self, obstacleX, obstacleY):
        if ([obstacleX, obstacleY] not in self.obstacles):
            self.obstacles.append([obstacleX, obstacleY])

    def distance(self, p1, p2):
        return np.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )
    
    def fastCalculate(self):
        self.resolution = 20
        self.padding = self.resolution / 2
        self.fast_x_dim = ( self.x_max - self.x_min ) / self.resolution
        self.fast_y_dim = ( self.y_max - self.y_min ) / self.resolution
        self.fast_a_x = np.zeros((self.fast_x_dim, self.fast_y_dim))
        self.fast_a_y = np.zeros((self.fast_x_dim, self.fast_y_dim))
        self.fast_h_x = np.zeros((self.fast_x_dim, self.fast_y_dim))
        self.fast_h_y = np.zeros((self.fast_x_dim, self.fast_y_dim))
        self.fast_r_x = np.zeros((self.fast_x_dim, self.fast_y_dim))
        self.fast_r_y = np.zeros((self.fast_x_dim, self.fast_y_dim))
        self.fast_t_x = np.zeros((self.fast_x_dim, self.fast_y_dim))
        self.fast_t_y = np.zeros((self.fast_x_dim, self.fast_y_dim))
        for i in xrange(self.fast_x_dim):
            for j in xrange(self.fast_y_dim):
                xPos = self.x_min + self.padding + (i * self.resolution)
                yPos = self.y_min + self.padding + (j * self.resolution)
                #print '( %s, %s )' % (xPos, yPos)
                res = self.calcAttraction(xPos, yPos, self.home[0], self.home[1])
                self.fast_h_x[j][i] = res[0]
                self.fast_h_y[j][i] = res[1]
                for g in self.goals:
                    res = self.calcAttraction(xPos, yPos, g[0], g[1])
                    self.fast_a_x[j][i] += res[0]
                    self.fast_a_y[j][i] += res[1]
                for o in self.obstacles:
                    res = self.calcRepulsion(xPos, yPos, o[0], o[1])
                    self.fast_r_x[j][i] += res[0]
                    self.fast_r_y[j][i] += res[1]
                    res = self.calcTangent(xPos, yPos, o[0], o[1])
                    self.fast_t_x[j][i] += res[0]
                    self.fast_t_y[j][i] += res[1]
                
                    
        #print np.sum(self.fast_r_x), np.sum(self.fast_r_y)
                #print self.fast_a_x[j][i], self.fast_a_y[j][i]
        
    def getFast(self, posX, posY):
        posX = np.floor((posX - self.x_min) / self.resolution) 
        posY = np.floor((posY - self.y_min) / self.resolution)
        if (self.homeIsGoal):
            return [ self.fast_h_x[posY][posX] + self.fast_r_x[posY][posX] + self.fast_t_x[posY][posX], self.fast_h_y[posY][posX] + self.fast_r_y[posY][posX] + self.fast_t_y[posY][posX] ]
        else:
            return [ self.fast_a_x[posY][posX] + self.fast_r_x[posY][posX] + self.fast_t_x[posY][posX], self.fast_a_y[posY][posX] + self.fast_r_y[posY][posX] + self.fast_t_y[posY][posX] ]
    
    def drawFast(self, showAttraction, showRepulsion, showTangents):
        viz_x = np.zeros((self.fast_x_dim, self.fast_y_dim))
        viz_y = np.zeros((self.fast_x_dim, self.fast_y_dim))
        
        for i in xrange(self.fast_x_dim):
            for j in xrange(self.fast_y_dim):
                if (showAttraction):
                    if (self.homeIsGoal):
                        viz_x[j][i] += self.fast_h_x[j][i]
                        viz_y[j][i] += self.fast_h_y[j][i] 
                    else:
                        viz_x[j][i] += self.fast_a_x[j][i]
                        viz_y[j][i] += self.fast_a_y[j][i] 
                if (showRepulsion):
                    viz_x[j][i] += self.fast_r_x[j][i]
                    viz_y[j][i] += self.fast_r_y[j][i] 
                if (showTangents):
                    viz_x[j][i] += self.fast_t_x[j][i]
                    viz_y[j][i] += self.fast_t_y[j][i] 
                    
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        #print viz_x
        
        x = range(self.x_min+self.padding, self.x_max+1, self.resolution)
        y = range(self.y_min+self.padding, self.y_max+1, self.resolution)
        x,y = np.meshgrid(x,y)
        # print 'x: ', np.shape(x), 'y: ', np.shape(y), 'viz_x: ', np.shape(viz_x), 'viz_y: ', np.shape(viz_y)
        ax.quiver(x, y, viz_x, viz_y, pivot='mid', color='r', headlength=6, headwidth=4)

        for g in self.goals:
            fig.gca().add_artist(plt.Circle(g, radius=self.radiusAttractive, color='g', fill=False))
        for o in self.obstacles:
            fig.gca().add_artist(plt.Circle(o, radius=self.radiusRepulsive, color='black', fill=False))
        plt.show()
                        
    '''
    TO-DO: separate out calculation methods into distinct functions
    '''
    def calcAttraction(self, xPos, yPos, xGoal, yGoal):
        dist = self.distance((xPos, yPos), (xGoal, yGoal))
        theta = np.arctan2(yGoal - yPos, xGoal - xPos)
        if (dist < self.radiusAttractive):
            #self.a_x[j][i] += 0
            #self.a_y[j][i] += 0
            return [ 0, 0 ]
        elif ((self.radiusAttractive <= dist) and (dist <= (self.radiusAttractive + self.spreadAttractive))):
            #self.a_x[j][i] += self.wAttractive * ( (dist - self.radiusAttractive)*np.cos(theta) )
            #self.a_y[j][i] += self.wAttractive * ( (dist - self.radiusAttractive)*np.sin(theta) )
            return [ self.wAttractive * ( (dist - self.radiusAttractive)*np.cos(theta) ), self.wAttractive * ( (dist - self.radiusAttractive)*np.sin(theta) ) ]
        elif (dist > (self.radiusAttractive + self.spreadAttractive)):
            #self.a_x[j][i] += self.wAttractive * self.spreadAttractive * np.cos(theta)
            #self.a_y[j][i] += self.wAttractive * self.spreadAttractive * np.sin(theta)
            return [ self.wAttractive * self.spreadAttractive * np.cos(theta), self.wAttractive * self.spreadAttractive * np.sin(theta) ]
        return [0,0]
    
    def calcRepulsion(self, xPos, yPos, xObstacle, yObstacle):
        dist = self.distance((xPos, yPos), (xObstacle,yObstacle))
        theta = np.arctan2(yObstacle - yPos, xObstacle - xPos)
        #repx = 0
        #repy = 0
        if (dist < self.radiusRepulsive):
            #repx = (-np.sign(np.cos(theta)) * 1) # set to zero? tank cannot be inside
            #repy = (-np.sign(np.sin(theta)) * 1) # set to zero? tank cannot be inside
            return [ (-np.sign(np.cos(theta)) * 1), (-np.sign(np.sin(theta)) * 1) ]
        elif ((self.radiusRepulsive <= dist) and (dist <= (self.radiusRepulsive + self.spreadRepulsive))):
            #repx = -self.wRepulsive * ( (self.spreadRepulsive + self.radiusRepulsive - dist) * np.cos(theta))
            #repy = -self.wRepulsive * ( (self.spreadRepulsive + self.radiusRepulsive - dist) * np.sin(theta))
            return [ -self.wRepulsive * ( (self.spreadRepulsive + self.radiusRepulsive - dist) * np.cos(theta)), -self.wRepulsive * ( (self.spreadRepulsive + self.radiusRepulsive - dist) * np.sin(theta)) ]
        elif (dist > (self.radiusRepulsive + self.spreadRepulsive)):    
            return [0,0]
        return [0,0]
    
    def calcTangent(self, xPos, yPos, xObstacle, yObstacle):
        dist = self.distance((xPos, yPos), (xObstacle,yObstacle))
        if ((self.radiusTangential <= dist) and (dist <= (self.radiusTangential + self.spreadTangential))):
            theta = np.arctan2(yObstacle - yPos, xObstacle - xPos) - (np.pi / 2) # clockwise
            return [ -self.wTangential * self.spreadTangential**2 * np.cos(theta),
                    -self.wTangential * self.spreadTangential**2 * np.sin(theta) ]
        return [0,0]