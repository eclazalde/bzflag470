#!/usr/bin/python -tt

from collections import defaultdict
from threading import Timer
from bzrc import BZRC, Command
from FieldClass import Field
import sys, math, time, numpy

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
        self.field = Field(-400, 400, -400, 400)
        self.field.setupMap4Ls()
        self.field.calculateFields()
        self.constants = self.bzrc.get_constants()
        self.commands = []
        self.prevError = defaultdict(list)
        self.vizualize = True
        self.gotFlag = False

    def tickAll(self, step):
        '''Some time has passed; decide what to do next'''
        # Get information from the BZRC server
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytanks = mytanks
        self.othertanks = othertanks
        self.flags = flags
        self.shots = shots
        self.enemies = [tank for tank in othertanks if tank.color !=
                self.constants['team']]

        # Reset my set of commands (we don't want to run old commands)
        self.commands = []

        if self.vizualize:
            self.field.visualize()
            self.vizualize = False
        
        # Check to see if the flag has been captured
        for bot in mytanks:
            if not self.gotFlag and bot.flag is not '-':
                self.gotFlag = True
                self.flipFieldToHome()
                
            if self.gotFlag and bot.flag is '-':
                self.gotFlag = False
                self.flipFieldToEnemy()
        
        # Decide what to do with each of my tanks
        for bot in mytanks:
            values = self.calculatePD(bot, step)
            command = Command(bot.index, values[0], values[1], False)
            self.commands.append(command)

        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)
        
    def tickOne(self, step):
        '''Some time has passed; decide what to do next'''
        # Get information from the BZRC server
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytanks = mytanks
        self.othertanks = othertanks
        self.flags = flags
        self.shots = shots
        self.enemies = [tank for tank in othertanks if tank.color !=
                self.constants['team']]

        # Reset my set of commands (we don't want to run old commands)
        self.commands = []

        # Visualize potential field
        if self.vizualize:
            self.field.visualize(True, True, True)
            self.vizualize = False
            print 'Done with visualization'
        
        # Which tank do you want to control
        bot = mytanks[0]
        
        # Check to see if the flag has been captured
        if not self.gotFlag and bot.flag is not '-':
            self.gotFlag = True
            self.flipFieldToHome()
            
        if self.gotFlag and bot.flag is '-':
            self.gotFlag = False
            self.flipFieldToEnemy()
        
        # Decide what to do with one tank of my tanks
        values = self.calculatePD(bot, step)
        command = Command(bot.index, values[0], values[1], True)
        self.commands.append(command)

        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)

    def calculatePD(self, bot, step):
        # Get the potential field magnitudes in the x and y at the current position
    	pf = self.field.queryPosition(bot.x, bot.y)
        
        # Tune these or set to zero to manipulate the PD controller
        kProportion = 1.0
        kDerivative = 1.0
        
        # Calculate values used in the PD controller formula
        angleReference = numpy.arctan2(pf[1], pf[0])
        errorAtStep = angleReference - bot.angle
        errorPrevStep = 0.0 # Previous error is zero if this is the first calculation.
         
        # Update the previous error to the last saved error if there is one
        if bot.index in self.prevError:
            errorPrevStep = self.prevError[bot.index]
    	
        # This is the PD formula
        angularAtStep = (kProportion * errorAtStep) + (kDerivative * ((errorAtStep - errorPrevStep) / step))
        
        # Calculates the speed based off the magnitude of the potential field vector
        speedAtStep = math.sqrt(pf[0]**2 + pf[1]**2)
        
        # Save the new error to use in the next iteration
        self.prevError[bot.index] = errorAtStep
                              
        return [speedAtStep, angularAtStep]
    
    def flipFieldToHome(self):
        print 'WIP'
        
    def flipFieldToEnemy(self):
        print 'WIP'
    
def main():
    # Process CLI arguments.
    try:
        execname, host, port = sys.argv
    except ValueError:
        execname = sys.argv[0]
        print >>sys.stderr, '%s: incorrect number of arguments' % execname
        print >>sys.stderr, 'usage: %s hostname port "one"(or "all")' % sys.argv[0]
        sys.exit(-1)

    # Connect.
    #bzrc = BZRC(host, int(port), debug=True)
    bzrc = BZRC(host, int(port))

    agent = Agent(bzrc)
    prev_time = time.time()
    step = .001
    
    # Do you want to control 1 tank or all of the tanks on a team?
    ctrl = 'one'
    #ctrl = 'all'
    
    # Run the agent
    try:
        while True:
            time_diff = time.time() - prev_time
            # Only do something if the set interval has passed
            if time_diff >= step:
                if ctrl is 'one': # This call the tickOne method for controlling 1 tank
                    agent.tickOne(step)
                    prev_time = time.time()
                elif ctrl is 'all': # This call the tickAll method for controlling all the tanks
                    agent.tickAll(step)
                    prev_time = time.time()
                else:
                    print >>sys.stderr, 'This shouldn\'t happen!!'
                    sys.exit(-1)
                
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
