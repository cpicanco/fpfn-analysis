# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço & François Tonneau.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import numpy as np
import cv2

ALGORITHM_KMEANS = 'kmeans'
ALGORITHM_QUANTILES = 'quantiles'

def unbiased_gaze(data, algorithm, min_block_size=1000,**kwargs):
    def bias(gaze_block,**kwargs):
        def kmeans(gaze_block,screen_center, k=2):
            """
            assumes equally distributed gaze_data and k clusters
            """
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,10,1.0)
            _, _, centers = cv2.kmeans(data=np.float32(gaze_block),
                                       K=k,
                                       criteria=criteria,
                                       attempts=10,
                                       flags=cv2.KMEANS_RANDOM_CENTERS)

            return centers.mean(axis=1) - screen_center 

        def quantiles(gaze_block,screen_center,q=[5, 10, 15, 85, 90, 95]):
            """
            assumes equally distributed gaze_data
            """
            x = gaze_block[:, 0].copy()
            y = gaze_block[:, 1].copy()
            sample_size = gaze_block.shape[0]

            x.sort()
            y.sort()
            x_stat = 0
            y_stat = 0

            for quantile in q:
                rank = (sample_size * quantile)//100
                x_stat += x[rank]
                y_stat += y[rank]

            # divide by length to get quantile average
            x_stat = x_stat/len(q)
            y_stat = y_stat/len(q)
            xy_stat = np.array([x_stat, y_stat])
            return xy_stat - screen_center

        kwargs['gaze_block'] = gaze_block
        if algorithm == ALGORITHM_KMEANS:
            return kmeans(**kwargs)
        elif algorithm == ALGORITHM_QUANTILES:
            return quantiles(**kwargs)

    def correction(gaze_block, bias):
        gaze_block[:, 0] = gaze_block[:, 0] - bias[0]
        gaze_block[:, 1] = gaze_block[:, 1] - bias[1]
        return gaze_block

    data_count = data.shape[0]    
    if data_count < min_block_size:
        print("\nToo few data to proceed. \nUsing min_block_size = %d"%data_count)
        min_block_size = data_count
    else:
        print("\nUsing min_block_size=%d for a total gaze count of %d"%(min_block_size, data_count))

    bias_along_blocks = {'bias':[], 'block':[]}
    unbiased = []
    for block_start in range(0, data_count, min_block_size):
        block_end = block_start + min_block_size
        if block_end <= data_count:
            gaze_block = data[block_start:block_end, :]
            gaze_bias = bias(gaze_block,**kwargs)
        else:
            gaze_block = data[block_start:data_count, :]
            
        unbiased.append(correction(gaze_block, gaze_bias))
        bias_along_blocks['bias'].append(gaze_bias)
        bias_along_blocks['block'].append([block_start,block_end])

    bias_along_blocks['bias'] = np.vstack(bias_along_blocks['bias'])
    bias_along_blocks['block'] = np.vstack(bias_along_blocks['block'])
    return np.vstack(unbiased), bias_along_blocks