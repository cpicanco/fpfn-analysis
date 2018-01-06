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

import matplotlib.patches as patches
from categorization.stimuli import circle_grid
from categorization.stimuli import donut_grid

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
    y_limit=[],
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
        axes.set_ylim(y_limit[0], y_limit[1])

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

def rates_double(data, error, title, labels, y_limit=[], save=True):
    def plot(ax, data, error, first_label, second_label):
        ax.errorbar(
            range(len(data[0])), data[0], error[0],
            label=first_label,
            color="k",marker='.', lw=1, alpha=0.6)
        ax.errorbar(
            np.array(range(len(data[1])))+0.18, data[1], error[1],
            label=second_label,
            color="k",marker='x', fmt='.k', ls='--', lw=1, alpha=0.3) 
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        if y_limit:
            ax.set_ylim(y_limit[0], y_limit[1])
        else:
            ax.set_ylim(1., 10.)
        ax.set_xlim(-0.5, len(data[0])+0.5)
 
    (d1, d2, d3, d4) = data
    (e1, e2, e3, e4) = error

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, sharex=True)
    plot(ax1, [d1, d2], [e1, e2], labels[2], labels[3])
    plot(ax2, [d3, d4], [e3, e4], labels[2], labels[3])

    ax1.set_ylabel(labels[0])
    ax1.text(0.5, .9,
        labels[4], ha='center', va='center',
        transform=ax1.transAxes)

    ax2.text(0.5, .9,
        labels[5], ha='center', va='center',
        transform=ax2.transAxes)

    handles, llabels = ax2.get_legend_handles_labels()
    ax2.legend(handles, llabels, loc="lower right")
      
    plt.xticks(
        [0,(len(data[0])//2)-1, len(data[0])-1],
        [1, len(data[0])//2, len(data[0])]
    )
    
    f.text(0.5, 0.04, labels[1], ha='center')

    if save:
        save_figure(title)        
    else:
        plt.show()


def xy_plot(data, factor=1.0):
    axes = plt.gca()
    axes.set_ylim(ymax = 1.5, ymin = -0.5)
    axes.set_xlim(xmax = 1.5, xmin = -0.5)
    plt.scatter(*data, s=1, c='b')   
    for circle in circle_grid(normalized=True):
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
    axes = plt.gca()
    axes.set_ylim(ymax = 2, ymin = -1)
    axes.set_xlim(xmax = 2, xmin = -1)
    plt.scatter(*data, s=1, c='b')   
    for donut in donut_grid(normalized=True):
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

def images(imgs, screen, save, title):
    (img1, img2) = imgs
    (w, h) = screen
    def fax(ax):
        # for circle in circle_grid(normalized=False):
        #     ax.add_patch(
        #         patches.Ellipse(
        #             circle.center,   
        #             width=circle.width*1.,          
        #             height=circle.height*1.,
        #             angle=360,
        #             facecolor="none",
        #             edgecolor="black",
        #             alpha=0.25      
        #         )
        #     ) 
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        ax.axis('off')
        # ax.set_ylim(0, h)
        # ax.set_xlim(0, w)        

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, sharex=True)
    ax1.imshow(img1)
    fax(ax1)
    ax2.imshow(img2)
    fax(ax2)
    f.tight_layout(pad= 0)
    f.subplots_adjust(wspace=0)
    if save:
        save_figure(title)       
    else:
        plt.show()

def images_four(imgs, save, title):
    from mpl_toolkits.axes_grid1 import Grid
    
    f = plt.figure(figsize=(4,4))
    grid = Grid(f, rect=111, nrows_ncols=(2,2),
            axes_pad=0.01, label_mode='none',)

    for ax, im in zip(grid, imgs):
        ax.imshow(im)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.axis('off')
         
    f.text(.08, .52, 'FP', ha='left', va='center')
    f.text(.95, .52, 'FN', ha='right', va='center')
    f.text(.52, .95, 'distinctive', ha='center', va='top',)
    f.text(.52, .08, 'common', ha='center', va='bottom',)   

    if save:
        save_figure(title)       
    else:
        plt.show()

if __name__ == '__main__':
    from random import randrange
    e1 = [randrange(1, 5) for _ in range(20)]
    e2 = [randrange(1, 5) for _ in range(20)]
    draw_rates([range(20), range(20)], error=[e1, e2],title='title')