# dependencies
import numpy as np
import os 
import sys

# qom modules
from qom.loopers import XYLooper
from qom.ui import init_log

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'entan_oem_mod')))
# import system
from systems.NJP00 import NJP00

# all parameters
params = {
    'looper': {
        'X': {
            'var': 'Delta_norm',
            'min': 0.4,
            'max': 1.6,
            'dim': 121
        },
        'Y': {
            'var': 'omega_LC_norm',
            'min': 0.4,
            'max': 1.6,
            'dim': 121
        }
    },
    'solver': {
        'measure_type': 'qcm',
        'qcm_type': 'entan',
        'idx_mode_i': 1,
        'idx_mode_j': 2,
    },
    'system': {
        'Delta_norm': 1.0,
        'Delta_type': 'absolute',
        'G_norm': 5, 
        'g_norm': 5, 
        'gamma_LC_norm': 1e-5,
        'gamma_m_norm': 1e-6,
        'kappa_norm': 0.1,
        'omega_LC_norm': 1.0,
        'omega_m': 2 * np.pi * 1e6,
        'T_LC': 1e-2,
        'T_m': 1e-2
    },
    'plotter': {
        'type': 'contourf',
        'palette': 'Greens',
        'bins': 11,
        'x_label': '$\\Delta / \\omega_{m}$',
        'x_bound': 'both',
        'x_ticks': [0.4, 1.0, 1.6],
        'y_label': '$\\omega_{LC} / \\omega_{m}$',
        'y_bound': 'both',
        'y_ticks': [0.4, 1.0, 1.6],
        'cbar_position': 'top',
        'cbar_ticks': [0, 0.1, 0.2]
    }
}

# initialize log
init_log()

# initialize system
system = NJP00(params['system'])

# function to calculate entanglement
def func_measure(system_params, val, logger, results):
    # update parameters
    system.params = system_params
    # get modes and correlations
    modes, corrs = system.get_modes_corrs_stationary(None, system.get_ivc, system.get_A)
    # get measure
    measure = system.get_measure_stationary(params['solver'], modes, corrs)
    # update results
    results.append((val, measure))
    
# looper
looper = XYLooper(func_measure, params)
looper.loop(plot=True)