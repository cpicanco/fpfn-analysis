# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import sys, yaml
sys.path.append('../file_handling')
sys.path.append('categorization')

from methods import rate, get_source_files
from methods import load_ini_data, load_fpe_data, load_fpe_timestamps
from methods import load_yaml_data, load_gaze_data
from categorization import gaze_rate
from data_organizer import PATHS_SOURCE, DATA_SKIP_HEADER

version = 'v2'

p = [

    # '2017_11_16_003_ALI'
    {'min_block_size':20000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},
    
    # '2017_11_16_002_LAR'
    {'min_block_size':20000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},

    # '2017_11_16_001_MAT'
    {'min_block_size':5000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},

    # '2017_11_16_000_VIN'
    {'min_block_size':1000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},

    # '2017_11_14_006_ALE'
    {'min_block_size':2000,             # <<<<<<<<<<<<<<<<<< complicated eyes
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_2d*',
     'excluded':True},

    # '2017_11_14_005_JOA'
    {'min_block_size':5000,
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_2d*',
     'excluded':False},
    
    # '2017_11_14_004_NEL'
    {'min_block_size':10000,
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},

    # '2017_11_14_003_LUC'
    {'min_block_size':10000,
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_2d*',
     'excluded':False},

    # '2017_11_14_002_TAT'
    {'min_block_size':20000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},

    # '2017_11_14_001_MAR'
    {'min_block_size':20000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},

    # '2017_11_14_000_SON'
    {'min_block_size':20000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},

    # '2017_11_13_005_KAR'
    {'min_block_size':10000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_2d*',
     'excluded':False},

    # '2017_11_13_004_ISA'
    {'min_block_size':20000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_2d*',
     'excluded':False},

    # '2017_11_13_003_LIZ'
    {'min_block_size':10000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_2d*',
     'excluded':False},

    # '2017_11_13_002_MAX'
    {'min_block_size':10000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_2d*',
     'excluded':False},

    # '2017_11_13_001_MAR'
    {'min_block_size':20000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_2d*',
     'excluded':False},

    # '2017_11_13_000_GAB'
    {'min_block_size':10000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_2d*',
     'excluded':False},

    # '2017_11_09_007_REN'
    {'min_block_size':20000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},

    # '2017_11_09_005_AMA'
    {'min_block_size':20000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},

    # '2017_11_09_004_BEL'
    {'min_block_size':10000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':True},

    # '2017_11_09_002_EST'       
    {'min_block_size':1000,              # <<<<<<<<<<<<<<<<<< complicated eyes
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':True},

    # '2017_11_09_001_KAL'
    {'min_block_size':5000,
     'do_remove_outside_screen':True,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},

    # '2017_11_09_000_JUL'
    {'min_block_size':5000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False},

    # '2017_11_08_003_REU'
    {'min_block_size':5000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_2d*',
     'excluded':False},

    # '2017_11_06_000_ROB'
    {'min_block_size':5000,
     'do_remove_outside_screen':False,
     'do_remove_outside_session_time':True,
     'gaze_file_filter':'*surface_3d*',
     'excluded':False}
]

def analyse(i, parameters):
    print('Running analysis for session:', PATHS_SOURCE[i])
    source_files = get_source_files(PATHS_SOURCE[i], gaze_file_filter=parameters['gaze_file_filter'])
    info = load_yaml_data(source_files[0])
    features = load_ini_data(source_files[1])
    data_file = load_fpe_data(source_files[2], skip_header=DATA_SKIP_HEADER[i])
    timestamps = load_fpe_timestamps(source_files[3])
    all_gaze_data = load_gaze_data(source_files[4], delimiter=',')
    title = str(i)+' - '+info['nickname']+'-'+info['group']
    # rate(data_file, timestamps, features, version, title=title, save=False)

    gaze_rate(data_file, timestamps, features, all_gaze_data,
        title=title,
        version=version,
        factor=1.95,
        min_block_size=parameters['min_block_size'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_remove_outside_session_time=parameters['do_remove_outside_session_time'],
        inspect=False,
        save=True
)


# i = 24
# analyse(i, p[i])

for path in PATHS_SOURCE:
    i = PATHS_SOURCE.index(path)

    if not p[i]['excluded']:
        analyse(i, p[i])