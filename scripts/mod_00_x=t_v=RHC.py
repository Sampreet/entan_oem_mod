# dependencies
import os 
import sys

# qom modules
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'entan_oem_mod')))
# import system
from systems.Mod00 import Mod00

# all parameters
params = {
    'solver': {
        'show_progress': True,
        'cache': True,
        'cache_dir': 'H:/Workspace/VSCode/Python/entan_oem_mod/data/mod_00/0.0_1000.0_10001',
        'method': 'ode',
        'range_min': 371,
        'range_max': 1001,
        't_min': 0,
        't_max': 100,
        't_dim': 1001
    },
    'system': {
        'Delta_0': - 1.0,
        'Es': [30.0, 0.0], 
        'gammas': [5e-3, 5e-2],
        'gs': [5e-3, 5e-12],
        'kappa': 0.15,
        'n_ths': [0, 0],
        'Omegas': [2.0, 2.0],
        'omegas': [1.0, 1.0],
        'Vs': [15.0, 0.0]
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
Counts, T = system.get_rhc_count_dynamics(params['solver'], system.ode_func, system.get_ivc, system.get_A)

# plotter
axes = {
    'X': T
}
plotter = MPLPlotter(axes, params['plotter'])
plotter.update(xs=T, vs=Counts)
plotter.show(True)