# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import os, sys, yaml
sys.path.append('../file_handling')

import numpy as np

from methods import rate, get_source_files, get_data_files, get_events_per_trial
from methods import load_ini_data, load_fpe_timestamps
from methods import load_yaml_data, load_gaze_data
from categorization import gaze_rate
from data_organizer import PATHS_SOURCE, PATHS_DESTIN, DATA_SKIP_HEADER, get_data_path
from data_organizer import PARAMETERS as p
from drawing import draw_rates

def analyse(i, parameters, source_files, inspect=False, info_file=None):
    print('Running analysis for session:', PATHS_SOURCE[i])
    if not info_file:
        info_file = load_yaml_data(source_files[0])
    ini_file = load_ini_data(source_files[1])
    time_file = load_fpe_timestamps(source_files[2])
    all_gaze_data = load_gaze_data(source_files[3])
    title = str(i)+' - '+info_file['nickname']+'-'+info_file['group']
    button_rate = rate(ini_file, time_file,
        title=title,
        save=False,
        inspect=inspect)

    looking_rate = gaze_rate(ini_file, time_file, all_gaze_data,
        title=title,
        factor=1.95,
        min_block_size=parameters['min_block_size'],
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_remove_outside_session_time=parameters['do_remove_outside_session_time'],
        inspect=inspect,
        save=False
    )
    return looking_rate, button_rate


def analyse_experiment(feature_degree):
    positive = []
    negative = []

    positive_button = []
    negative_button = []

    data_paths = get_data_path()
    data_paths = [os.path.join(data_paths, p) for p in PATHS_DESTIN]
    for path in data_paths:
        i = data_paths.index(path)
        if not p[i]['excluded']:
            source_files = get_data_files(data_paths[i], gaze_file_filter=p[i]['gaze_file_filter'])
            info_file = load_yaml_data(source_files[0])
            if info_file['feature_degree'] == feature_degree:
                looking_rate, button_rate = analyse(
                    i, p[i], source_files,
                    inspect=False,
                    info_file=info_file)

                if info_file['group'] == 'positive':
                    positive.append(np.array(looking_rate))
                    positive_button.append(np.array(button_rate))

                elif info_file['group'] == 'negative':
                    negative.append(np.array(looking_rate))
                    negative_button.append(np.array(button_rate))

    positive = np.vstack(positive)
    print('positive', len(positive))

    negative = np.vstack(negative)
    print('negative', len(negative))
    
    positive_min = np.array([np.nanmin(positive[:,i]) for i in range(positive.shape[1])])
    positive_max = np.array([np.nanmax(positive[:,i]) for i in range(positive.shape[1])])
    positive = np.array([np.nanmean(positive[:,i]) for i in range(positive.shape[1])])

    negative_min = np.array([np.nanmin(negative[:,i]) for i in range(negative.shape[1])])
    negative_max = np.array([np.nanmax(negative[:,i]) for i in range(negative.shape[1])])
    negative = np.array([np.nanmean(negative[:,i]) for i in range(negative.shape[1])])

    positive_error = [positive-positive_min, positive_max-positive]
    negative_error = [negative-negative_min, negative_max-negative]

    draw_rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title='mean looking proportion per trial with distinctive S '+str(feature_degree),
        save= True,
        y_label='Mean looking proportion',
        name='_looking_mean',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=True
        )

    positive_button = np.vstack(positive_button)
    negative_button = np.vstack(negative_button)

    positive_min = np.array([np.nanmin(positive_button[:,i]) for i in range(positive_button.shape[1])])
    positive_max = np.array([np.nanmax(positive_button[:,i]) for i in range(positive_button.shape[1])])
    positive = np.array([np.nanmean(positive_button[:,i]) for i in range(positive_button.shape[1])])

    negative_min = np.array([np.nanmin(negative_button[:,i]) for i in range(negative_button.shape[1])])
    negative_max = np.array([np.nanmax(negative_button[:,i]) for i in range(negative_button.shape[1])])
    negative = np.array([np.nanmean(negative_button[:,i]) for i in range(negative_button.shape[1])])
    positive_error = [positive-positive_min, positive_max-positive]
    negative_error = [negative-negative_min, negative_max-negative]

    draw_rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title='mean button-pressing proportion along trials '+str(feature_degree),
        save= True,
        y_label='mean button-pressing proportion',
        name='_button_mean',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=True
        )

if __name__ == '__main__':
    analyse_experiment(feature_degree=9)

    # negative = ['2017_11_16_000_VIN',
    #             '2017_11_14_005_JOA',
    #             '2017_11_14_004_NEL',
    #             '2017_11_14_003_LUC',
    #             '2017_11_14_002_TAT',
    #             '2017_11_14_001_MAR',
    #             '2017_11_14_000_SON']

    # for i in range(len(p)):
    #     for name in negative:
    #         if name in PATHS_SOURCE[i]:
    #             source_files = get_source_files(PATHS_SOURCE[i], gaze_file_filter=p[i]['gaze_file_filter'])
    #             analyse(i, p[i], source_files, inspect=True)


    # i = 19
    # source_files = get_source_files(PATHS_SOURCE[i], gaze_file_filter=p[i]['gaze_file_filter'])
    # if not p[i]['excluded']:
    #     analyse(i, p[i], source_files, inspect=True)        


    # data_paths = get_data_path()
    # data_paths = [os.path.join(data_paths, p) for p in PATHS_DESTIN]
    # i = 0
    # source_files = get_data_files(data_paths[i])
    # if not p[i]['excluded']:
    #     analyse(i, p[i], source_files, inspect=True)        