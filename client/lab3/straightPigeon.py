#!/usr/bin/python -tt

from collections import defaultdict
from threading import Timer
from bzrc import BZRC, Command
import sys, math, time, random, numpy
from CustomFieldClass import Field

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
     
    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.commands = []
        self.destination = defaultdict(list)
        self.dest1 = [-350, -20]
        self.dest2 = [350, -20]
        self.tankSpeed = .4
        self.fields = defaultdict(list)
        self.prevError = defaultdict(list)
        self.first = True

    def tick(self, step):
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
            print 'Set up field'
            for bot in mytanks:
                self.destination[bot.index] = [self.dest1[0], self.dest1[1]]
                self.fields[bot.index] = Field(-400, 400, -400, 400)
                self.fields[bot.index].setupMap([],[self.destination[bot.index][0], self.destination[bot.index][1]])
            self.first = False                               
                                                    
        # Reset my set of commands (we don't want to run old commands)
        self.commands = []

        # Decide what to do with each of my tanks
        for bot in mytanks:
            if bot.status == 'alive':
                self.go_to_goal(bot, step)
                #print '[{},{}]'.format(bot.vx, bot.vy)
            #else:
                #print "Dead. Respawning..."

        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)
    	
    def go_to_goal(self, bot, step):
        xdiff = math.fabs(self.destination[bot.index][0] - bot.x)
        ydiff = math.fabs(self.destination[bot.index][1] - bot.y)
        #print '[{},{}] to [{},{}]'.format(bot.x, bot.y, self.destination[bot.index][0], self.destination[bot.index][1])
        #print xdiff, ydiff
        if xdiff < 10 and ydiff < 10:
            self.switchGoal(bot)
            
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
            
        # Calculates the speed based off the magnitude of the potential field vector
        speedAtStep = self.tankSpeed #1 - .2 * math.fabs(angularAtStep) #math.sqrt(pf[0]**2 + pf[1]**2)
        
        # Save the new error to use in the next iteration
        self.prevError[bot.index] = errorAtStep
                              
        return [speedAtStep, angularAtStep]

    def switchGoal(self, bot):
        print 'Switch destination'
        if self.destination[bot.index][0] == self.dest1[0] and self.destination[bot.index][1] == self.dest1[1]:
            self.destination[bot.index][1] = self.dest2[1]
            self.destination[bot.index][0] = self.dest2[0]
            self.fields[bot.index].setupMap([],[self.destination[bot.index][0], self.destination[bot.index][1]])
        elif self.destination[bot.index][0] == self.dest2[0] and self.destination[bot.index][1] == self.dest2[1]:
            self.destination[bot.index][1] = self.dest1[1]
            self.destination[bot.index][0] = self.dest1[0]
            self.fields[bot.index].setupMap([],[self.destination[bot.index][0], self.destination[bot.index][1]])
        else:
            print 'Tank got lost. This shouldn\'t happen'

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

    agent = Agent(bzrc)

    prev_tick = time.time()
    step = .001

    # Run the agent
    try:
        while True:
            time_diff = time.time() - prev_tick
            if time_diff >= step:
                agent.tick(time_diff)
                prev_tick = time.time()
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
