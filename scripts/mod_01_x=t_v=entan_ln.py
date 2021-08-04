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
        'A_ls': [1e2, 0.0],
        'A_vs': [0.0, 1e4], 
        'Delta_0': 1.0,
        'gammas': [1e-3, 1e-2],
        'gs': [1e-3, 1e-6],
        'kappa': 0.1,
        'n_ths': [0, 0],
        'Omegas': [0.0, 0.0],
        'omegas': [1.0, 1.0],
        'epsis': [0.0, 0.0],
        't_mods': ['cos', 'cos', 'cos'],
        't_pos': 'top'
    },
    'plotter': {
        'type': 'lines',
        'show_legend': True,
        'palette': 'Reds',
        'bins': 4,
        'title': '$A_{l} = 100, A_{v} = 10^{4} \\cos ( \\Omega_{v} t )$',
        'x_label': '$\\omega_{0} t$',
        'y_legend': [
            '$\\Omega_{v} = 0.0, \\theta_{0} = 0.0, \\theta_{1} = 0.0$', 
            '$\\Omega_{v} = 2.0, \\theta_{0} = 0.0, \\theta_{1} = 0.0$', 
            '$\\Omega_{v} = 2.0, \\theta_{0} = - 0.5, \\theta_{1} = 2.0$'
        ],
        'v_label': '$E_{N}$',
        'v_bound': 'both',
        'v_ticks': [0.00, 0.05, 0.10, 0.15, 0.20]
    }
}

# initialize log
init_log()

# initialize system
system = Mod01(params['system'])

# get entanglement without any modulation
M_0, T = system.get_measure_dynamics(params['solver'], system.func_ode, system.get_ivc)

# get entanglement with voltage modulation
system.params['Omegas'][1] = 2.0
M_1, T = system.get_measure_dynamics(params['solver'], system.func_ode, system.get_ivc)

# get entanglement with voltage and frequency modulation
system.params['epsis'][0] = - 0.5
system.params['epsis'][1] = 1.0
M_2, T = system.get_measure_dynamics(params['solver'], system.func_ode, system.get_ivc)

# plotter
axes = {
    'X': T,
    'Y': {
        'var': 'As',
        'val': [0, 1, 2]
    }
}
plotter = MPLPlotter(axes, params['plotter'])
plotter.update(xs=[T, T, T], vs=[M_0, M_1, M_2])
plotter.show(True, width=8.0)