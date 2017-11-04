# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import sys, os
from glob import glob

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def draw_relative_rate(data,title, save=False, version='v1', y_label = 'Button-pressing proportion', name=''):
    x_label = 'Trials'
    axes = plt.gca()
    plt.suptitle(title, fontsize=12)

    if version == 'v1':
        plt.plot([0, 36], [.5, .5], 'k--', lw=1)
        plt.xticks([0,14, 35],[1, 15, 36])
    elif version == 'v2':
        plt.plot([0, 54], [.5, .5], 'k--', lw=1)
        plt.xticks([0, 26, 53],[1, 27, 54])

    axes.plot(data,color="k",marker='.', lw=1)


    # remove outer frame
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['right'].set_visible(False)

    axes.set_ylim(-0.1,1.1)
    axes.set_xlim(-0.5, len(data)+0.5)

    #remove ticks
    axes.xaxis.set_ticks_position('none')
    axes.yaxis.set_ticks_position('none')

    axes.set_ylabel(y_label)
    axes.set_xlabel(x_label)
    if save:
        data_path = os.path.dirname(os.path.abspath(__file__))
        f = os.path.join(os.path.dirname(data_path),title+'_relative'+name+'.png')
        print(f)
        plt.savefig(f, bbox_inches='tight')
        plt.close()        
    else:
        plt.show()

def draw_absolute_rate(data,title, save=False, version='v1', y_label='Button-pressing rate', name=''):
    x_label = 'Trials'
    axes = plt.gca()
    plt.suptitle(title, fontsize=12)
    
    # positive
    axes.plot(data[0],color="k",marker='.', lw=1, label="positive")

    # negative
    axes.plot(data[1],color="k",marker='x',ls='--', lw=1, label="negative")

    if version == 'v1':
        plt.xticks([0,14, 35],[1, 15, 36])
    elif version == 'v2':
        plt.xticks([0, 26, 53],[1, 27, 54])

    # remove outer frame
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['right'].set_visible(False)

    # axes.set_ylim(0.,1.)
    axes.set_xlim(-0.5, len(data[0])+0.5)

    #remove ticks
    axes.xaxis.set_ticks_position('none')
    axes.yaxis.set_ticks_position('none')

    axes.set_ylabel(y_label)
    axes.set_xlabel(x_label)


    handles, labels = axes.get_legend_handles_labels()
    axes.legend(handles, labels)
   
    if save:
        data_path = os.path.dirname(os.path.abspath(__file__))
        f = os.path.join(os.path.dirname(data_path),title+'_absolute'+name+'.png')
        print(f)
        plt.savefig(f, bbox_inches='tight')
        plt.close()        
    else:
        plt.show()

def plot_xy(data, factor=1.9):
    import matplotlib.patches as patches
    from stimuli import circular_grid as grid 
    axes = plt.gca()
    axes.set_ylim(ymax = 1, ymin = 0)
    axes.set_xlim(xmax = 1, xmin = 0)
    plt.scatter(*data, s=1, c='b')   
    for circle in grid(normalized=True):
        axes.add_patch(
            patches.Ellipse(
                circle.center,   
                width=circle.width*factor,          
                height=circle.height*factor,
                angle=360,
                facecolor="gray",
                edgecolor="red",
                alpha=0.5        
            )
        ) 
    plt.show()   
    plt.gcf().clear() 
