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
from pathlib import Path

import numpy as np

from methods import load_fpe_timestamps, load_gaze_data, get_source_files

def copy_file(src, dst):
    base_directory = os.path.dirname(dst)
    if not os.path.exists(base_directory):
        print("Creating directory:", base_directory)
        os.makedirs(base_directory)
    shutil.copyfile(src, dst)

def convert_gaze(src, dst, start_time):
    with open(dst, 'w+') as f:
        f.write("\t".join(('time','x_norm','y_norm','confidence'))+'\n')
        for timestamp, X, Y, confidence in zip(src['gaze_timestamp'], src['x_norm'], src['y_norm'], src['confidence']):
            timestamp -= start_time
            timestamp = '%.6f'%timestamp
            X = '%.3f'%round(X, 3)
            Y = '%.3f'%round(Y, 3)
            f.write("\t".join((timestamp, X, Y, repr(confidence)))+'\n')

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

def organize(src_directory, dst_directory, gaze_file_filter):
    """
    organize does not delete nor overrides any source data
    it will copy and convert data from source
    it will rename at destination
    it DOES overrides any previous copies in destination 
    it must be run after pupil surface data have been exported     
    """
    print('doing:', src_directory)
    # destination
    dst_filenames = ['info.yml',
                     'session_configuration.ini',
                     'session_events.txt',
                     'gaze_coordenates_'+gaze_file_filter.replace('*','')+'.txt']
    dst_files = [os.path.join(dst_directory, f) for f in dst_filenames]

    # source
    src_files = get_source_files(src_directory, gaze_file_filter=gaze_file_filter)

    # loading
    beha_file = load_fpe_timestamps(src_files[2], converted=False)
    gaze_file = load_gaze_data(src_files[3], converted=False)
    start_time = gaze_file['gaze_timestamp'][0]

    # copying
    copy_file(src_files[0], dst_files[0])
    copy_file(src_files[1], dst_files[1])

    #conversion
    convert_beha(beha_file, dst_files[2], start_time=start_time)
    convert_gaze(gaze_file, dst_files[3], start_time=start_time)

    # feedback
    print('done:', src_directory)
    # [print('source:', src) for src in src_files]   
    # [print('destination:', dst) for dst in dst_files]

def get_data_path(raw=False):
    data_path = os.path.dirname(os.path.abspath(__file__))
    if raw:
        return os.path.join(os.path.dirname(data_path), 'RAW_DATA')
    else:
        return os.path.join(os.path.dirname(data_path), 'DATA')


DATA_SKIP_HEADER = [
                    36,
                    24,
                    38,
                    38,
                    27,
                    32,
                    24,
                    19,
                    22,
                    27,
                    31,
                    31,
                    23,
                    21,
                    15,
                    31,
                    26,                    
                    31,
                    26,
                    30,
                    28,
                    22,
                    24,
                    28,
                    37,
                    26,
                    38,
                    30,
                    22,
                    26,
                    37,
                    24,
                    27,
                    40,
                    34,
                    40,
                    34,
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
                'recordings/2017_12_18_001_BRE/stimulus_control/',
                'recordings/2017_12_18_000_MAR/stimulus_control/',
                'recordings/2017_12_15_002_RUB/stimulus_control/',
                'recordings/2017_12_15_001_KAR/stimulus_control/',
                'recordings/2017_12_15_000_RAF/stimulus_control/',
                'recordings/2017_12_14_002_JOS/stimulus_control/',
                'recordings/2017_12_14_001_JUL/stimulus_control/',
                'recordings/2017_12_14_000_TAT/stimulus_control/',
                'recordings/2017_12_13_004_ANT/stimulus_control/',
                'recordings/2017_12_13_003_JOE/stimulus_control/',
                'recordings/2017_12_13_002_FER/stimulus_control/',
                'recordings/2017_12_13_001_LUK/stimulus_control/',
                'recordings/2017_12_13_000_WAN/stimulus_control/',
                'recordings/2017_12_01_001_LEX/stimulus_control/',
                'recordings/2017_12_01_000_LUI/stimulus_control/',
                'recordings/2017_11_29_001_FEL/stimulus_control/',
                'recordings/2017_11_29_000_DAN/stimulus_control/',
                'recordings/2017_11_28_003_GIO/stimulus_control/',
                'recordings/2017_11_28_002_FRA/stimulus_control/',
                'recordings/2017_11_28_001_ELI/stimulus_control/',
                'recordings/2017_11_28_000_SID/stimulus_control/',
                'recordings/2017_11_27_005_ANA/stimulus_control/',
                'recordings/2017_11_27_004_AUR/stimulus_control/',
                'recordings/2017_11_27_003_LUC/stimulus_control/',
                'recordings/2017_11_27_002_JOR/stimulus_control/',
                'recordings/2017_11_27_001_TUL/stimulus_control/',
                'recordings/2017_11_27_000_NAT/stimulus_control/',
                'recordings/2017_11_24_006_VER/stimulus_control/',
                'recordings/2017_11_24_005_THA/stimulus_control/',
                'recordings/2017_11_24_004_EUC/stimulus_control/',
                'recordings/2017_11_24_003_FER/stimulus_control/',
                'recordings/2017_11_24_002_JON/stimulus_control/',
                'recordings/2017_11_24_001_PED/stimulus_control/',
                'recordings/2017_11_24_000_MAN/stimulus_control/',
                'recordings/2017_11_23_006_MAY/stimulus_control/',
                'recordings/2017_11_23_005_RAU/stimulus_control/',
                'recordings/2017_11_23_004_ROM/stimulus_control/',
                'recordings/2017_11_23_003_YUR/stimulus_control/',
                'recordings/2017_11_23_002_EIL/stimulus_control/',
                'recordings/2017_11_23_001_JOS/stimulus_control/',
                'recordings/2017_11_23_000_DEN/stimulus_control/',
                'recordings/2017_11_22_001_TIA/stimulus_control/',
                'recordings/2017_11_22_000_EUL/stimulus_control/',
                'recordings/2017_11_16_003_ALI/stimulus_control/',
                'recordings/2017_11_16_002_LAR/stimulus_control/',
                'recordings/2017_11_16_001_MAT/stimulus_control/',
                'recordings/2017_11_16_000_VIN/stimulus_control/',
                'recordings/2017_11_14_006_ALE/stimulus_control/',
                'recordings/2017_11_14_005_JOA/stimulus_control/',
                'recordings/2017_11_14_004_NEL/stimulus_control/',
                'recordings/2017_11_14_003_LUC/stimulus_control/',
                'recordings/2017_11_14_002_TAT/stimulus_control/',
                'recordings/2017_11_14_001_MAR/stimulus_control/',
                'recordings/2017_11_14_000_SON/stimulus_control/',
                'recordings/2017_11_13_005_KAR/stimulus_control/',
                'recordings/2017_11_13_004_ISA/stimulus_control/',
                'recordings/2017_11_13_003_LIZ/stimulus_control/',
                'recordings/2017_11_13_002_MAX/stimulus_control/',
                'recordings/2017_11_13_001_MAR/stimulus_control/',
                'recordings/2017_11_13_000_GAB/stimulus_control/',
                'recordings/2017_11_09_007_REN/stimulus_control/',
                'recordings/2017_11_09_005_AMA/stimulus_control/',
                'recordings/2017_11_09_004_BEL/stimulus_control/',
                'recordings/2017_11_09_002_EST/stimulus_control/',
                'recordings/2017_11_09_001_KAL/stimulus_control/',
                'recordings/2017_11_09_000_JUL/stimulus_control/',
                'recordings/2017_11_08_003_REU/stimulus_control/',
                'recordings/2017_11_06_000_ROB/stimulus_control/']

PATHS_SOURCE = [os.path.join(str(Path.home()), p) for p in PATHS_SOURCE]

PATHS_DESTIN = [
                'P68',
                'P67',
                'P66',
                'P65',
                'P64',
                'P63',
                'P62',
                'P61',
                'P60',
                'P59',
                'P58',
                'P57',
                'P56',
                'P55',
                'P54',
                'P53',
                'P52',
                'P51',
                'P50',
                'P49',
                'P48',
                'P47',
                'P46',
                'P45',
                'P44',
                'P43',
                'P42',
                'P41',
                'P40',
                'P39',
                'P38',
                'P37',
                'P36',
                'P35',
                'P34',
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

PATHS_DESTIN = [os.path.join(get_data_path(), p) for p in PATHS_DESTIN]


PARAMETERS = [
    # '2017_12_18_001_BRE'
    {'min_block_size': 42778,
     'do_correction': False, # looking a lot at the top
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [-0.015, 0.03],     
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_18_000_MAR'
    {'min_block_size': 42300 // 8,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},


    # '2017_12_15_002_RUB'
    {'min_block_size': 42474 // 8,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1.25, .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_15_001_KAR'
    {'min_block_size': 41950 // 8,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_15_000_RAF'
    {'min_block_size': 41620 // 8,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_14_002_JOS'
    {'min_block_size': 42736 // 8,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold' :.65,
     'excluded':True}, # no conditional disc.

    # '2017_12_14_001_JUL'
    {'min_block_size': 40516 // 4,
     'do_correction': True,
     'do_remove_outside_screen': [0.80, .27, 1.10, .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [0.01, 0.03],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_14_000_TAT'
    {'min_block_size': 41339 // 8,
     'do_correction': True,
     'do_remove_outside_screen': [.83, .26, 1., -.08],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [0.015, 0.06],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_13_004_ANT'
    {'min_block_size': 20000,
     'do_correction': False,
     'do_remove_outside_screen': [.77, .20, 1., .08],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_13_003_JOE'
    {'min_block_size': 40536 // 4,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_13_002_FER'
    {'min_block_size': 42895 // 4,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_13_001_LUK'
    {'min_block_size': 42308 // 8,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_13_000_WAN'
    {'min_block_size': 42413 // 4,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1.20, .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_01_001_LEX'
    {'min_block_size': 20593,
     'do_correction': True,
     'do_remove_outside_screen': [.85, .23, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*', # unstable 3d models
     'do_manual_correction': [0., 0.06],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_12_01_000_LUI'  
    {'min_block_size': 19984,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_29_001_FEL'    
    {'min_block_size': 18842//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_29_000_DAN'
    {'min_block_size': 20468,
     'do_correction': False,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [-0.03, 0.],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_28_003_GIO'
    {'min_block_size': 20228//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0.01, 0.01],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_28_002_FRA'
    {'min_block_size': 20637,
     'do_correction': False,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold' :.65,
     'excluded':True}, # no conditional disc.

    # '2017_11_28_001_ELI'
    {'min_block_size': 20212//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_28_000_SID'
    {'min_block_size': 20546,
     'do_correction': False,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold' :.65,
     'excluded':True}, # no button differetiation

    # '2017_11_27_005_ANA'
    {'min_block_size': 20609,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0., 0.03],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_27_004_AUR'
    {'min_block_size': 20183,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0.005, 0.03],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_27_003_LUC'
    {'min_block_size': 19863//6,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_27_002_JOR'
    {'min_block_size': 20209//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0.02, 0.],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_27_001_TUL'
    {'min_block_size': 20365,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0.02, 0.04],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_27_000_NAT'
    {'min_block_size': 20359//2,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0.03, 0.],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_24_006_VER'
    {'min_block_size': 20000,
     'do_correction': False,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold' :.65,
     'excluded':True}, # bad eyes, looking to a fixed point

    # '2017_11_24_005_THA'
    {'min_block_size': 19119//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_24_004_EUC'
    {'min_block_size':  20644,
     'do_correction': False,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [-0.05, 0.02],
     'confidence_threshold' :.65,
     'excluded':True}, # no button differatiation

    # '2017_11_24_003_FER'
    {'min_block_size': 20300//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0., 0.02],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_24_002_JON'
    {'min_block_size': 20317,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0., 0.03],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_24_001_PED'
    {'min_block_size': 19980//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_24_000_MAN'
    {'min_block_size': 19214//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_23_006_MAY'
    {'min_block_size': 20561//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_23_005_RAU'
    {'min_block_size': 20327//4,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0., 0.01],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_23_004_ROM'
    {'min_block_size': 20416,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_23_003_YUR'
    {'min_block_size': 20571,
     'do_correction': False,
     'do_remove_outside_screen': [.80, .20, 1.03, .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold' :.65,
     'excluded':True}, # no button differentiation

    # '2017_11_23_002_EIL'
    {'min_block_size': 19876,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1.03, .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [-0.01, 0.01],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_23_001_JOS'
    {'min_block_size': 20604,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold' :.65,
     'excluded':True}, # no button differentiation

    # '2017_11_23_000_DEN'
    {'min_block_size': 20310//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1.06, .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0.0, 0.03],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_22_001_TIA'
    {'min_block_size': 20113,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_22_000_EUL'          
    {'min_block_size': 20310//2,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1.20, .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_ba*',
     'do_manual_correction': [0.03, 0.03],
     'confidence_threshold' :.65,
     'excluded':False}, # differentiation at the very end

    # '2017_11_16_003_ALI'
    {'min_block_size': 19631//8,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_ba*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},
    
    # '2017_11_16_002_LAR'
    {'min_block_size': 18869//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0.02, 0.02],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_16_001_MAT'
    {'min_block_size': 19176//8, # bias at the end
     'do_correction': True,           
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_ba*',
     'do_manual_correction': [],
     'confidence_threshold' :.65,
     'excluded':True}, # does not follow instructions

    # '2017_11_16_000_VIN'
    {'min_block_size': 20354//4,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_ba*',
     'do_manual_correction': [0.01, 0.01],
     'confidence_threshold' :.65,
     'excluded':False}, # differentiation at the very end
 
    # '2017_11_14_006_ALE'
    {'min_block_size': 18698,
     'do_correction': False,  
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_ba*',
     'do_manual_correction': [-0.04, -0.09],
     'confidence_threshold' :.65,
     'excluded':False}, # using too much peripheral vision

    # '2017_11_14_005_JOA'
    {'min_block_size': 18608//2,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [], # [-0.04, 0.06],
     'confidence_threshold': .65,
     'excluded':False},
    
    # '2017_11_14_004_NEL'
    {'min_block_size': 20234//4,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0.0, 0.05],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_14_003_LUC'
    {'min_block_size': 17836//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_14_002_TAT'
    {'min_block_size': 20557,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_14_001_MAR'
    {'min_block_size': 20179,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_14_000_SON'
    {'min_block_size': 20130//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [0., 0.05],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_13_005_KAR'  #***********
    {'min_block_size': 19042//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_13_004_ISA'
    {'min_block_size': 20000,
     'do_correction': True,        # <<<<<<<<<<<<<<<<<< complicated eyes
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold' :.65,
     'excluded':True},

    # '2017_11_13_003_LIZ'
    {'min_block_size': 19409//3,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_13_002_MAX'   
    {'min_block_size': 20472,
     'do_correction': False,       
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold' :.65,
     'excluded':False}, # looking first, then button

    # '2017_11_13_001_MAR'
    {'min_block_size': 19067//3, # bias at the end
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_13_000_GAB'
    {'min_block_size': 26905//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold' :.65,
     'excluded':False}, # wrong size, 108 instead 54

    # '2017_11_09_007_REN'
    {'min_block_size': 20217,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_09_005_AMA'
    {'min_block_size': 19738//4,
     'do_correction': True,
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_09_004_BEL'
    {'min_block_size': 10000,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*2d_pr*',
     'do_manual_correction': [],
     'confidence_threshold' :.65,
     'excluded':True}, # no button differentiation # unstable 3d model

    # '2017_11_09_002_EST'       
    {'min_block_size': 19777//6,
     'do_correction': True,              
     'do_remove_outside_screen': [.80, .20, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_09_001_KAL'
    {'min_block_size': 17264,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_09_000_JUL'
    {'min_block_size': 20573,
     'do_correction': False, # looking a lot at the top
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_08_003_REU'
    {'min_block_size': 20312, 
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False},

    # '2017_11_06_000_ROB'
    {'min_block_size': 20068//4,
     'do_correction': True,
     'do_remove_outside_screen': [1., .0, 1., .0],
     'do_remove_outside_session_time': True,
     'gaze_file_filter': '*3d_pr*',
     'do_manual_correction': [],
     'confidence_threshold': .65,
     'excluded':False}
]
if __name__ == '__main__':
    filenames = [
    '2017_12_18_001_BRE','2017_12_18_000_MAR','2017_12_15_002_RUB','2017_12_15_001_KAR',
    '2017_12_15_000_RAF','2017_12_14_002_JOS','2017_12_14_001_JUL','2017_12_14_000_TAT',
    '2017_12_13_004_ANT','2017_12_13_003_JOE','2017_12_13_002_FER','2017_12_13_001_LUK',
    '2017_12_13_000_WAN','2017_12_01_000_LUI','2017_11_29_001_FEL','2017_12_01_001_LEX',
    '2017_11_29_000_DAN','2017_11_28_003_GIO','2017_11_28_002_FRA','2017_11_28_001_ELI',
    '2017_11_28_000_SID','2017_11_27_005_ANA','2017_11_27_004_AUR','2017_11_27_003_LUC',
    '2017_11_27_002_JOR','2017_11_27_001_TUL','2017_11_27_000_NAT','2017_11_24_006_VER',
    '2017_11_24_005_THA','2017_11_24_004_EUC','2017_11_24_003_FER','2017_11_24_002_JON',
    '2017_11_24_001_PED','2017_11_24_000_MAN','2017_11_23_006_MAY','2017_11_23_005_RAU',
    '2017_11_23_004_ROM','2017_11_23_003_YUR','2017_11_23_002_EIL','2017_11_22_001_TIA',
    '2017_11_23_001_JOS','2017_11_23_000_DEN','2017_11_22_000_EUL','2017_11_16_003_ALI',
    '2017_11_16_002_LAR','2017_11_16_001_MAT','2017_11_16_000_VIN','2017_11_14_006_ALE',
    '2017_11_14_005_JOA','2017_11_14_004_NEL','2017_11_14_003_LUC','2017_11_14_002_TAT',
    '2017_11_14_001_MAR','2017_11_14_000_SON','2017_11_13_005_KAR','2017_11_13_004_ISA',
    '2017_11_13_003_LIZ','2017_11_13_002_MAX','2017_11_13_001_MAR','2017_11_13_000_GAB',
    '2017_11_09_007_REN','2017_11_09_005_AMA','2017_11_09_004_BEL','2017_11_09_002_EST',
    '2017_11_09_001_KAL','2017_11_09_000_JUL','2017_11_08_003_REU','2017_11_06_000_ROB']

    def organized(source_path):
        for filename in filenames:
            if filename in source_path:
                return True

    for s, d, p in zip(PATHS_SOURCE, PATHS_DESTIN, PARAMETERS):
        if not organized(s):
            organize(s, d, p['gaze_file_filter'])