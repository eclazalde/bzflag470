import numpy as np
import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class GridFilter:
    _grid_observations = []
    #_grid_occupancies = None
    _grid_filter = []
    _grid_draw = []
    
    _minx = 0
    _rangex = 0
    _miny = 0
    _rangey = 0
    
    _truepositive = 0.97
    _truenegative = 0.9
    
    grid = None
    
    def __init__(self, minX, widthX, minY, widthY, trueNegative, truePositive):
        self._minx = minX
        self._rangex = widthX
        self._miny = minY
        self._rangey = widthY
        
        self._truenegative = trueNegative
        self._truepositive = truePositive
        
        self._grid_observations = np.zeros((widthX+1, widthY+1))
        #self._grid_occupancies = np.zeros((widthX+1, widthY+1))
        self._grid_filter = 0.75*np.ones((widthX+1, widthY+1))
        self._grid_draw = np.zeros((widthX+1, widthY+1))
    
    def recordObservationGrid(self, xCoord, yCoord, occGrid):
        # update the model based on the grid
        g_x, g_y = np.shape(occGrid)
        startx = xCoord - self._minx
        starty = yCoord - self._miny
        #print occGrid, "\n", np.sum(occGrid)
        for i in xrange(g_x):
            for j in xrange(g_y):
                #print ('({},{})').format(startx+i, starty+j)
                self._grid_observations[i + startx][j + starty] = self._grid_observations[startx+i][starty+j] + 1
                if (occGrid[i][j] == 1):
                    belief_occupied = self._truepositive * self._grid_filter[i + startx][j + starty]
                    belief_unoccupied = self._truenegative * (1.0 - self._grid_filter[i + startx][j + starty])
                    self._grid_filter[i + startx][j + starty] = belief_occupied / (belief_occupied + belief_unoccupied)
                else:
                    belief_occupied = (1 - self._truepositive) * self._grid_filter[i + startx][j + starty]
                    belief_unoccupied = (1 - self._truenegative) * (1.0 - self._grid_filter[i + startx][j + starty])
                    self._grid_filter[i + startx][j + starty] = belief_occupied / (belief_occupied + belief_unoccupied)
       
    def stringToGrid(self, inputString, xCoord, yCoord):
        ''' returns a correctly rotated numpy matrix'''
        lines = inputString.splitlines()
        cols = len(lines)
        rows = len(lines[0])
        grid = np.zeros((cols, rows))
        for i in xrange(cols):
            grid[i] = list(lines[i])
        # TO-DO: crop
        final_width = min(rows, self._rangex + 1 + self._minx - xCoord)
        final_height = min(cols, self._rangey + 1 + self._miny - yCoord)
        grid = grid[0:final_width,0:final_height]
        return grid

    def draw_grid(self):
        # This assumes you are using a numpy array for your grid
        width, height = grid.shape
        glRasterPos2f(-1, -1)
        glDrawPixels(width, height, GL_LUMINANCE, GL_FLOAT, grid)
        glFlush()
        glutSwapBuffers()
    
    def update_grid(self):
        global grid
        threshold_occ = 0.9
        threshold_unocc = 0.6
        #print np.shape(self._grid_filter)
        #print np.shape(self._grid_draw)
        for i in xrange(self._rangex):
            for j in xrange(self._rangey):
                #self._grid_draw[j][i] = self._grid_filter[i][j]
                
                if (self._grid_filter[i][j] >= threshold_occ):
                    self._grid_draw[j][i] = 0
                elif (self._grid_filter[i][j] <= threshold_unocc):
                    self._grid_draw[j][i] = 1
                else:
                    #print i,j
                    self._grid_draw[j][i] = 0.5
        grid = self._grid_draw
        #print np.sum(grid)
    
    def init_window(self, width, height):
        global window
        global grid
        grid = np.zeros((width, height))
        glutInit(())
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutInitWindowPosition(0, 0)
        window = glutCreateWindow("Grid filter")
        glutDisplayFunc(self.draw_grid)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        #glutMainLoop()


'''
# vim: et sw=4 sts=4
'''
