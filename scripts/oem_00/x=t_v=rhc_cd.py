# dependencies
import os 
import sys

# qom modules
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter
from qom.utils.wrappers import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'entan_oem_mod')))
# import system
from systems.Mod00 import Mod00

# all parameters
params = {
    'solver': {
        'show_progress': True,
        'method': 'zvode',
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
        'type': 'line',
        'x_label': '$\\omega_{0} t$',
        'x_bound': 'both',
        'x_ticks': [960, 970, 980, 990, 1000],
        'v_label': 'Counts',
        'v_bound': 'both',
        'v_ticks': [0, 1, 2, 3]
    }
}

# initialize log
init_log()

# initialize system
system = Mod00(params['system'])

# get modes
Counts, T = system.get_rhc_count_dynamics(params['solver'], system.func_ode, system.get_ivc, system.get_A)

# plotter
axes = {
    'X': T
}
plotter = MPLPlotter(axes, params['plotter'])
plotter.update(xs=T, vs=Counts)
plotter.show(True, width=8.0)