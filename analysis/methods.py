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

from drawing import draw

import numpy as np

fp_strings = ['FP', 'Feature Positive']
fn_strings = ['FN', 'Feature Negative']

type1 = 'Positiva'
type2 = 'Negativa'
center1 = 'O'
center2 = 'X'

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
                target = type1
                non_target = type2

        for fn_string in fn_strings:
            if bloc_name in fn_string:
                target = type2
                non_target = type1

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

def load_ini_data_intrasubject(path):
    def get_feature_number(reference, target, ini_section):
        if reference == target:
            for n in range(1, 10):
                option = 'c'+str(n)+'gap'
                if Config.get(ini_section, option) == '1':
                    return n
        
    from configparser import ConfigParser
    Config = ConfigParser()
    Config.read(path)
    fp_indexes = []
    fn_indexes = []
    fp_features = []
    fn_features = []
    fp_contingencies = []
    fn_contingencies = []
    for section in Config.sections():
        if not 'T' in section:
            continue

        if not 'Blc 2' in section:
            continue
            
        bloc_name = Config.get('Blc 2', 'Name')
        if bloc_name == 'FPO':
            fp_center = center1
            fn_center = center2

        elif bloc_name == 'FPX':
            fp_center = center2
            fn_center = center1

        fp_target = type1+' '+fp_center
        fp_non_target = type2+' '+fp_center

        fn_target = type2+' '+fn_center
        fn_non_target = type1+' '+fn_center

        trial_name = Config.get(section, 'Name')
        if (trial_name == fp_target) or (trial_name == fp_non_target):
            fp_contingencies.append(Config.get(section, 'Contingency'))
            fp_features.append(get_feature_number(trial_name, fp_target, section))
            fp_indexes.append(int(section.replace('Blc 2 - T', ''))-1)

        if (trial_name == fn_target) or (trial_name == fn_non_target):
            fn_contingencies.append(Config.get(section, 'Contingency'))
            fn_features.append(get_feature_number(trial_name, fn_target, section))
            fn_indexes.append(int(section.replace('Blc 2 - T', ''))-1)

    fp = {'trial':fp_indexes, 'contingency':fp_contingencies, 'feature':fp_features}
    fn = {'trial':fn_indexes, 'contingency':fn_contingencies, 'feature':fn_features}

    return fp, fn


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

def variance(x, y, dependent=False):
    if dependent:
        return np.var(x, ddof=1), np.var(y, ddof=1)
    
    vx = np.var(x, ddof=1)
    vy = np.var(y, ddof=1)
    mux = np.mean(x)*np.mean(x)
    muy = np.mean(y)*np.mean(y)
    return (vx*vy)+(vx*muy)+(vy*mux)

def get_events_per_trial(ini_data, time_data):
    events_per_trial = {}
    first = True
    for time, bloc_id, trial, ev in time_data:
        trial_n = trial
        if bloc_id == 2:
            if first:
                first = False
                offset = 0
                if trial_n > 1:
                    offset = trial_n
            trial_n = trial_n - offset

            if trial_n not in events_per_trial:
                events_per_trial[trial_n] = {'Type':'','Feature':'','Time':[],'Event':[]}

            events_per_trial[trial_n]['Time'].append(time)    
            events_per_trial[trial_n]['Event'].append(ev.decode("utf-8"))

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
        if start['Type'] == type1:
            positive_intervals.append([start['Time'], end['Time']])

        if start['Type'] == type2:
            negative_intervals.append([start['Time'], end['Time']])
    return positive_intervals, negative_intervals

def get_responses(ts):
    return [time for time, event in zip(ts['time'], ts['event']) \
        if event.decode('utf-8') == 'RESPONSE']    

def is_inside(timestamps,rangein, rangeout):
    return [t for t in timestamps if (t >= rangein) and (t <= rangeout)]

def rate_in(time_interval_pairwise,timestamps):
    return [len(is_inside(timestamps, begin, end))/(end-begin) for begin, end in time_interval_pairwise]

def trial_mask(target_timestamps, begin, end):
    return (target_timestamps >= begin) & (target_timestamps <= end)

def get_relative_rate(data1, data2):
    return [a/(b+a) if b+a > 0 else 0.5 for a, b in zip(data1, data2)]

def rate(positive_intervals, negative_intervals, responses, title='', save=False, inspect=False):
    positive_data = rate_in(positive_intervals, responses)
    negative_data = rate_in(negative_intervals, responses)
    relative_rate = get_relative_rate(positive_data, negative_data)
    if inspect:
        draw.rates([positive_data, negative_data], title, save, y_label = 'Button-pressing per seconds')        
        draw.relative_rate(relative_rate,title, save, y_label = 'Button-pressing proportion')

    return relative_rate
    
def latency(trials):
    def get_time(timestamped_events):
        d = [] 
        for time, event in timestamped_events:
            if event == 'TRIAL_START':
                d.append(time)
                continue

            if event == 'RESPONSE':
                d.append(time)
                return d[1]-d[0]
        return np.nan
    data = []
    for i, trial in trials.items():
        if trial['Type'] == type1:
            data.append(get_time(zip(trial['Time'], trial['Event'])))

    return data

def get_source_files(src_directory, gaze_file_filter='*surface_3d_pr*'):
    target_filters = ['*.yml', '*.txt', '*.timestamps', gaze_file_filter]
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
