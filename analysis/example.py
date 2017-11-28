# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import sys, yaml
sys.path.append('../file_handling')

import numpy as np

from methods import rate, get_source_files
from methods import load_ini_data, load_fpe_data, load_fpe_timestamps
from methods import load_yaml_data, load_gaze_data
from categorization import gaze_rate
from data_organizer import PATHS_SOURCE, DATA_SKIP_HEADER
from data_organizer import PARAMETERS as p
from drawing import draw_rates

version = 'v2'

def analyse(i, parameters, source_files, inspect=False, info_file=None):
    print('Running analysis for session:', PATHS_SOURCE[i])
    if not info_file:
        info_file = load_yaml_data(source_files[0])
    features = load_ini_data(source_files[1])
    data_file = load_fpe_data(source_files[2], skip_header=DATA_SKIP_HEADER[i])
    timestamps = load_fpe_timestamps(source_files[3])
    all_gaze_data = load_gaze_data(source_files[4], delimiter=',')
    title = str(i)+' - '+info_file['nickname']+'-'+info_file['group']
    button_rate = rate(data_file, timestamps, features, version,
        title=title,
        save=False,
        inspect=inspect)

    looking_rate = gaze_rate(data_file, timestamps, features, all_gaze_data,
        title=title,
        version=version,
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
    for path in PATHS_SOURCE:
        i = PATHS_SOURCE.index(path)
        if not p[i]['excluded']:
            source_files = get_source_files(PATHS_SOURCE[i], gaze_file_filter=p[i]['gaze_file_filter'])
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
    
    positive = [np.nanmean(positive[:,i]) for i in range(positive.shape[1])]
    negative = [np.nanmean(negative[:,i]) for i in range(negative.shape[1])]

    draw_rates(
        data=[positive, negative],
        title='mean looking proportion per trial with distinctive S',
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
    positive_button = [np.nanmean(positive_button[:,i]) for i in range(positive_button.shape[1])]
    negative_button = [np.nanmean(negative_button[:,i]) for i in range(negative_button.shape[1])]

    draw_rates(
        data=[positive_button, negative_button],
        title='mean button-pressing proportion along trials',
        save= True,
        y_label='mean button-pressing proportion',
        name='_button_mean',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=True
        )

if __name__ == '__main__':
    positive = []
    negative = []

    positive_button = []
    negative_button = []
    for path in PATHS_SOURCE:
        i = PATHS_SOURCE.index(path)
        if not p[i]['excluded']:
            source_files = get_source_files(PATHS_SOURCE[i], gaze_file_filter=p[i]['gaze_file_filter'])
            info_file = load_yaml_data(source_files[0])
            if info_file['feature_degree'] == 9:
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

    #negative = np.vstack(negative)

    positive = [np.nanmean(positive[:,i]) for i in range(positive.shape[1])]
    #negative = [np.nanmean(negative[:,i]) for i in range(negative.shape[1])]

    draw_rates(
        data=[positive, negative],
        title='mean looking proportion per trial with distinctive S',
        save= True,
        y_label='Mean looking proportion',
        name='_looking_mean',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=True
        )

    positive_button = np.vstack(positive_button)
    #negative_button = np.vstack(negative_button)
    positive_button = [np.nanmean(positive_button[:,i]) for i in range(positive_button.shape[1])]
    #negative_button = [np.nanmean(negative_button[:,i]) for i in range(negative_button.shape[1])]

    draw_rates(
        data=[positive_button, negative_button],
        title='mean button-pressing proportion along trials',
        save= True,
        y_label='mean button-pressing proportion',
        name='_button_mean',
        single=True,
        first_label='FP group',
        second_label='FN group',
        y_limit=True
        )


    # analyse_experiment(feature_degree=90)

    # for i in range(len(p)+1):
    #     source_files = get_source_files(PATHS_SOURCE[i], gaze_file_filter=p[i]['gaze_file_filter'])
    #     analyse(i, p[i], source_files, inspect=True)