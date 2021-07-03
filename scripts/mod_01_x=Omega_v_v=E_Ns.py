# dependencies
import os 
import sys

# qom modules
from qom.utils import wrap_looper
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'entan_oem_mod')))
# import system
from systems.Mod01 import Mod01

# all parameters
params = {
    'looper': {
        'show_progress': True,
        'mode': 'multithread',
        'X': {
            'var': 'Omegas',
            'idx': 1,
            'min': 1.8,
            'max': 2.2,
            'dim': 41
        }
    },
    'solver': {
        'show_progress': True,
        'cache': True,
        'cache_dir': 'H:/Workspace/VSCode/Python/entan_oem_mod/data/mod_01/0.0_1000.0_10001',
        'method': 'ode',
        'measure_type': 'qcm',
        'qcm_type': 'entan',
        'idx_mode_i': 1,
        'idx_mode_j': 2,
        'range_min': 9371,
        'range_max': 10001,
        't_min': 0,
        't_max': 1000,
        't_dim': 10001
    },
    'system': {
        'A_ls': [1e2, 0.0],
        'A_vs': [0.0, 1e4], 
        'Delta_0': 1.0,
        'gammas': [1e-3, 1e-2],
        'gs': [1e-3, 1e-6],
        'kappa': 0.1,
        'n_ths': [0, 0],
        'Omegas': [0.0, 0.0],
        'omegas': [1.0, 1.0],
        'thetas': [0.0, 0.0],
        't_mod': 'cos',
        't_pos': 'top'
    },
    'plotter': {
        'type': 'lines',
        'show_legend': True,
        'palette': 'Reds',
        'bins': 3,
        'title': '$A_{l} = 10^{2}, A_{v} = 10^{4} \\cos ( \\Omega_{v} t )$',
        'x_label': '$\\Omega_{v} / \\omega_{0}$',
        'x_bound': 'both',
        'x_ticks': [1.8, 1.9, 2.0, 2.1, 2.2],
        'y_legend': ['$\\theta_{0} = 0.0, \\theta_{1} = 0.0$', '$\\theta_{0} = - 0.5, \\theta_{1} = 2.0$'],
        'v_label': '$\\bar{E}_{N_{EM}}$',
        'v_bound': 'both',
        'v_ticks': [0.00, 0.05, 0.10, 0.15, 0.20]
    }
}

# get average entanglement
params['solver']['idx_mode_i'] = 1
params['solver']['idx_mode_j'] = 2
looper = wrap_looper(Mod01, params, 'measure_average', 'XLooper')
print(looper.get_thresholds(thres_mode='minmax'))
X = looper.results['X']
M_0 = looper.results['V']

# get average entanglement
params['system']['thetas'][0] = - 0.5
params['system']['thetas'][1] = 2.0
params['solver']['idx_mode_i'] = 1
params['solver']['idx_mode_j'] = 2
looper = wrap_looper(Mod01, params, 'measure_average', 'XLooper')
print(looper.get_thresholds(thres_mode='minmax'))
M_1 = looper.results['V']

# plotter
axes = {
    'X': X,
    'Y': {
        'var': 'E_N',
        'val': [0, 1]
    }
}
plotter = MPLPlotter(axes, params['plotter'])
plotter.update(xs=[X, X], vs=[M_0, M_1])
plotter.show(True, width=6.0)