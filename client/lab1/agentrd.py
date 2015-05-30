#!/usr/bin/python -tt

from bzrc import BZRC, Command
import sys, math, time
from pycurl import SPEED_DOWNLOAD

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
        self.moving = False
        self.turning = False
        self.speed = 0.5
        self.angvel = 0.7
        self.prevShootTime = time.time()
        self.prevMoveTime = time.time()
        self.prevTurnTime = time.time()

    def tickAll(self):
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
        sDiff = time.time() - self.prevShootTime
        mDiff = time.time() - self.prevMoveTime
        tDiff = time.time() - self.prevTurnTime
        
        # Decide what to do with each of my tanks            
        if sDiff >= .5:
            for bot in mytanks:
                self.shoot(bot, self.moving, self.turning, self.speed, self.angvel)
                self.prevShootTime = time.time()
        if tDiff >= 2 and not self.moving:
            for bot in mytanks:
                self.move_forward(bot, self.speed)
                self.prevMoveTime = time.time()
                self.turning = False
                self.moving = True
        elif mDiff >= 3 and not self.turning:
            for bot in mytanks:
                self.turn(bot, self.angvel)
                self.prevTurnTime = time.time()
                self.moving = False
                self.turning = True

        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)
        
    def tickTwo(self):
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
        sDiff = time.time() - self.prevShootTime
        mDiff = time.time() - self.prevMoveTime
        tDiff = time.time() - self.prevTurnTime
        
        # Decide what to do with each of my tanks            
        if sDiff >= .5:
            self.shoot(mytanks[0], self.moving, self.turning, self.speed, self.angvel)
            self.shoot(mytanks[1], self.moving, self.turning, self.speed, self.angvel)
            self.prevShootTime = time.time()
        if tDiff >= 2 and not self.moving:
            self.move_forward(mytanks[0], self.speed)
            self.move_forward(mytanks[1], self.speed)
            self.prevMoveTime = time.time()
            self.turning = False
            self.moving = True
        elif mDiff >= 3 and not self.turning:
            self.turn(mytanks[0], self.angvel)
            self.turn(mytanks[1], self.angvel)
            self.prevTurnTime = time.time()
            self.moving = False
            self.turning = True

        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)
    
    def move_forward(self, bot, speed):
        # Move forward command
        command = Command(bot.index, speed, 0, 0)
        self.commands.append(command)
        
    def turn(self, bot, angvel):
        # Decide what to do with each of my tanks
        command = Command(bot.index, 0, angvel, 0)
        self.commands.append(command)
    
    def shoot(self, bot, moving, turning, s, a):
        # Shoot!!
        angvel = 0
        speed = 0
        if turning:
            angvel = a
        if moving:
            speed = s
        command = Command(bot.index, speed, angvel, 1)
        self.commands.append(command)

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
   # bzrc = BZRC(host, int(port), debug=True)
    bzrc = BZRC(host, int(port))

    agent = Agent(bzrc)
    prevTime = time.time()
    # Run the agent
    try:
        while True:
            timeDiff = time.time() - prevTime
            if timeDiff >= .001:
                agent.tickTwo()
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
