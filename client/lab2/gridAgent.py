#!/usr/bin/python -tt

from collections import defaultdict
from threading import Timer
from bzrc import BZRC, Command
import sys, math, time, random, numpy
from reportlab.pdfbase.pdfdoc import Destination
from CustomFieldClass import Field
from GridClass import GridFilter
import numpy.linalg as la

# An incredibly simple agent.  All we do is find the closest enemy tank, drive
# towards it, and shoot.  Note that if friendly fire is allowed, you will very
# often kill your own tanks with this code.

#################################################################
# NOTE TO STUDENTS
# This is a starting point for you.  You will need to greatly
# modify this code if you want to do anything useful.  But this
# should help you to know how to interact with BZRC in order to
# get the information you need.
# 
# After starting the bzrflag server, this is one way to start
# this code:
# python agent0.py [hostname] [port]
# 
# Often this translates to something like the following (with the
# port name being printed out by the bzrflag server):
# python agent0.py localhost 49857
#################################################################

class Agent(object):
    
    _gridVisualizer = None
    used = []
     
    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.commands = []
        self.destination = defaultdict(list)
        self.fields = defaultdict(list)
        self.timer = defaultdict(list)
        self.first = True
        self.used = []
        
        self.prevError = defaultdict(list)

    def loadTanks(self, numTanks,step, gridViz):
        # Get information from the BZRC server
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytanks = mytanks
        self.othertanks = othertanks
        self.flags = flags
        self.shots = shots
        self.enemies = [tank for tank in othertanks if tank.color !=
                self.constants['team']]
        
        for bot in mytanks:
            #destX = random.randrange(-400,400,1)
            #destY = random.randrange(-400,400,1)
            self.fields[bot.index] = Field(-400, 400, -400, 400)
            dest = self.generateGoal(bot, numTanks, gridViz)
            self.destination[bot.index] = [dest[0], dest[1]]
            #o = self.generateObstacles(gridViz._grid_filter)
            self.fields[bot.index].setupMap([],[dest[0], dest[1]])
            self.timer[bot.index] = time.time()
            
            #self.fields[bot.index].drawFast(True, True, True)
        #for bot in mytanks:
        #    print '({0},{1}) to ({2}, {3})'.format(bot.x, bot.y, self.destination[bot.index][0], self.destination[bot.index][1])

    def tick(self, step, gridViz):
        '''Some time has passed; decide what to do next'''
        # Get information from the BZRC server
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytanks = mytanks
        self.othertanks = othertanks
        self.flags = flags
        self.shots = shots
        self.enemies = [tank for tank in othertanks if tank.color !=
                self.constants['team']]
        
        if self.first:
            self.loadTanks(len(self.mytanks),step, gridViz)
            self.first = False

        # Reset my set of commands (we don't want to run old commands)
        self.commands = []

        # Decide what to do with each of my tanks
        for bot in mytanks:
            position, occgrid = self.bzrc.get_occgrid(bot.index)
            gridViz.recordObservationGrid(position[0], position[1], occgrid)
            self.go_to_goal(bot, len(self.mytanks),step, gridViz)

        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)
        return gridViz
    	
    def go_to_goal(self, bot, numTanks, step, gridViz):
        newGoalTimer = 60
        if bot.x != self.destination[bot.index][0] and bot.y != self.destination[bot.index][1]:
            t = time.time() - self.timer[bot.index]
            if t > newGoalTimer:
                #destX = random.randrange(-400,400,1)
                #destY = random.randrange(-400,400,1)
                dest = self.generateGoal(bot, numTanks, gridViz)
                self.destination[bot.index] = [dest[0], dest[1]]
                #o = self.generateObstacles(gridViz._grid_filter)
                self.fields[bot.index].setupMap([],[dest[0], dest[1]])
                self.timer[bot.index] = time.time()
            else:
                pass
        else:
            #destX = random.randrange(-400,400,1)
            #destY = random.randrange(-400,400,1)
            dest = self.generateGoal(bot, numTanks, gridViz)
            self.destination[bot.index] = [dest[0], dest[1]]
            #o = self.generateObstacles(gridViz._grid_filter)
            self.fields[bot.index].setupMap([],[dest[0], dest[1]])
            #self.destination[bot.index] = [destX, destY]
            #self.fields[bot.index].setupMap([],[destX,destY])
            
        values = self.calculatePD(bot, step)
        command = Command(bot.index, values[0], values[1], False)
        self.commands.append(command)
    
    def calculatePD(self, bot, step):
        # Get the potential field magnitudes in the x and y at the current position
        pf = self.fields[bot.index].getFast(bot.x, bot.y)
        
        # Tune these or set to zero to manipulate the PD controller
        kProportion = .5
        kDerivative = .002
        
        # Calculate values used in the PD controller formula
        angleReference = numpy.arctan2(pf[1], pf[0])
        angle = angleReference - bot.angle
        errorAtStep =  numpy.arctan2(math.sin(angle),math.cos(angle))                 
        errorPrevStep = 0.0 # Previous error is zero if this is the first calculation.
        
        # Update the previous error to the last saved error if there is one
        if bot.index in self.prevError:
            errorPrevStep = self.prevError[bot.index]
        
        # This is the PD formula
        angularAtStep = (kProportion * errorAtStep) + (kDerivative * ((errorAtStep - errorPrevStep) / step))
        #print angularAtStep
        if angularAtStep > 1:
            angularAtStep = 1
        if angularAtStep < -1:
            angularAtStep = -1
            
        #print errorAtStep, angularAtStep, pf  
        # Calculates the speed based off the magnitude of the potential field vector
        speedAtStep = 1 - .2 * math.fabs(angularAtStep) #math.sqrt(pf[0]**2 + pf[1]**2)
        #print speedAtStep
        # Save the new error to use in the next iteration
        self.prevError[bot.index] = errorAtStep
                              
        return [speedAtStep, angularAtStep]
    
    def generateGoal(self, bot, numTanks, gridViz):
        destX = 0
        destY = 0
        if bot.index == 0:
            destX = random.randrange(100,400,1)
            destY = random.randrange(-400,400,1)
        elif bot.index == 1:
                dest = self.findRegion(bot, gridViz)
                destX = dest[0]
                destY =  dest[1]
        elif bot.index == 2:
                dest = self.findRegion(bot, gridViz)
                destX = dest[0]
                destY =  dest[1]
        elif bot.index == 3:
                dest = self.findRegion(bot, gridViz)
                destX = dest[0]
                destY =  dest[1]
        elif bot.index == 4:
                dest = self.findRegion(bot, gridViz)
                destX = dest[0]
                destY =  dest[1]
        elif bot.index == 5:
                dest = self.findRegion(bot, gridViz)
                destX = dest[0]
                destY =  dest[1]
        elif bot.index == 6:
                dest = self.findRegion(bot, gridViz)
                destX = dest[0]
                destY =  dest[1]
        elif bot.index == 7:
                dest = self.findRegion(bot, gridViz)
                destX = dest[0]
                destY =  dest[1]
        elif bot.index == 8:
                dest = self.findRegion(bot, gridViz)
                destX = dest[0]
                destY =  dest[1]
        else:
                dest = self.findRegion(bot, gridViz)
                destX = dest[0]
                destY =  dest[1]
        
        #print ('Bot:{} ({},{})').format(bot.index, destX, destY)
        return destX, destY
    
    def findRegion(self, bot, gridViz):
        obs = gridViz._grid_observations
        threshhold = 1
        if bot.index == 1:
            cX = -399; cY = 133
            while cX <= -133:
                while cY < 399:
                    if obs[cX+400][cY+400] < threshhold and [cX, cY] not in self.used:
                        self.used = []
                        self.used.append([cX, cY])
                        return cX, cY
                    cY = cY + 1
                cX = cX + 1
            destX = random.randrange(-400,400,1)
            destY = random.randrange(-400,400,1)
            return destX, destY
        elif bot.index == 2:
            cX = -133; cY = 133
            while cX < 134:
                while cY < 399:
                    if obs[cX+400][cY+400] < threshhold and [cX, cY] not in self.used:
                        self.used = []
                        self.used.append([cX, cY])
                        return cX, cY
                    cY = cY + 1
                cX = cX + 1
            destX = random.randrange(-400,400,1)
            destY = random.randrange(-400,400,1)
            return destX, destY
        elif bot.index == 3:
            cX = 134; cY = 133
            while cX < 399:
                while cY < 399:
                    if obs[cX+400][cY+400] < threshhold and [cX, cY] not in self.used:
                        self.used = []
                        self.used.append([cX, cY])
                        return cX, cY
                    cY = cY + 1
                cX = cX + 1
            destX = random.randrange(-400,400,1)
            destY = random.randrange(-400,400,1)
            return destX, destY
        elif bot.index == 4:
            cX = -399; cY = -134
            while cX < -133:
                while cY < 133:
                    if obs[cX+400][cY+400] < threshhold and [cX, cY] not in self.used:
                        self.used = []
                        self.used.append([cX, cY])
                        return cX, cY
                    cY = cY + 1
                cX = cX + 1
            destX = random.randrange(-400,400,1)
            destY = random.randrange(-400,400,1)
            return destX, destY
        elif bot.index == 5:
            cX = -133; cY = -134
            while cX < 134:
                while cY < 133:
                    if obs[cX+400][cY+400] < threshhold and [cX, cY] not in self.used:
                        self.used = []
                        self.used.append([cX, cY])
                        return cX, cY
                    cY = cY + 1
                cX = cX + 1
            destX = random.randrange(-400,400,1)
            destY = random.randrange(-400,400,1)
            return destX, destY
        elif bot.index == 6:
            cX = 134; cY = -134
            while cX < 399:
                while cY < 133:
                    if obs[cX+400][cY+400] < threshhold and [cX, cY] not in self.used:
                        self.used = []
                        self.used.append([cX, cY])
                        return cX, cY
                    cY = cY + 1
                cX = cX + 1
            destX = random.randrange(-400,400,1)
            destY = random.randrange(-400,400,1)
            return destX, destY
        elif bot.index == 7:
            cX = -399; cY = -399
            while cX < -133:
                while cY < -134:
                    if obs[cX+400][cY+400] < threshhold and [cX, cY] not in self.used:
                        self.used = []
                        self.used.append([cX, cY])
                        return cX, cY
                    cY = cY + 1
                cX = cX + 1
            destX = random.randrange(-400,400,1)
            destY = random.randrange(-400,400,1)
            return destX, destY
        elif bot.index == 8:
            cX = -133; cY = -399
            while cX < 134:
                while cY < -134:
                    if obs[cX+400][cY+400] < threshhold and [cX, cY] not in self.used:
                        self.used = []
                        self.used.append([cX, cY])
                        return cX, cY
                    cY = cY + 1
                cX = cX + 1
            destX = random.randrange(-400,400,1)
            destY = random.randrange(-400,400,1)
            return destX, destY
        else:
            cX = 134; cY = -399
            while cX < 399:
                while cY < -134:
                    if obs[cX+400][cY+400] < threshhold and [cX, cY] not in self.used:
                        self.used = []
                        self.used.append([cX, cY])
                        return cX, cY
                    cY = cY + 1
                cX = cX + 1
            destX = random.randrange(-400,400,1)
            destY = random.randrange(-400,400,1)
            return destX, destY

    def generateObstacles(self, occupancyGrid):
        threshhold = .8
        resolution = 20
        row = 0
        column = 0
        obstacles = []
        
        for y in occupancyGrid:
            first = 0
            firstPair = False
            if row % resolution == 0:
                for x in y:
                    if column % resolution == 0:
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
                                obstacles.append([first-400, 400-row])
                                obstacles.append([column-1-400, 400-row])
                                firstPair = False
                                #print ('appended right obstacle [{},{}]').format(row, first)
                    column = column + 1   
            column = 0
            row = row + 1
        row = 0
        
        return obstacles
        #print obstacles

def main():
    # Process CLI arguments.
    try:
        execname, host, port = sys.argv
    except ValueError:
        execname = sys.argv[0]
        print >>sys.stderr, '%s: incorrect number of arguments' % execname
        print >>sys.stderr, 'usage: %s hostname port' % sys.argv[0]
        sys.exit(-1)

    # Connect.
    #bzrc = BZRC(host, int(port), debug=True)
    bzrc = BZRC(host, int(port))
    
    constants = bzrc.get_constants()
    
    gridVisualizer = GridFilter(-400,800,-400,800,constants['truenegative'],constants['truepositive'])

    agent = Agent(bzrc)

    prev_viz = time.time()
    prev_tick = time.time()
    step = .0001

    # Run the agent
    try:
        gridVisualizer.init_window(801, 801)
        while True:
            viz_timer = time.time() - prev_viz
            time_diff = time.time() - prev_tick
            if time_diff >= step:
                gridVisualizer = agent.tick(time_diff, gridVisualizer)
                prev_tick = time.time()
            if (viz_timer >= 1):
                gridVisualizer.update_grid()
                gridVisualizer.draw_grid()
                prev_viz = time.time()
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
