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
        'range_min': 9371,
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
        'type': 'line',
        'x_label': '$\\omega_{b0} t$',
        'x_ticks': [990, 995, 1000],
        'x_ticks_minor': [990 + i for i in range(11)],
        'y_colors': ['k', 'r', 'b'],
        'y_sizes': [1, 2, 2],
        'y_styles': ['--', '-', '-'],
        'v_label': '',
        'v_label_color': 'r',
        'v_limits': [0.35, 0.9],
        'v_tick_position': 'left-in',
        'v_tick_labels': [''] * 3,
        'v_ticks': [0.4, 0.6, 0.8],
        'v_ticks_minor': [0.35 + i * 0.05 for i in range(13)],
        'v_twin_label': '$E_{N}$',
        'v_twin_label_color': 'b',
        'v_twin_limits': [0.015, 0.18],
        'v_twin_tick_position': 'right-in',
        'v_twin_ticks': [0.03, 0.09, 0.15],
        'v_twin_ticks_minor': [0.015 + i * 0.015 for i in range(13)],
        'label_font_size': 32,
        'tick_font_size': 28,
        'width': 4.6,
        'height': 4.0,
        'annotations': [{
            's': '(d)',
            'xy': [0.12, 0.82]
        }]
    }
}

# initialize logger
init_log()

# initialize system
system = OEM_20(params=params['system'])

# get quadrature dynamics
params['solver']['measure_type'] = 'corr_ele'
params['solver']['idx_e'] = (2, 2)
M_0, T = system.get_measure_dynamics(solver_params=params['solver'])
M_0 = np.transpose(M_0)[0].tolist()
print(np.min(M_0))

# get entanglement dyanamics
params['solver']['measure_type'] = 'entan_ln'
params['solver']['idx_e'] = (0, 2)
M_1, T = system.get_measure_dynamics(solver_params=params['solver'])
print(np.max(M_1))

# plotter
plotter = MPLPlotter(axes={
    'X': T,
    'Y': list(range(3))
}, params=params['plotter'])
_colors = plotter.get_colors(palette='RdBu_r', bins=11)
# plot squeezing dynamics
ax = plotter.update(xs=T, vs=[np.zeros(np.shape(T)) + 0.5, M_0])
# plot entanglement dynamics
ax_twin = plotter.update_twin_axis(xs=T, vs=M_1)
# color patches
ax.axvspan(990.85, 991.90, color=_colors[8], alpha=0.25)
ax.axvspan(994.00, 995.05, color=_colors[8], alpha=0.25)
ax.axvspan(997.15, 998.20, color=_colors[8], alpha=0.25)
ax.axvspan(992.10, 993.20, color=_colors[2], alpha=0.25)
ax.axvspan(995.25, 996.35, color=_colors[2], alpha=0.25)
ax.axvspan(998.40, 999.50, color=_colors[2], alpha=0.25)
# show
plotter.show(True)