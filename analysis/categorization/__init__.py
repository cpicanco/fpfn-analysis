# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import os
import sys
sys.path.append('../../analysis')

import numpy as np
from matplotlib.path import Path as mp

from correction import unbiased_gaze, ALGORITHM_QUANTILES
from methods import remove_outside_screen

def clean_gaze_data(all_gaze_data,min_block_size=20000):
    x_norm = 'x_norm'
    y_norm = 'y_norm'
    
    keyword_arguments = {
        'screen_center':np.array([0.5, 0.5])
        }

    gaze_data = np.array([all_gaze_data[x_norm], all_gaze_data[y_norm]])

    gaze_data, mask = remove_outside_screen(gaze_data)
    all_gaze_data = all_gaze_data[mask]
    gaze_data, _ = unbiased_gaze(gaze_data.T, ALGORITHM_QUANTILES, min_block_size=min_block_size, **keyword_arguments)
    
    all_gaze_data[x_norm], all_gaze_data[y_norm] = gaze_data.T[0], gaze_data.T[1]
    return all_gaze_data

def get_gaze_mask(circle, gaze_data, factor=1.9):
    shape = mp(circle.points(factor=factor))  
    return shape.contains_points(gaze_data.T)

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

if __name__ == '__main__':
    from methods import load_gaze_data
    from methods import load_fpe_timestamps
    from methods import load_fpe_data
    from methods import load_ini_data
    from methods import get_events_per_trial_in_bloc, get_trial_intervals
    from methods import rate_in, get_relative_rate
    from stimuli import circular_grid as grid
    from drawing import plot_xy, draw_absolute_rate, draw_relative_rate

    all_gaze_data = load_gaze_data('/home/pupil/recordings/DATA/2017_11_03/EU/000/stimulus_control/gaze_positions_on_surface.csv', delimiter=',')
    
    # gaze_data = np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']])
    # plot_xy(gaze_data)
    # all_gaze_data = clean_gaze_data(all_gaze_data)
    # plot_xy(gaze_data)

    gaze_data = np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']])
    gaze_masks = [get_gaze_mask(circle, gaze_data) for circle in grid(normalized=True)]

    data_file = load_fpe_data('/home/pupil/recordings/DATA/2017_11_03/EU/000/stimulus_control/000.data', 12)
    timestamps = load_fpe_timestamps('/home/pupil/recordings/DATA/2017_11_03/EU/000/stimulus_control/000.timestamps')
    features = load_ini_data('/home/pupil/recordings/DATA/2017_11_03/EU/000/stimulus_control/positive.txt')
    trials = get_events_per_trial_in_bloc(data_file, timestamps, features, target_bloc=2, version='v2')
    
    print(len(features))
    trial_intervals = get_trial_intervals(trials, uncategorized=True) 
    #
    uncategorized_gaze_rates = []
    for mask in gaze_masks:
        target_circle_timestamps = all_gaze_data[mask]['gaze_timestamp']
        gaze_data = np.array([all_gaze_data[mask]['x_norm'], all_gaze_data[mask]['y_norm']])
        # plot_xy(gaze_data)
        uncategorized_gaze_rates.append(rate_in(trial_intervals, target_circle_timestamps))

    gaze_rates_per_trial = np.vstack(uncategorized_gaze_rates).T
    positive_feature_rate = []
    positive_else_rate = []
    for feature, rates in zip(features, gaze_rates_per_trial):
        if feature:
            positive_feature_rate.append(rates[feature-1])
            positive_else_rate.append(np.sum(np.delete(rates,feature-1)))
        else:
            pass

    draw_absolute_rate([positive_feature_rate, positive_else_rate], '2017_11_03_EU', True, 'v2',y_label='Looking rate',name='_looking')


    relative_rate = get_relative_rate(positive_feature_rate, positive_else_rate)
    draw_relative_rate(relative_rate, '2017_11_03_EU', True, 'v2',y_label='Looking proportion', name='_looking')