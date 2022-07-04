# dependencies
import numpy as np
import os
import sys

# qom modules
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'oem-systems')))
# import system
from systems import OEM_20

# all parameters
params = {
    'solver': {
        'show_progress': True,
        'cache': True,
        'cache_dir': 'H:/Workspace/data/oem_20/0.0_1000.0_10001',
        'method': 'zvode',
        'range_min': 0,
        'range_max': 10001,
        't_min': 0.0,
        't_max': 1000.0,
        't_dim': 10001
    },
    'system': {
        'A_ls': [100.0, 10.0, 10.0],
        'A_vs': [50.0, 50.0, 50.0], 
        'Delta_0': 1.0,
        'gammas': [0.1, 1e-6, 1e-2],
        'gs': [1e-3, 2e-4],
        'n_ths': [10, 0],
        'Omegas': [2.0, 2.0, 2.0],
        'omega_c0': 1.1,
        'theta': 0.5,
        't_mod': 'cos',
        't_pos': 'top'
    },
    'plotter': {
        'type': 'lines',
        'x_label': '$\\omega_{b0} t$',
        'x_label_pad': 20,
        'x_tick_pad': 16,
        'x_ticks': [i * 40 for i in range(6)],
        'x_ticks_minor': [i * 10 for i in range(21)],
        'y_colors': ['r'],
        'y_sizes': [2],
        'v_label': '$n_{b}$',
        'v_label_pad': 20,
        'v_tick_pad': 16,
        'v_ticks': [i * 5 for i in range(3)],
        'v_ticks_minor': [i * 1 for i in range(11)],
        'label_font_size': 40,
        'tick_font_size': 32,
        'width': 9.6,
        'height': 4.8
    }
}

# initialize logger
init_log()

# initialize system
system = OEM_20(params=params['system'])

# get quadrature dynamics
params['solver']['measure_type'] = 'corr_ele'
params['solver']['idx_e'] = [(2, 2), (3, 3)]
M, T = system.get_measure_dynamics(solver_params=params['solver'])
n_bs = [0.5 * (m[0] + m[1] - 1) for m in M]

# plotter
plotter = MPLPlotter(axes={
    'X': T,
}, params=params['plotter'])
plotter.update(xs=T, vs=n_bs)
plotter.show(True)