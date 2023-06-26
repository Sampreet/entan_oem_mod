# dependencies
import numpy as np
import os
import sys

# qom modules
from qom.solvers import HLESolver, QCMSolver
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('.')))
# import system
from systems.OptoElectroMechanical import OEM_20

# all parameters
params = {
    'solver'    : {
        'show_progress' : True,
        'cache'         : False,
        'measure_codes' : ['entan_ln'],
        'indices'       : (0, 2),
        'method'        : 'vode',
        't_min'         : 0.0,
        't_max'         : 1000.0,
        't_dim'         : 10001,
        't_range_min'   : 9371,
        't_range_max'   : 10001
    },
    'system'    : {
        'A_ls'      : [100.0, 10.0, 10.0],
        'A_vs'      : [50.0, 0.0, 0.0], 
        'Delta_0'   : 1.0,
        'gammas'    : [0.1, 1e-6, 1e-2],
        'gs'        : [1e-3, 2e-4],
        'n_ths'     : [0.0, 0.0],
        'Omegas'    : [2.0, 2.0, 2.0],
        'omega_c0'  : 1.1,
        'theta'     : 0.0,
        't_mod'     : 'cos',
        't_pos'     : 'top'
    },
    'plotter'   : {
        'type'                  : 'line',
        'x_label'               : '$\\omega_{b0} t$',
        'x_ticks'               : [990, 995, 1000],
        'x_ticks_minor'         : [990 + i for i in range(11)],
        'y_colors'              : ['k', 'r', 'b'],
        'y_sizes'               : [1, 2, 2],
        'y_styles'              : ['--', ':', ':'],
        'v_label'               : '$\\langle Q_{b}^{2} \\rangle$',
        'v_label_color'         : 'r',
        'v_limits'              : [0.35, 0.9],
        'v_tick_position'       : 'left-in',
        'v_ticks'               : [0.4, 0.6, 0.8],
        'v_ticks_minor'         : [0.35 + i * 0.05 for i in range(13)],
        'v_twin_label'          : '',
        'v_twin_label_color'    : 'b',
        'v_twin_limits'         : [0.015, 0.18],
        'v_twin_tick_labels'    : [''] * 3,
        'v_twin_tick_position'  : 'right-in',
        'v_twin_ticks'          : [0.03, 0.09, 0.15],
        'v_twin_ticks_minor'    : [0.015 + i * 0.015 for i in range(13)],
        'label_font_size'       : 32,
        'tick_font_size'        : 28,
        'width'                 : 4.6,
        'height'                : 4.0,
        'annotations'           : [{
            'text'  : '(a)',
            'xy'    : [0.33, 0.82]
        }],
        'vspan'                 : [
            {
                'xmin'  : 990.05,
                'xmax'  : 990.95,
                'color' : 2,
                'alpha' : 0.25
            },
            {
                'xmin'  : 990.70,
                'xmax'  : 991.65,
                'color' : 8,
                'alpha' : 0.25
            },
            {
                'xmin'  : 993.20,
                'xmax'  : 994.15,
                'color' : 2,
                'alpha' : 0.25
            },
            {
                'xmin'  : 993.85,
                'xmax'  : 994.80,
                'color' : 8,
                'alpha' : 0.25
            },
            {
                'xmin'  : 996.35,
                'xmax'  : 997.30,
                'color' : 2,
                'alpha' : 0.25
            },
            {
                'xmin'  : 997.00,
                'xmax'  : 997.95,
                'color' : 8,
                'alpha' : 0.25
            },
            {
                'xmin'  : 999.50,
                'xmax'  : 1000.0,
                'color' : 2,
                'alpha' : 0.25
            }
        ]
    }
}

# initialize logger
init_log()

# initialize system
system = OEM_20(
    params=params['system']
)

# initialize solver
hle_solver  = HLESolver(
    system=system,
    params=params['solver']
)
# get modes and correlations
Modes, Corrs, T = hle_solver.get_modes_corrs_times_in_range()
# get quantum correlation measures
Measures = QCMSolver(
    Modes=Modes,
    Corrs=Corrs,
    params=params['solver']
).get_measures()
# extract correlation
M_0 = Corrs[:, 2, 2]
# extract entanglement
M_1 = Measures[:, 0]
# output maximum squeezing and entanglement
print(np.min(M_0), np.max(M_1))

# plotter
plotter = MPLPlotter(
    axes={},
    params=params['plotter']
)
# plot correlation dynamics
plotter.update(
    xs=T,
    vs=[np.zeros(np.shape(T)) + 0.5, M_0]
)
# plot entanglement dynamics
plotter.update_twin_axis(
    xs=T,
    vs=M_1
)
# show
plotter.show(
    hold=True
)