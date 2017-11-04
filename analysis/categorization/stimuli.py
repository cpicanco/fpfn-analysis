# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import sys
sys.path.append('../../analysis')
from methods import load_ini_data

import numpy as np
import random

STIMULI_COORDENATES = [
    (874, 334),
    (808, 517),
    (639, 614),
    (448, 580),
    (323, 431),
    (323, 237),
    (448, 88 ),
    (639, 54 ),
    (808, 151)]

def normalize(x_px, y_px, inverted_y=False, screen=(1280, 768)):
    if inverted_y:
        return x_px/screen[0], 1-(y_px/screen[1])
    else:
        return x_px/screen[0], y_px/screen[1]

def denormalize(x_px, y_px,screen=(1280, 768)):
    return x_px*screen[0], y_px*screen[1]

def ellipse(center, width, height, n = 360):
    thetas = [np.pi*2 * i/n for i in range(n)]
    points = [(center[0] + np.cos(t) * width, center[1] + np.sin(t) * height) for t in thetas]
    return np.array(points)

def generate_random_gaze_data(seconds=1296):    
    filename = 'random_gaze_data.txt'
    random_data = open(filename,'w+')
    random_data.write('time'+'\t'+'x_norm'+'\t'+'y_norm'+'\n')
    gaze = RandomPoint.pick()
    stimulus = random.choice(STIMULI_COORDENATES)
    for i in np.arange(0,seconds,0.01): 
        gaze = gaze.add(gaze.pick(r=1))
        x, y = normalize((gaze.x*10)+stimulus[0]+50, (gaze.y*6)+stimulus[1]+50)
        random_data.write('%.2f\t%.3f\t%.3f\n'%(i, x, y))
        if x > stimulus[0]+100 or x < stimulus[0]:
            gaze = RandomPoint.pick()
            stimulus = random.choice(STIMULI_COORDENATES)

        if y > stimulus[1]+100 or y < stimulus[1]:
            gaze = RandomPoint.pick()
            stimulus = random.choice(STIMULI_COORDENATES)

    random_data.close()

class RandomPoint(object):
    """
    Modified from: 
    https://codereview.stackexchange.com/a/121187/62263
    """
    @staticmethod
    def pick(r=None):
        """Pick a point in a random direction with some magnitude.
           If r=1, this samples a unit circle uniformly.
           If r=None, this samples a unit disc uniformly."""
        if r is None:
            r = np.random.uniform(0, 1)**0.05
        theta = np.random.uniform(0, 2 * np.pi)
        return RandomPoint(r * np.cos(theta), r * np.sin(theta))

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

class Circle(object):
    """Circle"""
    def __init__(self, left_px, top_px, width_px=100, height_px=100, normalized=True): 
        if normalized:          
            self.left, self.top = normalize(left_px, top_px, inverted_y=True) 
            self.width, self.height = normalize(width_px, height_px)
            self.radius = [self.width/2, self.height/2]
            self.center = normalize(left_px+(width_px/2), top_px+(height_px/2), inverted_y=True)
        else:
            self.left, self.top = left_px, top_px 
            self.width, self.height = width_px, height_px
            self.radius = self.width/2, self.height/2
            self.center = left_px+(width_px/2), top_px+(height_px/2)

    def points(self, factor=1.):
        return ellipse(self.center, self.radius[0]*factor, self.radius[1]*factor)

def circular_grid(normalized=False):
    return [Circle(x, y, normalized=normalized) for (x, y) in STIMULI_COORDENATES]  
  
def debug_window():
    from graphics import GraphWin

    win = GraphWin('Floor', 1280, 768)
    win.setBackground("black")

    for circle in circular_grid():
        for [x, y] in circle.points():
            win.plotPixel(x, y, "white")

    # gaze = RandomPoint.pick()
    # stimulus = random.choice(STIMULI_COORDENATES)
    # for i in np.arange(0,1000,0.01): 
    #     gaze = gaze.add(gaze.pick(r=1))
    #     x, y = (gaze.x*10)+stimulus[0]+50, (gaze.y*6)+stimulus[1]+50
    #     win.plotPixel(x, y, "white")
    #     if x > stimulus[0]+100 or x < stimulus[0]:
    #         gaze = RandomPoint.pick()
    #         stimulus = random.choice(STIMULI_COORDENATES)

    #     if y > stimulus[1]+100 or y < stimulus[1]:
    #         gaze = RandomPoint.pick()
    #         stimulus = random.choice(STIMULI_COORDENATES)

    win.getKey()
    win.close()

if __name__ == '__main__':
    debug_window()