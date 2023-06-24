#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate an OEM system with multiple modulations in laser amplitude, voltage amplitude and mechanical spring constant."""

__authors__ = ['Sampreet Kalita']
__created__ = '2021-06-14'
__updated__ = '2022-07-04'
__version__ = '0.8.5'

# dependencies
import numpy as np

# qom modules
from qom.systems import SODMSystem

# TODO: Review `get_oss_modes`.

class OEM_20(SODMSystem):
    r"""Class to simulate an OEM system with multiple modulations in laser amplitude, voltage amplitude and mechanical spring constant.

    Parameters
    ----------
    params : dict
        Parameters for the system. The system parameters are:
        ========    ========================================================================
        key         meaning
        ========    ========================================================================
        A_ls        (list) amplitudes of the laser, in the format :math:`\left[ A_{l0}, A_{l-}, A_{l+} \right]`. Default is :math:`\left[ 100.0, 10.0, 10.0 \right]`.
        A_vs        (list) amplitudes of the voltage, in the format :math:`\left[ A_{v0}, A_{v-}, A_{v+} \right]`. Default is :math:`\left[ 50.0, 50.0, 50.0 \right]`.
        Delta_0     (float) detuning of the laser, :math:`\Delta_{0} = \omega_{a0} - \omega_{l}`. Default is :math:`1.0`.
        gammas      (list) optical decay and mechanical and electrical damping rates, in the format :math:`\left[ \gamma_{a}, \gamma_{b}, \gamma_{c} \right]`. Default is :math:`\left[ 0.1, 10^{-6}, 10^{-2} \right]`.
        gs          (list) optomechanical and electromechanical coupling constants, in the format :math:`\left[ g_{ab}, g_{bc} \right]`. Default is :math:`\left[ 10^{-3}, 2 \times 10^{-4} \right]`.
        n_ths       (list) number of mechanical and electrical thermal phonons, in the format :math:`\left[ n_{th_{b}}, n_{th_{c}} \right]`. Default is :math:`\left[ 0, 0 \right]`.
        Omegas      (list) laser and voltage modulation frequencies and the spring constant modulation frequency, in the format :math:`\left[ \Omega_{l}, \Omega_{v}, \Omega_{s} \right]`. Default is :math:`\left[ 2.0, 2.0, 2.0 \right]`.
        omega_c0    (list) LC circuit base resonance frequency, :math:`\omega_{c0}`. Default is :math:`1.1`.
        theta       (list) mechanical modulation amplitude, :math:`\theta`. Default is :math:`0.5`.
        t_mod       (str) type of modulation for the mechanical spring constant. Options are "cos" for cosinusoidal, "sin" for sinusoidal. Default is "cos".
        t_pos       (str) position of the mechanical membrame in the parallel-plate capacitor. Options are "top" and "bottom". Default is "top".
        ========    ========================================================================
    cb_update : callable, optional
        Callback function to update status and progress, formatted as ``cb_update(status, progress, reset)``, where ``status`` is a string, ``progress`` is an integer and ``reset`` is a boolean.
    """

    # default looping parameters
    looper_defaults = {
        'A_l0': {
            'var': 'A_ls',
            'idx': 0,
            'min': 75.0,
            'max': 125.0,
            'dim': 1001,
            'scale': 'linear'
        },
        'A_lm': {
            'var': 'A_ls',
            'idx': 1,
            'min': 0.0,
            'max': 10.0,
            'dim': 1001,
            'scale': 'linear'
        },
        'A_lp': {
            'var': 'A_ls',
            'idx': 2,
            'min': 0.0,
            'max': 10.0,
            'dim': 1001,
            'scale': 'linear'
        },
        'A_v0': {
            'var': 'A_vs',
            'idx': 0,
            'min': -150.0,
            'max': 150.0,
            'dim': 1001,
            'scale': 'linear'
        },
        'A_vm': {
            'var': 'A_vs',
            'idx': 1,
            'min': 0.0,
            'max': 50.0,
            'dim': 1001,
            'scale': 'linear'
        },
        'A_vp': {
            'var': 'A_vs',
            'idx': 2,
            'min': 0.0,
            'max': 50.0,
            'dim': 1001,
            'scale': 'linear'
        },
        'Delta_0': {
            'var': 'Delta_0',
            'min': -2.0,
            'max': 2.0,
            'dim': 1001,
            'scale': 'linear'
        },
        'gamma_a': {
            'var': 'gammas',
            'idx': 0,
            'min': -2,
            'max': 0,
            'dim': 1001,
            'scale': 'log'
        },
        'gamma_b': {
            'var': 'gammas',
            'idx': 1,
            'min': -7,
            'max': -5,
            'dim': 1001,
            'scale': 'log'
        },
        'gamma_c': {
            'var': 'gammas',
            'idx': 2,
            'min': -3,
            'max': -1,
            'dim': 1001,
            'scale': 'log'
        },
        'g_ab': {
            'var': 'gs',
            'idx': 0,
            'min': -5,
            'max': -1,
            'dim': 1001,
            'scale': 'log'
        },
        'g_bc': {
            'var': 'gs',
            'idx': 1,
            'min': -5,
            'max': -3,
            'dim': 1001,
            'scale': 'log'
        },
        'n_th_b': {
            'var': 'n_th',
            'idx': 0,
            'min': -2,
            'max': 4,
            'dim': 201,
            'scale': 'log' 
        },
        'n_th_c': {
            'var': 'n_th',
            'idx': 1,
            'min': -4,
            'max': 2,
            'dim': 201,
            'scale': 'log' 
        },
        'Omega_l': {
            'var': 'Omegas',
            'idx': 0,
            'min': 1.0,
            'max': 3.0,
            'dim': 1001,
            'scale': 'linear'
        },
        'Omega_v': {
            'var': 'Omegas',
            'idx': 1,
            'min': 1.0,
            'max': 3.0,
            'dim': 1001,
            'scale': 'linear'
        },
        'Omega_s': {
            'var': 'Omegas',
            'idx': 2,
            'min': 1.0,
            'max': 3.0,
            'dim': 1001,
            'scale': 'linear'
        },
        'omega_c0': {
            'var': 'omega_c0',
            'min': 0.5,
            'max': 1.5,
            'dim': 1001,
            'scale': 'linear'
        },
        'theta': {
            'var': 'theta',
            'min': 0.0,
            'max': 1.0,
            'dim': 1001,
            'scale': 'linear'
        },
        't_mod': {
            'var': 't_mod',
            'val': ['cos', 'sin']
        },
        't_pos': {
            'var': 't_pos',
            'val': ['top', 'bottom']
        }
    }

    # default system parameters
    system_defaults = {
        'A_ls'      : [100.0, 10.0, 10.0],
        'A_vs'      : [50.0, 50.0, 50.0],
        'Delta_0'   : 1.0,
        'gammas'    : [0.1, 1e-6, 1e-2],
        'gs'        : [1e-3, 2e-4],
        'n_ths'     : [0, 0],
        'Omegas'    : [2.0, 2.0, 2.0],
        'omega_c0'  : 1.1,
        'theta'     : 0.5,
        't_mod'     : 'cos',
        't_pos'     : 'top'
    }

    def __init__(self, params, cb_update=None):
        """Class constructor for OEM_20."""
        
        # initialize super class
        super().__init__(params=params, cb_update=cb_update)

        # set attributes
        self.code = 'oem_20'
        self.name = 'Multi-modulated OEM System'

        # update parameters
        self.params = dict()
        for key in self.system_defaults:
            self.params[key] = params.get(key, self.system_defaults[key])
        
        # matrices
        self.A = None

    def get_A(self, modes, params, t):
        """Method to obtain the drift matrix.

        Parameters
        ----------
        modes : list
            Values of the modes.
        params : list
            Constant parameters.
        t : float
            Time at which the drift matrix is calculated.
        
        Returns
        -------
        A : numpy.ndarray
            Drift matrix.
        """

        # extract frequently used variables
        Delta_0 = params[6]
        gamma_a, gamma_b, gamma_c = params[7:10]
        g_ab, g_bc = params[10:12]
        Omega_s = params[14]
        omega_c0 = params[15]
        theta = params[16]
        t_mod = params[17]
        t_pos = params[18]
        alpha, beta, chi = modes

        # effective values
        Delta = Delta_0 - 2 * g_ab * np.real(beta)
        G_alpha = g_ab * alpha
        g_1 = - g_bc if t_pos == 'bottom' else g_bc
        G_beta = 2 * g_1 * np.real(beta)
        G_chi = 2 * g_1 * np.real(chi)
        # handle fixed point 
        t = 0 if t is None else t
        # update modulations
        omega_b = np.sqrt(1 + theta * getattr(np, t_mod)(Omega_s * t))

        # initialize drift matrix
        if self.A is None or np.shape(self.A) != (6, 6):
            self.A = np.zeros([6, 6], dtype=np.float_)
        # optical position quadrature
        self.A[0][0] = - gamma_a 
        self.A[0][1] = Delta 
        self.A[0][2] = - 2 * np.imag(G_alpha) 
        # optical momentum quadrature
        self.A[1][0] = - Delta
        self.A[1][1] = - gamma_a
        self.A[1][2] = 2 * np.real(G_alpha)
        # mechanical position quadrature
        self.A[2][2] = - gamma_b
        self.A[2][3] = omega_b
        # mechanical momentum quadrature
        self.A[3][0] = 2 * np.real(G_alpha)
        self.A[3][1] = 2 * np.imag(G_alpha)
        self.A[3][2] = - omega_b
        self.A[3][3] = - gamma_b
        self.A[3][4] = 4 * G_chi
        # LC charge quadrature
        self.A[4][4] = - gamma_c
        self.A[4][5] = omega_c0
        # LC flux quadrature
        self.A[5][2] = 4 * G_chi
        self.A[5][4] = - omega_c0 + 4 * G_beta
        self.A[5][5] = - gamma_c

        return self.A

    def get_coeffs(self, modes, params, t=None):
        """Method to obtain the coefficients of the characteristic equation.

        Parameters
        ----------
        modes : list
            Values of the modes.
        params : list
            Constants parameters.
        t : float
            Time at which the coefficients are calculated.

        Returns
        -------
        coeffs : int
            Coefficients of the characteristic equation.
        """

        # extract frequently used variables
        Delta_0 = params[6]
        gamma_a, gamma_b, gamma_c = params[7:10]
        g_ab, g_bc = params[10:12]
        Omega_s = params[14]
        omega_c0 = params[15]
        theta = params[16]
        t_mod = params[17]
        t_pos = params[18]
        alpha, beta, chi = modes

        # effective values
        Delta = Delta_0 - 2 * g_ab * np.real(beta)
        G_alpha = g_ab * alpha
        g_1 = - g_bc if t_pos == 'bottom' else g_bc
        G_beta = 2 * g_1 * np.real(beta)
        G_chi = 2 * g_1 * np.real(chi)
        # handle fixed point 
        t = 0 if t is None else t
        # update modulations
        omega_b = np.sqrt(1 + theta * getattr(np, t_mod)(Omega_s * t))

        # substituted parameters
        D_2 = Delta**2 + gamma_a**2
        G_2 = np.real(np.conjugate(G_alpha) * G_alpha)
        Omega_b_2 = gamma_b**2 + omega_b**2
        Omega_c_2 = gamma_c**2 + omega_c0 * (omega_c0 - 4 * G_beta)

        # coefficients
        coeffs = list()
        # a_0
        coeffs.append(1)
        # a_1 
        coeffs.append(2 * (gamma_a + gamma_b + gamma_c))
        # a_2
        coeffs.append(D_2**2 + Omega_b_2**2 + Omega_c_2**2 + 4 * (gamma_b * gamma_c + gamma_b * gamma_a + gamma_c * gamma_a))
        # a_3
        coeffs.append(2 * (gamma_b + gamma_c) * D_2**2 + 2 * (Omega_b_2**2 * gamma_c + Omega_c_2**2 * gamma_b) + 2 * gamma_a * (Omega_b_2**2 + Omega_c_2**2) + 8 * gamma_b * gamma_c * gamma_a)
        # a_4
        coeffs.append((Omega_b_2**2 + Omega_c_2**2 + 4 * gamma_b * gamma_c) * D_2**2 + 4 * (Omega_b_2**2 * gamma_c + Omega_c_2**2 * gamma_b) * gamma_a + Omega_b_2**2 * Omega_c_2**2 - 4 * G_2**2 * Delta * omega_b - 16 * G_chi**2 * omega_b * omega_c0)
        # a_5
        coeffs.append(2 * (Omega_b_2**2 * gamma_c + Omega_c_2**2 * gamma_b) * D_2**2 + 2 * Omega_b_2**2 * Omega_c_2**2 * gamma_a - 8 * G_2**2 * Delta * gamma_c * omega_b - 32 * G_chi**2 * gamma_a * omega_b * omega_c0)
        # a_6
        coeffs.append(Omega_b_2**2 * Omega_c_2**2 * D_2**2 - 4 * G_2**2 * Omega_c_2**2 * Delta * omega_b - 16 * G_chi**2 * D_2**2 * omega_b * omega_c0)

        return coeffs

    def get_ivc(self):
        """Method to obtain the initial values and constants required for the IVP.
        
        Returns
        -------
        iv : list
            Initial values of variables.
            First element contains the optical mode.
            Second element contains the mechanical mode.
            Third element contains the electrical mode.
            Remaining :math:`4 \times 3^{2}` elements contain the quadrature correlations.

        c : list
            Constants of the IVP.
            First :math:`4 \times 3^{2}` elements contain the noise matrix.
            Rest of the elements contain the system parameters ``params`` in the following order:
            ========    =====================================================
            index       parameter
            ========    =====================================================
            0           laser base amplitude :math:`A_{l0}`.
            1           laser Stokes sideband amplitude :math:`A_{l-}`.
            2           laser anti-Stokes sideband amplitude :math:`A_{l+}`.
            3           voltage base amplitude :math:`A_{v0}`.
            4           voltage Stokes sideband amplitude :math:`A_{v-}`.
            5           voltage anti-Stokes sideband amplitude :math:`A_{v+}`.
            6           cavity detuning :math:`\Delta_{0}`.
            7           optical decay rate :math:`\gamma_{a}`.
            8           mechanical damping rate :math:`\gamma_{b}`.
            9           LC circuit damping rate :math:`\gamma_{c}`.
            10          optomechanical coupling constant :math:`g_{ab}`.
            11          electromechanical coupling constant :math:`g_{bc}`.
            12          laser modulation frequency :math:`\Omega_{l}`.
            13          voltage modulation frequency :math:`\Omega_{v}`.
            14          spring constant modulation frequency :math:`\Omega_{s}`.
            15          LC circuit frequency :math:`\omega_{c}`.
            16          spring constant modulation amplitude :math:`\theta`.
            17          spring constant modulation type ``t_mod``.
            18          position of the mechanical membrane ``t_pos``.
            ========    =====================================================
        """

        # extract frequently used variables
        A_ls    = self.params['A_ls']
        A_vs    = self.params['A_vs']
        Delta_0 = self.params['Delta_0']
        gammas  = self.params['gammas']
        gs      = self.params['gs']
        n_ths   = self.params['n_ths']
        Omegas  = self.params['Omegas']
        omega_c0= self.params['omega_c0']
        theta   = self.params['theta']
        t_mod   = self.params['t_mod']
        t_pos   = self.params['t_pos']

        # validate parameters
        assert t_mod in ['cos', 'sin'], 'Parameter ``t_mod`` should be either "sin" or "cos"'
        assert t_pos in ['top', 'bottom'], 'Parameter ``t_pos`` should be either "top" or "bottom"'
 
        # initial mode values as 1D list
        modes_0 = np.zeros(3, dtype=np.complex_).tolist()

        # initial quadrature correlations
        corrs_0 = np.zeros([6, 6], dtype=np.float_)
        corrs_0[0][0] = 0.5 
        corrs_0[1][1] = 0.5
        corrs_0[2][2] = (n_ths[0] + 0.5)
        corrs_0[3][3] = (n_ths[0] + 0.5)
        corrs_0[4][4] = (n_ths[1] + 0.5)
        corrs_0[5][5] = (n_ths[1] + 0.5)

        # convert to 1D list and concatenate all variables
        iv = modes_0 + [np.complex(element) for element in corrs_0.flatten()]

        # noise correlation matrix
        D = np.zeros([6, 6], dtype=np.float_)
        # optical mode
        D[0][0] = gammas[0]
        D[1][1] = gammas[0]
        # mechanical mode
        D[2][2] = gammas[1] * (2 * n_ths[0] + 1) 
        D[3][3] = gammas[1] * (2 * n_ths[0] + 1) 
        # LC mode
        D[4][4] = gammas[2] * (2 * n_ths[1] + 1) 
        D[5][5] = gammas[2] * (2 * n_ths[1] + 1) 
        
        # constant parameters
        params = A_ls + \
            A_vs + \
            [Delta_0] + \
            gammas + \
            gs + \
            Omegas + \
            [omega_c0, theta] + \
            [t_mod, t_pos]

        # all constants
        c = D.flatten().tolist() + params

        return iv, c

    def get_mode_rates(self, modes, params, t):
        """Method to obtain the rates of the optical and mechanical modes.

        Parameters
        ----------
        modes : list
            Values of the modes.
        params : list
            Constants parameters.
        t : float
            Time at which the rates are calculated.
        
        Returns
        -------
        mode_rates : list
            Rates for each mode.
        """

        # extract frequently used variables
        A_l0, A_lm, A_lp = params[0:3]
        A_v0, A_vm, A_vp = params[3:6]
        Delta_0 = params[6]
        gamma_a, gamma_b, gamma_c = params[7:10]
        g_ab, g_bc = params[10:12]
        Omega_l, Omega_v, Omega_s = params[12:15]
        omega_c0 = params[15]
        theta = params[16]
        t_mod = params[17]
        t_pos = params[18]
        alpha, beta, chi = modes

        # effective values
        Delta = Delta_0 - 2 * g_ab * np.real(beta)
        g_bc = - g_bc if t_pos == 'bottom' else g_bc 
        # handle fixed point 
        t = 0 if t is None else t
        # update modulations
        A_l = A_l0 + A_lm * np.exp(1j * Omega_l * t) + A_lp * np.exp(-1j * Omega_l * t)
        A_v = A_v0 + A_vm * np.exp(1j * Omega_v * t) + A_vp * np.exp(-1j * Omega_v * t)
        omega_b = np.sqrt(1 + theta * getattr(np, t_mod)(Omega_s * t))

        # calculate mode rates
        # optical
        dalpha_dt = - (gamma_a + 1j * Delta) * alpha + A_l
        # mechanical
        dbeta_dt = 1j * g_ab * np.conjugate(alpha) * alpha - (gamma_b + 1j * omega_b) * beta + 4j * g_bc * np.real(chi)**2
        # circuit
        dchi_dt = 8j * g_bc * np.real(beta) * np.real(chi) - (gamma_c + 1j * omega_c0) * chi + 1j * A_v

        # arrange rates
        mode_rates = [dalpha_dt, dbeta_dt, dchi_dt]

        return mode_rates

    def get_oss_modes(self, params):
        """Method to obtain the steady state optical and mechanical mode apmlitudes.
        
        Parameters
        ----------
        params : list
            Constant parameters of the system.
        
        Returns 
        -------
        Modes : list
            Optical and mechanical mode amplitudes.
        """
        
        # extract frequently used variables
        A_l0 = params[0]
        A_v0 = params[3]
        Delta_0 = params[6]
        gamma_a, gamma_b, gamma_c = params[7:10]
        g_ab, g_bc = params[10:12]
        omega_c0 = params[15]
        theta = params[16]
        t_pos = params[18]

        # effective values
        g_bc = - g_bc if t_pos == 'bottom' else g_bc 
        A_l = A_l0
        A_v = A_v0
        omega_b = np.sqrt(1 + theta)

        # polynomial coefficients
        coeff_0 = 16 * omega_c0**2 * g_ab**2 * g_bc**2 * (gamma_b**2 + omega_b**2)
        coeff_1 = - 8 * omega_c0 * g_ab * g_bc * (4 * Delta_0 * omega_c0 * g_bc + g_ab * (gamma_c**2 + omega_c0**2)) * (gamma_b**2 + omega_b**2)
        coeff_2 = (16 * (gamma_a**2 + Delta_0**2) * omega_c0**2 * g_bc**2 + g_ab * (gamma_c**2 + omega_c0**2) * (16 * Delta_0 * omega_c0 * g_bc + g_ab * (gamma_c**2 + omega_c0**2))) * (gamma_b**2 + omega_b**2)
        coeff_3 = (- 2 * Delta_0 * g_ab * (gamma_c**2 + omega_c0**2)**2 - 8 * omega_c0 * g_bc * (gamma_c**2 + omega_c0**2) * (gamma_a**2 + Delta_0**2)) * (gamma_b**2 + omega_b**2) - 32 * omega_b * omega_c0**2 * g_ab * g_bc**2 * A_l**2 - 8 * omega_b * omega_c0**2 * g_ab**2 * g_bc * A_v**2
        coeff_4 = (gamma_a**2 + Delta_0**2) * (gamma_c**2 + omega_c0**2)**2 * (gamma_b**2 + omega_b**2) + 16 * omega_b * omega_c0 * g_ab * g_bc * A_l**2 * (gamma_c**2 + omega_c0**2) + 16 * omega_b * omega_c0**2 * g_ab * g_bc * A_v**2 * Delta_0
        coeff_5 = - 2 * omega_b * g_ab * A_l**2 * (gamma_c**2 + omega_c0**2) - 8 * omega_b * omega_c0**2 * g_bc * A_v**2 * (gamma_a**2 + Delta_0**2)

        # get roots
        roots = np.roots([coeff_0, coeff_1, coeff_2, coeff_3, coeff_4, coeff_5])
        # sum of beta_0s and its conjugate
        beta_0s_sums = list()
        # retain real roots
        for root in roots:
            if np.imag(root) == 0.0:
                beta_0s_sums.append(np.real(root))

        # initialize lists
        Modes = list()

        for beta_0s_sum in beta_0s_sums:
            # calculate mode amplitudes
            # optical mode
            alpha_s = A_l / (gamma_a + 1j * Delta_0 - 1j * g_ab * beta_0s_sum)
            # sum of beta_1s and its conjugate
            beta_1s_sum = 2 * omega_c0 * A_v / (gamma_c**2 + omega_c0**2 - 4 * omega_c0 * g_bc * beta_0s_sum)
            # mechanical mode
            beta_0s = (1j * g_ab * np.conjugate(alpha_s) * alpha_s + 1j * g_bc * beta_1s_sum**2) / (gamma_b + 1j * omega_b)
            # LC circuit mode
            beta_1s = (1j * A_v + 2j * g_bc * beta_0s_sum * beta_1s_sum) / (gamma_c + 1j * omega_c0)

            # append to list
            Modes.append([alpha_s, beta_0s, beta_1s])

        return Modes