# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import sys
sys.path.append('../../analysis')
sys.path.append('../../file_handling')

from data_organizer import PATHS_DESTIN, PATHS_SOURCE, PARAMETERS
from methods import load_yaml_data, load_ini_data
from methods import load_fpe_timestamps, load_gaze_data
from methods import get_data_files
from methods import get_events_per_trial, get_trial_intervals
from correction.utils import clean_gaze_data

from categorization.stimuli import SCREEN_WIDTH_PX as sw
from categorization.stimuli import SCREEN_HEIGHT_PX as sh
from drawing import colormaps, draw

import numpy as np
import cv2

def invert_y(gaze_points):
    return gaze_points['x_norm'], 1-gaze_points['y_norm']   

def custom_heatmap(data, heatmap_detail=0.05, colormap=colormaps.viridis):
    grid = [sh, sw]
    xvals, yvals = invert_y(data)
    hist, *edges = np.histogram2d(
        yvals, xvals,
        bins= grid,
        range= [[0, 1.], [0, 1.]],
        normed= False)
    filter_h = int(heatmap_detail * grid[0]) // 2 * 2 + 1
    filter_w = int(heatmap_detail * grid[1]) // 2 * 2 + 1
    hist = cv2.GaussianBlur(hist, (filter_h, filter_w), 15)

    hist_max = hist.max()
    hist *= (255. / hist_max) if hist_max else 0.
    hist = hist.astype(np.uint8)

    v = np.asarray(colormap)
    v *= 255
    v = v.astype(np.uint8)

    heatmap = np.zeros((sh,sw,4), np.uint8)
    heatmap[:,:,2] = cv2.LUT(hist, v[:,2]) # R matplotlib, 0 B opencv
    heatmap[:,:,1] = cv2.LUT(hist, v[:,1]) # G matplotlib, 1 G opencv
    heatmap[:,:,0] = cv2.LUT(hist, v[:,0]) # B matplotlib, 2 R opencv
    hist[hist>0] = 150
    heatmap[:,:,3] = hist # alpha

    # cv2.imwrite('temp.png', heatmap)
    draw.image(heatmap)

def analyse(i):
    parameters = PARAMETERS[i]
    print('\nRunning analysis for session:')
    print('\t', PATHS_DESTIN[i])
    print('\t', PATHS_SOURCE[i])
    data_files = get_data_files(PATHS_DESTIN[i],
        gaze_file_filter=parameters['gaze_file_filter'])
      
    info_file = load_yaml_data(data_files[0])
    ini_file = load_ini_data(data_files[1])
    time_file = load_fpe_timestamps(data_files[2])
    all_gaze_data = load_gaze_data(data_files[3])

    title = ' - '.join((str(i), info_file['nickname'], info_file['group']))

    time_data = zip(time_file['time'], time_file['bloc'], time_file['trial'], time_file['event'])
    ini_data = zip(ini_file['trial'], ini_file['contingency'], ini_file['feature'])
    trials = get_events_per_trial(ini_data, time_data)
    positive_intervals, negative_intervals = get_trial_intervals(trials)
    # trial_intervals = get_trial_intervals(trials, uncategorized=True)  

    positive_gaze_data = clean_gaze_data(all_gaze_data, 
        do_remove_outside_session_time=positive_intervals,        
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_manual_correction=parameters['do_manual_correction'],
        do_confidence_threshold=parameters['confidence_threshold'],
        min_block_size=parameters['min_block_size'],
        inspect=False)

    negative_gaze_data = clean_gaze_data(all_gaze_data, 
        do_remove_outside_session_time=negative_intervals,        
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_manual_correction=parameters['do_manual_correction'],
        do_confidence_threshold=parameters['confidence_threshold'],
        min_block_size=parameters['min_block_size'],
        inspect=False)

    custom_heatmap(positive_gaze_data)
    custom_heatmap(negative_gaze_data)

if __name__ == '__main__':
    analyse(-2)
