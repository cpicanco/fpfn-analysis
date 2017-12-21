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

def organize(src_directory, dst_directory, gaze_file_filter):
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
                     'session_events.txt',
                     'gaze_coordenates_'+gaze_file_filter.replace('*','')+'.txt']
    dst_files = [os.path.join(dst_directory, f) for f in dst_filenames]

    # source
    src_files = get_source_files(src_directory, gaze_file_filter=gaze_file_filter)

    # feedback
    [print('source:', src) for src in src_files]   
    [print('destination:', dst) for dst in dst_files]

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


PARAMETERS = [
    # '2017_12_18_001_BRE'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_18_000_MAR'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},


    # '2017_12_15_002_RUB'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_15_001_KAR'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_15_000_RAF'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_14_002_JOS'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_14_001_JUL'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_14_000_TAT'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_13_004_ANT'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_13_003_JOE'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_13_002_FER'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_13_001_LUK'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_13_000_WAN'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_01_001_LEX'
    {'min_block_size':20593,
     'do_correction': True,
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*2d_pr*',
     'excluded':False},

    # '2017_12_01_000_LUI'  
    {'min_block_size':20636,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_29_001_FEL'    
    {'min_block_size':10597,
     'do_correction': True,
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_29_000_DAN'
    {'min_block_size':20643,
     'do_correction': False,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_28_003_GIO'
    {'min_block_size':20650,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_28_002_FRA'
    {'min_block_size':20637,
     'do_correction': False,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_28_001_ELI'
    {'min_block_size':20654,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_28_000_SID'
    {'min_block_size':20546,
     'do_correction': False,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_27_005_ANA'
    {'min_block_size':20609,
     'do_correction': True,
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_27_004_AUR'
    {'min_block_size':20627,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_27_003_LUC'
    {'min_block_size':20628,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_27_002_JOR'
    {'min_block_size':20623,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_27_001_TUL'
    {'min_block_size':20575,
     'do_correction': False,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_27_000_NAT'
    {'min_block_size':20526,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_24_006_VER'
    {'min_block_size':20000,
     'do_correction': False,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_24_005_THA'
    {'min_block_size':20660,
     'do_correction': False,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_24_004_EUC'
    {'min_block_size': 20644,
     'do_correction': False,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_24_003_FER'
    {'min_block_size':20387,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_24_002_JON'
    {'min_block_size':20545,
     'do_correction': True,
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_24_001_PED'
    {'min_block_size':20664,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_24_000_MAN'
    {'min_block_size':20582,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_23_006_MAY'
    {'min_block_size':20645,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_23_005_RAU'
    {'min_block_size':20656,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_23_004_ROM'
    {'min_block_size':20656,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_23_003_YUR'
    {'min_block_size':20571,
     'do_correction': False,
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_23_002_EIL'
    {'min_block_size':20619,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_23_001_JOS'
    {'min_block_size':20604,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_23_000_DEN'
    {'min_block_size':20567,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_22_001_TIA'
    {'min_block_size':20656,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_22_000_EUL'          # <<<<<<<<<<<<<<<<<< complicated eyes
    {'min_block_size':10000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_16_003_ALI'
    {'min_block_size':20643,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},
    
    # '2017_11_16_002_LAR'
    {'min_block_size':20597,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_16_001_MAT'
    {'min_block_size':5000,
     'do_correction': True,             # <<<<<<<<<<<<<<<<<< complicated eyes
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_16_000_VIN'
    {'min_block_size':2000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_14_006_ALE'
    {'min_block_size':2000,
     'do_correction': True,             # <<<<<<<<<<<<<<<<<< complicated eyes
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_14_005_JOA'
    {'min_block_size':10000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},
    
    # '2017_11_14_004_NEL'
    {'min_block_size':10000,
     'do_correction': True,
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_14_003_LUC'
    {'min_block_size':10000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_14_002_TAT'
    {'min_block_size':10000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_14_001_MAR'
    {'min_block_size':10000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_14_000_SON'
    {'min_block_size':10000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_13_005_KAR'  #***********
    {'min_block_size':20000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_13_004_ISA'
    {'min_block_size':20000,
     'do_correction': True,        # <<<<<<<<<<<<<<<<<< complicated eyes
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_13_003_LIZ'
    {'min_block_size':10000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_13_002_MAX'   
    {'min_block_size':1000,
     'do_correction': True,         # <<<<<<<<<<<<<<<<<< complicated eyes
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_13_001_MAR'
    {'min_block_size':10000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_13_000_GAB'
    {'min_block_size':10000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_09_007_REN'
    {'min_block_size':20000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_09_005_AMA'
    {'min_block_size':20000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_09_004_BEL'
    {'min_block_size':10000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_09_002_EST'       
    {'min_block_size':1000,
     'do_correction': True,              # <<<<<<<<<<<<<<<<<< complicated eyes
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':True},

    # '2017_11_09_001_KAL'
    {'min_block_size':5000,
     'do_correction': True,
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_09_000_JUL'
    {'min_block_size':5000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_08_003_REU'
    {'min_block_size':5000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False},

    # '2017_11_06_000_ROB'
    {'min_block_size':5000,
     'do_correction': True,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*3d_pr*',
     'excluded':False}
]
if __name__ == '__main__':
    src_directories = [os.path.join(str(Path.home()), p) for p in PATHS_SOURCE]
    data_path = get_data_path()
    dst_directories = [os.path.join(data_path, p) for p in PATHS_DESTIN]
    for s, d, p in zip(src_directories, dst_directories, PARAMETERS):
        organize(s, d, p['gaze_file_filter'])