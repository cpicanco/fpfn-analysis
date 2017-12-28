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

def save_figure(filename):
    f = os.path.dirname(os.path.abspath(__file__))
    f = os.path.dirname(f)
    f = os.path.join(f,'images')
    f = os.path.join(f, filename+'.png')
    print(f)
    plt.savefig(f, bbox_inches='tight')
    plt.close() 

def points(x, y, title='scatter', save=False):
    x_label = 'FP'
    y_label = 'FN'
    axes = plt.gca()
    plt.suptitle(title, fontsize=12)

    # plt.xticks([0,(len(x)//2)-1, len(x)-1],[1, len(x)//2, len(x)])
    axes.scatter(x, y, color="k",marker='.', lw=1)


    # remove outer frame
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['right'].set_visible(False)

    axes.set_ylim(-0.1, 1.1)
    axes.set_xlim(-0.1, 1.1)

    #remove ticks
    axes.xaxis.set_ticks_position('none')
    axes.yaxis.set_ticks_position('none')

    axes.set_ylabel(y_label)
    axes.set_xlabel(x_label)
    if save:
        save_figure(title)       
    else:
        plt.show()    

def rate(data,title, save=False, y_label = 'FPS by trial'):
    x_label = 'Trials'
    axes = plt.gca()
    plt.suptitle(title, fontsize=12)

    plt.xticks([0,(len(data)//2)-1, len(data)-1],[1, len(data)//2, len(data)])
    axes.plot(data,color="k",marker='.', lw=1)


    # remove outer frame
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['right'].set_visible(False)

    axes.set_ylim(-0.1,120.)
    axes.set_xlim(-0.5, len(data)+0.5)

    #remove ticks
    axes.xaxis.set_ticks_position('none')
    axes.yaxis.set_ticks_position('none')

    axes.set_ylabel(y_label)
    axes.set_xlabel(x_label)
    if save:
        save_figure(title+'_fps')      
    else:
        plt.show()


def relative_rate(data,title, save=False, y_label = 'Button-pressing proportion', name=''):
    x_label = 'Trials'
    axes = plt.gca()
    plt.suptitle(title, fontsize=12)

    if 'looking' in name:
        plt.plot([0, len(data)], [1./9, 1./9], 'k--', lw=1)
    
    else:
        plt.plot([0, len(data)], [1./2, 1./2], 'k--', lw=1)

    
    plt.xticks([0,(len(data)//2)-1, len(data)-1],[1, len(data)//2, len(data)])

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
        save_figure(title+name)       
    else:
        plt.show()

def rates(data,title, save=False,
    y_label='Button-pressing rate',
    name='',
    single=False,
    first_label="positive",
    second_label="negative",
    y_limit=False,
    error=None):
    x_label = 'Trials'
    axes = plt.gca()
    plt.suptitle(title, fontsize=12)
    
    # positive
    if error:
        #axes.plot(data[0],color="k",marker='.', lw=1, label=first_label)
        #axes.plot(data[1],color="k",marker='x',ls='--', lw=1, label=second_label)
        axes.errorbar(range(len(data[0])), data[0], error[0], label=first_label,
            color="k",marker='.', lw=1, alpha=0.6)
        axes.errorbar(np.array(range(len(data[1])))+0.18, data[1], error[1], label=second_label,
            color="k",marker='x', fmt='.k', ls='--', lw=1, alpha=0.3)
    else:
        axes.plot(data[0],color="k",marker='.', lw=1, label=first_label)
        if not single:
            axes.plot(data[1],color="k",marker='x',ls='--', lw=1, label=second_label)

    # negative

    # if version == 'v1':
    #     plt.xticks([0,14, 35],[1, 15, 36])
    # elif version == 'v2':
    #     plt.xticks([0, 26, 53],[1, 27, 54])

    plt.xticks([0,(len(data[0])//2)-1, len(data[0])-1],[1, len(data[0])//2, len(data[0])])

    # remove outer frame
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['right'].set_visible(False)

    if y_limit:
        axes.set_ylim(-0.1,1.1)

    if 'latency' in title:
        axes.set_ylim(-0.1, 4.)

    axes.set_xlim(-0.5, len(data[0])+0.5)

    #remove ticks
    axes.xaxis.set_ticks_position('none')
    axes.yaxis.set_ticks_position('none')

    axes.set_ylabel(y_label)
    axes.set_xlabel(x_label)

    handles, labels = axes.get_legend_handles_labels()

    if error:
        axes.legend(handles, labels, loc="lower right")
    else:
        axes.legend(handles, labels)

    if save:
        save_figure(title+name)        
    else:
        plt.show()

def xy_plot(data, factor=1.0):
    import matplotlib.patches as patches
    from categorization.stimuli import circle_grid as grid 
    axes = plt.gca()
    axes.set_ylim(ymax = 1.5, ymin = -0.5)
    axes.set_xlim(xmax = 1.5, xmin = -0.5)
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

def xy_donut_plot(data):
    import matplotlib.patches as patches
    from matplotlib.path import Path as mp
    from categorization.stimuli import donut_grid as grid 
    axes = plt.gca()
    axes.set_ylim(ymax = 2, ymin = -1)
    axes.set_xlim(xmax = 2, xmin = -1)
    plt.scatter(*data, s=1, c='b')   
    for donut in grid(normalized=True):
        axes.add_patch(
            patches.PathPatch(
                mp(donut),
                facecolor="gray",
                edgecolor="red",
                alpha=0.5        
            )
        ) 
    plt.show()   
    plt.gcf().clear() 

def image(img=None, filename=None):
    import matplotlib.patches as patches
    from categorization.stimuli import circle_grid as grid
    fig, axes = plt.subplots()
    for circle in grid(normalized=False):
        axes.add_patch(
            patches.Ellipse(
                circle.center,   
                width=circle.width*1.,          
                height=circle.height*1.,
                angle=360,
                facecolor="none",
                edgecolor="black",
                alpha=0.5       
            )
        ) 

    # img = plt.imread(filename)
    plt.imshow(img)
    plt.show()
    # print(matplotlib.__version__)

if __name__ == '__main__':
    from random import randrange
    e1 = [randrange(1, 5) for _ in range(20)]
    e2 = [randrange(1, 5) for _ in range(20)]
    draw_rates([range(20), range(20)], error=[e1, e2],title='title')