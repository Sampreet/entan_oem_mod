#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to simulate the OEM system in New J. Phys. **22**, 063041 (2020)."""

__authors__ = ['Sampreet Kalita']
__created__ = '2020-05-14'
__updated__ = '2021-05-19'

# dependencies
import numpy as np
import scipy.constants as sc

# qom modules
from qom.systems import SODMSystem

class NJP00(SODMSystem):
    """Class to simulate the OEM system in New J. Phys. **22**, 063041 (2020).

    Parameters
    ----------
    params : dict
        Parameters for the system.
    """

    def __init__(self, params):
        """Class constructor for NJP00."""
        
        # initialize super class
        super().__init__(params)

        # set attributes
        self.code = 'njp_00'
        self.name = 'OEM System in NJP 22, 063041'  
        # default parameters
        self.params = {
            'Delta_norm': params.get('Delta_norm', 1.0),
            'Delta_type': params.get('Delta_type', 'absolute'),
            'G_norm': params.get('G_norm', 0.3),
            'g_norm': params.get('g_norm', 0.3),
            'gamma_LC_norm': params.get('gamma_LC_norm', 1.0),
            'gamma_m_norm': params.get('gamma_m_norm', 1.0),
            'kappa_norm': params.get('kappa_norm', 1.0),
            'omega_LC_norm': params.get('omega_LC_norm', 1.0),
            'omega_m': params.get('omega_m', 1.0),
            'T_LC': params.get('n_LC', 0),
            'T_m': params.get('n_m', 0)
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
        Delta           = params[0]
        G               = params[1]
        g               = params[2]
        gamma_LC        = params[3]
        gamma_m         = params[4]
        kappa           = params[5]
        omega_LC_prime  = params[6]
        omega_m         = params[7]

        # drift matrix
        if self.A is None or np.shape(self.A) != (6, 6):
            self.A = np.zeros([6, 6], dtype=np.float_)
        self.A[0][0] = - kappa
        self.A[0][1] = Delta
        self.A[1][0] = - Delta
        self.A[1][1] = - kappa
        self.A[1][2] = G

        self.A[2][3] = omega_m
        self.A[3][0] = G
        self.A[3][2] = - omega_m
        self.A[3][3] = - gamma_m
        self.A[3][4] = - g

        self.A[4][5] = omega_LC_prime
        self.A[5][2] = - g
        self.A[5][4] = - omega_LC_prime
        self.A[5][5] = - gamma_LC

        return self.A

    def get_ivc(self):
        """Function to obtain the initial values and constants required for the IVP.
        
        Returns
        -------
        iv : list
            Initial values of variables.

        c : list
            Constant parameters.
            First (4 * 3^2) elements contain the noise matrix.
            Next element contains the laser detuning.
            Next element contains the effective LC coupling strength.
            Next element contains the effective OM coupling strength.
            Next element contains the LC decay rate.
            Next element contains the mechanical decay rate.
            Next element contains the optical decay rate.
            Next element contains the modified LC frequency.
            Next element contains the mechanical frequency.
        """
        
        # extract frequently used variables
        Delta_norm      = self.params['Delta_norm']
        Delta_type      = self.params['Delta_type']
        omega_LC_norm   = self.params['omega_LC_norm']
        omega_m         = self.params['omega_m']
        G_norm          = self.params['G_norm']
        g_norm          = self.params['g_norm']
        gamma_LC_norm   = self.params['gamma_LC_norm']
        gamma_m_norm    = self.params['gamma_m_norm']
        kappa_norm      = self.params['kappa_norm']
        T_LC            = self.params['T_LC']
        T_m             = self.params['T_m']

        # effective cavity-laser detuning
        if Delta_type == 'relative':
            Delta = Delta_norm * omega_LC_norm * omega_m
        else:
            Delta = Delta_norm * omega_m
        # LC frequency
        omega_LC = omega_LC_norm * omega_m
        # effective LC frequency
        omega_LC_prime = omega_LC

        # update variables
        G       = G_norm * kappa_norm * omega_m
        g       = g_norm * kappa_norm * omega_m
        gamma_LC= gamma_LC_norm * omega_LC
        gamma_m = gamma_m_norm * omega_m
        kappa   = kappa_norm * omega_m
        n_LC    = sc.k * T_LC / sc.hbar / omega_LC
        n_m     = sc.k * T_m / sc.hbar / omega_m

        # noise matrix
        D = np.zeros([6, 6], dtype=np.float_)
        D[0][0] = kappa
        D[1][1] = kappa
        D[3][3] = gamma_m * (2 * n_m + 1)
        D[5][5] = gamma_LC * (2 * n_LC + 1)
        
        # constant parameters
        params = [Delta] + \
            [G] + \
            [g] + \
            [gamma_LC] + \
            [gamma_m] + \
            [kappa] + \
            [omega_LC_prime] + \
            [omega_m]

        # all constants
        c = D.flatten().tolist() + params

        return None, c