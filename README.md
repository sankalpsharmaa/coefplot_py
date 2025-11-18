# Python Implementation of Stata's coefplot

This module provides a Python implementation of Stata's `coefplot` functionality that can be called directly from Stata (Stata 16+) or used standalone in Python.

## Features

- Plot coefficients with confidence intervals
- Horizontal and vertical orientations
- Multiple models/plots support
- Custom styling options
- **LaTeX text rendering** for publication-quality figures
- Direct integration with Stata estimation results
- Export to high-resolution figures

## Installation

### Install as a Python Package

The recommended way to install `coefplot_py` is as a Python package:

```bash
# Install from source (development mode)
git clone https://github.com/sankalpsharma/coefplot_py.git
cd coefplot_py
pip install -e .

# Or install directly (if published to PyPI)
pip install coefplot-py
```

This will automatically install all required dependencies:
- numpy>=1.19.0
- pandas>=1.2.0
- matplotlib>=3.3.0
- scipy>=1.5.0

### Manual Installation (Alternative)

If you prefer not to install as a package, you can install dependencies manually:

```bash
pip install matplotlib numpy pandas scipy
```

### LaTeX Support (Optional but Recommended)

For publication-quality figures with LaTeX-rendered text:

- **macOS**: Install MacTeX or BasicTeX
- **Linux**: Install `texlive-latex-base` or full `texlive` distribution
- **Windows**: Install MiKTeX or TeX Live

The code will automatically detect LaTeX availability and use it if present. If LaTeX is not available, it falls back to regular text rendering with serif fonts.

**Note**: Variable names with underscores (e.g., `post_treated`) are automatically formatted as subscripts in math mode when LaTeX is available.

### For Stata Integration

1. **Install Python packages** (see above)

2. **Install the Stata command:**
   - Copy `coefplot_py.ado` to your Stata personal ado directory
   - To find your personal ado directory, type in Stata: `sysdir`
   - Usually it's something like `C:\Users\YourName\ado\personal\` (Windows) or `~/ado/personal/` (Mac/Linux)
   - Place `coefplot_py.ado` in that directory

3. **Make sure `coefplot_py` package is accessible:**
   - Place the `coefplot_py/` folder in your project directory, OR
   - Add the directory containing `coefplot_py/` to your Python path
   - The command will automatically add the current Stata working directory and `coefplot_py/` subdirectory to Python's path

4. **Verify Python is configured in Stata:**
   ```stata
   python query
   ```
   If Python is not set up, configure it:
   ```stata
   python set exec "C:/Python/python.exe"  // Adjust path as needed
   ```

5. **Test the installation:**
   ```stata
   sysuse auto, clear
   regress price mpg weight
   coefplot_py, save("test.png")
   ```
   
   **Note**: Make sure you're in a directory that contains the `coefplot_py/` folder,
   or adjust the Python path in the `.ado` file to point to the correct location.

You need Stata 16+ with Python integration enabled. The `sfi` package is automatically available when running Python from Stata.

## Usage

### From Stata (Recommended)

The easiest way is to use the `coefplot_py` Stata command directly after estimation:

#### Basic Example

```stata
* Run regression
regress y x1 x2 x3, cluster(id)

* Plot all coefficients
coefplot_py, save("coefplot.png") title("Regression Results")

* Plot specific coefficients only
coefplot_py x1 x2, save("coefplot.png") title("Selected Coefficients")
```

#### With Custom Options

```stata
regress num_sisters post_treated, cluster(plot_id)
coefplot_py post_treated, ///
    save("coefplot.png") ///
    title("HSA Amendment Effect") ///
    colors("red") ///
    markers("s") ///
    markersize(10) ///
    cilevel(90) ///
    vertical
```

#### Using Stored Estimates

```stata
regress y x1 x2, cluster(id)
estimates store model1

coefplot_py x1, estimates(model1) save("coefplot.png")
```

### Direct Python Usage (Advanced)

If you need more control, you can call Python directly:

```stata
* Run regression
regress y x1 x2 x3, cluster(id)

* Plot coefficients using Python
python: import sys
python: sys.path.append("path/to/coefplot_py")
python: from coefplot_py import coefplot_from_stata
python: coefplot_from_stata(est_name='.', 
                            coefs=['x1', 'x2'],
                            title='Regression Results',
                            savepath='coefplot.png')
```

#### Manual Data Input

```stata
python: import sys
python: sys.path.append("path/to/coefplot_py")
python: from coefplot_py import coefplot_py
python: coefplot_py(coefs=[0.5, -0.3, 0.8],
                    ses=[0.1, 0.15, 0.12],
                    labels=['Treatment', 'Control', 'Interaction'],
                    title='Treatment Effects',
                    savepath='coefplot.png',
                    horizontal=True,
                    ci_level=95)
```

### From Python

#### Basic Usage

```python
from coefplot_py import coefplot_py

# Simple plot
coefplot_py(
    coefs=[0.5, -0.3, 0.8],
    ses=[0.1, 0.15, 0.12],
    labels=['Var1', 'Var2', 'Var3'],
    title='Coefficient Plot',
    savepath='coefplot.png'
)
```

#### Advanced Usage with Custom Styling

```python
from coefplot_py import CoefPlot

plotter = CoefPlot(horizontal=True, ci_level=95, figsize=(10, 6))
plotter.plot(
    coefs=[0.5, -0.3, 0.8],
    ses=[0.1, 0.15, 0.12],
    labels=['Treatment', 'Control', 'Interaction'],
    colors=['red', 'blue', 'green'],
    markers=['o', 's', '^'],
    marker_size=8,
    ci_width=0.3,
    ci_style='line',  # 'line', 'bar', or 'area'
    zero_line=True,
    grid=True,
    title='Custom Styled Plot',
    savepath='coefplot_custom.png'
)
```

#### Multiple Models Comparison

```python
from coefplot_py import CoefPlot
import numpy as np

plotter = CoefPlot(horizontal=True)

# Combine coefficients from multiple models
all_coefs = np.concatenate([[0.5], [0.48], [0.47]])  # From 3 models
all_ses = np.concatenate([[0.1], [0.095], [0.09]])
all_labels = ['Treatment'] * 3
plot_labels = ['Model 1', 'Model 2', 'Model 3']  # Identifies which model

plotter.plot(
    coefs=all_coefs,
    ses=all_ses,
    labels=all_labels,
    plot_labels=plot_labels,
    title='Treatment Effect Across Models',
    savepath='coefplot_multi.png'
)
```

## Parameters

### Main Function: `coefplot_py()`

- **coefs** (required): Array-like of coefficient values
- **ses** (optional): Standard errors. Required if `ci_lower`/`ci_upper` not provided
- **labels** (optional): Labels for coefficients
- **ci_lower** (optional): Lower bounds of confidence intervals
- **ci_upper** (optional): Upper bounds of confidence intervals
- **horizontal** (default: True): Plot orientation
- **ci_level** (default: 95): Confidence interval level
- **title** (default: ""): Plot title
- **savepath** (optional): Path to save figure
- **colors**: Single color or list of colors
- **markers**: Single marker or list of markers
- **marker_size** (default: 6): Size of coefficient markers
- **ci_width** (default: 0.3): Width of CI lines/bars
- **ci_style** (default: "line"): Style of CI - "line", "bar", or "area"
- **zero_line** (default: True): Draw line at zero
- **grid** (default: True): Show grid
- **legend** (default: True): Show legend

### Class: `CoefPlot`

Same parameters as `coefplot_py()`, but allows more control:

```python
plotter = CoefPlot(horizontal=True, ci_level=95, figsize=(10, 6), dpi=300)
plotter.plot(...)
```

## Integration with Stata Analysis

### Example: Event Study Plot

```stata
* Run event study regression
reghdfe outcome i.event##i.treated, absorb(fe) cluster(id)

* Extract event study coefficients
matrix b = e(b)
matrix V = e(V)

python: import numpy as np
python: import sfi
python: from coefplot_py import coefplot_py
python: 
python: # Read from Stata
python: b = sfi.Matrix.get("b")
python: V = sfi.Matrix.get("V")
python: coefs = b[0, :]
python: ses = np.sqrt(np.diag(V))
python: labels = sfi.Matrix.getRowNames("b")[0]
python: 
python: # Filter to event study coefficients
python: event_coefs = [c for c, l in zip(coefs, labels) if 'event' in l]
python: event_ses = [s for s, l in zip(ses, labels) if 'event' in l]
python: event_labels = [l for l in labels if 'event' in l]
python: 
python: coefplot_py(coefs=event_coefs, ses=event_ses, labels=event_labels,
python:             title='Event Study: Treatment Effect Over Time',
python:             savepath='event_study.png')
```

### Example: Difference-in-Differences Results

```stata
* DID regression
reghdfe outcome i.post##i.treated, absorb(group year) cluster(id)
estimates store did_model

python: from coefplot_py import coefplot_from_stata
python: coefplot_from_stata(est_name='did_model',
python:                     coefs=['1.post#1.treated'],
python:                     title='Difference-in-Differences Estimate',
python:                     savepath='did_coefplot.png',
python:                     horizontal=True)
```

## Comparison with Stata coefplot

Capabilities:
- Coefficients with confidence intervals
- Horizontal and vertical orientations
- Multiple models
- Custom styling options

Use cases:
- Call from Stata after estimation
- Generate figures from Python pipelines
- Produce high-resolution images

Limitations:
- Does not implement all features of Stata’s `coefplot`
- No automatic equation/group handling
- Basic label management
- No built-in sorting/ordering

## Troubleshooting

### Python not found in Stata

```stata
python query

Set Python path if needed:
python set exec "C:/Python/python.exe"
```

### Import errors

Ensure `tools.py` is in your Python path:

```python
import sys
sys.path.append("/path/to/coefplot_py")
```

### Missing packages

Install required packages:

```bash
pip install matplotlib numpy pandas scipy
```

## Examples

See `tools_example.do` for complete Stata examples.

## Notes

- This is a simplified implementation focusing on core plotting functionality
- For full Stata coefplot features, use the original Stata command
- The Python version is useful for:
  - Custom styling not available in Stata
  - Integration with Python analysis pipelines
  - High-resolution publication-quality figures
  - Automated figure generation from Stata results
