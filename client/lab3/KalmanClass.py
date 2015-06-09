import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import time
import Queue
from bzrc import *

#from scipy.stats import multivariate_normal

class KalmanFilter:
    
    _fig = None
    _ax = None
    _debug = True
    _prevtime = None
    _latestActual = (0, 0)
    X_new = None
    X_old = None
    
    _F = None
    _F_transpose = None
    _covMatrix = None
    _H = None
    _H_transpose = None
    _covNoiseMatrix = None
    
    _mu_old = None
    _mu_new = None
    
    _cov_old = None
    _cov_new = None
    
    _killCount = 0
    _justKilled = False
    
    _mu_queue = None
    
    
    # set when initializing the class per parameter
    _posNoise = 5
    
    # following can all be tweaked
    T = 0.001
    cF = 0.0
    _covPosition = 0.1
    _covVelocity = 0.1
    _covAcceleration = 10 # default from spec is 100
    
    def __init__(self, positionNoise):
        self._fig = plt.figure()
        self._ax = plt.axes(xlim=(-400,400), ylim=(-400,400))
        plt.show(block=False)
        self._prevtime = time.time()
        
        self._posNoise = positionNoise
        
        self._mu_queue = Queue.Queue(maxsize=10)
        
        self._F = np.matrix([
                             [1, self.T,    ((self.T**2)/2), 0, 0,        0],
                             [0, 1,         self.T,          0, 0,        0],
                             [0, -self.cF,  1,               0, 0,        0],
                             [0, 0,         0,               1, self.T,   ((self.T**2)/2)],
                             [0, 0,         0,               0, 1,        self.T],
                             [0, 0,         0,               0, -self.cF, 1]
                             ])
        
        self._F_transpose = self._F.transpose()
        
        self._covMatrix = np.matrix([
                                [self._covPosition, 0, 0, 0, 0, 0],
                                [0, self._covVelocity, 0, 0, 0, 0],
                                [0, 0, self._covAcceleration, 0, 0, 0],
                                [0, 0, 0, self._covPosition, 0, 0],
                                [0, 0, 0, 0, self._covVelocity, 0],
                                [0, 0, 0, 0, 0, self._covAcceleration]
                                ])
        
        self._H = np.matrix([
                             [1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0]
                             ])
        
        self._H_transpose = self._H.transpose()
        
        self._covNoiseMatrix = np.matrix([
                                [self._posNoise**2, 0],
                                [0, self._posNoise**2]
                                ])
        
        self._mu_new = np.matrix([
                                  [0],
                                  [0],
                                  [0],
                                  [0],
                                  [0],
                                  [0]
                                  ])
        
        self.X_new = self._mu_new
        self.X_old = self._mu_new
        
        self._cov_new = np.matrix([
                                   [100, 0, 0, 0, 0, 0],
                                   [0, 0.1, 0, 0, 0, 0],
                                   [0, 0, 0.1, 0, 0, 0],
                                   [0, 0, 0, 100, 0, 0],
                                   [0, 0, 0, 0, 0.1, 0],
                                   [0, 0, 0, 0, 0, 0.1]
                                   ])
        
        self._I = np.matrix([
                             [1, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0],
                             [0, 0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 0, 1]
                             ])
        
        if self._debug:
            print "Kalman filter initialized"
            
    def makeObservation(self, bzProtocolEngine):
        others = bzProtocolEngine.get_othertanks()
        newtime = time.time()
        timediff = newtime - self._prevtime
        if (timediff < self.T):
            return # respect the time step
        self._prevtime = newtime
        if (len(others) > 0):
            self._justKilled = False
            self._latestActual = (others[0].x, others[0].y)
        else:
            if (self._justKilled == False):
                self._justKilled = True
                self._killCount += 1
                print "Total kills = ", self._killCount
            return # no enemy tanks remaining
        
        self._cov_old = self._cov_new
        self._mu_old = self._mu_new
        
        # make a matrix from the current observation
        observation = np.matrix(  [
                                   [self._latestActual[0]],
                                   [0],
                                   [0],
                                   [self._latestActual[1]],
                                   [0],
                                   [0]
                                   ])
        
        # Prediction
        
        # X_new 
        self.X_new = (self._F * self._mu_old) + (np.sqrt(self._covMatrix) * np.random.randn(6,1))
        
        # Z_new - adding observation noise
        Z_new = (self._H * self._mu_old) + (np.sqrt(self._covNoiseMatrix) * np.random.randn(2,1))
        #print Z_new
        
        # Correction
        subpart = self._F * self._cov_old * self._F_transpose + self._covMatrix
        
        # Kalman gain
        K_new = subpart * self._H_transpose * ((self._H * subpart * self._H_transpose + self._covNoiseMatrix).getI())
        #print K_new
        
        # covariance
        self._cov_new = (self._I - K_new * self._H) * subpart

        #mean
        self._mu_new = (self._F * observation) + K_new * (Z_new - (self._H * self._F * observation))
        
        if (self._mu_queue.full()):
            self._mu_queue.get_nowait()
        else:
            self._mu_queue.put_nowait([self._mu_new[0,0], self._mu_new[3,0]])
        return
    
    def getPrediction(self):
        p = self._F * self._mu_new
        try:
            return (p[0,0], p[3,3])
        except:
            return (0,0)
    
    def getMu(self):
        # print self._mu_new
        return [self._mu_new[0,0], self._mu_new[3,0]]
        
    def getMuAvg(self):
        x = 0
        y = 0
        s = self._mu_queue.qsize()
        if (s == 0):
            return [0,0]
        for i in xrange(s):
            t = self._mu_queue.get(block=True, timeout=None)
            x += t[0]
            y += t[1]
        return [x/s,y/s]
        
    def updateViz(self):
        #try:
        self._fig.gca().clear()
        ''' TODO: plot things '''
        # print self.getMu()
        # latest observation
        self._fig.gca().add_patch(plt.Circle(self._latestActual, radius=5, color='g', fill=True))
        # current calculated mean + covariance
        self._fig.gca().add_patch(ptch.Ellipse((self._mu_new[0,0], self._mu_new[3,0]), width=2*self._cov_new[0,0], height=2*self._cov_new[3,3], color='b', fill=False))
        # current calculated mean
        self._fig.gca().add_patch(plt.Rectangle((self._mu_new[0,0]-5, self._mu_new[3,0]-5), 10, 10, color='r', fill=False))
        # general prediction using F and mu
        # self._fig.gca().add_patch(plt.Circle(self.getPrediction(), radius=5, color='m', fill=False))
        #print self.getMuAvg()
        self._fig.canvas.draw()
        #except:
        #    print "Viz update failed"