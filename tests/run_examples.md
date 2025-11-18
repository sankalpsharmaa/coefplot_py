# Run examples

The example script shows typical usage and generates PNG outputs.

## Run in Stata

```stata
cd /path/to/coefplot_py
do coefplot_py_example.do
```

## Run from shell

```bash
cd /path/to/coefplot_py
stata-se -b do coefplot_py_example.do
```

## Use the helper script

```bash
./tests/run_examples.sh stata-se
```

## Output

Images are saved to `tests/` as `example*.png`.

## Requirements

- Stata 16+ with Python integration
- `coefplot_py/coefplot_py.ado` available in your ado-path
- Python dependencies installed: matplotlib, numpy, pandas, scipy

