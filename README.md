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

## Related Works

### Stationary Quantum Entanglement between a Massive Mechanical Membrane and a Low Frequency LC Circuit

> New J. Phys. **22**, 063041 (2020)

Author              | Affiliation
---                 | ---
Jie Li              | Delft University of Technology, 2628CJ Delft, The Netherlands
Simon Groblacher    | Delft University of Technology, 2628CJ Delft, The Netherlands

#### Objectives
* Entangling a massive mechanical oscillator to a macroscopic low-frequency LC circuit.

#### Novelty
* LC resonator frequency in the radio-frequency domain close to the mechanical frequency.
* Membrane-LC interaction is quadratic in LC charge and linear in mechanical position.
* DC drive to enhance the electromechanical coupling rate.
* Red-detuned laser to cool the mechanical mode.

#### Assumptions
* Nearly resonant mechanical and LC oscillators.
* Linearized description of the modes.

#### Results
* Strong optomechanical and electromechanical rates are required.
* Entanglement is robust against temperature.

### Gently Modulating Optomechanical Systems

> Phys. Rev. Lett. **103**, 213603 (2009)

Author      | Affiliation
---         | ---
A. Mari     | Institute of Physics and Astronomy, Univerity of Potsdam, D-14476 Postdam, Germany
J. Eisert   | Institute of Advanced Study Berlin, D-14193 Berlin, Germany

#### Objectives
* Modulated entanglement dynamics between optics and mechanics.

#### Novelty
* Driving with mildly amplitude-modulated light.
* No classical feedback or squeezed-light driving.

#### Assumptions
* Linearized description of the modes.

#### Results
* High degrees of squeezing below the vacuum noise level.

## Structure of the Repository
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

To run in GUI mode, from `ROOT_DIR`, execute:

```bash
python -c 'from qom.ui import run; run()'
```

Alternatively, run `GUI.py`.

