# Example summary

This document summarizes what the `coefplot_py_example.do` file does and how to run it.

## What it does

The example script:
- Creates a small panel dataset (5,000 rows, 1,000 units × 5 periods).
- Runs 20 regressions covering common plotting scenarios.
- Saves a PNG for each case in `tests/`.

Variables generated include: `plot_id`, `individual_id`, `time`, `year`,
`post_treated`, `religion_type`, `event_period`, `num_sisters`, `age`,
`education`, and `income`.

## Running the example

From Stata GUI:
```stata
cd /path/to/coefplot_py
do coefplot_py_example.do
```

From command line:
```bash
stata-se -b do coefplot_py_example.do
```

Using the helper script:
```bash
./tests/run_examples.sh stata-se
```

## Outputs

Files are written to `tests/` as `example*.png` (20 images).

## Notes

- The script uses a fixed random seed for reproducibility.
- Runtime is roughly 1–2 minutes depending on your machine.

