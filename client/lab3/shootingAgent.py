#!/usr/bin/python -tt

from collections import defaultdict
from threading import Timer
from bzrc import BZRC, Command
import sys, math, time, numpy
from CustomFieldClass import Field
from KalmanClass import KalmanFilter

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
    
    _KF = None
     
    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.commands = []
        self.location = []
        self.target = []
        self.prevError = defaultdict(list)
        self.shotspeed = 100
        self.prevpos = [0,0]
        self.targetvel = [0, 0]
        self._KF = KalmanFilter(5) # have to set manually as bzrc.get_constants doesn't return this
        
    def tick(self, step, calcVel, velStep):
        '''Some time has passed; decide what to do next'''
        # Get information from the BZRC server
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytanks = mytanks
        self.othertanks = othertanks
        self.flags = flags
        self.shots = shots
        self.enemies = [tank for tank in othertanks if tank.color !=
                self.constants['team']]
        
        self._KF.makeObservation(self.bzrc)                            
                                         
        # Reset my set of commands (we don't want to run old commands)
        self.commands = []

        if calcVel:
            self.target = self._KF.getMuAvg()
            self.targetvel = self.getVel(self.target, velStep)
            self.prevpos = self.target

        # Decide what to do with each of my tanks
        for bot in mytanks:
            self.target = self._KF.getMu()
            if othertanks[0].status == 'alive':
                self.location = [bot.x, bot.y]
                tpoint = self.getTargetPoint(bot, self.target, self.targetvel)
                self.turnTank(bot, tpoint[0], tpoint[1], step)
            else:
                #print "No enemy. Searching..."
                command = Command(bot.index, 0, 0, False)
                self.commands.append(command)
                
        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)

    def turnTank(self, bot, targetx, targety, step):        
        # Tune these or set to zero to manipulate the PD controller
        distance = math.sqrt(math.pow(targetx - bot.x, 2) + math.pow(targety - bot.y, 2))
        shootingThreshold = .01
        kProportion = 1 + 5 * (1 - distance / 800)
        kDerivative = .5
        errorPrevStep = 0.0 # Previous error is zero if this is the first calculation.

        # Update the previous error to the last saved error if there is one
        if bot.index in self.prevError:
            errorPrevStep = self.prevError[bot.index]

        # Calculate values used in the PD controller formula              
        angleReference = numpy.arctan2(targety - self.location[1], targetx - self.location[0])
        angle = angleReference - bot.angle
        errorAtStep =  numpy.arctan2(math.sin(angle),math.cos(angle))
        # This is the PD formula
        angularAtStep = (kProportion * angle) + (kDerivative * ((angle - errorPrevStep) / step))
        if angularAtStep > 1:
            angularAtStep = 1
        if angularAtStep < -1:
            angularAtStep = -1
        
        # Save the new error to use in the next iteration
        self.prevError[bot.index] = angle
        
        command = Command(bot.index, 0, angularAtStep, False)
        if math.fabs(errorAtStep) <= shootingThreshold:
            command = Command(bot.index, 0, angularAtStep, True)
        else:
            command = Command(bot.index, 0, angularAtStep, False)
        self.commands.append(command)
        
    def getVel(self, enemy, step):
        #print '[{},{}]'.format(enemy[0] - self.prevpos[0], enemy[1] - self.prevpos[1])
        vx = (enemy[0] - self.prevpos[0]) / step
        vy = (enemy[1] - self.prevpos[1]) / step
        return [vx, vy]

    def getTargetPoint(self, bot, targetpos, targetvel):
        disTotarget = math.sqrt(math.pow(targetpos[0] - bot.x, 2) + math.pow(targetpos[1] - bot.y, 2))
        timeTotarget = disTotarget / self.shotspeed
        xn = targetpos[0] + targetvel[0] * 1 * timeTotarget
        yn = targetpos[1] + targetvel[1] * 1 * timeTotarget
        #print 'Tank:[{},{}] Shoot at:[{},{}]'.format(targetpos[0], targetpos[1], xn, yn)
        return [xn, yn]
    
    def updateVisualization(self):
        self._KF.updateViz()
  
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
    vel_tick = time.time()
    viz_tick = time.time()
    calulateVel = False
    velStep = .25
    vizStep = 1.0
    step = .001

    # Run the agent
    try:
        while True:
            newtime = time.time()
            time_diff = newtime - prev_tick
            vel_diff = newtime - vel_tick
            viz_diff = newtime - viz_tick
            if vel_diff >= velStep:
                calulateVel = True
                vel_tick = newtime
            if time_diff >= step:
                agent.tick(time_diff, calulateVel, velStep)
                prev_tick = newtime
                calulateVel = False
            if viz_diff >= vizStep:
                agent.updateVisualization()
                viz_tick = newtime
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
