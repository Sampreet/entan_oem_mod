# dependencies
import numpy as np
import os 
import sys

# qom modules
from qom.solvers import HLESolver
from qom.solvers.MeasureSolver import get_wigner_single_mode
from qom.ui import init_log
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('.')))
# import system
from systems.OptoElectroMechanical import OEM_20

# parameters
params = {
    'solver': {
        'show_progress' : True,
        'cache'         : False,
        'method'        : 'vode',
        'indices'       : [1],
        'wigner_xs'     : np.linspace(-2.0, 2.0, 401),
        'wigner_ys'     : np.linspace(-2.0, 2.0, 401),
        't_min'         : 0.0,
        't_max'         : 1000.0,
        't_dim'         : 10001,
        't_range_min'   : 9900,
        't_range_max'   : 10001
    },
    'system': {
        'A_ls'      : [100.0, 10.0, 10.0],
        'A_vs'      : [50.0, 50.0, 50.0], 
        'Delta_0'   : 1.0,
        'gammas'    : [0.1, 1e-6, 1e-2],
        'gs'        : [1e-3, 2e-4],
        'n_ths'     : [0.0, 0.0],
        'Omegas'    : [2.0, 2.0, 2.0],
        'omega_c0'  : 1.1,
        'theta'     : 0.5,
        't_mod'     : 'cos',
        't_pos'     : 'top'
    },
    'plotter': {
        'type'              : 'contourf',
        'title'             : '$\\omega_{b0} t = 991.4$',
        'x_label'           : '$Q_{b}$',
        'x_label_pad'       : -16,
        'x_tick_labels'     : [-2, '', 2],
        'x_tick_position'   : 'both-out',
        'x_ticks'           : [-2, 0, 2],
        'x_ticks_minor'     : [-2, -1, 0, 1, 2],
        'y_label'           : '$P_{b}$',
        'y_label_pad'       : -16,
        'y_tick_labels'     : [-2, '', 2],
        'y_tick_position'   : 'both-out',
        'y_ticks'           : [-2, 0, 2],
        'y_ticks_minor'     : [-2, -1, 0, 1, 2],
        'show_cbar'         : False,
        'cbar_title'        : '$\\times 10^{-2}$',
        'cbar_ticks'        : [0.0, 0.025, 0.05],
        'cbar_tick_labels'  : ['0.0', '2.5', '5.0'],
        'label_font_size'   : 40,
        'tick_font_size'    : 35,
        'width'             : 4.25,
        'height'            : 4.5
    }
}

# initialize logger
init_log()

# initialize system
system = OEM_20(
    params=params['system']
)

# get modes and correlations
_, Corrs, T = HLESolver(
    system=system,
    params=params['solver']
).get_modes_corrs_times_in_range()
# get Wigner distributions
Wigners = get_wigner_single_mode(
    Corrs=Corrs,
    params=params['solver']
)

# plot squeezed Wigners
for i in [14, 91]:
    params['plotter']['title'] = '$\\omega_{b0} t = ' + str(T[i]) +'$'
    plotter = MPLPlotter(
        axes={
            'X': params['solver']['wigner_xs'],
            'Y': params['solver']['wigner_ys']
        },
        params=params['plotter']
    )
    plotter.update(
        vs=Wigners[i, 0]
    )
    plotter.show(
        hold=True
    )