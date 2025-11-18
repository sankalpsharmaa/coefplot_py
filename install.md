# Install

This project has two parts:
- Python package: `coefplot_py`
- Stata wrapper command: `coefplot_py.ado`

The sections below cover common setups on macOS, Linux, and Windows.

## Requirements

- Python 3.7 or newer (3.8–3.12 tested)
- Stata 16 or newer with Python integration enabled
- Packages: `matplotlib`, `numpy`, `pandas`, `scipy`

## Option A — Python package (recommended)

Use a virtual environment to keep dependencies isolated.

Virtualenv:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

Conda:
```bash
conda create -n coefplot_py python=3.10 -y
conda activate coefplot_py
pip install -e .
```

Verification:
```bash
python -c "from coefplot_py import coefplot_py, CoefPlot; print('ok')"
```

## Option B — Stata command

Install the ado in Stata’s PERSONAL directory (shown by `sysdir`).

In Stata:
```stata
sysdir
```

Copy the ado file to PERSONAL.

macOS/Linux (bash):
```bash
cp coefplot_py/coefplot_py.ado ~/ado/personal/
```

Windows (cmd):
```bat
copy coefplot_py\coefplot_py.ado %USERPROFILE%\ado\personal\
```

Alternative (session‑only): add a path to your ado‑path.
```stata
adopath + "/path/to/coefplot_py"
```

## Configure Python in Stata

Check Python availability:
```stata
python query
```

Set the Python executable if needed:
```stata
python set exec "/usr/bin/python3", perm   // macOS/Linux example
python set exec "C:/Python311/python.exe", perm   // Windows example
python query
```

## Quick test (Stata)

```stata
sysuse auto, clear
regress price mpg weight
coefplot_py, save("coefplot_test.png")
```

If Stata does not find the command:
```stata
which coefplot_py
```
Confirm that the path points to PERSONAL and that the file exists there.

## Running the full example

From the project root, run in Stata’s batch mode:
```bash
stata-se -b do coefplot_py_example.do
```

Or use the helper script:
```bash
./tests/run_examples.sh stata-se
```

All example PNGs are saved under `tests/`.

## Troubleshooting

- Command not found in Stata:
  - Run `which coefplot_py` and verify the ado resides under PERSONAL.
  - Add the repo path to ado‑path for the session: `adopath + "/path/to/coefplot_py"`.

- Python not configured in Stata:
  - Run `python query` and set the interpreter with `python set exec ... , perm`.

- Images not created / saved to a different folder:
  - Check Stata’s working directory with `pwd`.
  - Use absolute paths in `save(...)` or run from the project root.

- Import errors from Python:
  - Ensure the package is installed: `pip install -e .`.
  - In Stata sessions, the ado adjusts `sys.path` to include the repo when possible.

## Uninstall / upgrade

Uninstall the Python package:
```bash
pip uninstall coefplot-py
```

Upgrade in editable mode:
```bash
git pull
pip install -e . --upgrade
```
