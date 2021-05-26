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
        'show_progress': True,
        'X': {
            'var': 'Omegas',
            'idx': 1,
            'min': 1.0,
            'max': 2.0,
            'dim': 51
        }
    },
    'solver': {
        'cache': True,
        'cache_dir': 'H:/Workspace/VSCode/Python/entan_oem_mod/data/mod_00/0.0_1000.0_10001',
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
        'Delta_0': 1.0,
        'Es': [25.0, 2.5], 
        'gammas': [0.005, 0.005],
        'gs': [0.005, 0.005],
        'kappa': 0.15,
        'n_ths': [0, 0],
        'Omegas': [1.16, 1.0],
        'omegas': [1.0, 1.0],
        'Vs': [10.0, 1.0]
    },
    'plotter': {
        'type': 'line',
        'x_label': '$\\Omega_{V} / \\omega_{0}$',
        'x_bound': 'both',
        'x_ticks': [1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
        'v_label': '$E_{N}$',
        'v_bound': 'both',
        'v_ticks': [0.0, 0.2, 0.4, 0.6]
    }
}

# get average entanglement
looper = wrap_looper(Mod00, params, 'measure_average', 'XLooper', 'H:/Workspace/VSCode/Python/entan_oem_mod/data/mod_00/E_N_g_0_0.005_g_1_0.005_Omega_E_1.16', True)

# calculate thresholds
print(looper.get_thresholds())