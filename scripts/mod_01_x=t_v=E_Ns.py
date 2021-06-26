# dependencies
import os 
import sys

# qom modules
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'entan_oem_mod')))
# import system
from systems.Mod01 import Mod01

# all parameters
params = {
    'solver': {
        'show_progress': True,
        'cache': True,
        'cache_dir': 'H:/Workspace/VSCode/Python/entan_oem_mod/data/mod_01/0.0_1000.0_10001',
        'method': 'ode',
        'measure_type': 'qcm',
        'qcm_type': 'entan',
        'idx_mode_i': 0,
        'idx_mode_j': 1,
        'range_min': 0,
        'range_max': 10001,
        't_min': 0,
        't_max': 1000,
        't_dim': 10001
    },
    'system': {
        'A_ls': [2e2, 0.0],
        'A_vs': [0.0, 0.0], 
        'Delta_0': - 1.0,
        'gammas': [1e-6, 1e-4],
        'gs': [1e-3, 1e-9],
        'kappa': 0.1,
        'n_ths': [0, 0],
        'Omegas': [2.0, 0.0],
        'omegas': [1.0, 1.0],
        'thetas': [0.1, 0.0],
        't_mod': 'cos',
        't_pos': 'bottom'
    },
    'plotter': {
        'type': 'lines',
        'show_legend': True,
        'title': '$\\theta_{1} = 2.0$',
        'x_label': '$\\omega_{0} t$',
        'y_legend': ['$\\theta_{0} = 0.0$', '$\\theta_{0} = 0.1$'],
        'y_colors': ['b', 'r'],
        'v_label': '$E_{N}$'
    }
}

# initialize log
init_log()

# initialize system
system = Mod01(params['system'])

# get entanglement without modulation
system.params['A_vs'][0] = 0.0
system.params['A_vs'][1] = 1e5
system.params['Omegas'][1] = 0.0
system.params['thetas'][0] = 0.0
system.params['thetas'][1] = 0.0
M_0, T = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)

# get entanglement with modulation
system.params['A_vs'][0] = 0.0
system.params['A_vs'][1] = 1e5
system.params['Omegas'][1] = 2.0
system.params['thetas'][0] = 0.0
system.params['thetas'][1] = 0.0
M_1, T = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)

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