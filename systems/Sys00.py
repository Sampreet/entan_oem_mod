#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate an OEM system driven by modulated lasers and voltages."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-05-18'
__updated__ = '2021-05-19'

# dependencies
import numpy as np
import scipy.constants as sc

# qom modules
from qom.systems import SODMSystem

class Sys00(SODMSystem):
    """Class to simulate an OEM system driven by modulated lasers and voltages.

    Parameters
    ----------
    params : dict
        Parameters for the system.
    """

    def __init__(self, params):
        """Class constructor for Sys00."""
        
        # initialize super class
        super().__init__(params)

        # set attributes
        self.code = 'sys_00'
        self.name = 'Modulated OEM System'
        # default parameters
        self.params = {
            'Delta_0': params.get('Delta_0', 1),
            'E_0': params.get('E_0', 200),
            'E_1': params.get('E_1', 2),
            'gammas': params.get('gammas', [0.005, 0.005]),
            'gs': params.get('gs', [0.005, 0.005]),
            'kappa': params.get('kappa', 0.15),
            'n_ths': params.get('n_ths', [0, 0]),
            'Omegas': params.get('Omegas', [2, 2]),
            'omegas': params.get('omegas', [1, 1]),
            'V_0': params.get('V_0', 100),
            'V_1': params.get('V_1', 1)
        }
        # drift matrix
        self.A = None

    def get_A(self, modes, params):
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
        Delta_0 = params[0]
        gammas  = [params[3], params[4]]
        gs      = [params[5], params[6]]
        kappa   = params[7]
        omegas  = [params[10], params[11]]
        alpha   = modes[0]
        betas   = [modes[1], modes[2]]

        # effective values
        Delta = Delta_0 - 2 * gs[0] * np.real(betas[0])
        G_0 = gs[0] * alpha
        G_10 = 2 * gs[1] * np.real(betas[0])
        G_11 = 2 * gs[1] * np.real(betas[1])

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
        self.A[2][4] = 4 * np.imag(G_11)
        # mechanical momentum quadrature
        self.A[3][0] = 2 * np.real(G_0)
        self.A[3][1] = 2 * np.imag(G_0)
        self.A[3][2] = - omegas[0]
        self.A[3][3] = - gammas[0]
        self.A[3][4] = - 4 * np.real(G_11)
        # LC charge quadrature
        self.A[4][2] = 4 * np.imag(G_11)
        self.A[4][4] = - gammas[1] + 4 * np.imag(G_10)
        self.A[4][5] = omegas[1]
        # LC flux quadrature
        self.A[5][2] = - 4 * np.real(G_11)
        self.A[5][4] = - omegas[1] - 4 * np.real(G_10)
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
            Next element contains the laser detuning.
            Next 2 elements contain the laser base and modulation amplitudes.
            Next 2 elements contain the mechanical and LC decay rates.
            Next 2 elements contain the mechanical and LC coupling strengths.
            Next element contains the optical decay rate.
            Next 2 elements contain the laser and voltage modulation frequencies.
            Next 2 elements contain the mechanical and LC frequencies.
            Next 2 elements contain the voltage base and modulation amplitudes.
        """

        # extract frequently used variables
        Delta_0 = self.params['Delta_0']
        E_0     = self.params['E_0']
        E_1     = self.params['E_1']
        gammas  = self.params['gammas']
        gs      = self.params['gs']
        kappa   = self.params['kappa']
        n_ths   = self.params['n_ths']
        Omegas  = self.params['Omegas']
        omegas  = self.params['omegas']
        V_0     = self.params['V_0']
        V_1     = self.params['V_1']
 
        # initial mode values as 1D list
        u_0 = np.zeros(3, dtype=np.complex_).tolist()

        # initial quadrature correlations
        V_0 = np.zeros([6, 6], dtype=np.float_)
        V_0[0][0] = 1/2 
        V_0[1][1] = 1/2
        V_0[2][2] = (n_ths[0] + 1/2)
        V_0[3][3] = (n_ths[0] + 1/2)
        V_0[4][4] = (n_ths[1] + 1/2)
        V_0[5][5] = (n_ths[1] + 1/2)

        # convert to 1D list and concatenate all variables
        iv = u_0 + [np.complex(element) for element in V_0.flatten()]

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
        params = [Delta_0] + \
            [E_0, E_1] + \
            gammas + \
            gs + \
            [kappa] + \
            Omegas + \
            omegas + \
            [V_0, V_1]

        # all constants
        c = D.flatten().tolist() + params

        return iv, c

    def get_rates_modes(self, modes, params, t):
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
        Delta_0 = params[0]
        E_0     = params[1]
        E_1     = params[2]
        gammas  = [params[3], params[4]]
        gs      = [params[5], params[6]]
        kappa   = params[7]
        Omegas  = [params[8], params[9]]
        omegas  = [params[10], params[11]]
        V_0     = params[12]
        V_1     = params[13]
        alpha   = modes[0]
        betas   = [modes[1], modes[2]]

        # effective values
        Delta = Delta_0 - 2 * gs[0] * np.real(betas[0])

        # calculate rates
        # optical mode
        dalpha_dt = - (kappa + 1j * Delta) * alpha + E_0 + E_1 * np.cos(Omegas[0] * t)
        # mechanical mode
        dbeta_0_dt = 1j * gs[0] * np.conjugate(alpha) * alpha - (gammas[0] + 1j * omegas[0]) * betas[0] - 4j * gs[1] * np.real(betas[1])**2
        # circuit mode
        dbeta_1_dt = - 8j * gs[1] * np.real(betas[0]) * np.real(betas[1]) - (gammas[1] + 1j * omegas[1]) * betas[1] + 1j * (V_0 + V_1 * np.cos(Omegas[1] * t))

        # arrange rates
        mode_rates = [dalpha_dt, dbeta_0_dt, dbeta_1_dt]

        return mode_rates