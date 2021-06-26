#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate an OEM system driven by modulated lasers and voltages."""

__authors__ = ['Sampreet Kalita']
__created__ = '2021-05-18'
__updated__ = '2021-06-26'

# dependencies
import numpy as np

# qom modules
from qom.systems import SODMSystem

class Mod00(SODMSystem):
    """Class to simulate an OEM system driven by modulated lasers and voltages.

    Parameters
    ----------
    params : dict
        Parameters for the system.
    """

    def __init__(self, params):
        """Class constructor for Mod00."""
        
        # initialize super class
        super().__init__(params)

        # set attributes
        self.code = 'mod_00'
        self.name = 'Modulated OEM System'
        # default parameters
        self.params = {
            'A_ls': params.get('A_ls', [25.0, 2.5]),
            'A_vs': params.get('A_vs', [10.0, 1.0]),
            'Delta_0': params.get('Delta_0', 1.0),
            'gammas': params.get('gammas', [5e-3, 5e-1]),
            'gs': params.get('gs', [5e-3, 5e-6]),
            'kappa': params.get('kappa', 0.15),
            'n_ths': params.get('n_ths', [0, 0]),
            'Omegas': params.get('Omegas', [2.0, 2.0]),
            'omegas': params.get('omegas', [1.0, 1.0]),
            't_mod': params.get('t_mod', 'cos'),
            't_pos': params.get('t_pos', 'top')
        }
        # drift matrix
        self.A = None

    def get_A(self, modes, params, t):
        """Function to obtain the drift matrix.

        Parameters
        ----------
        modes : list
            Values of the optical and mechancial modes.
        params : list
            Constant parameters.
        
        Returns
        -------
        A : list
            Drift matrix.
        """

        # extract frequently used variables
        Delta_0 = params[4]
        gammas  = [params[5], params[6]]
        gs      = [params[7], params[8]]
        kappa   = params[9]
        omegas  = [params[12], params[13]]
        t_pos   = params[15]
        alpha   = modes[0]
        betas   = [modes[1], modes[2]]

        # effective values
        Delta = Delta_0 - 2 * gs[0] * np.real(betas[0])
        G_0 = gs[0] * alpha
        g_1 = - gs[1] if t_pos == 'bottom' else gs[1]
        G_10 = 2 * g_1 * np.real(betas[0])
        G_11 = 2 * g_1 * np.real(betas[1])

        # initialize drift matrix
        if self.A is None or np.shape(self.A) != (6, 6):
            self.A = np.zeros([6, 6], dtype=np.float_)
        # optical position quadrature
        self.A[0][0] = - kappa 
        self.A[0][1] = Delta 
        self.A[0][2] = - 2 * np.imag(G_0) 
        # optical momentum quadrature
        self.A[1][0] = - Delta
        self.A[1][1] = - kappa
        self.A[1][2] = 2 * np.real(G_0)
        # mechanical position quadrature
        self.A[2][2] = - gammas[0]
        self.A[2][3] = omegas[0]
        # mechanical momentum quadrature
        self.A[3][0] = 2 * np.real(G_0)
        self.A[3][1] = 2 * np.imag(G_0)
        self.A[3][2] = - omegas[0]
        self.A[3][3] = - gammas[0]
        self.A[3][4] = 4 * G_11
        # LC charge quadrature
        self.A[4][4] = - gammas[1]
        self.A[4][5] = omegas[1]
        # LC flux quadrature
        self.A[5][2] = 4 * G_11
        self.A[5][4] = - omegas[1] + 4 * G_10
        self.A[5][5] = - gammas[1]

        return self.A

    def get_ivc(self):
        """Function to obtain the initial values and constants required for the IVP.
        
        Returns
        -------
        iv : list
            Initial values of variables.
            First element contains the optical mode.
            Second element contains the mechanical mode.
            Third element contains the circuit mode.
            Remaining elements contain the quadrature correlations.

        c : list
            Constants of the IVP.
            First (4 * 3^2) elements contain the noise matrix.
            Next 2 elements contain the laser base and modulation amplitudes.
            Next 2 elements contain the voltage base and modulation amplitudes.
            Next element contains the laser detuning.
            Next 2 elements contain the mechanical and LC decay rates.
            Next 2 elements contain the mechanical and LC coupling strengths.
            Next element contains the optical decay rate.
            Next 2 elements contain the laser and voltage modulation frequencies.
            Next 2 elements contain the mechanical and LC frequencies.
            Next element contains the type of modulation function.
            Next element contains the position of the mechanical element.
        """

        # extract frequently used variables
        A_ls    = self.params['A_ls']
        A_vs    = self.params['A_vs']
        Delta_0 = self.params['Delta_0']
        gammas  = self.params['gammas']
        gs      = self.params['gs']
        kappa   = self.params['kappa']
        n_ths   = self.params['n_ths']
        Omegas  = self.params['Omegas']
        omegas  = self.params['omegas']
        t_mod   = self.params['t_mod']
        t_pos   = self.params['t_pos']
 
        # initial mode values as 1D list
        modes_0 = np.zeros(3, dtype=np.complex_).tolist()

        # initial quadrature correlations
        corrs_0 = np.zeros([6, 6], dtype=np.float_)
        corrs_0[0][0] = 1/2 
        corrs_0[1][1] = 1/2
        corrs_0[2][2] = (n_ths[0] + 1/2)
        corrs_0[3][3] = (n_ths[0] + 1/2)
        corrs_0[4][4] = (n_ths[1] + 1/2)
        corrs_0[5][5] = (n_ths[1] + 1/2)

        # convert to 1D list and concatenate all variables
        iv = modes_0 + [np.complex(element) for element in corrs_0.flatten()]

        # noise correlation matrix
        D = np.zeros([6, 6], dtype=np.float_)
        # optical mode
        D[0][0] = kappa
        D[1][1] = kappa
        # mechanical mode
        D[2][2] = gammas[0] * (2 * n_ths[0] + 1) 
        D[3][3] = gammas[0] * (2 * n_ths[0] + 1) 
        # LC mode
        D[4][4] = gammas[1] * (2 * n_ths[1] + 1) 
        D[5][5] = gammas[1] * (2 * n_ths[1] + 1) 
        
        # constant parameters
        params = [A_ls[0], A_ls[1]] + \
            [A_vs[0], A_vs[1]] + \
            [Delta_0] + \
            gammas + \
            gs + \
            [kappa] + \
            Omegas + \
            omegas + \
            [t_mod, t_pos]

        # all constants
        c = D.flatten().tolist() + params

        return iv, c

    def get_mode_rates(self, modes, params, t):
        """Function to obtain the rates of the optical and mechanical modes.

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
        A_ls    = [params[0], params[1]]
        A_vs    = [params[2], params[3]]
        Delta_0 = params[4]
        gammas  = [params[5], params[6]]
        gs      = [params[7], params[8]]
        kappa   = params[9]
        Omegas  = [params[10], params[11]]
        omegas  = [params[12], params[13]]
        t_mod   = params[14]
        t_pos   = params[15]
        alpha   = modes[0]
        betas   = [modes[1], modes[2]]

        # effective values
        Delta = Delta_0 - 2 * gs[0] * np.real(betas[0])
        g_1 = - gs[1] if t_pos == 'bottom' else gs[1] 
        func_mod = lambda Theta : {
            'exp': np.exp(1j * Theta),
            'cos': np.cos(Theta),
            'sin': np.sin(Theta)
        }.get(t_mod, np.cos(Theta))

        # calculate rates
        # optical mode
        dalpha_dt = - (kappa + 1j * Delta) * alpha + A_ls[0] + A_ls[1] * func_mod(Omegas[0] * t)
        # mechanical mode
        dbeta_0_dt = 1j * gs[0] * np.conjugate(alpha) * alpha - (gammas[0] + 1j * omegas[0]) * betas[0] + 4j * g_1 * np.real(betas[1])**2
        # circuit mode
        dbeta_1_dt = 8j * g_1 * np.real(betas[0]) * np.real(betas[1]) - (gammas[1] + 1j * omegas[1]) * betas[1] + 1j * (A_vs[0] + A_vs[1] * func_mod(Omegas[1] * t))

        # arrange rates
        mode_rates = [dalpha_dt, dbeta_0_dt, dbeta_1_dt]

        return mode_rates