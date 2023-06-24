# dependencies
import itertools
import numpy as np
import os 
import sys

# qom modules
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'entan_oem_mod')))
# import system
from systems import OEM_20

# parameters
params = {
    'solver': {
        'show_progress': True,
        'cache': True,
        'cache_dir': 'H:/Workspace/data/oem_20/0.0_1000.0_10001',
        'method': 'zvode',
        'measure_type': 'corr_ele',
        'idx_e': list(itertools.product([2, 3], [2, 3])),
        'range_min': 9900,
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
        'n_ths': [0, 0],
        'Omegas': [2.0, 2.0, 2.0],
        'omega_c0': 1.1,
        'theta': 0.5,
        't_mod': 'cos',
        't_pos': 'top'
    },
    'plotter': {
        'type': 'contourf',
        'title': '$\\omega_{b0} t = 990$',
        'x_label': '$P_{b}$',
        'x_label_pad': -16,
        'x_tick_labels': [-2, '', 2],
        'x_tick_position': 'both-out',
        'x_ticks': [-2, 0, 2],
        'x_ticks_minor': [-2, -1, 0, 1, 2],
        'y_label': '$Q_{b}$',
        'y_label_pad': -16,
        'y_tick_labels': [-2, '', 2],
        'y_tick_position': 'both-out',
        'y_ticks': [-2, 0, 2],
        'y_ticks_minor': [-2, -1, 0, 1, 2],
        'show_cbar': False,
        'cbar_title': '$\\times 10^{-2}$',
        'cbar_ticks': [0.0, 0.025, 0.05],
        'cbar_tick_labels': ['0.0', '2.5', '5.0'],
        'label_font_size': 40,
        'tick_font_size': 35,
        'width': 4.25,
        'height': 4.5
    }
}

# initialize logger
init_log()

# initialize system
system = OEM_20(params=params['system'])

# get correlation elements
M, _ = system.get_measure_dynamics(solver_params=params['solver'])
V_mech = [np.reshape(m, (2, 2)) for m in M[0::1]]

# initialize variables
qs = np.around(np.linspace(-2, 2, 101), 1)
ps = np.around(np.linspace(-2, 2, 101), 1)
i = 0
for V in V_mech:
    # select plots
    if i==14 or i==91:
        # wigner function
        W = list()
        for q in qs:
            temp = list()
            for p in ps:
                X = np.array([q, p])
                ele = np.exp(-1 / 2 * np.dot(X, np.dot(np.linalg.inv(V), np.transpose(X)))) / 4 / np.pi**2 / np.sqrt(np.linalg.det(V))
                temp.append(ele)
            W.append(temp)

        # plotter
        params['plotter']['title'] = '$\\omega_{b0} t = ' + str(990 + 0.1 * i) + '$'
        plotter = MPLPlotter(axes={
            'X': qs.tolist(),
            'Y': ps.tolist()
        }, params=params['plotter'])
        plotter.update(vs=W)
        plotter.show(True)
    # update count
    i += 1