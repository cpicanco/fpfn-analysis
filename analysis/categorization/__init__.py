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
from methods import load_ini_data, load_fpe_timestamps, load_gaze_data
from methods import rate_in, get_relative_rate
from .stimuli import circular_grid
from .stimuli import donut_grid

def remove_outside_screen(data, screen=[1., .0, 1., .0], horizontal=True):
    xmax=screen[0]
    xmin=screen[1]
    ymax=screen[2]
    ymin=screen[3]
    if horizontal:
        x = (xmin <= data[0, :]) & (data[0, :] < xmax)
        y = (ymin <= data[1, :]) & (data[1, :] < ymax)
        mask = x & y
        data_clamped = data[:, mask]
        deleted_count = data.shape[1] - data_clamped.shape[1]
    else:
        x = (xmin <= data[:, 0]) & (data[:, 0] < xmax)
        y = (ymin <= data[:, 1]) & (data[:, 1] < ymax)
        mask = x & y
        data_clamped = data[mask, :]
        deleted_count = data.shape[0] - data_clamped.shape[0]

    if deleted_count > 0:
        print("\nRemoved", deleted_count, "data point(s) with out-of-screen coordinates!")
    return data_clamped, mask

def manual_correction(data, x, y):
    data['x_norm'] += x
    data['y_norm'] += y

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
    do_remove_outside_screen=[],
    do_remove_outside_session_time=True,
    do_manual_correction=[],
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
        gaze_data, mask = remove_outside_screen(gaze_data, do_remove_outside_screen)
        all_gaze_data = all_gaze_data[mask]

    if inspect and do_correction:
        data_count = all_gaze_data.shape[0]
        for block_start in range(0, data_count, min_block_size):
            block_end = block_start + min_block_size
            if block_end <= data_count:
                pass  
            else:
                block_end = data_count
            plot_xy(np.array([all_gaze_data[x_norm][block_start:block_end],
                              all_gaze_data[y_norm][block_start:block_end]]), factor=1.)
    if do_correction:    
        gaze_data, _ = unbiased_gaze(gaze_data.T, ALGORITHM_QUANTILES, min_block_size=min_block_size, **keyword_arguments)
        all_gaze_data[x_norm], all_gaze_data[y_norm] = gaze_data.T[0], gaze_data.T[1]

    if do_manual_correction:
        manual_correction(all_gaze_data, do_manual_correction[0], do_manual_correction[1])

    return all_gaze_data

def get_gaze_mask(circle, gaze_data, factor=4.):
    shape = mp(circle.points(factor=factor))  
    return shape.contains_points(gaze_data.T)

def get_gaze_mask_donut(shape, gaze_data):
    shape = mp(shape)  
    return shape.contains_points(gaze_data.T)

def get_gaze_rate_per_trial(all_trial_intervals, all_gaze_data,
    factor=4.,
    min_block_size=1000,
    do_correction=True,
    do_remove_outside_screen=[],
    do_remove_outside_session_time=True,
    do_manual_correction=[],
    inspect=False,
    save=False):

    # if inspect:
    #     plot_xy(np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']]),factor)

    all_gaze_data = clean_gaze_data(all_gaze_data, all_trial_intervals,
        min_block_size=min_block_size,
        do_correction=do_correction,
        do_remove_outside_screen=do_remove_outside_screen,
        do_remove_outside_session_time=do_remove_outside_session_time,
        do_manual_correction=do_manual_correction,
        inspect=False)
    
    # if inspect:
    #     plot_xy(np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']]),factor)

    gaze_data = np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']])
    # gaze_masks = [get_gaze_mask(circle, gaze_data, factor) for circle in circular_grid(normalized=True)]
    gaze_masks = [get_gaze_mask_donut(donut, gaze_data) for donut in donut_grid(normalized=True)]

    gaze_rates = []
    gaz_mirror = []
    for mask in gaze_masks:
        # if inspect:
        #     gaze_data = np.array([all_gaze_data[mask]['x_norm'], all_gaze_data[mask]['y_norm']])
        #     plot_xy(gaze_data, factor=1.)

        #     gaze_data = np.array([all_gaze_data[~mask]['x_norm'], all_gaze_data[~mask]['y_norm']])
        #     plot_xy(gaze_data, factor=1.)

        
        gaze_rates.append(rate_in(all_trial_intervals, all_gaze_data[mask]['time']))
        gaz_mirror.append(rate_in(all_trial_intervals, all_gaze_data[~mask]['time']))
    return np.vstack(gaze_rates).T, np.vstack(gaz_mirror).T

def get_relative_gaze_rate(features, gaze_rates_per_trial, gaze_rate_mirror):
    positive_feature_rate = []
    positive_feature_mirror = []
    for feature, rates, mirror in zip(features, gaze_rates_per_trial, gaze_rate_mirror):
        if feature:
            # print(rates[feature-1])
            positive_feature_rate.append(rates[feature-1])
            positive_feature_mirror.append(mirror[feature-1])
        else:
            continue
    return get_relative_rate(positive_feature_rate, positive_feature_mirror)

def gaze_rate(trial_intervals, features, all_gaze_data, title,
    factor=1.95,
    min_block_size=1000,
    do_correction=True,
    do_remove_outside_screen=True,
    do_remove_outside_session_time=True,
    inspect=False,
    save=False):

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
    for feature, rates in zip(features, gaze_rates_per_trial):
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