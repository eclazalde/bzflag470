#!/usr/bin/python -tt

from collections import defaultdict
from bzrc import BZRC, Command
import sys, math, time, random
from reportlab.pdfbase.pdfdoc import Destination
from GridClass import GridFilter

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

    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.commands = []
        self.destination = defaultdict(list)
        self.timer = defaultdict(list)
        self.loadTanks()

    def tick(self, time_diff, gridViz):
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
        for bot in mytanks:
            position, occgrid = self.bzrc.get_occgrid(bot.index)
            #print occgrid
            gridViz.recordObservationGrid(position[0], position[1], occgrid)
            self.go_to_goal(bot)

        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)
        return gridViz

    def loadTanks(self):
		# Get information from the BZRC server
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytanks = mytanks
        self.othertanks = othertanks
        self.flags = flags
        self.shots = shots
        self.enemies = [tank for tank in othertanks if tank.color !=
                self.constants['team']]
        
        for bot in mytanks:
            destX = random.randrange(-400,400,1)
            destY = random.randrange(-400,400,1)
            self.destination[bot.index] = [destX, destY]
            self.timer[bot.index] = time.time()
            
        #for bot in mytanks:
        #    print '({0},{1}) to ({2}, {3})'.format(bot.x, bot.y, self.destination[bot.index][0], self.destination[bot.index][1])
	
    def go_to_goal(self, bot):
        if bot.x != self.destination[bot.index][0] and bot.y != self.destination[bot.index][1]:
            t = time.time() - self.timer[bot.index]
            if t > 30:
                destX = random.randrange(-400,400,1)
                destY = random.randrange(-400,400,1)
                self.destination[bot.index] = [destX, destY]
            else:
                pass
        else:
            destX = random.randrange(-400,400,1)
            destY = random.randrange(-400,400,1)
            self.destination[bot.index] = [destX, destY]

        self.move_to_position(bot, self.destination[bot.index][0], self.destination[bot.index][1])

    def move_to_position(self, bot, target_x, target_y):
        target_angle = math.atan2(target_y - bot.y,
                target_x - bot.x)
        relative_angle = self.normalize_angle(target_angle - bot.angle)
        command = Command(bot.index, 1, 2 * relative_angle, False)
        self.commands.append(command)

    def normalize_angle(self, angle):
        '''Make any angle be between +/- pi.'''
        angle -= 2 * math.pi * int (angle / (2 * math.pi))
        if angle <= -math.pi:
            angle += 2 * math.pi
        elif angle > math.pi:
            angle -= 2 * math.pi
        return angle


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
    
    gridVisualizer = GridFilter(-400,800,-400,800,0.9,0.97)
    
    agent = Agent(bzrc)

    prev_time = time.time()

    # Run the agent
    try:
        gridVisualizer.init_window(801, 801)
        while True:
            time_diff = time.time() - prev_time
            gridVisualizer = agent.tick(time_diff, gridVisualizer)
            if (time_diff >= 1):
                gridVisualizer.update_grid()
                gridVisualizer.draw_grid()
                prev_time = time.time()
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
