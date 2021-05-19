# dependencies
import numpy as np
import os 
import sys

# qom modules
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'entan_lc_mod')))
# import system
from systems.PRL00 import PRL00

# all parameters
params = {
    "solver": {
        "show_progress": True,
        "cache": False,
        "method": "ode",
        "measure_type": "qcm",
        "qcm_type": "entan",
        "idx_mode_i": 0,
        "idx_mode_j": 1,
        "range_min": 3000,
        "range_max": 3201,
        "t_min": 0,
        "t_max": 50,
        "t_dim": 5001
    },
    "system": {
        "F": 1.4e4,
        "lambda_l": 1064e-9, 
        "L": 25e-3, 
        "m": 150e-12,
        "omega_m": 6283195.31,
        "P_0": 10e-3,
        "P_1": 2e-3,
        "Q": 1e6,
        "T": 0.1
    },
    "plotter": {
        "type": "lines",
        "show_legend": True,
        "x_label": "$t / \\tau$",
        "y_name": "$P_{\\pm 1}$",
        "y_unit": "$\\mathrm{mW}$",
        "y_colors": ["b", "g"],
        "v_label": "$E_{N}$",
        "v_bound": "both",
        "v_ticks": [0.0, 0.1, 0.2, 0.3, 0.4]
    }
}

# initialize log
init_log()

# initialize system
system = PRL00(params['system'])

# without modulation
system.params['P_1'] = 0.0
M_0 = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)
# with modulation
system.params['P_1'] = 2e-3
M_1 = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)

# plotter
t_min = params['solver']['range_min']
t_max = params['solver']['range_max'] - 1
t_ss = (params['solver']['t_dim'] - 1) / params['solver']['t_max']
T = np.linspace(t_min / t_ss, t_max / t_ss, t_max - t_min + 1).tolist()
axes = {
    'X': T,
    'Y': {
        'var': 'P_1',
        'val': [0, 2]
    }
}
plotter = MPLPlotter(axes, params['plotter'])
_xs = [T, T]
_ys = [M_0, M_1]
plotter.update(xs=_xs, vs=_ys)
plotter.show(True)