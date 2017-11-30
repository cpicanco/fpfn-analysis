# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import sys, os
from glob import glob
from itertools import islice

import numpy as np

from drawing import draw_rates, draw_relative_rate
    
fp_strings = ['FP', 'Feature Positive']
fn_strings = ['FN', 'Feature Negative']

def load_yaml_data(path):
    import yaml
    with open(path, 'r') as stream:
        return yaml.load(stream)

def load_ini_data(path='../data/positive_01.txt'):
    from configparser import ConfigParser
    Config = ConfigParser()
    Config.read(path)
    features = []
    contingencies = []
    for section in Config.sections():
        if not 'T' in section:
            continue

        if not 'Blc 2' in section:
            continue
            
        bloc_name = Config.get('Blc 2', 'Name')
        for fp_string in fp_strings:
            if bloc_name in fp_string:
                target = 'Positiva'
                non_target = 'Negativa'

        for fn_string in fn_strings:
            if bloc_name in fn_string:
                target = 'Negativa'
                non_target = 'Positiva'

        contingency = Config.get(section, 'Contingency')  
        contingencies.append(contingency) 

        if contingency == target:
            for n in range(1, 10):
                option = 'c'+str(n)+'gap'
                if Config.get(section, option) == '1':
                    features.append(n)

        elif contingency == non_target:
            features.append(None)

    return {'trial':range(len(features)), 'contingency':contingencies, 'feature':features}

def load_gaze_data(path, converted=True):
    if not os.path.isfile(path):
        print(path)
        raise IOError(path+": was not found.")

    if converted:
        delimiter = '\t'
    else:
        delimiter = ','

    data = np.genfromtxt(path,
        delimiter=delimiter,
        missing_values=["NA"],
        filling_values=None,
        names=True,
        autostrip=True,
        dtype=None
    )

    return data

def load_fpe_timestamps(path, converted=True):
    """
    Columns v1:
        Time
        Bloc__Id
        Trial_Id
        Trial_No
        Event


    Columns v2:
        Tempo
        BlocoID
        TentativaID
        TentativaContador
        Evento

    """
    if not os.path.isfile(path):
        raise "Path was not found:"+path

    if converted:
        skip_header = 0
        skip_footer = 0
    else:
        skip_header = 5
        skip_footer = 1

    data = np.genfromtxt(path,
        delimiter="\t",
        missing_values=["NA"],
        skip_header=skip_header,
        skip_footer=skip_footer,
        filling_values=None,
        names=True,
        autostrip=True,
        dtype=None
    )
    return data

def remove_outside_screen(data, xmax=1, ymax=1, xmin=0, ymin=0, horizontal=True):
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

def get_events_per_trial(ini_data, time_data):
    events_per_trial = {}
    first = True
    for time, bloc_id, trial, ev in time_data:
        if bloc_id == 2:
            if first:
                first = False
                offset = 0
                if trial > 1:
                    offset = trial
            trial = trial - offset

            if trial not in events_per_trial:
                events_per_trial[trial] = {'Type':'','Feature':'','Time':[],'Event':[]}
            events_per_trial[trial]['Time'].append(time)    
            events_per_trial[trial]['Event'].append(ev.decode("utf-8"))

    type1 = 'Positiva'
    type2 = 'Negativa'
    for i, contingency, feature in ini_data:
        events_per_trial[i]['Feature'] = feature
        if type1 in contingency: 
            events_per_trial[i]['Type'] = type1

        if type2 in contingency:
            events_per_trial[i]['Type'] = type2

    return events_per_trial

def get_trial_intervals(trials, uncategorized=False):
    starts = []
    ends = []
    for i, trial in trials.items():
        for time, event in zip(trial['Time'], trial['Event']):
            if event == 'TRIAL_START':
                starts.append({'Time':time, 'Type':trial['Type']})

            if event == 'TRIAL_END':
                ends.append({'Time':time, 'Type':trial['Type']})

    if uncategorized:
        return [[start['Time'], end['Time']] for start, end in zip(starts, ends)]

    positive_intervals = []
    negative_intervals = []
    for start, end in zip(starts, ends):
        if start['Type'] == 'Positiva':
            positive_intervals.append([start['Time'], end['Time']])

        if start['Type'] == 'Negativa':
            negative_intervals.append([start['Time'], end['Time']])
    return positive_intervals, negative_intervals

def get_responses(ts):
    return [time for time, event in zip(ts['time'], ts['event']) \
        if event.decode('utf-8') == 'RESPONSE']    

def is_inside(timestamps,rangein, rangeout):
    return [t for t in timestamps if (t >= rangein) and (t <= rangeout)]

def rate_in(time_interval_pairwise,timestamps):
    return [len(is_inside(timestamps, begin, end))/(end-begin) for begin, end in time_interval_pairwise]

def get_relative_rate(data1, data2):
    return [a/(b+a) if b+a > 0 else np.nan for a, b in zip(data1, data2)]

def rate(ini_file, ts_file, title='', save=False, inspect=False):
    time_data = zip(ts_file['time'], ts_file['bloc'], ts_file['trial'], ts_file['event'])
    ini_data = zip(ini_file['trial'], ini_file['contingency'], ini_file['feature'])
    trials = get_events_per_trial(ini_data, time_data)
    positive_intervals, negative_intervals = get_trial_intervals(trials)  

    responses = get_responses(ts_file)
    positive_data = rate_in(positive_intervals, responses)
    negative_data = rate_in(negative_intervals, responses)

    relative_rate = get_relative_rate(positive_data, negative_data)

    if inspect:
        draw_rates([positive_data, negative_data], title, save, y_label = 'Button-pressing per seconds')        
        draw_relative_rate(relative_rate,title, save, y_label = 'Button-pressing proportion')

    return relative_rate
    
def get_source_files(src_directory, gaze_file_filter='*surface_3d_pr*'):
    target_filters = ['*.yml', '*.txt', '*.data', '*.timestamps', gaze_file_filter]
    glob_lists = [glob(os.path.join(src_directory, tf)) for tf in target_filters]
    return [sorted(glob_list)[0] for glob_list in glob_lists]

def get_data_files(src_directory, gaze_file_filter='gaze_coordenates_3d_pr.txt'):
    target_filters = ['info.yml',
                      'session_configuration.ini',
                      'session_events.txt',
                      gaze_file_filter
                      ]
    glob_lists = [glob(os.path.join(src_directory, tf)) for tf in target_filters]
    return [sorted(glob_list)[0] for glob_list in glob_lists]    


if __name__ == '__main__':
    pass
