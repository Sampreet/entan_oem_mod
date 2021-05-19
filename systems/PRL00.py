#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate the OEM system in Phys. Rev. Lett. **103** 213603 (2009)."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-05-15'
__updated__ = '2021-05-19'

# dependencies
import numpy as np
import scipy.constants as sc

# qom modules
from qom.systems import SOSMSystem

class PRL00(SOSMSystem):
    """Class to simulate the gently modulated QOM system in Phys. Rev. Lett. **103** 213603 (2009).

    Parameters
    ----------
    params : dict
        Parameters for the system.
    """

    def __init__(self, params):
        """Class constructor for PRL00."""
        
        # initialize super class
        super().__init__(params)

        # set attributes
        self.code = 'prl_00'
        self.name = 'Gently Modulated QOM System'
        # default parameters
        self.params = {
            'F': params.get('F', 1.4e4),
            'lambda_l': params.get('lambda_l', 1064e-9),
            'L': params.get('L', 25e-3),
            'm': params.get('m', 150e-9),
            'omega_m': params.get('omega_m', 2e6 * np.pi),
            'P_0': params.get('P_0', 10e-3),
            'P_1': params.get('P_1', 2e-3),
            'Q': params.get('Q', 1e6),
            'T': params.get('T', 0.1)
        }
        # drift matrices
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
        G_0     = params[3]
        gamma_m = params[4]
        kappa   = params[5]
        Omega   = params[6]
        omega_m = params[7]
        alpha   = modes[0]
        beta    = modes[1]

        # time frame
        tau = 2 * np.pi / Omega

        # effective values
        Delta = Delta_0 - np.sqrt(2) * G_0 * np.real(beta)
        G = np.sqrt(2) * G_0 * alpha

        # initialize drift matrix
        if self.A is None or np.shape(self.A) != (4, 4):
            self.A = np.zeros([4, 4], dtype=np.float_)
        # optical position quadrature
        self.A[0][0] = - kappa 
        self.A[0][1] = Delta 
        self.A[0][2] = - np.imag(G) 
        # optical momentum quadrature
        self.A[1][0] = - Delta
        self.A[1][1] = - kappa
        self.A[1][2] = np.real(G)
        # mechanical position quadrature
        self.A[2][3] = omega_m
        # mechanical momentum quadrature
        self.A[3][0] = np.real(G)
        self.A[3][1] = np.imag(G)
        self.A[3][2] = - omega_m
        self.A[3][3] = - gamma_m

        return self.A * tau

    def get_ivc(self):
        """Function to obtain the initial values and constants required for the IVP.
        
        Returns
        -------
        iv : list
            Initial values of variables.
            First element contains the optical mode.
            Second element contains the mechanical mode.
            Remaining elements contain the quadrature correlations.

        c : list
            Constant parameters.
            First (4 * 2^2) elements contain the noise matrix.
            Next element contains the laser detuning.
            Next 2 elements contain the laser base and modulation amplitudes.
            Next element contains the coupling strength.
            Next element contains the mechanical decay rate.
            Next element contains the optical decay rate.
            Next element contains the laser modulation frequency.
            Next element contains the mechanical frequency.
        """

        # extract frequently used variables
        F       = self.params['F']
        L       = self.params['L']
        lambda_l= self.params['lambda_l']
        m       = self.params['m']
        omega_m = self.params['omega_m']
        P_0     = self.params['P_0']
        P_1     = self.params['P_1']
        Q       = self.params['Q']
        T       = self.params['T']

        # laser detuning
        Delta_0 = omega_m
        # laser frequency
        omega_l = 2 * np.pi * sc.c / lambda_l
        # optical frequency
        omega_c = Delta_0 + omega_l
        # coupling strength
        G_0 = np.sqrt(sc.hbar / (m * omega_m)) * omega_c / L
        # modulation frequency
        Omega = 2 * omega_m
        # optical decay rate
        kappa = np.pi * sc.c / (2 * F * L)
        # mechanical decay rates
        gamma_m = omega_m / Q
        # thermal phonon number
        if T != 0.0 or T != 0:
            n_th = 1 / (np.exp(sc.hbar * omega_m / (sc.k * T)) - 1)
        else:
            n_th = 0
        # laser amplitudes
        E_0 = np.sqrt(2 * kappa * P_0 / (sc.hbar * omega_l)) 
        E_1 = np.sqrt(2 * kappa * P_1 / (sc.hbar * omega_l))
        # time frame
        tau = 2 * np.pi / Omega
 
        # initial mode values as 1D list
        modes_0 = np.zeros(2, dtype=np.complex_).tolist()

        # initial quadrature correlations
        corrs_0 = np.zeros([4, 4], dtype=np.float_)
        corrs_0[0][0] = 1/2 
        corrs_0[1][1] = 1/2
        corrs_0[2][2] = (n_th + 1/2)
        corrs_0[3][3] = (n_th + 1/2)

        # convert to 1D list and concatenate all variables
        iv = modes_0 + [np.complex(element) for element in corrs_0.flatten()]

        # noise correlation matrix
        D = np.zeros([4, 4], dtype=np.float_)
        # optical mode
        D[0][0] = kappa
        D[1][1] = kappa
        # mechanical mode
        D[3][3] = gamma_m * (2 * n_th + 1) 
        
        # constant parameters
        params = [Delta_0] + \
            [E_0, E_1] + \
            [G_0] + \
            [gamma_m] + \
            [kappa] + \
            [Omega] + \
            [omega_m]

        # all constants
        c = (D * tau).flatten().tolist() + params

        return iv, c

    def get_mode_rates(self, modes, params, t):
        """Function to obtain the rates of the optical and mechanical modes.

        Parameters
        ----------
        modes : list
            Values of the modes.
        params : list
            Constant parameters.
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
        G_0     = params[3]
        gamma_m = params[4]
        kappa   = params[5]
        Omega   = params[6]
        omega_m = params[7]
        alpha   = modes[0]
        beta    = modes[1]

        # time frame
        tau = 2 * np.pi / Omega

        # effective values
        Delta = Delta_0 - np.sqrt(2) * G_0 * np.real(beta)
        G = np.sqrt(2) * G_0 * alpha

        # calculate rates
        dalpha_dt = (- (kappa + 1j * Delta) * alpha + E_0 + E_1 * (np.exp(- 1j * Omega * t * tau) + np.exp(1j * Omega * t * tau)))
        dbeta_dt = (1j * G * np.conjugate(alpha) / 2 - (gamma_m + 1j * omega_m) * beta)

        # arrange rates
        mode_rates = [dalpha_dt * tau, dbeta_dt * tau]

        return mode_rates