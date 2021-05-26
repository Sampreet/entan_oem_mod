# Quantum Entanglement in a Modulated Optoelectromechanical System

Author                  | Affiliation
---                     | ---
Sampreet Kalita         | Indian Institute of Technology Guwahati, Guwahati-781039, India
Subhadeep Chakraborty   | ICFAI University Tripura, Tripura-799210, India
Saumya Amit Shah        | Indian Institute of Technology Guwahati, Guwahati-781039, India
Amarendra Kumar Sarma   | Indian Institute of Technology Guwahati, Guwahati-781039, India

## About the Work

We investigate the dynamics of quantum entanglement in an optoelectromechanical system consisting of an optical cavity and an LC circuit sharing a common mechanical membrane.
The cavity and circuit are driven by modulated lasers and voltages respectively.
Each modulation consists of a small amplitude varying cosinusoidally with time.
We analyze:
* The stability of the system in presence of either or both modulations.
* The maximum entanglement achievable by the stable system.

## Related Works

* J. Li and S. Groblacher, *Stationary Quantum Entanglement between a Massive Mechanical Membrane and a Low Frequency LC Circuit*, [New J. Phys. **22**, 063041](https://doi.org/10.1088/1367-2630/ab90d2) (2020).

* A. Mari and J. Eisert, *Gently Modulating Optomechanical Systems*, [Phys. Rev. Lett. **103**, 213603](https://doi.org/10.1103/PhysRevLett.103.213603) (2009).

## Structure of the Repository

The work is based on the packages provided by [The Quantum Optomechanics Toolbox](https://github.com/Sampreet/qom) and follows the following directory structure:

```
ROOT_DIR/
|
├───notebooks/
│   ├───foo_bar.ipynb
│   └───...
|
│───scripts/
│   ├───foo_bar.py
│   └───...
|
├───systems/
│   ├───__init__.py
│   ├───FooBar.py
│   └───...
│
├───.gitignore
├───CHANGELOG.md
├───GUI.py
└───README.md
```

## Running the Scripts

To run the scripts, navigate *inside* the top-level directory, `ROOT_DIR`, and execute:

```bash
python scripts/foo_bar.py
```

Here, `foo_bar.py` is the name of the script.

To run in GUI mode using `PowerShell` or `bash`, navigate to `ROOT_DIR` and execute:

```bash
python -c 'from qom.ui import run; run()'
```

Alternatively, run `GUI.py`.

