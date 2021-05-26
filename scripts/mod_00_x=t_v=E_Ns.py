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
        'Omegas': [1.16, 1.14],
        'omegas': [1.0, 1.0],
        'Vs': [10.0, 1.0]
    },
    'plotter': {
        'type': 'lines',
        'show_legend': True,
        'title': '$\\Omega_{E} = 1.16, \\Omega_{V} = 1.14$',
        'x_label': '$\\omega_{0} t$',
        'x_bound': 'both',
        'x_ticks': [960, 970, 980, 990, 1000],
        'y_legend': ['$E_{1} = 0.0, V_{1} = 0.0$', '$E_{1} = 2.5, V_{1} = 1.0$'],
        'y_colors': ['b', 'r'],
        'v_label': '$E_{N}$',
        'v_bound': 'both',
        'v_ticks': [0.0, 0.5, 1.0]
    }
}

# initialize log
init_log()

# initialize system
system = Mod00(params['system'])

# get entanglement without modulation
system.params['Es'][1] = 0.0
system.params['Vs'][1] = 0.0
M_0, T = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)

# get entanglement with modulation
system.params['Es'][1] = 2.5
system.params['Vs'][1] = 1.0
M_1, T = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)

# plotter
axes = {
    'X': T,
    'Y': {
        'var': 'Es',
        'val': [0, 1]
    }
}
plotter = MPLPlotter(axes, params['plotter'])
plotter.update(xs=[T, T], vs=[M_0, M_1])
plotter.show(True)