# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import matplotlib.patches as patches
from categorization.stimuli import circle_grid as grid 

i = 10000
all_gaze = None

def load_frame(axes):
    axes.set_ylim(ymax = 1., ymin = 0.)
    axes.set_xlim(xmax = 1., xmin = 0.)
    for circle in grid(normalized=True):
        axes.add_patch(
            patches.Ellipse(
                circle.center,   
                width=circle.width,          
                height=circle.height,
                angle=360,
                facecolor="gray",
                edgecolor="red",
                alpha=0.5        
            )
        )  

def updatefig(*args):
    global i, all_gaze, image
    if i < all_gaze.shape[0]:
        image.clear()
        load_frame(image)
        image.scatter(
            all_gaze['x_norm'][i],
            all_gaze['y_norm'][i], s=2, c='b')
        i += 1
    else:
        i = 0
        image.clear()
        load_frame(image)
    return image,

def animate_gaze(all_gaze_coordenates):
    global all_gaze, image
    all_gaze = all_gaze_coordenates
    figure = plt.figure()
    image = figure.add_axes([.08, .08, .85, (1/1.67539267016)], facecolor=(1., 1., 1., .1))
    axes = plt.gca()


    ani = animation.FuncAnimation(
        figure,
        updatefig,
        interval=0.1,
        blit=True)
    load_frame(image)
    plt.show()