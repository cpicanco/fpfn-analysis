# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import sys
sys.path.append('../analysis')

import os
import shutil

import numpy as np

from methods import load_fpe_timestamps, load_gaze_data, load_ini_data, get_source_files


def copy_file(src, dst):
    base_directory = os.path.dirname(dst)
    if not os.path.exists(base_directory):
        print("Creating directory:", base_directory)
        os.makedirs(base_directory)
    shutil.copyfile(src,dst)

def convert_gaze(src, dst, start_time):
    with open(dst, 'w+') as f:
        f.write("\t".join(('time','x_norm','y_norm'))+'\n')
        for timestamp, X, Y in zip(src['gaze_timestamp'], src['x_norm'], src['y_norm']):
            timestamp -= start_time
            timestamp = '%.6f'%timestamp
            X = '%.3f'%round(X, 3)
            Y = '%.3f'%round(Y, 3)
            f.write("\t".join((timestamp, X, Y))+'\n')

def convert_beha(src, dst, start_time):
    with open(dst, 'w+') as f:
        f.write("\t".join(('time', 'bloc', 'trial', 'event'))+'\n')
        for timestamp, bloc, trial, event in zip(src['Tempo'], src['BlocoID'], src['TentativaContador'], src['Evento']):
            timestamp -= start_time
            timestamp = '%.6f'%timestamp
            bloc = '%s'%bloc
            trial = '%s'%trial

            event_converted = event.decode('utf-8')
            if event_converted == 'C':
                event_converted = 'CONSEQUENCE'

            if event_converted == 'R':
                event_converted = 'RESPONSE'

            if event_converted == 'ITI R':
                event_converted = 'ITI_RESPONSE'

            if event_converted == 'TS':
                event_converted = 'TRIAL_START'

            if event_converted == 'TE':
                event_converted = 'TRIAL_END'

            f.write("\t".join((timestamp, bloc, trial, event_converted))+'\n')

def convert_fpfn(src, dst):
    with open(dst, 'w+') as f:
        f.write('feature_stimulus_per_trial_in_bloc_2\n')
        for stimulus in src:
            if stimulus:
                f.write(str(stimulus) +'\n')
            else:
                f.write('NA' +'\n')

def organize(src_directory, dst_directory):
    """
    organize does not delete nor overrides any source data
    it will copy and convert data from source
    it will rename at destination
    it DOES overrides any previous copies in destination 
    it must be run after pupil surface data have been exported     
    """
    # destination
    dst_filenames = ['info.yml',
                     'session_configuration.ini',
                     'session_features.txt',
                     'session_events.txt',
                     'gaze_coordenates_3d_pr.txt']
    dst_files = [os.path.join(dst_directory, f) for f in dst_filenames]

    # source
    src_files = get_source_files(src_directory, gaze_file_filter='*surface_3d_pr*')
    
    # feedback
    [print('source:', src) for src in src_files]   
    [print('destination:', dst) for dst in dst_files]

    # loading
    fpfn_file = load_ini_data(src_files[1])
    beha_file = load_fpe_timestamps(src_files[3])
    gaze_file = load_gaze_data(src_files[4], delimiter=',')
    start_time = gaze_file['gaze_timestamp'][0]

    # copying

    copy_file(src_files[0], dst_files[0])
    copy_file(src_files[1], dst_files[1])

    #conversion
    convert_fpfn(fpfn_file, dst_files[2])
    convert_beha(beha_file, dst_files[3], start_time=start_time)
    convert_gaze(gaze_file, dst_files[4], start_time=start_time)

def get_data_path(raw=False):
    data_path = os.path.dirname(os.path.abspath(__file__))
    if raw:
        return os.path.join(os.path.dirname(data_path), 'RAW_DATA')
    else:
        return os.path.join(os.path.dirname(data_path), 'DATA')


DATA_SKIP_HEADER = [34,
                    44,
                    43,
                    35,
                    28,
                    36,
                    39,
                    32,
                    34,
                    38,
                    29,
                    31,
                    42,
                    44,
                    27,
                    32,
                    38,
                    33,
                    41,
                    44,
                    35,
                    40,
                    35,
                    38,
                    44,
                    35,
                    32,
                    35,
                    41,
                    43,
                    39,
                    38,
                    41,
                    12]

PATHS_SOURCE = [
                '/home/pupil/recordings/2017_11_23_006_MAY/stimulus_control/',
                '/home/pupil/recordings/2017_11_23_005_RAU/stimulus_control/',
                '/home/pupil/recordings/2017_11_23_004_ROM/stimulus_control/',
                '/home/pupil/recordings/2017_11_23_003_YUR/stimulus_control/',
                '/home/pupil/recordings/2017_11_23_002_EIL/stimulus_control/',
                '/home/pupil/recordings/2017_11_23_001_JOS/stimulus_control/',
                '/home/pupil/recordings/2017_11_23_000_DEN/stimulus_control/',
                '/home/pupil/recordings/2017_11_22_001_TIA/stimulus_control/',
                '/home/pupil/recordings/2017_11_22_000_EUL/stimulus_control/',
                '/home/pupil/recordings/2017_11_16_003_ALI/stimulus_control/',
                '/home/pupil/recordings/2017_11_16_002_LAR/stimulus_control/',
                '/home/pupil/recordings/2017_11_16_001_MAT/stimulus_control/',
                '/home/pupil/recordings/2017_11_16_000_VIN/stimulus_control/',
                '/home/pupil/recordings/2017_11_14_006_ALE/stimulus_control/',
                '/home/pupil/recordings/2017_11_14_005_JOA/stimulus_control/',
                '/home/pupil/recordings/2017_11_14_004_NEL/stimulus_control/',
                '/home/pupil/recordings/2017_11_14_003_LUC/stimulus_control/',
                '/home/pupil/recordings/2017_11_14_002_TAT/stimulus_control/',
                '/home/pupil/recordings/2017_11_14_001_MAR/stimulus_control/',
                '/home/pupil/recordings/2017_11_14_000_SON/stimulus_control/',
                '/home/pupil/recordings/2017_11_13_005_KAR/stimulus_control/',
                '/home/pupil/recordings/2017_11_13_004_ISA/stimulus_control/',
                '/home/pupil/recordings/2017_11_13_003_LIZ/stimulus_control/',
                '/home/pupil/recordings/2017_11_13_002_MAX/stimulus_control/',
                '/home/pupil/recordings/2017_11_13_001_MAR/stimulus_control/',
                '/home/pupil/recordings/2017_11_13_000_GAB/stimulus_control/',
                '/home/pupil/recordings/2017_11_09_007_REN/stimulus_control/',
                '/home/pupil/recordings/2017_11_09_005_AMA/stimulus_control/',
                '/home/pupil/recordings/2017_11_09_004_BEL/stimulus_control/',
                '/home/pupil/recordings/2017_11_09_002_EST/stimulus_control/',
                '/home/pupil/recordings/2017_11_09_001_KAL/stimulus_control/',
                '/home/pupil/recordings/2017_11_09_000_JUL/stimulus_control/',
                '/home/pupil/recordings/2017_11_08_003_REU/stimulus_control/',
                '/home/pupil/recordings/2017_11_06_000_ROB/stimulus_control/']

PATHS_DESTIN = [ 'P34',
                 'P33',
                 'P32',
                 'P31',
                 'P30',
                 'P29',
                 'P28',
                 'P27',
                 'P26',   
                 'P25',
                 'P24',
                 'P23',   
                 'P22',
                 'P21',
                 'P20',
                 'P19',
                 'P18',
                 'P17',
                 'P16',
                 'P15',
                 'P14',
                 'P13',
                 'P12',
                 'P11',
                 'P10',
                 'P09',
                 'P08',
                 'P07',
                 'P06',
                 'P05',
                 'P04',
                 'P03',
                 'P02',
                 'P01']

if __name__ == '__main__':
    data_path = get_data_path()
    source_directories = [p for p in PATHS_SOURCE]
    destinat_directory = [os.path.join(data_path, p) for p in PATHS_DESTIN]
    for s, d in zip(source_directories, destinat_directory):
        if 'P29' or 'P30' or 'P31' or 'P32' or 'P33' or 'P34' in d:
            organize(s, d)