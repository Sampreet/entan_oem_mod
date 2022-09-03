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

# frequently used parameters
cyc = 1000
t_max = 10000.0
t_dim = 100001
range_min = int(t_dim - 2 * cyc * np.pi)

# all parameters
params = {
    'looper': {
        'show_progress_x': True,
        'X': {
            'var': 'Omegas',
            'idx': 2,
            'min': 1.6,
            'max': 2.4,
            'dim': 801
        }
    },
    'solver': {
        'cache': True,
        'cache_dir': 'H:/Workspace/data/oem_20/0.0_' + str(t_max) + '_' + str(t_dim),
        'method': 'zvode',
        'measure_type': 'corr_ele',
        'idx_e': (2, 2),
        'range_min': range_min,
        'range_max': t_dim,
        't_min': 0.0,
        't_max': t_max,
        't_dim': t_dim
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
        'x_label': '$\\Omega_{s} / \\omega_{b0}$',
        'x_ticks': [1.6, 1.8, 2.0, 2.2, 2.4],
        'x_ticks_minor': [1.6 + i * 0.04 for i in range(21)],
        # 'x_ticks': [1.99, 2.0, 2.01],
        # 'x_ticks_minor': [1.99 + i * 0.002 for i in range(11)],
        'y_colors': ['k'] + ['r'] * 2 + ['b'] * 2,
        'y_sizes': [1] + [2] * 4,
        'y_styles': ['--'] + ['-.', '-'] * 2,
        # 'v_label': '$\\langle Q_{b}^{2} \\rangle_{min}$',
        'v_label': '',
        'v_label_color': 'r',
        'v_limits': [0.325, 0.675],
        'v_tick_position': 'left-in',
        'v_tick_labels': ['', '', ''],
        'v_ticks': [0.4, 0.5, 0.6],
        'v_ticks_minor': [0.325 + i * 0.025 for i in range(14)],
        # 'v_twin_label': '$E_{N_{max}}$',
        'v_twin_label': '',
        'v_twin_label_color': 'b',
        'v_twin_limits': [-0.015, 0.195],
        'v_twin_tick_position': 'right-in',
        'v_twin_tick_labels': ['', '', ''],
        'v_twin_ticks': [0.03, 0.09, 0.15],
        'v_twin_ticks_minor': [i * 0.015 for i in range(14)],
        'label_font_size': 32,
        'tick_font_size': 28,
        # 'width': 7.0,
        'width': 6.6,
        # 'width': 5.4,
        'height': 4.0,
        'annotations': [{
            's': '$N = ' + str(cyc) + '$',
            # 'xy': [0.22, 0.82],
            'xy': [0.09, 0.82],
            # 'xy': [0.12, 0.82],
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

# looper with laser and frequency modulation
params['system']['A_vs'] = [50.0, 0.0, 0.0]
params['system']['theta'] = 0.5
looper = wrap_looper(SystemClass=OEM_20, params=params, func=func_mdy_min, looper='XLooper', file_path_prefix='data/v3.0-qom-v0.8.6/r_3b_Sq_0_' + str(t_max) + '_' + str(cyc))
Sq_0 = looper.results['V']

# looper with laser, voltage and frequency modulation
params['system']['A_vs'] = [50.0, 50.0, 50.0]
params['system']['theta'] = 0.5
looper = wrap_looper(SystemClass=OEM_20, params=params, func=func_mdy_min, looper='XLooper', file_path_prefix='data/v3.0-qom-v0.8.6/r_3b_Sq_1_' + str(t_max) + '_' + str(cyc))
Sq_1 = looper.results['V']
print(min(Sq_1), looper.axes['X']['val'][np.argmin(Sq_1)])

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

# looper with laser and frequency modulation
params['system']['A_vs'] = [50.0, 0.0, 0.0]
params['system']['theta'] = 0.5
looper = wrap_looper(SystemClass=OEM_20, params=params, func=func_mdy_max, looper='XLooper', file_path_prefix='data/v3.0-qom-v0.8.6/r_3b_En_0_' + str(t_max) + '_' + str(cyc))
En_0 = looper.results['V']

# looper with laser, voltage and frequency modulation
params['system']['A_vs'] = [50.0, 50.0, 50.0]
params['system']['theta'] = 0.5
looper = wrap_looper(SystemClass=OEM_20, params=params, func=func_mdy_max, looper='XLooper', file_path_prefix='data/v3.0-qom-v0.8.6/r_3b_En_1_' + str(t_max) + '_' + str(cyc))
En_1 = looper.results['V']
print(max(En_1), looper.axes['X']['val'][np.argmax(En_1)])

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