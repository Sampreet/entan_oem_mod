# dependencies
import os 
import sys

# qom modules
from qom.utils import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'entan_oem_mod')))
# import system
from systems.Mod00 import Mod00

# all parameters
params = {
    'looper': {
        'X': {
            'var': 'gs',
            'idx': 0,
            'min': 0.000,
            'max': 0.005,
            'dim': 51
        },
        'Y': {
            'var': 'gs',
            'idx': 1,
            'min': 0.000,
            'max': 0.005,
            'dim': 51
        }
    },
    'solver': {
        'cache': True,
        'cache_dir': 'H:/Workspace/data/mod_00/0.0_1000.0_10001',
        'method': 'zvode',
        'measure_type': 'entan_ln',
        'idx_e': (1, 2),
        'range_min': 9371,
        'range_max': 10001,
        't_min': 0,
        't_max': 1000,
        't_dim': 10001
    },
    'system': {
        'A_ls': [50, 0.0],
        'A_vs': [1e2, 0.0], 
        'Delta_0': 1.0,
        'gammas': [5e-3, 5e-2],
        'gs': [5e-3, 5e-4],
        'kappa': 0.15,
        'n_ths': [0, 0],
        'Omegas': [2.0, 2.0],
        'omegas': [1.0, 1.0],
        't_mods': ['cos', 'cos'],
        't_pos': 'bottom'
    },
    'plotter': {
        'type': 'contourf',
        'palette': 'Blues',
        'bins': 11,
        'x_label': '$g_{0}$',
        'x_bound': 'both',
        'x_ticks': [0.000, 0.001, 0.002, 0.003, 0.004, 0.005],
        'y_label': '$g_{1}$',
        'y_bound': 'both',
        'y_ticks': [0.000, 0.001, 0.002, 0.003, 0.004, 0.005],
        'show_cbar': True,
        'cbar_position': 'top',
        'cbar_title': '$E_{N}$',
        'cbar_ticks': [0.0, 0.05, 0.1, 0.15, 0.2]
    }
}

# looper
looper = wrap_looper(system=Mod00, params=params, func='ams', looper='xy_looper', file_path='data/mod_00/entan_ln', plot=True)
# calculate thresholds
print(looper.get_thresholds(thres_mode='minmax'))