# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import sys
sys.path.append('../../analysis')

from time import sleep
import random

import numpy as np


STIMULI_WIDTH_PX = 100
STIMULI_HEIGHT_PX = 100

SCREEN_WIDTH_PX = 1280
SCREEN_HEIGHT_PX = 768

SCREEN_DISTANCE_CM = 240.
SCREEN_WIDTH_CM = 70.

EXT_W = 830
EXT_H = 830

INT_W = 300
INT_H = 300

def get_central_rect(width, height):
    left = (SCREEN_WIDTH_PX // 2) - (width // 2)
    top = (SCREEN_HEIGHT_PX // 2) - (height // 2)
    return (left, top)

(EXT_L, EXT_T) = get_central_rect(EXT_W, EXT_H)
EXTERNAL_SCREEN_RECT = [EXT_L, EXT_T, EXT_W, EXT_H]

(INT_L, INT_T) = get_central_rect(INT_W, INT_H)
INTERNAL_SCREEN_RECT = [INT_L, INT_T, INT_W, INT_H]

STIMULI_COORDENATES = [
    (874, 334), # <=== right, 0 degree
    (808, 517), 
    (639, 614),
    (448, 580),
    (323, 431),
    (323, 237),
    (448, 88 ),
    (639, 54 ),
    (808, 151)]

def normalize(x_px, y_px, inverted_y=False, screen=(SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX)):
    if inverted_y:
        return x_px/screen[0], 1-(y_px/screen[1])
    else:
        return x_px/screen[0], y_px/screen[1]

def denormalize(x_px, y_px,screen=(SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX)):
    return x_px*screen[0], y_px*screen[1]

def ellipse(center, width, height, start = 0, end = 360, step=1):
    thetas = [np.pi*2 * i/360 for i in range(start, end, step)]
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
    def __init__(self, left_px, top_px,
        width_px=STIMULI_WIDTH_PX, height_px=STIMULI_HEIGHT_PX, normalized=True, inverted_y=True): 
        if normalized:          
            self.left, self.top = normalize(left_px, top_px, inverted_y=inverted_y) 
            self.width, self.height = normalize(width_px, height_px)
            self.radius = [self.width/2, self.height/2]
            self.center = normalize(left_px+(width_px/2), top_px+(height_px/2), inverted_y=inverted_y)
        else:
            self.left, self.top = left_px, top_px 
            self.width, self.height = width_px, height_px
            self.radius = self.width/2, self.height/2
            self.center = left_px+(width_px/2), top_px+(height_px/2)

    def points(self, factor=1., low=0, high=360, step=1):
        return ellipse(self.center, self.radius[0]*factor, self.radius[1]*factor, low, high, step)

def circle_grid(normalized=False, inverted_y=True):
    return [Circle(x, y, normalized=normalized, inverted_y=inverted_y) for (x, y) in STIMULI_COORDENATES]  
 
def donut_grid(normalized=False, inverted_y=False):
    grid = []
    step = 40

    # grid.append(Circle(
    #             left_px=INTERNAL_SCREEN_RECT[0],
    #             top_px=INTERNAL_SCREEN_RECT[1],
    #             width_px=INTERNAL_SCREEN_RECT[2],
    #             height_px=INTERNAL_SCREEN_RECT[3],
    #             normalized=normalized,
    #             inverted_y=inverted_y).points())

    # loop for the rest
    for i in range(20, 301, step):
        external_arc = Circle(
                left_px=EXTERNAL_SCREEN_RECT[0],
                top_px=EXTERNAL_SCREEN_RECT[1],
                width_px=EXTERNAL_SCREEN_RECT[2],
                height_px=EXTERNAL_SCREEN_RECT[3],
                normalized=normalized,
                inverted_y=inverted_y).points(low=i, high=i+step+1)
        internal_arc = Circle(
                left_px=INTERNAL_SCREEN_RECT[0],
                top_px=INTERNAL_SCREEN_RECT[1],
                width_px=INTERNAL_SCREEN_RECT[2],
                height_px=INTERNAL_SCREEN_RECT[3],
                normalized=normalized,
                inverted_y=inverted_y).points(low=i+step, high=i-1, step=-1)
        grid.append(np.vstack([external_arc, internal_arc]))

    # last/first requires especial treatment
    a = Circle(
            left_px=EXTERNAL_SCREEN_RECT[0],
            top_px=EXTERNAL_SCREEN_RECT[1],
            width_px=EXTERNAL_SCREEN_RECT[2],
            height_px=EXTERNAL_SCREEN_RECT[3],
            normalized=normalized,
            inverted_y=inverted_y).points(low=340, high=360)
    b = Circle(
            left_px=EXTERNAL_SCREEN_RECT[0],
            top_px=EXTERNAL_SCREEN_RECT[1],
            width_px=EXTERNAL_SCREEN_RECT[2],
            height_px=EXTERNAL_SCREEN_RECT[3],
            normalized=normalized,
            inverted_y=inverted_y).points(low=0, high=20+1)
    external_arc = np.vstack([a, b])
    a = Circle(
            left_px=INTERNAL_SCREEN_RECT[0],
            top_px=INTERNAL_SCREEN_RECT[1],
            width_px=INTERNAL_SCREEN_RECT[2],
            height_px=INTERNAL_SCREEN_RECT[3],
            normalized=normalized,
            inverted_y=inverted_y).points(low=20, high=-1, step=-1)
    b = Circle(
            left_px=INTERNAL_SCREEN_RECT[0],
            top_px=INTERNAL_SCREEN_RECT[1],
            width_px=INTERNAL_SCREEN_RECT[2],
            height_px=INTERNAL_SCREEN_RECT[3],
            normalized=normalized,
            inverted_y=inverted_y).points(low=359, high=339, step=-1)
    internal_arc = np.vstack([a, b])
    grid.append(np.vstack([external_arc, internal_arc]))

    return reversed(grid)

def debug_window():
    from graphics import GraphWin

    win = GraphWin('Floor', SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX)
    win.setBackground("black")

    for circle in circle_grid():
        for [x, y] in circle.points(factor=1.):
            win.plotPixel(x, y, "white")
    
    # for circle in circle_grid():
    #     for [x, y] in circle.points(factor=2.):
    #         win.plotPixel(x, y, "white")

    for donut_slice in donut_grid():
        for [x, y] in donut_slice:
            win.plotPixel(x, y, "white")
            sleep(0.001)

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
    