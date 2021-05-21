# dependencies
import numpy as np
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
        'cache_dir': 'H:/Workspace/VSCode/Python/entan_oem_mod/data/sys_00/0.0_1000.0_10001',
        'method': 'ode',
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
        'gs': [0.005, 0.0],
        'kappa': 0.15,
        'n_ths': [0, 0],
        'Omegas': [2.0, 1.0],
        'omegas': [1.0, 1.0],
        'Vs': [10.0, 1.0]
    },
    'plotter': {
        'type': 'line',
        'x_label': '$\\omega_{0} t$',
        'y_name': '$P_{\\pm 1}$',
        'y_unit': '$\\mathrm{mW}$',
        'y_colors': ['b', 'g'],
        'v_label': '$E_{N}$'
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