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

def join_images(path1, path2):
    import cv2
    im1 = cv2.imread(path1, cv2.IMREAD_UNCHANGED)
    im2 = cv2.imread(path2, cv2.IMREAD_UNCHANGED)
    print(im1.shape)
    print(im2.shape)
    os.remove(path1)
    os.remove(path2)
    cv2.imwrite(path1, np.concatenate((im1, im2), axis=1))

def save_figure(filename, extension = '.png'):
    f = os.path.dirname(os.path.abspath(__file__))
    f = os.path.dirname(f)
    f = os.path.join(f,'images')
    f = os.path.join(f, ''.join([filename,extension]))
    print(f)
    plt.savefig(f, bbox_inches='tight', dpi=100)
    plt.close() 
    return f

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
        return save_figure(title)       
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
        return save_figure(title+'_fps')      
    else:
        plt.show()


def relative_rate(data,title, save=False, y_label = 'Proporção de pressionar o botão', name=''):
    x_label = 'Tentativas'
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
        return save_figure(title+name)       
    else:
        plt.show()

def rates(data,title, save=False,
    y_label='Proporção de pressionar o botão',
    name='',
    single=False,
    first_label="Positivo",
    second_label="Negativo",
    y_limit=[],
    error=None):
    x_label = 'Tentativas'
    axes = plt.gca()
    # plt.suptitle(title, fontsize=12)

    if y_limit:
        axes.set_ylim(y_limit[0], y_limit[1])

    if 'latency' in title:
        axes.set_ylim(-0.1, 4.)
    
    # positive
    if error:
        #axes.plot(data[0],color="k",marker='.', lw=1, label=first_label)
        #axes.plot(data[1],color="k",marker='x',ls='--', lw=1, label=second_label)
        axes.errorbar(range(len(data[0])), data[0], error[0], label=first_label,
            color="k",marker='o', markersize= 2, lw=1, alpha=0.8)
        axes.errorbar(np.array(range(len(data[1])))+0.18, data[1], error[1], label=second_label,
            color="k",marker='x', markersize=4, fmt='.k', ls='--', lw=1, alpha=0.3)
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


    axes.set_xlim(-0.5, len(data[0])+0.5)

    #remove ticks
    # axes.xaxis.set_ticks_position('none')
    # axes.yaxis.set_ticks_position('none')

    axes.set_ylabel(y_label)
    axes.set_xlabel(x_label)

    handles, labels = axes.get_legend_handles_labels()

    if error:
        axes.legend(handles, labels, loc="lower right")
    else:
        axes.legend(handles, labels)

    if save:
        return save_figure(title+name)        
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
        return save_figure(title)        
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
    from matplotlib.path import Path
    axes = plt.gca()
    axes.set_ylim(ymax = 2, ymin = -1)
    axes.set_xlim(xmax = 2, xmin = -1)
    plt.scatter(*data, s=1, c='b')   
    for donut in donut_grid(normalized=True):
        axes.add_patch(
            patches.PathPatch(
                Path(donut),
                facecolor="gray",
                edgecolor="red",
                alpha=0.5        
            )
        ) 
    plt.show()   
    plt.gcf().clear() 

def xy_example(data):
    from matplotlib.path import Path
    axes = plt.gca()
    axes.set_ylim(ymax = 1.1, ymin = -0.1)
    axes.set_xlim(xmax = .86, xmin = .14)
    for donut in donut_grid(normalized=True):
        axes.add_patch(
            patches.PathPatch(
                Path(donut),
                facecolor="gray",
                edgecolor="black",
                alpha=0.5        
            )
        ) 
    for circle in circle_grid(normalized=True):
        axes.add_patch(
            patches.Ellipse(
                circle.center,   
                width=circle.width,          
                height=circle.height,
                angle=360,
                facecolor="white",
                edgecolor="black",
                alpha=0.5        
            )
        ) 
    plt.scatter(*data, s=3, c='k')   
    plt.axes().set_aspect(0.596875)
    plt.show()   
    plt.gcf().clear() 

def images(imgs, screen, save, title):
    (img1, img2) = imgs
    # (w, h) = screen
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
        ax.yaxis.set_ticks_position('none')
        ax.yaxis.set_ticklabels([])
        ax.xaxis.set_ticks_position('none')
        ax.xaxis.set_ticklabels([])
        ax.axis('off')
        # ax.set_ylim(0, h)
        # ax.set_xlim(0, w)        

    # dpi = 100
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(3.5,3.5), sharey=True, sharex=True)
    ax1.imshow(img1)
    fax(ax1)
    ax2.imshow(img2)
    fax(ax2)
    f.tight_layout(pad= 0)
    f.subplots_adjust(wspace=0)
    if save:
        return save_figure(title)       
    else:
        plt.show()

def images_four(imgs, save, title):
    from mpl_toolkits.axes_grid1 import Grid
    
    f = plt.figure(figsize=(4,4))
    grid = Grid(
        f, rect=111, nrows_ncols=(2,2),
        axes_pad=0.0, label_mode='none',)

    for ax, im in zip(grid, imgs):
        ax.imshow(im)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.set_ticks_position('none')
        ax.yaxis.set_ticklabels([])
        ax.xaxis.set_ticks_position('none')
        ax.xaxis.set_ticklabels([])
        ax.axis('off')
         
    f.text(.08, .52, 'AP', ha='left', va='center')
    f.text(.95, .52, 'AN', ha='right', va='center')
    f.text(.50, .95, 'distintivo', ha='center', va='top',)
    f.text(.50, .08, 'comum', ha='center', va='bottom',)   

    f.text(.15, .90, 'S+', ha='left', va='top')
    f.text(.85, .90, 'S-', ha='right', va='top')
    f.text(.90, .15, 'S+', ha='right', va='bottom',)
    f.text(.15, .15, 'S-', ha='left', va='bottom',)   

    if save:
        return save_figure(title)       
    else:
        plt.show()

def all_proportions(gaze_proportion, button_proportion):
    def by_button(x):
        (gz, btn, i) = x 
        return np.sum(btn)

    from mpl_toolkits.axes_grid1 import Grid

    (positive_gaze, negative_gaze) = gaze_proportion
    (positive_button, negative_button) = button_proportion

    positive = [(gaze, button, 'P%i'%p) for gaze, button, p in zip(positive_gaze, positive_button, range(1, len(positive_gaze)+1))]
    negative = [(gaze, button, 'P%i'%p) for gaze, button, p in zip(negative_gaze, negative_button, range(len(negative_gaze)+1,(len(negative_gaze)*2)+1))]
 
    positive.sort(key=by_button, reverse=True)
    negative.sort(key=by_button, reverse=True)

    data = []
    for posi, nega in zip(positive,negative):
        data.append(posi)
        data.append(nega)

    rows = np.max([len(positive), len(negative)])
    cols = 2
    x_label = 'Tentativas'
    y_label = 'Proporção'
    first_label = 'Pressionar botão durante S+'
    second_label = 'Olhar estímulo distintivo'

    f = plt.figure(figsize=(5,8))
    grid = Grid(
        f, rect=111, share_all=True, nrows_ncols=(rows, cols),
        axes_pad=0.25, label_mode='none',)
    title = 'all_proportions'

    i = 0
    for ax, datum in zip(grid, data):
        (gaze, button, pname) = datum
        ax.text(.45, 1.1, pname, ha='center', va='center', transform=ax.transAxes)
        ax.set_ylim(-0.1, 1.1)

        ax.plot(button,color="k",marker='', lw=1)
        ax.plot(gaze,color="k",marker='',ls='--', lw=1)

        plt.xticks([0,(len(button)//2)-1, len(button)-1],[1, len(button)//2, len(button)])

        # remove outer frame
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.set_xlim(-0.5, len(button)+0.5)
        ax.set_xticklabels([])

        #remove ticks
        # ax.xaxis.set_ticks_position('none')
        # ax.yaxis.set_ticks_position('none')

        # handles, labels = ax.get_legend_handles_labels()
        # ax.legend(handles, labels)
        i += 1

    # 9
    grid[8].set_ylabel(y_label)
    grid[19].set_xlabel(x_label)

    # 90
    # grid[10].set_ylabel(y_label)
    # grid[21].set_xlabel(x_label)
    f.tight_layout()
    # f.subplots_adjust(wspace=0)
    save_figure(title, '.svg')

def all_proportions_intra(gaze_proportion, button_proportion):
    def by_button(x):
        (gp, gn, bp, bn, p)  = x 
        return np.mean(bp)- np.mean(bn)

    from mpl_toolkits.axes_grid1 import Grid

    (p_gz, n_gz) = gaze_proportion
    (p_btn, n_btn) = button_proportion

    data = [(gp, gn, bp, bn, 'P%i'%p) \
    for gp, gn, bp, bn, p in zip(p_gz, n_gz, p_btn, n_btn, range(1, len(p_gz)+1))]

    data.sort(key=by_button, reverse=True)

    rows = 6
    cols = 2
    x_label = 'Tentativas'
    y_label = 'Proporção'

    f = plt.figure(figsize=(5,8))
    grid = Grid(
        f, rect=111, share_all=True, nrows_ncols=(rows, cols),
        axes_pad=0.25, label_mode='none',)
    title = 'all_proportions'

    i = 0
    for ax, datum in zip(grid, data):
        (p_gaze, n_gaze, p_button, n_button, pname) = datum

        bindex = '%.3f'%(np.mean(p_button)- np.mean(n_button))
        gindex = '%.3f'%(np.mean(p_gaze)- np.mean(n_gaze))
        ax.text(.45, 1.1, pname+', b='+bindex+', o='+gindex, ha='center', va='center', transform=ax.transAxes)
        ax.set_ylim(-0.1, 1.1)

        
        ax.plot(n_button,color="gray",marker='', lw=1)
        ax.plot(n_gaze,color="gray",marker='',ls='--', lw=.6)

        ax.plot(p_button,color="k",marker='', lw=1)
        ax.plot(p_gaze,color="k",marker='',ls='--', lw=.6)
        
        plt.xticks(
            [0,(len(p_button)//2)-1, len(p_button)-1],[1, len(p_button)//2, len(p_button)])

        # remove outer frame
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.set_xlim(-0.5, len(p_button)+0.5)
        ax.set_xticklabels([])

        #remove ticks
        # ax.xaxis.set_ticks_position('none')
        # ax.yaxis.set_ticks_position('none')

        # handles, labels = ax.get_legend_handles_labels()
        # ax.legend(handles, labels)
        i += 1

    grid[4].set_ylabel(y_label)
    grid[11].set_xlabel(x_label)

    f.tight_layout()
    # f.subplots_adjust(wspace=0)
    save_figure(title, '.svg')       
  

def scale(y_maximum, image, save, title, size):
    labels = ['%0.2f'%y_maximum, '0\n(transparente)']
    # frame.get_xaxis().set_visible(False)
    # plt.yticks([0, 256], labels)
    # frame.yaxis.tick_right()
    dpi = 100
    figure = plt.figure(figsize=(1, size/dpi), dpi=dpi)
    frame = plt.gca()
    frame.imshow(image)
    frame.set_title(labels[0], fontsize=10)
    frame.set_xlabel(labels[1], fontsize=10)

    # remove outer frame
    frame.spines['top'].set_visible(False)
    frame.spines['bottom'].set_visible(False)
    frame.spines['left'].set_visible(False)
    frame.spines['right'].set_visible(False) 

    # remove ticks and tick labels
    frame.axes.yaxis.set_ticks_position('none')
    frame.axes.yaxis.set_ticklabels([])
    frame.axes.xaxis.set_ticks_position('none')
    frame.axes.xaxis.set_ticklabels([])
    
    if save:
        filename = save_figure(title+'_scale')
        plt.gcf().clear()  
        return filename       
    else:
        plt.show() 
        plt.gcf().clear() 

if __name__ == '__main__':
    from random import randrange
    e1 = [randrange(1, 5) for _ in range(20)]
    e2 = [randrange(1, 5) for _ in range(20)]
    draw_rates([range(20), range(20)], error=[e1, e2],title='title')