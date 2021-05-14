# Quantum Entanglement in a Modulated Optoelectromechanical System

## About the Work

We investigate the dynamics of quantum entanglement in an optoelectromechanical system consisting of an optical cavity and an LC circuit sharing a common mechanical membrane.

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

