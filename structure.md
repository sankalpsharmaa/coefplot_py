# Package structure

This directory contains the code and Stata integration for `coefplot_py`.

## Directory contents

```
coefplot_py/
├── coefplot_py/             # Package
│   ├── __init__.py
│   ├── tools.py             # Plotting implementation
│   └── coefplot_py.ado      # Stata wrapper command
├── tests/
│   ├── __init__.py
│   ├── test_coefplot.py     # Python tests
│   ├── test_coefplot_stata.do  # Stata example tests
│   └── example*.png         # Example outputs
├── coefplot_py_example.do   # Stata example
├── README.md                # Project overview
├── setup.py
├── pyproject.toml
├── requirements.txt
├── MANIFEST.in
├── .gitignore
└── structure.md             # This file
```

## Installation

### For Stata users

1. Copy `coefplot_py/coefplot_py.ado` to your PERSONAL ado directory (`sysdir`).
2. The `.ado` file looks for `tools.py` in a `coefplot_py/` folder under your working directory.

### For Python users

```python
from coefplot_py import coefplot_py, CoefPlot
```

Or install in editable mode:
```bash
pip install -e .
```

## File descriptions

- `coefplot_py/tools.py`: Plotting functions with optional LaTeX labels
- `coefplot_py/coefplot_py.ado`: Stata wrapper (install in ado-path)
- `coefplot_py_example.do`: Example usage from Stata
- `tests/test_coefplot.py`: Python unit tests
- `tests/test_coefplot_stata.do`: Stata tests/examples
- `README.md`: Overview and usage
- `setup.py`, `pyproject.toml`: Packaging

## Usage

### From Stata

```stata
regress y x1 x2, cluster(id)
coefplot_py, save("plot.png") title("Results")
```

### From Python

```python
from coefplot_py import coefplot_py
coefplot_py(coefs=[0.5, -0.3], ses=[0.1, 0.15], labels=['Var1', 'Var2'], savepath='plot.png')
```

## Notes

- Paths are relative to the Stata working directory unless you pass absolute paths.
- If LaTeX is installed, labels render with LaTeX; otherwise regular text is used.

