#!/usr/bin/python -tt

from bzrc import BZRC, Command
from FieldClass import Field
import sys, math, time

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
        self.field = Field
        self.constants = self.bzrc.get_constants()
        self.commands = []

    def tick(self, time_diff):
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

        # Decide what to do with each of my tanks
        #for bot in mytanks:
        #    self.attack_enemies(bot)

        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)

    def move_to_position(self, bot, target_x, target_y):
        target_angle = math.atan2(target_y - bot.y,
                target_x - bot.x)
        relative_angle = self.normalize_angle(target_angle - bot.angle)
        command = Command(bot.index, 1, 2 * relative_angle, True)
        self.commands.append(command)

    def normalize_angle(self, angle):
        '''Make any angle be between +/- pi.'''
        angle -= 2 * math.pi * int (angle / (2 * math.pi))
        if angle <= -math.pi:
            angle += 2 * math.pi
        elif angle > math.pi:
            angle -= 2 * math.pi
        return angle

	def calculatePD(self, tank):
		pf = self.field.queryPosition(tank.x, tank.y)
		

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

    agent = Agent(bzrc)

    prev_time = time.time()

    # Run the agent
    try:
        moving = False
        turning = False
        while True:
            time_diff = time.time() - prev_time
            if time_diff >= 1.5:
                agent.commands = []
                command = Command(0, 0, 0.8, 1)
                agent.commands.append(command)
                agent.bzrc.do_commands(agent.commands)
            if moving:
                if time_diff >= 3:
                    prev_time = time.time()
                    agent.commands = []
                    command = Command(0, 0, 0.8, 1)
                    agent.commands.append(command)
                    agent.bzrc.do_commands(agent.commands)
                    moving = False
            else:
                if time_diff >= 2:  
                    prev_time = time.time()                 
                    agent.commands = []
                    command = Command(0, .5, 0, 1)
                    agent.commands.append(command)
                    agent.bzrc.do_commands(agent.commands)
                    turning = False
                    moving = True
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
