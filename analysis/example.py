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

from methods import trial_mask, variance, statistics
from methods import latency, get_trial_intervals, get_responses
from methods import relative_rate_from, rate_in
from methods import get_data_files, get_events_per_trial
from methods import load_ini_data_intrasubject, load_ini_data, load_fpe_timestamps
from methods import load_yaml_data, load_gaze_data
from categorization import get_gaze_rate_per_trial, get_relative_gaze_rate
from correction.utils import confidence_threshold
from data_organizer import PATHS_SOURCE, PATHS_DESTIN, DATA_SKIP_HEADER, get_data_path
from data_organizer import PARAMETERS as p
from drawing import draw

def analyse_button(trials, responses, title, inspect=False):
    positive_intervals, negative_intervals = get_trial_intervals(trials)
    button_rate_positive = rate_in(positive_intervals, responses)
    button_rate_negative = rate_in(negative_intervals, responses)
    button_relative_rate = relative_rate_from(
        button_rate_positive, button_rate_negative)
    
    # draw.rates([button_rate_positive, button_rate_negative],
    #     title= title+'_absolute',
    #     save= not inspect,
    #     first_label='S+',
    #     second_label='S-',
    #     y_label= 'Button-pressing per seconds'
    # ) 

    # draw.rates([button_relative_rate, []],
    #     title= title+'_relative',
    #     save= not inspect,
    #     y_label='Button-pressing proportion',
    #     single= True,
    #     y_limit= [-0.1, 1.1],
    #     ) 
    return button_relative_rate

def analyse(i, factor='donut_slice', inspect=False, data_files=None):
    print('\nRunning analysis for session:')
    print('\t', PATHS_DESTIN[i])
    print('\t', PATHS_SOURCE[i])
    parameters = p[i]
    if not data_files:
        data_files = get_data_files(
            PATHS_DESTIN[i],
            gaze_file_filter=parameters['gaze_file_filter'])
          
    info_file = load_yaml_data(data_files[0])
    ini_file = load_ini_data(data_files[1])
    time_file = load_fpe_timestamps(data_files[2])
    all_gaze_data = load_gaze_data(data_files[3])
    title = ' - '.join(['%02d'%i, '%02d'%info_file['feature_degree'], info_file['group'], info_file['nickname'], str(factor)])

    time_data = zip(time_file['time'], time_file['bloc'], time_file['trial'], time_file['event'])
    ini_data = zip(ini_file['trial'], ini_file['contingency'], ini_file['feature'])
    trials = get_events_per_trial(ini_data, time_data)
    responses = get_responses(time_file)    
    button_proportion = analyse_button(trials, responses, title, inspect)

    features = ini_file['feature']
    trial_intervals = get_trial_intervals(trials, uncategorized=True)  

    gaze_rate_per_trial, gaze_rate_mirror = get_gaze_rate_per_trial(
        trial_intervals,
        all_gaze_data,
        factor=factor,
        inspect=inspect,
        min_block_size=parameters['min_block_size'],
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_remove_outside_session_time=parameters['do_remove_outside_session_time'],
        do_manual_correction=parameters['do_manual_correction'],
        do_confidence_threshold=parameters['confidence_threshold']
        )
    gaze_rate = get_relative_gaze_rate(
        ini_file['feature'],
        gaze_rate_per_trial,
        gaze_rate_mirror)

    # draw.rates([gaze_rate, []],
    #     title= title,
    #     save= not inspect,
    #     y_label='Looking proportion',
    #     single= True,
    #     first_label= 'feature fp',
    #     y_limit= [-0.1, 1.1],
    #     ) 

    draw.rates([button_proportion, gaze_rate],
        title= title,
        save= not inspect,
        y_label='Looking/button-pressing proportion',
        single= False,
        first_label= 'feature looking',
        second_label='button-pressing',
        y_limit= [-0.1, 1.1],
        ) 

    return gaze_rate, button_proportion, latency(trials)

def analyse_experiment(feature_degree, factor):
    positive = []
    negative = []

    positive_button = []
    negative_button = []

    positive_latency = []
    negative_latency = []

    for path in PATHS_DESTIN:
        i = PATHS_DESTIN.index(path)
        if p[i]['excluded']:
            continue

        data_files = get_data_files(path, gaze_file_filter=p[i]['gaze_file_filter'])
        info_file = load_yaml_data(data_files[0])
        if not ((info_file['group'] == 'positive') or (info_file['group'] == 'negative')):
            continue

        if info_file['feature_degree'] == feature_degree:
            looking_rate, button_rate, latencies = analyse(
                i,
                factor,
                inspect=False,
                data_files=data_files)

            if info_file['group'] == 'positive':
                # wrong size
                if '2017_11_13_000_GAB' in info_file['nickname']:
                    positive.append(np.array(looking_rate)[:27])
                    positive_button.append(np.array(button_rate)[:27])
                    positive_latency.append(np.array(latencies)[:27])
                    continue

                positive.append(np.array(looking_rate))
                positive_button.append(np.array(button_rate))
                positive_latency.append(np.array(latencies))

            elif info_file['group'] == 'negative':
                negative.append(np.array(looking_rate))
                negative_button.append(np.array(button_rate))
                negative_latency.append(np.array(latencies))

    positive, negative, positive_error, negative_error = statistics(
        positive,
        negative,
        [str(feature_degree)+'_looking_negative_relative_rate.txt',
         str(feature_degree)+'_looking_positive_relative_rate.txt']
    )
    draw.rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title= ' - '.join(['average looking proportion', 'fp %i°'%feature_degree, str(factor)]),
        save= True,
        y_label='average looking proportion',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=[-0.1, 1.1]
        )


    positive, negative, positive_error, negative_error = statistics(
        positive_button,
        negative_button,
        [str(feature_degree)+'_button_positive_relative_rate.txt',
         str(feature_degree)+'_button_negative_relative_rate.txt']
    )
    draw.rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title=' - '.join(['average button-pressing proportion', 'fp %i°'%feature_degree, str(factor)]),
        save= True,
        y_label='average button-pressing proportion',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=[-0.1, 1.1]
        )

    positive, negative, positive_error, negative_error = statistics(
        positive_latency,
        negative_latency,
        [str(feature_degree)+'_latency_positive_relative_rate.txt',
         str(feature_degree)+'_latency_negative_relative_rate.txt']
    )
    draw.rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title=' - '.join(['average latency', 'fp %i°'%feature_degree, str(factor)]),
        save= True,
        y_label='latency (s)',
        single=False,
        first_label='FP group',
        second_label='FN group'
        )

def analyse_intra_subject(i, factor='donut_slice', inspect=False, data_files=None):
    print('\nRunning analysis for session:')
    print('\t', PATHS_DESTIN[i])
    print('\t', PATHS_SOURCE[i])
    parameters = p[i]
    if not data_files:
        data_files = get_data_files(PATHS_DESTIN[i], gaze_file_filter=p[i]['gaze_file_filter'])
    
    info_file = load_yaml_data(data_files[0])     
    fp_ini_file, fn_ini_file = load_ini_data_intrasubject(data_files[1])
    time_file = load_fpe_timestamps(data_files[2])
    
    responses = get_responses(time_file) 

    title = ' - '.join(['%02d'%i, info_file['nickname'], 'square (FP)', str(factor)])
    time_data = zip(time_file['time'], time_file['bloc'], time_file['trial'], time_file['event'])
    fp_ini_data = zip(fp_ini_file['trial'], fp_ini_file['contingency'], fp_ini_file['feature'])
    fp_trials = get_events_per_trial(fp_ini_data, time_data)
    fp_button_proportion = analyse_button(fp_trials, responses, title)  

    title = ' - '.join(['%02d'%i, info_file['nickname'], 'X (FN)', str(factor)])
    time_data = zip(time_file['time'], time_file['bloc'], time_file['trial'], time_file['event'])
    fn_ini_data = zip(fn_ini_file['trial'], fn_ini_file['contingency'], fn_ini_file['feature'])
    fn_trials = get_events_per_trial(fn_ini_data, time_data)
    fn_button_proportion = analyse_button(fn_trials, responses, title)  

    all_gaze_data = load_gaze_data(data_files[3])
    all_trial_intervals = get_trial_intervals({**fp_trials, **fn_trials}, uncategorized=True)   
    gaze_rate_per_trial, gaze_rate_mirror = get_gaze_rate_per_trial(
        all_trial_intervals,
        all_gaze_data,
        factor=factor,
        inspect=False,
        min_block_size=parameters['min_block_size'],
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_remove_outside_session_time=parameters['do_remove_outside_session_time'],
        do_manual_correction=parameters['do_manual_correction'],
        do_confidence_threshold=parameters['confidence_threshold']
        )
    fp_gaze_rate = get_relative_gaze_rate(
        fp_ini_file['feature'],
        gaze_rate_per_trial[fp_ini_file['trial']],
        gaze_rate_mirror[fp_ini_file['trial']])

    fn_gaze_rate = get_relative_gaze_rate(
        fn_ini_file['feature'],
        gaze_rate_per_trial[fn_ini_file['trial']],
        gaze_rate_mirror[fn_ini_file['trial']])

    title = ' - '.join(['%02d'%i, info_file['nickname'],'square(FP)_X(FN)', str(factor)])
    draw.rates([fp_gaze_rate, fn_gaze_rate], title,
        save=not inspect,
        y_label='Looking proportion at the feature',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=[-0.1, 1.1],
        )
    latencies = (latency(fp_trials), latency(fn_trials))
    button = (fp_button_proportion, fn_button_proportion)
    gaze = (fp_gaze_rate, fn_gaze_rate)
    return button, gaze, latencies

def analyse_experiment_intrasubject(feature_degree=9, factor='donut_slice'):
    positive_gaze = []
    negative_gaze = []

    positive_button = []
    negative_button = []

    positive_latency = []
    negative_latency = []

    for path in PATHS_DESTIN:
        i = PATHS_DESTIN.index(path)
        if p[i]['excluded']:
            continue

        data_files = get_data_files(path, gaze_file_filter=p[i]['gaze_file_filter'])
        info_file = load_yaml_data(data_files[0])
        if not info_file['group'] == 'fp-square/fn-x':
            continue
            
        if info_file['feature_degree'] == feature_degree:
            button_rate, looking_rate, latencies = analyse_intra_subject(
                i,
                factor,
                inspect=False,
                data_files=data_files)

            (fp_button, fn_button) = button_rate
            (fp_gaze, fn_gaze) = looking_rate
            (fp_latency, fn_latency) = latencies
            positive_button.append(np.array(fp_button))
            negative_button.append(np.array(fn_button))

            positive_gaze.append(np.array(fp_gaze))
            negative_gaze.append(np.array(fn_gaze))

            positive_latency.append(np.array(fp_latency))
            negative_latency.append(np.array(fn_latency))

    positive, negative, positive_error, negative_error = statistics(
        positive_button,
        negative_button,
        [str(feature_degree)+'_intra_button_positive_relative_rate.txt',
         str(feature_degree)+'_intra_button_negative_relative_rate.txt']
    )
    draw.rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title=' - '.join(['average button-pressing proportion', 'intra-subject', 'fp %i°'%feature_degree, str(factor)]),
        save= True,
        y_label='average button-pressing proportion',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=[-0.1, 1.1]
        )


    positive, negative, positive_error, negative_error = statistics(
        positive_gaze,
        negative_gaze,
        [str(feature_degree)+'_intra_gaze_positive_relative_rate.txt',
         str(feature_degree)+'_intra_gaze_negative_relative_rate.txt']
    )
    draw.rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title=' - '.join(['average looking proportion', 'intra-subject', 'fp %i°'%feature_degree, str(factor)]),
        save= True,
        y_label='average looking proportion',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=[-0.1, 1.1]
        )

    positive, negative, positive_error, negative_error = statistics(
        positive_latency,
        negative_latency,
        [str(feature_degree)+'_intra_latency_positive_relative_rate.txt',
         str(feature_degree)+'_intra_latency_negative_relative_rate.txt']
    )
    draw.rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title=' - '.join(['average latency', 'intra-subject', 'fp %i°'%feature_degree, str(factor)]),
        save= True,
        y_label='average latency',
        single=False,
        first_label='FP group',
        second_label='FN group'
        )


def analyse_excluded(feature_degree):
    positive = []
    negative = []

    positive_button = []
    negative_button = []

    positive_latency = []
    negative_latency = []

    for path in PATHS_DESTIN:
        i = PATHS_DESTIN.index(path)
        if not p[i]['excluded']:
            continue

        data_files = get_data_files(path, gaze_file_filter=p[i]['gaze_file_filter'])
        info_file = load_yaml_data(data_files[0])
        if not ((info_file['group'] == 'positive') or (info_file['group'] == 'negative')):
            continue

        if info_file['feature_degree'] == feature_degree:
            looking_rate, button_rate, latencies = analyse(
                i,
                inspect=False,
                data_files=data_files)

            if info_file['group'] == 'positive':
                positive.append(np.array(looking_rate))
                positive_button.append(np.array(button_rate))
                positive_latency.append(np.array(latencies))

            elif info_file['group'] == 'negative':
                negative.append(np.array(looking_rate))
                negative_button.append(np.array(button_rate))
                negative_latency.append(np.array(latencies))

if __name__ == '__main__':
    factors = ['donut_slice', 1, 2, 3, 4]
    for factor in factors:
        # analyse_experiment(feature_degree=9, factor=factor)
        # analyse_experiment(feature_degree=90, factor=factor)
        analyse_experiment_intrasubject(feature_degree=9, factor=factor)

    # analyse_excluded(9)
    # analyse(13)
    # analyse_intra_subject(8)    