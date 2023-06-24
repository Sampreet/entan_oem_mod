# dependencies
import numpy as np
import os
import sys

# qom modules
from qom.utils.looper import wrap_looper
from qom.ui.plotters import MPLPlotter

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'entan_oem_mod')))
# import system
from systems import OEM_20

# all parameters
params = {
    'looper': {
        'show_progress_x': True,
        'X': {
            'var': 'n_ths',
            'idx': 1,
            'min': -4,
            'max': 2,
            'dim': 201,
            'scale': 'log' 
        }
    },
    'solver': {
        'cache': True,
        'cache_dir': 'H:/Workspace/data/oem_20/0.0_1000.0_10001',
        'method': 'zvode',
        'measure_type': 'entan_ln',
        'idx_e': (0, 2),
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
        'type': 'lines',
        'x_label': '$n_{th_{c}}$',
        'x_label_pad': 20,
        'x_tick_labels': ['$10^{' + str(i - 4) + '}$' for i in range(5)],
        'x_tick_pad': 16,
        'x_ticks': [10**(i - 4) for i in range(5)],
        'x_ticks_minor': [(i % 10 + 1) * 10**(int(i / 10) - 4) for i in range(41)],
        'x_scale': 'log',
        'y_colors': ['b', 'b'],
        'y_sizes': [2, 2],
        'y_styles': [':', '-'],
        'v_label': '$E_{N_{max}}$',
        'v_label_pad': 20,
        'v_tick_labels': ['{:0.2f}'.format(i * 0.04) for i in range(5)],
        'v_tick_pad': 16,
        'v_ticks': [i * 0.04 for i in range(5)],
        'v_ticks_minor': [i * 0.01 for i in range(17)],
        'show_legend': True,
        'legend_location': 'upper right',
        'label_font_size': 40,
        'legend_font_size': 32,
        'tick_font_size': 32,
        'width': 9.6,
        'height': 9.6,
        'annotations': [{
            's': '(b)',
            'xy': [0.23, 0.88]
        }]
    }
}

# function to calculate the maximum value of dynamics
def func_mdy_max(system_params, val, logger, results):
    # update parameters
    system = OEM_20(params=system_params)
    # get measure dynamics
    M, _ = system.get_measure_dynamics(solver_params=params['solver'])
    # get maximum value
    m_max = np.max(M)
    # update results
    results.append((val, m_max))

# looper with laser modulation
params['system']['A_vs'] = [50.0, 0.0, 0.0]
params['system']['theta'] = 0.0
looper = wrap_looper(SystemClass=OEM_20, params=params, func=func_mdy_max, looper='XLooper', file_path_prefix='data/v2.0-qom-v0.8.5/r_1b_alt_En_0')
X = looper.axes['X']['val']
En_0 = looper.results['V']
print(looper.get_thresholds(thres_mode='minmax'))

# looper with all modulations
params['system']['A_vs'] = [50.0, 50.0, 50.0]
params['system']['theta'] = 0.5
looper = wrap_looper(SystemClass=OEM_20, params=params, func=func_mdy_max, looper='XLooper', file_path_prefix='data/v2.0-qom-v0.8.5/r_1b_alt_En_1')
En_1 = looper.results['V']
print(looper.get_thresholds(thres_mode='minmax'))

# plotter
plotter = MPLPlotter(axes={
    'X': X,
    'Y': [
        'only laser modulation', 
        'with all modulations'
    ]
}, params=params['plotter'])
plotter.update(xs=X, vs=[En_0, En_1])
plotter.show(True)

