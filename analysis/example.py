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

def analyse(i):
    print('Running analysis for session:', PATHS_SOURCE[i])
    source_files = get_source_files(PATHS_SOURCE[i], gaze_file_filter='*surface_3d*')
    info = load_yaml_data(source_files[0])
    features = load_ini_data(source_files[1])
    data_file = load_fpe_data(source_files[2], skip_header=DATA_SKIP_HEADER[i])
    timestamps = load_fpe_timestamps(source_files[3])
    all_gaze_data = load_gaze_data(source_files[4], delimiter=',')
    title = str(i)+' - '+info['nickname']+'-'+info['group']
    # rate(data_file, timestamps, features, version, title=title)

    # 2017_11_16_003_ALI
    # gaze_rate(data_file, timestamps, features, all_gaze_data,
    #     title=title,
    #     version=version,
    #     factor=1.95,
    #     min_block_size=20000,
    #     do_remove_outside_screen=False,
    #     do_remove_outside_session_time=True,
    #     inspect=True)

    gaze_rate(data_file, timestamps, features, all_gaze_data,
        title=title,
        version=version,
        factor=1.95,
        min_block_size=20000,
        do_remove_outside_screen=False,
        do_remove_outside_session_time=True,
        inspect=True)


analyse(1)
# for i, _ in enumerate(PATHS_SOURCE):
#     analyse(i)    