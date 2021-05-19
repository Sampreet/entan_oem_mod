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
    "solver": {
        "show_progress": True,
        "cache": False,
        "method": "ode",
        "measure_type": "qcm",
        "qcm_type": "entan",
        "idx_mode_i": 1,
        "idx_mode_j": 2,
        "range_min": 0,
        "range_max": 10001,
        "t_min": 0,
        "t_max": 1000,
        "t_dim": 10001
    },
    "system": {
        "Delta_0": 1.0,
        "E_0": 25.0, 
        "E_1": 2.5, 
        "gammas": [0.005, 0.005],
        "gs": [0.005, 0.005],
        "kappa": 0.15,
        "n_ths": [0, 0],
        "Omegas": [2.0, 1.0],
        "omegas": [1.0, 1.0],
        "V_0": 10.0,
        "V_1": 1.0
    },
    "plotter": {
        "type": "line",
        "x_label": "$\\omega_{0} t$",
        "y_name": "$P_{\\pm 1}$",
        "y_unit": "$\\mathrm{mW}$",
        "y_colors": ["b", "g"],
        "v_label": "$E_{N}$"
    }
}

# initialize log
init_log()

# initialize system
system = Mod00(params['system'])

# get entanglement
M_1 = system.get_measure_dynamics(params['solver'], system.ode_func, system.get_ivc)

# plotter
t_min = params['solver']['range_min']
t_max = params['solver']['range_max'] - 1
t_ss = (params['solver']['t_dim'] - 1) / params['solver']['t_max']
T = np.linspace(t_min / t_ss, t_max / t_ss, t_max - t_min + 1).tolist()
axes = {
    'X': T
}
plotter = MPLPlotter(axes, params['plotter'])
plotter.update(xs=T, vs=M_1)
plotter.show(True)