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
        'cache_dir': 'H:/Workspace/VSCode/Python/entan_oem_mod/data/sys_00/0.0_1000.0_10001',
        'range_min': 9999,
        'range_max': 10001,
        't_min': 0,
        't_max': 1000,
        't_dim': 10001
    },
    'system': {
        'Delta_0': 1.0,
        'Es': [25.0, 2.5], 
        'gammas': [0.005, 0.005],
        'gs': [0.005, 0.005],
        'kappa': 0.15,
        'n_ths': [0, 0],
        'Omegas': [2.0, 1.0],
        'omegas': [1.0, 1.0],
        'Vs': [10.0, 1.0]
    },
    'plotter': {
        'type': 'contourf',
        'palette': 'RdBu',
        'bins': 11,
        'x_label': '$g_{0}$',
        'x_bound': 'both',
        'x_ticks': [0.000, 0.001, 0.002, 0.003, 0.004, 0.005],
        'y_label': '$g_{1}$',
        'y_bound': 'both',
        'y_ticks': [0.000, 0.001, 0.002, 0.003, 0.004, 0.005],
        'show_cbar': True,
        'cbar_position': 'top',
        'cbar_title': '$Counts$',
        'cbar_ticks': [0.0, 0.5, 1.0]
    }
}

# initialize log
init_log()

# initialize system
system = Mod00(params['system'])

# function to calculate Routh-Hurwitz criteria
def func_stability(system_params, val, logger, results):
    # update parameters
    system.params = system_params
    # get RHC counts
    Counts, _ = system.get_rhc_count_dynamics(params['solver'], system.ode_func, system.get_ivc, system.get_A)
    # check for stability
    stable = 1
    if np.mean(Counts) != 0.0:
        stable = 0
    # update results
    results.append((val, stable))

# looper
looper = XYLooper(func_stability, params)
looper.loop(plot=True)