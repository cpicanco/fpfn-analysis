# -*- coding: utf-8 -*-
'''
    Copyright (C) 2017 Rafael Picanço.

    The present file is distributed under the terms of the GNU General Public License (GPL v3.0).

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import sys
sys.path.append('../../analysis')
sys.path.append('../../file_handling')

from data_organizer import PATHS_DESTIN, PATHS_SOURCE, PARAMETERS
from methods import load_yaml_data, load_ini_data, trial_mask
from methods import load_fpe_timestamps, load_gaze_data, load_ini_data_intrasubject
from methods import get_data_files, statistics
from methods import get_events_per_trial, get_trial_intervals
from correction.utils import clean_gaze_data

from categorization.stimuli import SCREEN_WIDTH_PX as sw
from categorization.stimuli import SCREEN_HEIGHT_PX as sh
from categorization.stimuli import SCREEN_DISTANCE_CM as sd_cm
from categorization.stimuli import SCREEN_WIDTH_CM as sw_cm

from drawing import colormaps, draw

import numpy as np
import cv2

def invert_y(gaze_points):
    return gaze_points['x_norm'], 1-gaze_points['y_norm']   

def custom_heatmap(data, heatmap_detail=0.06, colormap=colormaps.viridis):
    """
    adapted from pupil-labs
    """
    grid = [sh, sw]
    # grid = [1075, 1792]
    xvals, yvals = invert_y(data)
    hist, *edges = np.histogram2d(
        yvals, xvals,
        bins= grid,
        range= [[-0.2, 1.20], [-0.2, 1.20]],
        normed= False)
    filter_h = int(heatmap_detail * grid[0]) // 2 * 2 + 1
    filter_w = int(heatmap_detail * grid[1]) // 2 * 2 + 1
    hist = cv2.GaussianBlur(hist, (filter_h, filter_w), 10)

    hist_max = hist.max()
    hist *= (255. / hist_max) if hist_max else 0.
    hist = hist.astype(np.uint8)

    v = np.asarray(colormap)
    v *= 255
    v = v.astype(np.uint8)

    heatmap = np.zeros((grid[0], grid[1],4), np.uint8)
    heatmap[:,:,2] = cv2.LUT(hist, v[:,2]) # R matplotlib, 0 B opencv
    heatmap[:,:,1] = cv2.LUT(hist, v[:,1]) # G matplotlib, 1 G opencv
    heatmap[:,:,0] = cv2.LUT(hist, v[:,0]) # B matplotlib, 2 R opencv
    hist[hist>0] = 150
    heatmap[:,:,3] = hist # alpha
    return heatmap

def denormalize(gaze_points):
    gaze_points['x_norm'] *= sw
    gaze_points['y_norm'] = 1 - gaze_points['y_norm']
    gaze_points['y_norm'] *= sh
    return gaze_points

def cm_to_degree(sw, sh):
    V = 2 * np.arctan(sw_cm/(sd_cm*2))
    degrees = np.degrees(V)
    return degrees, (sh*degrees)/sw

def pixels_per_degree():
    sw_d, sh_d = cm_to_degree(sw, sh)
    return np.sqrt((sw**2)+(sh**2))/np.sqrt((sw_d**2)+(sh_d**2))

PIXELS_PER_DEGREE = pixels_per_degree()

def pixel_to_degree(gaze_points):
    gaze_points['x_norm'] /= PIXELS_PER_DEGREE
    gaze_points['y_norm'] /= PIXELS_PER_DEGREE
    return gaze_points

def move_mean_to_zero(gaze_points):
    MX = np.mean(gaze_points['x_norm'])
    MY = np.mean(gaze_points['y_norm'])
    gaze_points['x_norm'] = MX - gaze_points['x_norm']
    gaze_points['y_norm'] = MY - gaze_points['y_norm']
    return gaze_points

def convert_gaze(gaze_points):
    return pixel_to_degree(denormalize(move_mean_to_zero(gaze_points)))

def dispersion(all_gaze_data, trial_intervals, title):
    gaze_data = convert_gaze(np.copy(all_gaze_data))
    dispersion_per_trial = []  
    for begin, end in trial_intervals:
        mask = trial_mask(gaze_data['time'], begin, end)

        # we convert mean=0 so that RMS is equal to std
        data = gaze_data[mask] 
        data = np.array([data['x_norm'], data['y_norm']])
        dispersion_per_trial.append(np.std(data, ddof=1, dtype=np.float64))
    return dispersion_per_trial

def analyse(i, inspect=False, data_files=None):
    parameters = PARAMETERS[i]
    print('\nRunning analysis for session:')
    print('\t', PATHS_DESTIN[i])
    print('\t', PATHS_SOURCE[i])
    if not data_files:
        data_files = get_data_files(PATHS_DESTIN[i],
            gaze_file_filter=parameters['gaze_file_filter'])
          
    info_file = load_yaml_data(data_files[0])
    ini_file = load_ini_data(data_files[1])
    time_file = load_fpe_timestamps(data_files[2])
    all_gaze_data = load_gaze_data(data_files[3])

    title = ' - '.join((str(i), str(info_file['feature_degree']), info_file['nickname'], info_file['group']))

    time_data = zip(time_file['time'], time_file['bloc'], time_file['trial'], time_file['event'])
    ini_data = zip(ini_file['trial'], ini_file['contingency'], ini_file['feature'])
    trials = get_events_per_trial(ini_data, time_data)
    positive_intervals, negative_intervals = get_trial_intervals(trials)
    # trial_intervals = get_trial_intervals(trials, uncategorized=True)  

    titlea = title + '_positive'
    titleb = title + '_negative'

    positive_gaze_data = clean_gaze_data(all_gaze_data, 
        do_remove_outside_session_time=positive_intervals,        
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_manual_correction=parameters['do_manual_correction'],
        do_confidence_threshold=parameters['confidence_threshold'],
        min_block_size=parameters['min_block_size'],
        inspect=False)
    pdispersion = dispersion(positive_gaze_data, positive_intervals, titlea)

    negative_gaze_data = clean_gaze_data(all_gaze_data, 
        do_remove_outside_session_time=negative_intervals,        
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_manual_correction=parameters['do_manual_correction'],
        do_confidence_threshold=parameters['confidence_threshold'],
        min_block_size=parameters['min_block_size'],
        inspect=False)
    ndispersion = dispersion(negative_gaze_data, negative_intervals, titleb)

    draw.rates(
        [pdispersion, ndispersion],
        title= title+'_dispersion',
        save= not inspect,
        y_label='2d dispersion (RMS) in deggres of visual angle',
        single=False,
        first_label='S+',
        second_label='S-',
        y_limit= [1., 10.]       
    )

    # if inspect:
    #     draw.images(
    #         custom_heatmap(positive_gaze_data),
    #         custom_heatmap(negative_gaze_data), (sw, sh))

    return (positive_gaze_data, negative_gaze_data), (pdispersion, ndispersion)

def analyse_intrasubject(i, inspect=False, data_files=None):
    parameters = PARAMETERS[i]
    print('\nRunning analysis for session:')
    print('\t', PATHS_DESTIN[i])
    print('\t', PATHS_SOURCE[i])
    if not data_files:
        data_files = get_data_files(PATHS_DESTIN[i],
            gaze_file_filter=parameters['gaze_file_filter'])
          
    info_file = load_yaml_data(data_files[0])
    fp_ini_file, fn_ini_file = load_ini_data_intrasubject(data_files[1])
    time_file = load_fpe_timestamps(data_files[2])
    all_gaze_data = load_gaze_data(data_files[3])

    time_data = zip(time_file['time'], time_file['bloc'], time_file['trial'], time_file['event'])
    fp_ini_data = zip(fp_ini_file['trial'], fp_ini_file['contingency'], fp_ini_file['feature'])
    fp_trials = get_events_per_trial(fp_ini_data, time_data)
    
    time_data = zip(time_file['time'], time_file['bloc'], time_file['trial'], time_file['event'])
    fn_ini_data = zip(fn_ini_file['trial'], fn_ini_file['contingency'], fn_ini_file['feature'])
    fn_trials = get_events_per_trial(fn_ini_data, time_data)    

    fp_positive_intervals, fp_negative_intervals = get_trial_intervals(fp_trials)
    fn_positive_intervals, fn_negative_intervals = get_trial_intervals(fn_trials)


    title = ' - '.join((str(i), str(info_file['feature_degree']), info_file['nickname'], 'FP'))
    titlea = title + '_fp_positive'
    titleb = title + '_fp_negative'

    title = ' - '.join((str(i), str(info_file['feature_degree']), info_file['nickname'], 'FN'))
    titlec = title + '_fn_positive'
    titled = title + '_fn_negative'

    fp_positive_gaze_data = clean_gaze_data(all_gaze_data, 
        do_remove_outside_session_time=fp_positive_intervals,        
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_manual_correction=parameters['do_manual_correction'],
        do_confidence_threshold=parameters['confidence_threshold'],
        min_block_size=parameters['min_block_size'],
        inspect=False)

    fp_pdispersion = dispersion(fp_positive_gaze_data, fp_positive_intervals, titlea)

    fp_negative_gaze_data = clean_gaze_data(all_gaze_data, 
        do_remove_outside_session_time=fp_negative_intervals,        
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_manual_correction=parameters['do_manual_correction'],
        do_confidence_threshold=parameters['confidence_threshold'],
        min_block_size=parameters['min_block_size'],
        inspect=False)
    fp_ndispersion = dispersion(fp_negative_gaze_data, fp_negative_intervals, titleb)

    fn_positive_gaze_data = clean_gaze_data(all_gaze_data, 
        do_remove_outside_session_time=fn_positive_intervals,        
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_manual_correction=parameters['do_manual_correction'],
        do_confidence_threshold=parameters['confidence_threshold'],
        min_block_size=parameters['min_block_size'],
        inspect=False)
    fn_pdispersion = dispersion(fn_positive_gaze_data, fn_positive_intervals, titlec)

    fn_negative_gaze_data = clean_gaze_data(all_gaze_data, 
        do_remove_outside_session_time=fn_negative_intervals,        
        do_correction=parameters['do_correction'],
        do_remove_outside_screen=parameters['do_remove_outside_screen'],
        do_manual_correction=parameters['do_manual_correction'],
        do_confidence_threshold=parameters['confidence_threshold'],
        min_block_size=parameters['min_block_size'],
        inspect=False)
    fn_ndispersion = dispersion(fn_negative_gaze_data, fn_negative_intervals, titled)

    title = ' - '.join((str(i), str(info_file['feature_degree']), info_file['nickname'], 'distinctive'))
    draw.rates(
        [fp_pdispersion, fn_pdispersion],
        title= title+'_pdispersion',
        save= not inspect,
        y_label='2d dispersion (RMS) in deggres of visual angle',
        single=False,
        first_label='FP Group',
        second_label='FN Group',
        y_limit= [1., 10.]       
    )

    title = ' - '.join((str(i), str(info_file['feature_degree']), info_file['nickname'], 'common'))   
    draw.rates(
        [fp_ndispersion, fn_ndispersion],
        title= title+'_ndispersion',
        save= not inspect,
        y_label='2d dispersion (RMS) in deggres of visual angle',
        single=False,
        first_label='FP Group',
        second_label='FN Group',
        y_limit= [1., 10.]       
    )

    title = ' - '.join(('heat', str(i), str(info_file['feature_degree']), info_file['nickname'], 'distinctive-common'))   
    hm = custom_heatmap(fp_positive_gaze_data)

    # [:,256:1024,:] <- crop horizontally
    imgs = (
        custom_heatmap(fp_positive_gaze_data)[:,256:1024,:],
        custom_heatmap(fn_negative_gaze_data)[:,256:1024,:],
        custom_heatmap(fp_negative_gaze_data)[:,256:1024,:],
        custom_heatmap(fn_positive_gaze_data)[:,256:1024,:]
    ) 
    draw.images_four(
        imgs,
        (sw, sh),
        title=title,
        save= not inspect)

    gaze = (fp_positive_gaze_data, fp_negative_gaze_data, fn_positive_gaze_data, fn_negative_gaze_data)
    disp = (fp_pdispersion, fp_ndispersion, fn_pdispersion, fn_ndispersion)
    return gaze, disp

def analyse_experiment(feature_degree):
    fp_positivex, fp_positivey = [], []
    fp_negativex, fp_negativey = [], []

    fn_positivex, fn_positivey = [], []
    fn_negativex, fn_negativey = [], []

    fp_pdispersion, fp_ndispersion = [], []
    fn_pdispersion, fn_ndispersion = [], []
    for path in PATHS_DESTIN:
        i = PATHS_DESTIN.index(path)
        parameters = PARAMETERS[i]
        if parameters['excluded']:
            continue

        data_files = get_data_files(path,
            gaze_file_filter=parameters['gaze_file_filter'])
        info_file = load_yaml_data(data_files[0])
        if not ((info_file['group'] == 'positive') or (info_file['group'] == 'negative')):
            continue

        if info_file['feature_degree'] == feature_degree:
            gaze, gaze_dispersion = analyse(i, 
                inspect= False,
                data_files= data_files)

            (positive_gaze, negative_gaze) = gaze
            (pdispersion, ndispersion) = gaze_dispersion

            if info_file['group'] == 'positive':
                fp_positivex.append(positive_gaze['x_norm'])
                fp_positivey.append(positive_gaze['y_norm'])

                fp_negativex.append(negative_gaze['x_norm'])
                fp_negativey.append(negative_gaze['y_norm'])
                
                fp_pdispersion.append(pdispersion)
                fp_ndispersion.append(ndispersion)

            elif info_file['group'] == 'negative':
                fn_positivex.append(positive_gaze['x_norm'])
                fn_positivey.append(positive_gaze['y_norm'])

                fn_negativex.append(negative_gaze['x_norm'])
                fn_negativey.append(negative_gaze['y_norm'])

                fn_pdispersion.append(pdispersion)
                fn_ndispersion.append(ndispersion)

    fp_positivex = np.hstack(fp_positivex)
    fp_positivey = np.hstack(fp_positivey)
    fp_negativex = np.hstack(fp_negativex)
    fp_negativey = np.hstack(fp_negativey)

    fn_positivex = np.hstack(fn_positivex)
    fn_positivey = np.hstack(fn_positivey)
    fn_negativex = np.hstack(fn_negativex)
    fn_negativey = np.hstack(fn_negativey)

    dt = {'names':['x_norm', 'y_norm'], 'formats':[np.float64, np.float64]}
    fp_negative = np.zeros(fp_negativex.shape[0], dtype=dt)
    fp_negative['x_norm'] = fp_negativex
    fp_negative['y_norm'] = fp_negativey
    fp_positive = np.zeros(fp_positivex.shape[0], dtype=dt)
    fp_positive['x_norm'] = fp_positivex
    fp_positive['y_norm'] = fp_positivey

    fn_negative = np.zeros(fn_negativex.shape[0], dtype=dt)
    fn_negative['x_norm'] = fn_negativex
    fn_negative['y_norm'] = fn_negativey
    fn_positive = np.zeros(fn_positivex.shape[0], dtype=dt)
    fn_positive['x_norm'] = fn_positivex
    fn_positive['y_norm'] = fn_positivey

    # np.savetxt('positive%i.txt'%feature_degree, positive)
    # np.savetxt('negative%i.txt'%feature_degree, negative)

    d1, d2, e1, e2 = statistics(fp_pdispersion, fp_ndispersion)
    d3, d4, e3, e4 = statistics(fn_pdispersion, fn_ndispersion)

    labels = [
        'average RMS in deggres of visual angle',
        'Trials',
        'FP Group',
        'FN Group',
        'distinctive',
        'common'
    ]
    draw.rates_double(
        (d1, d4, d2, d3),
        (e1, e4, e2, e3),
        title= 'comparing FP and FN looking dispersion - '+str(feature_degree),
        labels= labels
    )
    # draw.images(
    #     custom_heatmap(positive),
    #     custom_heatmap(negative), (sw, sh))        

def analyse_experiment_intrasubject(feature_degree):
    fp_positivex, fp_positivey = [], []
    fp_negativex, fp_negativey = [], []

    fn_positivex, fn_positivey = [], []
    fn_negativex, fn_negativey = [], []

    fp_pdispersion, fp_ndispersion = [], []
    fn_pdispersion, fn_ndispersion = [], []
    for path in PATHS_DESTIN:
        i = PATHS_DESTIN.index(path)
        parameters = PARAMETERS[i]
        if parameters['excluded']:
            continue

        data_files = get_data_files(path,
            gaze_file_filter=parameters['gaze_file_filter'])
        info_file = load_yaml_data(data_files[0])
        if not info_file['group'] == 'fp-square/fn-x':
            continue
            
        if info_file['feature_degree'] == feature_degree:
            gaze, gaze_dispersion = analyse_intrasubject(i, 
                inspect= False,
                data_files= data_files)

            (fp_posgaze, fp_neggaze, fn_posgaze, fn_neggaze) = gaze
            (fp_pdisp, fp_ndisp, fn_pdisp, fn_ndisp) = gaze_dispersion

            fp_positivex.append(fp_posgaze['x_norm'])
            fp_positivey.append(fp_posgaze['y_norm'])

            fp_negativex.append(fp_neggaze['x_norm'])
            fp_negativey.append(fp_neggaze['y_norm'])
            
            fp_pdispersion.append(fp_pdisp)
            fp_ndispersion.append(fp_ndisp)

            fn_positivex.append(fn_posgaze['x_norm'])
            fn_positivey.append(fn_posgaze['y_norm'])

            fn_negativex.append(fn_neggaze['x_norm'])
            fn_negativey.append(fn_neggaze['y_norm'])

            fn_pdispersion.append(fn_pdisp)
            fn_ndispersion.append(fn_ndisp)

    fp_positivex = np.hstack(fp_positivex)
    fp_positivey = np.hstack(fp_positivey)
    fp_negativex = np.hstack(fp_negativex)
    fp_negativey = np.hstack(fp_negativey)

    fn_positivex = np.hstack(fn_positivex)
    fn_positivey = np.hstack(fn_positivey)
    fn_negativex = np.hstack(fn_negativex)
    fn_negativey = np.hstack(fn_negativey)

    dt = {'names':['x_norm', 'y_norm'], 'formats':[np.float64, np.float64]}
    fp_negative = np.zeros(fp_negativex.shape[0], dtype=dt)
    fp_negative['x_norm'] = fp_negativex
    fp_negative['y_norm'] = fp_negativey
    fp_positive = np.zeros(fp_positivex.shape[0], dtype=dt)
    fp_positive['x_norm'] = fp_positivex
    fp_positive['y_norm'] = fp_positivey

    fn_negative = np.zeros(fn_negativex.shape[0], dtype=dt)
    fn_negative['x_norm'] = fn_negativex
    fn_negative['y_norm'] = fn_negativey
    fn_positive = np.zeros(fn_positivex.shape[0], dtype=dt)
    fn_positive['x_norm'] = fn_positivex
    fn_positive['y_norm'] = fn_positivey

    # np.savetxt('positive%i.txt'%feature_degree, positive)
    # np.savetxt('negative%i.txt'%feature_degree, negative)

    d1, d2, e1, e2 = statistics(fp_pdispersion, fp_ndispersion)
    d3, d4, e3, e4 = statistics(fn_pdispersion, fn_ndispersion)

    labels = [
        'average RMS in deggres of visual angle',
        'Trials',
        'FP Group',
        'FN Group',
        'distinctive',
        'common'
    ]
    draw.rates_double(
        (d1, d4, d2, d3),
        (e1, e4, e2, e3),
        title= 'comparing FP and FN looking dispersion - '+str(feature_degree)+'_intra',
        labels= labels
    )

    draw.images(
        custom_heatmap(fp_positive),
        custom_heatmap(fn_negative), (sw, sh),
        title='comparing FP and FN looking dispersion - '+str(feature_degree)+'_intra_distinctive_heatmaps',
        save=True
    )

    draw.images(
        custom_heatmap(fp_negative),
        custom_heatmap(fn_positive), (sw, sh),
        title='comparing FP and FN looking dispersion - '+str(feature_degree)+'_intra_common_heatmaps',
        save=True
        )


if __name__ == '__main__':
    analyse_experiment_intrasubject(9)
    # analyse_experiment(9)

    # positive = np.genfromtxt('positive90.txt',
    #     delimiter=' ',
    #     filling_values=None,
    #     names=True,
    #     dtype=None
    # )
    # negative = np.genfromtxt('negative90.txt',
    #     delimiter=' ',
    #     filling_values=None,
    #     names=True,
    #     dtype=None
    # )

    # draw.images(
    #     custom_heatmap(positive),
    #     custom_heatmap(negative), (sw, sh))        
