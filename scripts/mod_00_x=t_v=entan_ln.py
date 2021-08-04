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
        'method': 'zvode',
        'measure_type': 'entan_ln',
        'idx_e': (1, 2),
        'range_min': 0,
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
        'type': 'lines',
        'show_legend': True,
        'title': '$\\Omega_{l} = 2.0, \\Omega_{v} = 2.0$',
        'x_label': '$\\omega_{0} t$',
        'y_legend': ['$A_{l}^{(1)} = 0.0, A_{v}^{(1)} = 0.0$', '$A_{l}^{(1)} = 3.0, A_{v}^{(1)} = 1.5$'],
        'y_colors': ['b', 'r'],
        'v_label': '$E_{N}$'
    }
}

# initialize log
init_log()

# initialize system
system = Mod00(params['system'])

# get entanglement without modulation
system.params['A_ls'][1] = 0.0
system.params['A_vs'][1] = 0.0
M_0, T = system.get_measure_dynamics(params['solver'], system.func_ode, system.get_ivc)

# get entanglement with modulation
system.params['A_ls'][1] = 5.0
system.params['A_vs'][1] = 10.0
M_1, T = system.get_measure_dynamics(params['solver'], system.func_ode, system.get_ivc)

# plotter
axes = {
    'X': T,
    'Y': {
        'var': 'As',
        'val': [0, 1]
    }
}
plotter = MPLPlotter(axes, params['plotter'])
plotter.update(xs=[T, T], vs=[M_0, M_1])
plotter.show(True)