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
from drawing import plot_xy, plot_xy_donut, draw_rates
from drawing import draw_relative_rate, draw_rate
from methods import remove_outside_screen
from methods import load_ini_data, load_fpe_timestamps, load_gaze_data
from methods import get_events_per_trial, get_trial_intervals
from methods import rate_in, get_relative_rate
from .stimuli import circular_grid
from .stimuli import donut_grid

def remove_outside_session_time(target_timestamps, intervals):
    mask = [False for _ in target_timestamps]
    for begin, end in intervals:
        a = target_timestamps >= begin
        b = target_timestamps <= end
        mask = mask | (a & b)
    return mask

def clean_gaze_data(all_gaze_data, intervals,
    min_block_size=1000,
    do_correction=True,
    do_remove_outside_screen=True,
    do_remove_outside_session_time=True,
    inspect=False):
    x_norm = 'x_norm'
    y_norm = 'y_norm'
    
    keyword_arguments = {
        'screen_center':np.array([0.5, 0.5])
        }

    if do_remove_outside_session_time:
        mask = remove_outside_session_time(all_gaze_data['time'], intervals)
        all_gaze_data = all_gaze_data[mask]

    gaze_data = np.array([all_gaze_data[x_norm], all_gaze_data[y_norm]])
    if do_remove_outside_screen:
        gaze_data, mask = remove_outside_screen(gaze_data)
        all_gaze_data = all_gaze_data[mask]

    if inspect:
        data_count = all_gaze_data.shape[0]
        for block_start in range(0, data_count, min_block_size):
            block_end = block_start + min_block_size
            if block_end <= data_count:
                pass  
            else:
                block_end = data_count
            plot_xy_donut(np.array([all_gaze_data['x_norm'][block_start:block_end],
                              all_gaze_data['y_norm'][block_start:block_end]]))
    if do_correction:    
        gaze_data, _ = unbiased_gaze(gaze_data.T, ALGORITHM_QUANTILES, min_block_size=min_block_size, **keyword_arguments)
        all_gaze_data[x_norm], all_gaze_data[y_norm] = gaze_data.T[0], gaze_data.T[1]

    return all_gaze_data

def get_gaze_mask(circle, gaze_data, factor=2.):
    shape = mp(circle.points(factor=factor))  
    return shape.contains_points(gaze_data.T)

def get_gaze_mask_donut(shape, gaze_data):
    shape = mp(shape)  
    return shape.contains_points(gaze_data.T)

def gaze_rate(ini_file, ts_file, all_gaze_data, title,
    factor=1.95,
    min_block_size=1000,
    do_correction=True,
    do_remove_outside_screen=True,
    do_remove_outside_session_time=True,
    inspect=False,
    save=False):

    time_data = zip(ts_file['time'], ts_file['bloc'], ts_file['trial'], ts_file['event'])
    ini_data = zip(ini_file['trial'], ini_file['contingency'], ini_file['feature'])
    trials = get_events_per_trial(ini_data, time_data)
    trial_intervals = get_trial_intervals(trials, uncategorized=True) 

    if inspect:
        # plot_xy(np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']]),factor)
        plot_xy_donut(np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']]))

    all_gaze_data = clean_gaze_data(all_gaze_data, trial_intervals,
        min_block_size=min_block_size,
        do_correction=do_correction,
        do_remove_outside_screen=do_remove_outside_screen,
        do_remove_outside_session_time=do_remove_outside_session_time,
        inspect=inspect)
    
    if inspect:
        # plot_xy(np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']]),factor)
        plot_xy_donut(np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']]))

    gaze_data = np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']])
    #gaze_masks = [get_gaze_mask(circle, gaze_data, factor) for circle in circular_grid(normalized=True)]
    gaze_masks = [get_gaze_mask_donut(donut, gaze_data) for donut in reversed(donut_grid(normalized=True))]

    uncategorized_gaze_rates = []
    for mask in gaze_masks:
        if False:
            gaze_data = np.array([all_gaze_data[mask]['x_norm'], all_gaze_data[mask]['y_norm']])
            # plot_xy(gaze_data)
            plot_xy_donut(gaze_data)
        target_timestamps = all_gaze_data[mask]['time']
        uncategorized_gaze_rates.append(rate_in(trial_intervals, target_timestamps))

    gaze_rates_per_trial = np.vstack(uncategorized_gaze_rates).T
    positive_feature_rate = []
    positive_else_rate = []
    for feature, rates in zip(ini_file['feature'], gaze_rates_per_trial):
        if feature:
            # print(rates[feature-1])
            positive_feature_rate.append(rates[feature-1])
            positive_else_rate.append(np.sum(np.delete(rates,feature-1)))
        else:
            pass
    relative_rate = get_relative_rate(positive_feature_rate, positive_else_rate)

    if inspect:
        draw_rate(rate_in(trial_intervals, all_gaze_data[:]['time']), title, save=save)
        draw_rates([positive_feature_rate, positive_else_rate], title, save,
            y_label='Looking rate',
            name='_absolute_looking',
            single=False,
            first_label='distinctive feature',
            second_label='common features and center',
            y_limit=False
            )
        draw_relative_rate(relative_rate, title, save, y_label='Looking proportion', name='_looking')
    
    return relative_rate

if __name__ == '__main__':
    pass