# Quantum Entanglement in Modulated Optoelectromechanical Systems

## About the Work

We investigate the dynamics of quantum entanglement in an optoelectromechanical system consisting of an optical cavity and an LC circuit sharing a common mechanical membrane.
We analyze the stability of the system in presence of modulations and the maximum entanglement achievable by the stable system.

The following models are studied:
* ***Model 00 - Amplitude Modulation*** - The cavity and circuit are driven by modulated laser and voltage amplitudes.
* ***Model 01 - Frequency Modulation*** - The spring constant of the mechanical motion is modulated.

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

## Execution

### Installing Dependencies

The project requires `Python 3.8+` installed via the [Anaconda distribution](https://www.anaconda.com/products/individual). 
An extensive guide to set up your python environment same can be found [here](https://sampreet.github.io/python-for-physicists/modules/m01-getting-started/m01t01-setting-up-python.html).

Once the installation is complete and `conda` is configured, it is preferable to create a new conda environment (say `qom`) and activate it using:

```bash
conda create -n qom python=3
conda activate qom
```

This project uses [The Quantum Optomechanics Toolbox](https://github.com/Sampreet/qom) via Python Package Index using `pip`:

```bash
pip install -i https://test.pypi.org/simple/ qom
```

Alternatively, [clone the repository](https://github.com/Sampreet/qom) or [download the sources](https://github.com/Sampreet/qom/archive/refs/heads/master.zip) as `.zip` and extract the contents.
Now, execute the following from *outside* the top-level directory, `ROOT_DIR`, inside which `setup.py` is located:

```bash
pip install -e ROOT_DIR
```

### Running the Scripts

To run the scripts, navigate *inside* the top-level directory, `ROOT_DIR`, and execute:

```bash
python scripts/foo_bar.py
```

Here, `foo_bar.py` is the name of the script.

To run in GUI mode using `PowerShell` or `bash`, navigate to `ROOT_DIR` and execute:

```bash
python -c 'from qom.ui.gui import run; run()'
```

Alternatively, run `GUI.py` from within the directory.