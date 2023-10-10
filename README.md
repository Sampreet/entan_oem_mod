# Significant Optoelectrical Entanglement and Mechanical Squeezing in a Multi-modulated Optoelectromechanical System

[![Manuscript Version](https://img.shields.io/badge/manuscript-4.0-red?style=for-the-badge)](https://doi.org/10.1103/PhysRevA.106.043501)
[![Toolbox Version](https://img.shields.io/badge/qom-v1.0.1-red?style=for-the-badge)](https://sampreet.github.io/qom-docs/v1.0.1)

> A collection of all data and scripts for the work.

Author | Affiliation
------------ | -------------
[Sampreet Kalita](https://www.iitg.ac.in/stud/sampreet/) | Department of Physics, Indian Institute of Technology Guwahati, Assam 781039, India
[Saumya Shah Amit](https://www.iitg.ac.in/stud/shah18/) | Department of Physics, Indian Institute of Technology Guwahati, Assam 781039, India
[Amarendra Kumar Sarma](https://www.iitg.ac.in/aksarma/) | Department of Physics, Indian Institute of Technology Guwahati, Assam 781039, India

## About the Work

We propose the effective generation of entangled and squeezed states in an optoelectromechanical system comprising of a macroscopic LC electrical circuit and an optomechanical system.
We notice an enhancement in the optoelectrical entanglement. 
This boost is obtained by application of modulations in the laser drive amplitude, the voltage drive amplitude and the spring constant of the moveable end-mirror. 
The maximum amount of entanglement is observed to be primarily dependent on the voltage modulation. 
Alongside the generated entanglement, we also study the variation of squeezing in the mechanical mode for different parameter regimes.
The observation of maximum squeezing and maximum entanglement windows for the system, when all three types of modulations are applied, is reported.

## Related Works

* D. Vitali, P. Tombesi, M. J. Woolley, A. C. Doherty and G. J. Milburn, *Entangling a Nanomechanical Resonator and a Superconducting Microwave Cavity*, [Phys. Rev. A **76**, 042336](https://doi.org/10.1103/PhysRevA.76.042336) (2007)

* A. Mari and J. Eisert, *Gently Modulating Optomechanical Systems*, [Phys. Rev. Lett. **103**, 213603](https://doi.org/10.1103/PhysRevLett.103.213603) (2009)

* S. Barzanjeh, D. Vitali, P. Tombesi and G. J. Milburn, *Entangling Optical and Microwave Cavity Modes by means of a Nanomechanical Resonator*, [Phys. Rev. A **84**, 042342](https://doi.org/10.1103/PhysRevA.84.042342) (2011)

* A. Farace and V. Giovannetti, *Enhancing Quantum Effects via Periodic Modulations in Optomechanical Systems*, [Phys. Rev. A **86**, 013820](https://doi.org/10.1103/PhysRevA.86.013820) (2012)

* Y.-D. Wang and A. A. Clerk, *Reservoir-engineered Entanglement in Optomechanical Systems*, [Phys. Rev. Lett. **110**, 253601](https://doi.org/10.1103/PhysRevLett.110.253601) (2013)

* R.-X. Chen, L.-T. Shen, Z.-B. Yang, H.-Z. Wu and S.-B. Zheng, *Enhancement of Entanglement in Distant Mechanical Vibrations via Modulation in a Coupled Optomechanical System*, [Phys. Rev. A **89**, 023843](https://link.aps.org/doi/10.1103/PhysRevA.89.023843) (2014)

* E. A. Sete, H. Eleuch and C. H. Raymond Ooi, *Light-to-matter Entanglement Transfer in Optomechanics*, [J. Opt. Soc. Am. B **31**, 2821](https://doi.org/10.1364/JOSAB.31.002821) (2014)

* S. Huang, *Quantum State Transfer in Cavity Electro-optic Modulators*, [Phys. Rev. A **92**, 043845](https://doi.org/10.1103/PhysRevA.92.043845) (2015)

* M. Wang, X.-Y. Lu, Y.-D. Wang, J. Q. You and Y. Wu, *Macroscopic Quantum Entanglement in Modulated Optomechanics*, [Phys. Rev. A **94**, 053807](https://doi.org/10.1103/PhysRevA.94.053807) (2016)

* D. Bothner, S. Yanai, A. Iniguuz-Rabago, M. Yaun, Y. M. Blanter and G. A . Steele, *Cavity Electromechanics with Parametric Mechanical Driving*, [Nat. Commun. **11**, 1589](https://doi.org/10.1038/s41467-020-15389-4) (2020)

* J. Li and S. Groblacher, *Stationary Quantum Entanglement between a Massive Mechanical Membrane and a Low Frequency LC Circuit*, [New J. Phys. **22**, 063041](https://doi.org/10.1088/1367-2630/ab90d2) (2020)

* N. Malossi, P. Piergentili, J. Li, E. Serra, R. Natali, G. Di Giuseppe and D. Vitali, *Sympathetic Cooling of a Radio-frequency LC Circuit to its Ground State in an Optoelectromechanical System*, [Phys. Rev. A **103**, 033516](https://link.aps.org/doi/10.1103/PhysRevA.103.0335166) (2021).

## Notebooks

* [Plots in the Latest Version of the Manuscript](notebooks/v4.0_qom-v1.0.1/plots.ipynb)

## Structure of the Repository

```
ROOT_DIR/
|
├───data/
│   ├───bar/
│   │   ├───baz_xyz.npz
│   │   └───...
│   └───...
|
├───notebooks/
│   ├───bar/
│   │   ├───baz.ipynb
│   │   └───...
│   │
│   ├───foo_baz.ipynb
│   └───...
|
│───scripts/
│   ├───bar/
│   │   ├───baz.py
│   │   └───...
│   └───...
|
├───systems/
│   ├───__init__.py
│   ├───Foo.py
│   └───...
│
├───.gitignore
├───CHANGELOG.md
└───README.md
```

Here, `foo` represents the module or system and `bar` represents the version.

## Installing Dependencies

All numerical data and plots are obtained using the [Quantum Optomechanics Toolbox](https://github.com/sampreet/qom), an open-source Python framework to simulate optomechanical systems.
Refer to the [QOM toolbox documentation](https://sampreet.github.io/qom-docs/v1.0.1) for the steps to install this libary.

## Running the Scripts

To run the scripts, navigate *inside* the top-level directory, and execute:

```bash
python scripts/bar/baz.py
```

Here, `bar` is the name of the folder (containing the version information) inside `scripts` and `baz.py` is the name of the script (refer to the repository structure).