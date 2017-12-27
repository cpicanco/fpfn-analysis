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

from methods import latency, get_trial_intervals, get_responses
from methods import rate, get_source_files, get_data_files, get_events_per_trial
from methods import load_ini_data_intrasubject, load_ini_data, load_fpe_timestamps
from methods import load_yaml_data, load_gaze_data
from categorization import get_gaze_rate_per_trial, get_relative_gaze_rate
from data_organizer import PATHS_SOURCE, PATHS_DESTIN, DATA_SKIP_HEADER, get_data_path
from data_organizer import PARAMETERS as p
from drawing import draw_rates, draw_points

def analyse(i, parameters, source_files, inspect=False, info_file=None):
    print('\nRunning analysis for session:', PATHS_SOURCE[i])
    if not info_file:
        info_file = load_yaml_data(source_files[0])
    ini_file = load_ini_data(source_files[1])
    time_file = load_fpe_timestamps(source_files[2])
    all_gaze_data = load_gaze_data(source_files[3])
    title = str(i)+' - '+info_file['nickname']+'-'+info_file['group']

    time_data = zip(time_file['time'], time_file['bloc'], time_file['trial'], time_file['event'])
    ini_data = zip(ini_file['trial'], ini_file['contingency'], ini_file['feature'])
    trials = get_events_per_trial(ini_data, time_data)

    positive_intervals, negative_intervals = get_trial_intervals(trials)
    responses = get_responses(time_file)    
    button_rate = rate(positive_intervals, negative_intervals, responses,
        title=title,
        save=False,
        inspect=False)

    features = ini_file['feature']
    trial_intervals = get_trial_intervals(trials, uncategorized=True)  

    factor = 'donut_slice'
    gaze_rate_per_trial, gaze_rate_mirror = get_gaze_rate_per_trial(
        trial_intervals,
        all_gaze_data,
        factor=factor,
        inspect=inspect,
        min_block_size=parameters['min_block_size'],
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_remove_outside_session_time=parameters['do_remove_outside_session_time'],
        do_manual_correction=parameters['do_manual_correction']
        )
    gaze_rate = get_relative_gaze_rate(
        ini_file['feature'],
        gaze_rate_per_trial,
        gaze_rate_mirror)

    if False:
        draw_rates([gaze_rate, []], title,
            save=False,
            y_label='Looking rate',
            single=True,
            first_label='feature fp',
            y_limit=True,
            )

    latencies = latency(trials)
    return gaze_rate, button_rate, latencies

def statistics(positive, negative, export=None):
    positive = np.vstack(positive)
    negative = np.vstack(negative)
    
    print('positive', len(positive))
    print('negative', len(negative))
    
    if export:
        np.savetxt(export[0], positive)
        np.savetxt(export[1], negative)
    
    positive_std = np.array([np.nanstd(positive[:,i]) for i in range(positive.shape[1])])
    # positive_min = np.array([np.nanmin(positive[:,i]) for i in range(positive.shape[1])])
    # positive_max = np.array([np.nanmax(positive[:,i]) for i in range(positive.shape[1])])
    positive = np.array([np.nanmean(positive[:,i]) for i in range(positive.shape[1])])

    negative_std = np.array([np.nanstd(negative[:,i]) for i in range(negative.shape[1])])
    # negative_min = np.array([np.nanmin(negative[:,i]) for i in range(negative.shape[1])])
    # negative_max = np.array([np.nanmax(negative[:,i]) for i in range(negative.shape[1])])
    negative = np.array([np.nanmean(negative[:,i]) for i in range(negative.shape[1])])

    # positive_error = [positive-positive_min, positive_max-positive]
    # negative_error = [negative-negative_min, negative_max-negative]
    return positive, negative, positive_std, negative_std

def analyse_experiment(feature_degree):
    positive = []
    negative = []

    positive_button = []
    negative_button = []

    positive_latency = []
    negative_latency = []

    data_paths = get_data_path()
    data_paths = [os.path.join(data_paths, p) for p in PATHS_DESTIN]
    for path in data_paths:
        i = data_paths.index(path)
        if p[i]['excluded']:
            continue

        source_files = get_data_files(data_paths[i], gaze_file_filter=p[i]['gaze_file_filter'])
        info_file = load_yaml_data(source_files[0])
        if not ((info_file['group'] == 'positive') or (info_file['group'] == 'negative')):
            continue

        if info_file['feature_degree'] == feature_degree:
            looking_rate, button_rate, latencies = analyse(
                i, p[i], source_files,
                inspect=False,
                info_file=info_file)

            if info_file['group'] == 'positive':
                positive.append(np.array(looking_rate))
                positive_button.append(np.array(button_rate))
                positive_latency.append(np.array(latencies))

            elif info_file['group'] == 'negative':
                negative.append(np.array(looking_rate))
                negative_button.append(np.array(button_rate))
                negative_latency.append(np.array(latencies))

    positive, negative, positive_error, negative_error = statistics(
        positive,
        negative
        # ['_looking_negative_relative_rate.txt', '_looking_positive_relative_rate.txt']
    )
    draw_rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title='mean looking proportion per trial with distinctive S '+str(feature_degree),
        save= True,
        y_label='Mean looking proportion',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=True
        )


    positive, negative, positive_error, negative_error = statistics(
        positive_button,
        negative_button
        # ['_button_positive_relative_rate.txt', '_button_negative_relative_rate.txt']
    )
    draw_rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title='mean button-pressing proportion along trials '+str(feature_degree),
        save= True,
        y_label='mean button-pressing proportion',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=True
        )

    positive, negative, positive_error, negative_error = statistics(
        positive_latency,
        negative_latency
        # ['_latency_positive_relative_rate.txt', '_latency_negative_relative_rate.txt']
    )
    draw_rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title='mean latency along trials '+str(feature_degree),
        save= True,
        y_label='latency (s)',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=False
        )

def analyse_intra_subject(i, parameters, source_files, inspect, info_file=None):
    print('\nRunning analysis for session:', PATHS_SOURCE[i])
    if not info_file:
        info_file = load_yaml_data(source_files[0]) 
        
    fp_ini_file, fn_ini_file = load_ini_data_intrasubject(source_files[1])
    time_file = load_fpe_timestamps(source_files[2])
    time_data = zip(time_file['time'], time_file['bloc'], time_file['trial'], time_file['event'])

    responses = get_responses(time_file) 
    title = str(i)+' - '+info_file['nickname']+' - '+ 'square (FP)'

    fp_ini_data = zip(fp_ini_file['trial'], fp_ini_file['contingency'], fp_ini_file['feature'])
    fp_trials = get_events_per_trial(fp_ini_data, time_data)
    fp_positive_intervals, fp_negative_intervals = get_trial_intervals(fp_trials)
    fp_button_rate = rate(fp_positive_intervals, fp_negative_intervals, responses,
        title=title,
        save=False,
        inspect=False)

    title = str(i)+' - '+info_file['nickname']+' - '+ 'X (FN)'
    time_data = zip(time_file['time'], time_file['bloc'], time_file['trial'], time_file['event'])
    fn_ini_data = zip(fn_ini_file['trial'], fn_ini_file['contingency'], fn_ini_file['feature'])
    fn_trials = get_events_per_trial(fn_ini_data, time_data)
    fn_positive_intervals, fn_negative_intervals = get_trial_intervals(fn_trials)
    fn_button_rate = rate(fn_positive_intervals, fn_negative_intervals, responses,
        title=title,
        save=False,
        inspect=False)

    factor = 'donut_slice'
    all_gaze_data = load_gaze_data(source_files[3])
    all_trial_intervals = get_trial_intervals({**fp_trials, **fn_trials}, uncategorized=True)   
    gaze_rate_per_trial, gaze_rate_mirror = get_gaze_rate_per_trial(
        all_trial_intervals,
        all_gaze_data,
        factor=factor,
        inspect=inspect,
        min_block_size=parameters['min_block_size'],
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_remove_outside_session_time=parameters['do_remove_outside_session_time'],
        do_manual_correction=parameters['do_manual_correction']
        )
    fp_gaze_rate = get_relative_gaze_rate(
        fp_ini_file['feature'],
        gaze_rate_per_trial[fp_ini_file['trial']],
        gaze_rate_mirror[fp_ini_file['trial']])

    fn_gaze_rate = get_relative_gaze_rate(
        fn_ini_file['feature'],
        gaze_rate_per_trial[fn_ini_file['trial']],
        gaze_rate_mirror[fn_ini_file['trial']])

    if inspect:
        title = str(i)+'_'+info_file['nickname']+'_'+ 'square(FP)_X(FN)'+'_factor_'+str(factor)
        draw_rates([fp_gaze_rate, fn_gaze_rate], title,
            save=True,
            y_label='Looking rate',
            single=False,
            first_label='feature fp',
            second_label='feature fn',
            y_limit=True,
            )

    return (fp_button_rate, fn_button_rate), (fp_gaze_rate, fn_gaze_rate), (None, None)

def analyse_experiment_intrasubject(feature_degree=9):
    positive_gaze = []
    negative_gaze = []

    positive_button = []
    negative_button = []

    positive_latency = []
    negative_latency = []

    data_paths = get_data_path()
    data_paths = [os.path.join(data_paths, p) for p in PATHS_DESTIN]
    for path in data_paths:
        i = data_paths.index(path)
        if p[i]['excluded']:
            continue

        source_files = get_data_files(data_paths[i], gaze_file_filter=p[i]['gaze_file_filter'])
        info_file = load_yaml_data(source_files[0])
        if not info_file['group'] == 'fp-square/fn-x':
            continue
            
        if info_file['feature_degree'] == feature_degree:
            button_rate, looking_rate, latencies = analyse_intra_subject(
                i, p[i], source_files,
                inspect=False,
                info_file=info_file)

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
    draw_rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title='button-pressing proportion along trials - intra-subject - '+str(feature_degree),
        save= True,
        y_label='average button-pressing proportion',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=True
        )

    positive, negative, positive_error, negative_error = statistics(
        positive_gaze,
        negative_gaze,
        [str(feature_degree)+'_intra_gaze_positive_relative_rate.txt',
         str(feature_degree)+'_intra_gaze_negative_relative_rate.txt']
    )
    draw_rates(
        data=[positive, negative],
        error=[positive_error, negative_error],
        title='feature (%i degrees) looking proportion - intra-subject'%feature_degree,
        save= True,
        y_label='average looking proportion',
        single=False,
        first_label='FP group',
        second_label='FN group',
        y_limit=True
        )

    # positive, negative, positive_error, negative_error = statistics(
    #     positive_latency,
    #     negative_latency,
    #     [str(feature_degree)+'_intra_latency_positive_relative_rate.txt',
    #      str(feature_degree)+'_intra_latency_negative_relative_rate.txt']
    # )
    # draw_rates(
    #     data=[positive, negative],
    #     error=[positive_error, negative_error],
    #     title='average feature latency along trials - intra-subject',
    #     save= True,
    #     y_label='average latency',
    #     single=False,
    #     first_label='FP group',
    #     second_label='FN group',
    #     y_limit=True
    #     )

if __name__ == '__main__':
    # analyse_experiment(feature_degree=9)
    # analyse_experiment(feature_degree=90)
    analyse_experiment_intrasubject(feature_degree=9)

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

    # single
    # for i in range(13):
    #     source_files = get_data_files(PATHS_DESTIN[i],gaze_file_filter=p[i]['gaze_file_filter'])
    #     analyse_intra_subject(i, p[i], source_files, inspect=True)         

    # i = -29
    
    # i = -69
    # source_files = get_data_files(PATHS_DESTIN[i], gaze_file_filter=p[i]['gaze_file_filter'])
    # analyse(i, p[i], source_files, inspect=True)