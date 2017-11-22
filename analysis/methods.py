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
    data = []
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
           
        if Config.get(section, 'Contingency') == target:
            for n in range(1, 10):
                option = 'c'+str(n)+'gap'
                if Config.get(section, option) == '1':
                    data.append(n)

        elif Config.get(section, 'Contingency') == non_target:
            data.append(None)

    return data

def load_gaze_data(path, delimiter="\t"):
    if not os.path.isfile(path):
        print(path)
        raise IOError(path+": was not found.")

    return np.genfromtxt(path, delimiter=delimiter,missing_values=["NA"],
        filling_values=None,names=True, autostrip=True, dtype=None)

def load_fpe_data(path, skip_header):
    """
    
    Columns v1:
        Bloc__Id
        Bloc_Nam
        Trial_No
        Trial_Id
        TrialNam
        ITIBegin
        __ITIEnd
        StmBegin
        _Latency
        __StmEnd
        RespFreq
        ExpcResp
        __Result

    Columns v2:
        BlocoID
        BlocoNome
        TentativaContador
        TentativaID
        TentativaNome
        IETInicio
        IETFim
        CResultado
        SInicio
        RLatencia
        SFim
        RFrequencia
        RPrevista    
    """
    if not os.path.isfile(path):
        print(path)
        raise "Path was not found:"

    data = np.genfromtxt(path,
        delimiter="\t",
        missing_values=["NA"],
        skip_header=skip_header,
        skip_footer=1,
        filling_values=None,
        names=True,
        autostrip=True,
        dtype=None
    )
    return data

def load_fpe_timestamps(path):
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

    data = np.genfromtxt(path,
        delimiter="\t",
        missing_values=["NA"],
        skip_header=5,
        skip_footer=1,
        filling_values=None,
        names=True,
        autostrip=True,
        dtype=None
    )
    return data

def remove_outside_screen(data, xmax=1, ymax=1, horizontal=True):
    if horizontal:
        x = (0 <= data[0, :]) & (data[0, :] < xmax)
        y = (0 <= data[1, :]) & (data[1, :] < ymax)
        mask = x & y
        data_clamped = data[:, mask]
        deleted_count = data.shape[1] - data_clamped.shape[1]
    else:
        x = (0 <= data[:, 0]) & (data[:, 0] < xmax)
        y = (0 <= data[:, 1]) & (data[:, 1] < ymax)
        mask = x & y
        data_clamped = data[mask, :]
        deleted_count = data.shape[0] - data_clamped.shape[0]

    if deleted_count > 0:
        print("\nRemoved", deleted_count, "data point(s) with out-of-screen coordinates!")
    return data_clamped, mask

def window(seq, n=2):
    """
    https://docs.python.org/release/2.3.5/lib/itertools-example.html
     "Returns a sliding window (of width n) over data from the iterable"
     "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result    
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def get_perfomance(data):
    return [line.decode("utf-8") for line in data['__Result']]

def get_session_type(data, version='v1'):    
    if version == 'v1':
        bloc_name = data['Bloc_Nam'][0].decode("utf-8")
    elif version == 'v2':
        bloc_name = data['BlocoNome'][0].decode("utf-8")

    for fp_string in fp_strings:
        if bloc_name in fp_string:
            return 'feature positive'

    for fn_string in fn_strings:
        if bloc_name in fn_string:
            return 'feature negative'

    return None

def plot_fpfn(fp_paths, fn_paths):
    pass

def consecutive_hits(paths, skip_header=13):
    overall_performance = []
    count = 0
    for path in paths:
        count += 1
        data = load_fpe_data(path, skip_header)
        session_type = get_session_type(data)
        trials = data['Trial_Id'].max()
        performance = get_perfomance(data) 
        hits = performance.count('HIT') 

        print('Session %s'%count)
        print('Session Type: %s'%session_type)
        print('Trials:',trials)
        print('Hits:',hits, '(%s %%)'%round((hits/trials)*100,2),'\n')
        overall_performance += performance


    # consecutive hits
    size = 12
    count = 0
    for performance_chunk in window(overall_performance,size):
        count += 1
        if performance_chunk.count('HIT') == size:
            print('The participant reached %s consecutive hits in trial %s.'%(size,count+size-1),'\n')
            return

    print('The participant DO NOT reached %s consecutive hits in %s trials.'%(size,count+size-1),'\n')
 
def get_events_per_trial_in_bloc(data, ts, feat, target_bloc=2, version='v1'):
    # print(ts.dtype.names)
    # print(data.dtype.names)
    if version == 'v1':
        session = zip(ts['Time'], ts['Bloc__Id'], ts['Trial_No'], ts['Event'])
    elif version == 'v2':
        session = zip(ts['Tempo'], ts['BlocoID'], ts['TentativaContador'], ts['Evento'])

    events_per_trial = {} 
    for time, bloc_id, trial, ev in session:
        event = ev.decode("utf-8")
        if bloc_id == target_bloc:
            if trial not in events_per_trial:
                events_per_trial[trial] = {'Type':'','Feature':'','Time':[],'Event':[]}
            
            if event == 'ITI R': # fix for ITI trial number
                events_per_trial[trial-1]['Time'].append(time)    
                events_per_trial[trial-1]['Event'].append(event)
            else:
                events_per_trial[trial]['Time'].append(time)    
                events_per_trial[trial]['Event'].append(event)


    if version == 'v1':
        session = zip(data['TrialNam'], data['Trial_No'], feat)
    elif version == 'v2':
        session = zip(data['TentativaNome'], data['TentativaContador'], feat)

    type1 = 'Positiva'
    type2 = 'Negativa'
    for trial_name, trial_number, feature in session:
        name = trial_name.decode('utf-8')
        events_per_trial[trial_number]['Feature'] = feature
        if type1 in name: 
            events_per_trial[trial_number]['Type'] = type1

        if type2 in name:
            events_per_trial[trial_number]['Type'] = type2

    return events_per_trial

def get_trial_intervals(trials, uncategorized=False):
    starts = []
    ends = []
    for i, trial in trials.items():
        for time, event in zip(trial['Time'], trial['Event']):
            if event == 'TS':
                starts.append({'Time':time, 'Type':trial['Type']})

            if event == 'TE':
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

def get_all_responses(ts, version='v1'):
    if version == 'v1':
        session = zip(ts['Time'], ts['Event'])

    if version == 'v2':
        session = zip(ts['Tempo'], ts['Evento'])

    return [time for time, event in session  \
        if event.decode('utf-8') == 'R' or 'ITI R']

def get_responses(ts, version='v1'):
    if version == 'v1':
        session = zip(ts['Time'], ts['Event'])

    if version == 'v2':
        session = zip(ts['Tempo'], ts['Evento'])

    return [time for time, event in session \
        if event.decode('utf-8') == 'R']    

def is_inside(timestamps,rangein, rangeout):
    return [t for t in timestamps if (t >= rangein) and (t <= rangeout)]

def rate_in(time_interval_pairwise,timestamps):
    return [len(is_inside(timestamps, begin, end))/(end-begin) for begin, end in time_interval_pairwise]

def get_relative_rate(data1, data2):
    return [a/(b+a) if b+a > 0 else np.nan for a, b in zip(data1, data2)]

# def get_trial_starts(trials):
#     starts = []
#     for i, trial in trials.items():
#         for time, event in zip(trial['Time'], trial['Event']):
#             if event == 'TS':
#                 starts.append({'Time':time, 'Type':trial['Type']})

#     last_type = list(trials.values())[-1]['Type']
#     last_time = starts[-1]['Time']

#     l = [end['Time'] - start['Time'] for start, end in zip(starts, starts[1:])] 
#     last_time += np.mean(l) 
    
#     starts.append({'Time':last_time, 'Type':last_type})
#     return starts

# def get_start_end_intervals_with_iti(starts):
#     positive_intervals = []
#     negative_intervals = []
#     for start, end in zip(starts, starts[1:]):
#         if start['Type'] == 'Positiva':
#             positive_intervals.append([start['Time'], end['Time']])

#         if start['Type'] == 'Negativa':
#             negative_intervals.append([start['Time'], end['Time']])
        
#     return positive_intervals, negative_intervals

# def rate(paths, skip_header=13):
#     overall_performance = []
#     count = 0
#     for path in paths:
#         data_file = load_fpe_data(path[0],skip_header)
#         timestamps_file = load_fpe_timestamps(path[1])
#         responses = get_all_responses(timestamps_file)
#         trials = get_events_per_trial_in_bloc(data_file,timestamps_file)
#         starts = get_trial_starts(trials)
#         positive_intervals, negative_intervals = get_start_end_intervals_with_iti(starts)  
#         positive_data = rate_in(positive_intervals,responses)
#         negative_data = rate_in(negative_intervals,responses)
#         relative_rate = get_relative_rate(positive_data, negative_data)
#         title = path[0].replace('/home/pupil/recordings/DATA/','')
#         title = title.replace('/stimulus_control/000.data','')
#         title = title.replace('/','_')
#         title = title+'_'+get_session_type(data_file)
#         title = title.replace(' ', '_')
#         draw_relative_rate(relative_rate,title, False)

def rates(paths, skip_header=13, version='v1'):
    for path in paths:
        title = path[0].replace('/home/pupil/recordings/DATA/','')
        title = title.replace('/stimulus_control/000.data','')
        title = title.replace('/','_')
        title = title+'_'+get_session_type(data_file, version)
        title = title.replace(' ', '_')
        rate(path, skip_header, version, title)

def rate(data_file, timestamps, features, version, title='', save=False, inspect=False):
    trials = get_events_per_trial_in_bloc(data_file, timestamps, features,
        target_bloc=2, version=version)
    positive_intervals, negative_intervals = get_trial_intervals(trials)  

    responses = get_responses(timestamps, version=version)
    positive_data = rate_in(positive_intervals, responses)
    negative_data = rate_in(negative_intervals, responses)

    relative_rate = get_relative_rate(positive_data, negative_data)

    if inspect:
        draw_absolute_rate([positive_data, negative_data],title, save, version)        
        draw_relative_rate(relative_rate,title, save, version)

    return relative_rate
    
def get_paths(paths):
    p = []
    for root in paths['root']:
        s = []
        for path in paths['file']:
            s.append(os.path.join(root, path))
        p.append(s)
    return p

def get_source_files(src_directory, gaze_file_filter='*surface_3d_pr*'):
    target_filters = ['*.yml', '*.txt', '*.data', '*.timestamps', gaze_file_filter]
    glob_lists = [glob(os.path.join(src_directory, tf)) for tf in target_filters]
    return [sorted(glob_list)[0] for glob_list in glob_lists]

def positive_negative_groups():
    pass

if __name__ == '__main__':
    pass
