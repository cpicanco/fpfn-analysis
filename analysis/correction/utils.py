# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import numpy as np

from . import unbiased_gaze, ALGORITHM_QUANTILES

def remove_outside_screen(data, screen=[1., .0, 1., .0], horizontal=True):
    xmax, xmin = screen[0], screen[1]
    ymax, ymin = screen[2], screen[3]
    if horizontal:
        x = (xmin <= data[0, :]) & (data[0, :] < xmax)
        y = (ymin <= data[1, :]) & (data[1, :] < ymax)
    else:
        x = (xmin <= data[:, 0]) & (data[:, 0] < xmax)
        y = (ymin <= data[:, 1]) & (data[:, 1] < ymax)
    return x & y

def manual_correction(data, x, y):
    data['x_norm'] += x
    data['y_norm'] += y

def confidence_threshold(all_gaze_data, threshold):
    return all_gaze_data['confidence']>=threshold

def remove_outside_session_time(target_timestamps, intervals):
    mask = [False for _ in target_timestamps]
    for begin, end in intervals:
        a = target_timestamps >= begin
        b = target_timestamps <= end
        mask = mask | (a & b)
    return mask

def clean_gaze_data(all_gaze_data, 
    min_block_size=1000,
    do_correction=True,
    do_remove_outside_screen=[],
    do_remove_outside_session_time=[],
    do_manual_correction=[],
    do_confidence_threshold=None,
    inspect=False):
    x_norm = 'x_norm'
    y_norm = 'y_norm'
    
    keyword_arguments = {
        'screen_center':np.array([0.5, 0.5])
        }

    data_count = all_gaze_data.shape[0]

    if do_remove_outside_session_time:
        mask = remove_outside_session_time(all_gaze_data['time'], do_remove_outside_session_time)
        all_gaze_data = all_gaze_data[mask]
        deleted_count = data_count - all_gaze_data.shape[0]   
        if deleted_count > 0:
            data_count = all_gaze_data.shape[0]
            print("Removed", deleted_count, "data point(s) with out-of-time coordinates!")

    if do_remove_outside_screen:
        gaze_data = np.array([all_gaze_data[x_norm], all_gaze_data[y_norm]])
        mask = remove_outside_screen(gaze_data, do_remove_outside_screen)
        all_gaze_data = all_gaze_data[mask]
        deleted_count = data_count - all_gaze_data.shape[0] 
        if deleted_count > 0:
            data_count = all_gaze_data.shape[0]
            print("Removed", deleted_count, "data point(s) with out-of-screen coordinates!")

    if do_confidence_threshold:
        mask = confidence_threshold(all_gaze_data, do_confidence_threshold)
        all_gaze_data = all_gaze_data[mask]
        deleted_count = data_count - all_gaze_data.shape[0]   
        if deleted_count > 0:
            print("Removed %i from %i (%.2f%%) data point(s) below confidence threshold!"%(deleted_count, data_count, (deleted_count/data_count)*100))

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
        print("Remaining data points will be corrected using %s algorithm!"%ALGORITHM_QUANTILES)
        gaze_data = np.array([all_gaze_data[x_norm], all_gaze_data[y_norm]])   
        gaze_data, _ = unbiased_gaze(gaze_data.T, ALGORITHM_QUANTILES, min_block_size=min_block_size, **keyword_arguments)
        all_gaze_data[x_norm], all_gaze_data[y_norm] = gaze_data.T[0], gaze_data.T[1]

    if do_manual_correction:
        print("Remaining data points will be corrected using manual (x=%.2f, y=%.2f) correction also!"%(do_manual_correction[0], do_manual_correction[1]))
        manual_correction(all_gaze_data, do_manual_correction[0], do_manual_correction[1])

    return all_gaze_data