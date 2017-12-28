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
from gaze_animation import animate_gaze
    
from correction.utils import clean_gaze_data
from drawing import draw

from methods import load_ini_data, load_fpe_timestamps, load_gaze_data
from methods import rate_in, get_relative_rate
from .stimuli import circle_grid
from .stimuli import donut_grid

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
    do_confidence_threshold=None,
    inspect=False,
    save=False):

    if inspect:
        draw.xy_plot(np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']]),1.)

    if do_remove_outside_session_time:
        intervals = all_trial_intervals
    else:
        intervals = None

    all_gaze_data = clean_gaze_data(all_gaze_data, 
        min_block_size=min_block_size,
        do_correction=do_correction,
        do_remove_outside_screen=do_remove_outside_screen,
        do_remove_outside_session_time=all_trial_intervals,
        do_manual_correction=do_manual_correction,
        do_confidence_threshold=do_confidence_threshold,
        inspect=inspect)

    # animate_gaze(all_gaze_data)
    
    if inspect:
        draw.xy_plot(np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']]),1.)

    gaze_data = np.array([all_gaze_data['x_norm'], all_gaze_data['y_norm']])
    
    if factor == 'donut_slice':
        gaze_masks = [get_gaze_mask_donut(i, gaze_data) \
        for i in donut_grid(normalized=True)]
    
    else:
        gaze_masks = [get_gaze_mask(i, gaze_data, factor) \
        for i in circle_grid(normalized=True, inverted_y=True)]
    
    gaze_rates = []
    gaz_mirror = []
    for mask in gaze_masks:
        # if inspect:
        #     gaze_data = np.array([all_gaze_data[mask]['x_norm'], all_gaze_data[mask]['y_norm']])
        #     draw.xy_plot(gaze_data, factor=1.)

        #     gaze_data = np.array([all_gaze_data[~mask]['x_norm'], all_gaze_data[~mask]['y_norm']])
        #     draw.xy_plot(gaze_data, factor=1.)

        gaze_rates.append(rate_in(all_trial_intervals, all_gaze_data[mask]['time']))
        gaz_mirror.append(rate_in(all_trial_intervals, all_gaze_data[~mask]['time']))
    return np.vstack(gaze_rates).T, np.vstack(gaz_mirror).T

def get_relative_gaze_rate(features, gaze_rates_per_trial, gaze_rate_mirror, absolute=False):
    positive_feature_rate = []
    positive_feature_mirror = []
    for feature, rates, mirror in zip(features, gaze_rates_per_trial, gaze_rate_mirror):
        if feature:
            positive_feature_rate.append(rates[feature-1])
            positive_feature_mirror.append(mirror[feature-1])
        else:
            continue
    
    if absolute:
        return positive_feature_rate, positive_feature_mirror
    return get_relative_rate(positive_feature_rate, positive_feature_mirror)

if __name__ == '__main__':
    pass