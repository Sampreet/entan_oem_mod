# dependencies
import numpy as np
import os
import sys

# qom modules
from qom.ui.plotters import MPLPlotter
from qom.utils.looper import wrap_looper

# add path to local libraries
sys.path.append(os.path.abspath(os.path.join('..', 'oem-systems')))
# import system
from systems import OEM_20

# all parameters
params = {
    'looper': {
        'show_progress_x': True,
        'X': {
            'var': 'Omegas',
            'idx': 1,
            'min': 1.9,
            'max': 2.1,
            'dim': 801
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
        'x_label': '$\\Omega_{v} / \\omega_{b0}$',
        'x_ticks': [1.9, 1.95, 2.0, 2.05, 2.1],
        'x_ticks_minor': [1.9 + i * 0.00625 for i in range(33)],
        'y_colors': ['k'] + ['r'] * 2 + ['b'] * 2,
        'y_sizes': [1] + [2] * 4,
        'y_styles': ['--'] + ['-.', '-'] * 2,
        'v_label': '$\\langle Q_{b}^{2} \\rangle_{min}$',
        'v_label_color': 'r',
        'v_limits': [0.325, 0.675],
        'v_tick_position': 'left-in',
        'v_ticks': [0.4, 0.5, 0.6],
        'v_ticks_minor': [0.325 + i * 0.025 for i in range(14)],
        'v_twin_label': '$E_{N_{max}}$',
        'v_twin_label_color': 'b',
        'v_twin_limits': [-0.015, 0.195],
        'v_twin_tick_position': 'right-in',
        'v_twin_ticks': [0.03, 0.09, 0.15],
        'v_twin_ticks_minor': [i * 0.015 for i in range(14)],
        'label_font_size': 32,
        'tick_font_size': 28,
        'width': 9.6,
        'height': 4.0,
        'annotations': [{
            's': '(a)',
            'xy': [0.16, 0.82]
        }]
    }
}

# function to calculate the minimum value of variance
params['solver']['measure_type'] = 'corr_ele'
params['solver']['idx_e'] = (2, 2)
def func_mdy_min(system_params, val, logger, results):
    # update parameters
    system = OEM_20(params=system_params)
    # get measure dynamics
    M, _ = system.get_measure_dynamics(solver_params=params['solver'])
    # get minimum value
    m_min = np.min(M)
    # update results
    results.append((val, m_min))

# looper with laser and voltage modulation
params['system']['A_vs'] = [50.0, 50.0, 50.0]
params['system']['theta'] = 0.0
looper = wrap_looper(SystemClass=OEM_20, params=params, func=func_mdy_min, looper='XLooper', file_path_prefix='data/v2.0-qom-v0.8.5/3a_Sq_0')
Sq_0 = looper.results['V']

# looper with laser, voltage and frequency modulation
params['system']['A_vs'] = [50.0, 50.0, 50.0]
params['system']['theta'] = 0.5
looper = wrap_looper(SystemClass=OEM_20, params=params, func=func_mdy_min, looper='XLooper', file_path_prefix='data/v2.0-qom-v0.8.5/3a_Sq_1')
Sq_1 = looper.results['V']

# function to calculate the maximum value of entanglement
params['solver']['measure_type'] = 'entan_ln'
params['solver']['idx_e'] = (0, 2)
def func_mdy_max(system_params, val, logger, results):
    # update parameters
    system = OEM_20(params=system_params)
    # get measure dynamics
    M, _ = system.get_measure_dynamics(solver_params=params['solver'])
    # get maximum value
    m_max = np.max(M)
    # update results
    results.append((val, m_max))

# looper with laser and voltage modulation
params['system']['A_vs'] = [50.0, 50.0, 50.0]
params['system']['theta'] = 0.0
looper = wrap_looper(SystemClass=OEM_20, params=params, func=func_mdy_max, looper='XLooper', file_path_prefix='data/v2.0-qom-v0.8.5/3a_En_0')
En_0 = looper.results['V']

# looper with laser, voltage and frequency modulation
params['system']['A_vs'] = [50.0, 50.0, 50.0]
params['system']['theta'] = 0.5
looper = wrap_looper(SystemClass=OEM_20, params=params, func=func_mdy_max, looper='XLooper', file_path_prefix='data/v2.0-qom-v0.8.5/3a_En_1')
En_1 = looper.results['V']

# plotter
X = looper.axes['X']['val']
plotter = MPLPlotter(axes={
    'X': X,
    'Y': list(range(5))
}, params=params['plotter'])
# plot squeezing dynamics
plotter.update(xs=X, vs=[np.zeros(np.shape(X)) + 0.5, Sq_0, Sq_1])
# plot entanglement dynamics
plotter.update_twin_axis(xs=X, vs=[En_0, En_1])
# show
plotter.show(True)