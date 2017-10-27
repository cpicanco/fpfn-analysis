
import sys, os
from glob import glob

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def draw_relative_rate(data,title, save=False):
    x_label = 'Trials'
    y_label = 'Button-pressing proportion'
    axes = plt.gca()
    plt.suptitle(title, fontsize=12)

    plt.plot([0, 36], [.5, .5], 'k--', lw=1)
    plt.xticks([0,14, 35],[1, 15, 36])
    axes.plot(data,color="k", label="Right")


    # remove outer frame
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['right'].set_visible(False)

    axes.set_ylim(0.,1.)
    axes.set_xlim(-0.5, len(data)+0.5)

    #remove ticks
    axes.xaxis.set_ticks_position('none')
    axes.yaxis.set_ticks_position('none')

    axes.set_ylabel(y_label)
    axes.set_xlabel(x_label)
    if save:
        data_path = os.path.dirname(os.path.abspath(__file__))
        f = os.path.join(os.path.dirname(data_path),title+'.png')
        print(f)
        plt.savefig(f, bbox_inches='tight')
        plt.close()        
    else:
        plt.show()
