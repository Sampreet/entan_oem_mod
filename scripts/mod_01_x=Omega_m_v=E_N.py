# dependencies
import os 
import sys

# qom modules
from qom.utils import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'entan_oem_mod')))
# import system
from systems.Mod01 import Mod01

# all parameters
params = {
    'looper': {
        'show_progress': True,
        'X': {
            'var': 'thetas',
            'idx': 1,
            'min': 1.0,
            'max': 3.0,
            'dim': 21
        }
    },
    'solver': {
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
        'A_ls': [50, 0.0],
        'A_vs': [1e2, 10.0], 
        'Delta_0': 1.0,
        'gammas': [5e-3, 5e-2],
        'gs': [5e-3, 5e-4],
        'kappa': 0.15,
        'n_ths': [0, 0],
        'Omegas': [2.0, 2.0],
        'omegas': [1.0, 1.0],
        'thetas': [0.1, 2.0],
        't_mod': 'cos',
        't_pos': 'bottom'
    },
    'plotter': {
        'type': 'line',
        'x_label': '$\\theta_{1} / \\omega_{0}$',
        'x_bound': 'both',
        'x_ticks': [1.0, 1.5, 2.0, 2.5, 3.0],
        'v_label': '$E_{N}$',
        'v_bound': 'both',
    }
}

# get average entanglement
looper = wrap_looper(Mod01, params, 'measure_average', 'XLooper', 'H:/Workspace/VSCode/Python/entan_oem_mod/data/mod_01/E_N_g_0_5e-3_g_1_5e-4_A_v_1_10.0_Omega_v_2.0', True)

# calculate thresholds
print(looper.get_thresholds())