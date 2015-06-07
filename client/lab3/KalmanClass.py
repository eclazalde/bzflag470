import numpy as np
import matplotlib.pyplot as plt
import time
from bzrc import *
#from scipy.stats import multivariate_normal

class KalmanFilter:
    
    _fig = None
    _ax = None
    _debug = True
    _prevtime = None
    _latestActual = (0, 0)
    
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
    
    # set when initializing the class per parameter
    _posNoise = 5
    
    # following can all be tweaked
    _timestep = 0.5
    _cFriction = 0.0
    _covPosition = 0.1
    _covVelocity = 0.1
    _covAcceleration = 100 # default from spec is 100
    
    def __init__(self, positionNoise):
        self._fig = plt.figure()
        self._ax = plt.axes(xlim=(-400,400), ylim=(-400,400))
        plt.show(block=False)
        self._prevtime = time.time()
        
        self._posNoise = positionNoise
        
        self._F = np.matrix([
                             [1, self._timestep,    ((self._timestep**2)/2),    0, 0,                   0],
                             [0, 1,                 self._timestep,             0, 0,                   0],
                             [0, -self._cFriction,  1,                          0, 0,                   0],
                             [0, 0,                 0,                          1, self._timestep,      ((self._timestep**2)/2)],
                             [0, 0,                 0,                          0, 1,                   self._timestep],
                             [0, 0,                 0,                          0, -self._cFriction,    1]
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
        if (timediff < self._timestep):
            return # need to wait a little longer
        self._prevtime = newtime
        if (len(others) > 0):
            self._latestActual = (others[0].x, others[0].y)
        else:
            return # no enemy tanks remaining
        
        self._cov_old = self._cov_new
        self._mu_old = self._mu_new
        
        # Kalman gain
        K_new = (self._F * self._cov_old * self._F_transpose + self._covMatrix) * self._H_transpose * ((self._H * (self._F * self._cov_old * self._F_transpose + self._covMatrix) * self._H_transpose + self._covNoiseMatrix).getI())
        
        # covariance
        self._cov_new = (self._I - K_new * self._H) * (self._F * self._cov_old * self._F_transpose + self._covMatrix)
        
        # mean
        #self._mu_new = self._F * self._mu_old + K_new * (Z_new - self._H * self._F * self._mu_old)
        
        
        
    def updateViz(self):
        #try:
        self._fig.gca().clear()
        ''' TODO: plot things '''
        '''
        mu = [0, 0]
        #sigma = [10 0; 0 10]
        covar = [[10, 0],[0, 50]]
        #self._fig.gca().contour(np.random.multivariate_normal(mean, cov, 5000))
        x = np.linspace(-400,400)
        y = np.linspace(-400,400)
        x,y = np.meshgrid(x,y)
        xy = np.column_stack([x.flat, y.flat])
        z = multivariate_normal.pdf(xy, mean=mu, cov=covar)
        '''
        # just tick on the first quadrant
        self._fig.gca().add_patch(plt.Rectangle((self._prevtime % 400 - 5,self._prevtime % 400 - 5), 10, 10, color='r', fill=False))
        self._fig.gca().add_patch(plt.Circle(self._latestActual, radius=5, color='g', fill=True))
        self._fig.canvas.draw()
        #except:
        #    print "Viz update failed"