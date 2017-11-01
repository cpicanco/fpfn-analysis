# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import sys
sys.path.append('../../analysis')

import os
import numpy as np

# from drawing import plot_xy as plot
from correction import unbiased_gaze, ALGORITHM_QUANTILES

from methods import load_data, get_filenames, remove_outside_screen
from methods import stimuli_onset, all_stimuli, all_responses
from methods import switching_timestamps
from methods import rate_in, relative_rate

def clean_gaze_data(all_gaze_data):
    x_norm = 'x_norm'
    y_norm = 'y_norm'
    
    keyword_arguments = {
        'screen_center':np.array([0.5, 0.5])
        }

    gaze_data = np.array([all_gaze_data[x_norm], all_gaze_data[y_norm]])

    gaze_data, mask = remove_outside_screen(gaze_data)
    all_gaze_data = all_gaze_data[mask]
    gaze_data, _ = unbiased_gaze(gaze_data.T, ALGORITHM_QUANTILES, min_block_size=1000, **keyword_arguments)
    
    all_gaze_data[x_norm], all_gaze_data[y_norm] = gaze_data.T[0], gaze_data.T[1]
    return np.array([all_gaze_data[x_norm], all_gaze_data[y_norm]])

def get_gaze_mask(circle, gaze_data, factor=2.):
    shape = mp(circle.points(factor=factor))  
    print('Data inside shape: %d'%(len(gaze_data)))
    return shape.contains_points(gaze_data.T)

# def relative_rate_left_right(src_dir, target_intervals='all_onsets'):
#     timestamps = 'time'
#     paths = sorted(glob(os.path.join(src_dir,'0*')))
#     data = []
#     for path in paths:
#         all_gaze_data = load_data(os.path.join(path,"gaze_coordenates_on_screen.txt"))
#         left_gaze_mask, right_gaze_mask = gaze_mask_left_right(all_gaze_data)
#         left_timestamps = all_gaze_data[left_gaze_mask][timestamps] 
#         right_timestamps = all_gaze_data[right_gaze_mask][timestamps]

#         beha_data = load_data(os.path.join(path,"behavioral_events.txt"))
#         if 'all_onsets' in target_intervals: 
#             l_target_intervals = all_stimuli(beha_data)
#             l_target_intervals = zip(l_target_intervals, l_target_intervals[1:])
#             left_data = rate_in(l_target_intervals, left_timestamps)
#             right_data = rate_in(l_target_intervals, right_timestamps)
#             relative_rate_all = relative_rate(left_data, right_data)
#             data.append(relative_rate_all)

#         elif 'left_right_onsets':
#             l_target_intervals = all_stimuli(beha_data)
#             l_target_intervals = zip(l_target_intervals, l_target_intervals[1:])
#             left_data = rate_in(l_target_intervals, left_timestamps)
#             right_data = rate_in(l_target_intervals, right_timestamps)
#             relative_rate_all = relative_rate(left_data, right_data)
#             data.append([relative_rate_all[::2],relative_rate_all[1::2]])

#         elif 'red_blue_onsets' in target_intervals:
#             l_target_intervals = stimuli_onset(beha_data)
#             red_intervals = zip(l_target_intervals[0], l_target_intervals[1])
#             blue_intervals = zip(l_target_intervals[1], l_target_intervals[0][1:])

#             left_red_data = rate_in(red_intervals, left_timestamps)
#             right_red_data = rate_in(red_intervals, right_timestamps)
#             relative_rate_positive = relative_rate(left_red_data, right_red_data)

#             left_blue_data = rate_in(blue_intervals, left_timestamps)
#             right_blue_data = rate_in(blue_intervals, right_timestamps)
#             relative_rate_negative = relative_rate(left_blue_data, right_blue_data)
#             data.append((relative_rate_positive, relative_rate_negative))
#     return data

# def relative_rate_blue_red(src_dir, cycles_set=slice(0,8)):
#     paths = sorted(glob(os.path.join(src_dir,'0*')))
#     data = []
#     for path in paths:
#         beha_data = load_data(os.path.join(path,"behavioral_events.txt"))
#         target_intervals = stimuli_onset(beha_data)
#         red_intervals = zip(target_intervals[0], target_intervals[1])
#         blue_intervals = zip(target_intervals[1], target_intervals[0][1:])
#         responses = all_responses(beha_data)
        
#         red_data = rate_in(red_intervals, responses)
#         blue_data = rate_in(blue_intervals, responses)

#         relative_rate_all = relative_rate(red_data, blue_data)
#         data.append(relative_rate_all[cycles_set])
#     return data

# def rate_switching(src_dir, cycles_set=slice(0,8)):
#     paths = sorted(glob(os.path.join(src_dir,'0*')))
#     data = []
#     for path in paths:
#         all_gaze_data = load_data(os.path.join(path,"gaze_coordenates_on_screen.txt"))
#         left_gaze_mask, right_gaze_mask = gaze_mask_left_right(all_gaze_data)
#         switchings = switching_timestamps(all_gaze_data, left_gaze_mask, right_gaze_mask)
#         beha_data = load_data(os.path.join(path,"behavioral_events.txt"))
#         target_intervals = stimuli_onset(beha_data)
#         red_intervals = zip(target_intervals[0], target_intervals[1])
#         blue_intervals = zip(target_intervals[1], target_intervals[0][1:])
#         red_data = rate_in(red_intervals, switchings)[cycles_set]
#         blue_data = rate_in(blue_intervals, switchings)[cycles_set]
#         data.append((red_data,blue_data,switchings.shape[0]))
#     return data

# def relative_rate_switching(src_dir, cycles_set=slice(0,8)):
#     paths = sorted(glob(os.path.join(src_dir,'0*')))
#     data = []
#     for path in paths:
#         all_gaze_data = load_data(os.path.join(path,"gaze_coordenates_on_screen.txt"))

#         left_gaze_mask, right_gaze_mask = gaze_mask_left_right(all_gaze_data)
#         switchings = switching_timestamps(all_gaze_data, left_gaze_mask, right_gaze_mask)
#         # print(switchings.shape)
#         # stimuli
#         beha_data = load_data(os.path.join(path,"behavioral_events.txt"))
#         target_intervals = stimuli_onset(beha_data)
#         red_intervals = zip(target_intervals[0], target_intervals[1])
#         blue_intervals = zip(target_intervals[1], target_intervals[0][1:])


#         red_data = rate_in(red_intervals, switchings)
#         blue_data = rate_in(blue_intervals, switchings)

#         relative_rate_all = relative_rate(red_data, blue_data)
#         data.append(relative_rate_all[cycles_set])
#     return data

# def baseline_tracking_extinction_switching_correlation():
#     from constants import INNER_PATHS_DISCRIMINATION
#     from methods import get_data_path

#     X = [] 
#     Y = []
#     filenames = [os.path.join(get_data_path(), filename) for filename in INNER_PATHS_DISCRIMINATION]
#     for filename in filenames:
#         # ID = os.path.basename(os.path.dirname(filename))
#         timestamps = 'time'
#         paths = sorted(glob(os.path.join(filename,'0*')))

#         baseline_tracking_path = paths[0]
#         all_gaze_data = load_data(os.path.join(baseline_tracking_path,"gaze_coordenates_on_screen.txt"))
#         left_gaze_mask, right_gaze_mask = gaze_mask_left_right(all_gaze_data)
#         left_timestamps = all_gaze_data[left_gaze_mask][timestamps] 
#         right_timestamps = all_gaze_data[right_gaze_mask][timestamps]

#         beha_data = load_data(os.path.join(baseline_tracking_path,"behavioral_events.txt"))

#         # left_right_onsets
#         l_target_intervals = all_stimuli(beha_data)
#         l_target_intervals = zip(l_target_intervals, l_target_intervals[1:])
#         left_data = rate_in(l_target_intervals, left_timestamps)
#         right_data = rate_in(l_target_intervals, right_timestamps)
#         relative_rate_all = relative_rate(left_data, right_data)
#         X.append(np.nanmean(relative_rate_all[::2])-np.nanmean(relative_rate_all[1::2])) 


#         extintion_switching_path = paths[1]
#         all_gaze_data = load_data(os.path.join(extintion_switching_path,"gaze_coordenates_on_screen.txt"))

#         left_gaze_mask, right_gaze_mask = gaze_mask_left_right(all_gaze_data)
#         switchings = switching_timestamps(all_gaze_data, left_gaze_mask, right_gaze_mask)
#         beha_data = load_data(os.path.join(extintion_switching_path,"behavioral_events.txt"))
#         target_intervals = stimuli_onset(beha_data)
#         red_intervals = zip(target_intervals[0], target_intervals[1])
#         blue_intervals = zip(target_intervals[1], target_intervals[0][1:])

#         red_data = rate_in(red_intervals, switchings)
#         blue_data = rate_in(blue_intervals, switchings)
#         Y.append(np.nanmean(blue_data)-np.nanmean(red_data))

#     return np.array(X), np.array(Y)