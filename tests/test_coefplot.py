#!/usr/bin/env python3
"""
Test script for coefplot_py functionality
Tests both the Python functions and simulates Stata integration
"""

import sys
import os

# Check dependencies
print("Checking dependencies...")
missing = []
try:
    import numpy as np
    print("✓ numpy available")
except ImportError:
    missing.append("numpy")
    print("✗ numpy not available")

try:
    import pandas as pd
    print("✓ pandas available")
except ImportError:
    missing.append("pandas")
    print("✗ pandas not available")

try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    print("✓ matplotlib available")
except ImportError:
    missing.append("matplotlib")
    print("✗ matplotlib not available")

try:
    import scipy
    print("✓ scipy available")
except ImportError:
    print("⚠ scipy not available (will use fallback z-scores)")

if missing:
    print(f"\nMissing required packages: {', '.join(missing)}")
    print("Install with: pip install " + " ".join(missing))
    sys.exit(1)

# Test imports
print("\nTesting imports...")
try:
    # Import from installed package
    from coefplot_py import coefplot_py, CoefPlot, coefplot_from_stata
    print("✓ Successfully imported coefplot_py package")
except ImportError as e:
    # Fallback: try importing from parent directory (for development)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    try:
        from coefplot_py import coefplot_py, CoefPlot, coefplot_from_stata
        print("✓ Successfully imported coefplot_py package (development mode)")
    except ImportError as e2:
        print(f"✗ Failed to import coefplot_py: {e2}")
        sys.exit(1)

# Test 1: Basic coefplot_py function
print("\nTest 1: Basic coefplot_py function...")
try:
    coefplot_py(
        coefs=[0.5, -0.3, 0.8, 0.2],
        ses=[0.1, 0.15, 0.12, 0.08],
        labels=['Treatment', 'Control', 'Interaction', 'Constant'],
        title='Test Plot 1: Basic Function',
        savepath=os.path.join(os.path.dirname(__file__), 'test_coefplot1.png'),
        show=False
    )
    print("✓ Test 1 passed: Basic plot created")
except Exception as e:
    print(f"✗ Test 1 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: CoefPlot class
print("\nTest 2: CoefPlot class...")
try:
    plotter = CoefPlot(horizontal=True, ci_level=95)
    plotter.plot(
        coefs=[0.5, -0.3, 0.8],
        ses=[0.1, 0.15, 0.12],
        labels=['Var1', 'Var2', 'Var3'],
        title='Test Plot 2: CoefPlot Class',
        savepath=os.path.join(os.path.dirname(__file__), 'test_coefplot2.png'),
        show=False
    )
    print("✓ Test 2 passed: CoefPlot class works")
except Exception as e:
    print(f"✗ Test 2 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Vertical orientation
print("\nTest 3: Vertical orientation...")
try:
    plotter = CoefPlot(horizontal=False, ci_level=95)
    plotter.plot(
        coefs=[0.5, -0.3, 0.8],
        ses=[0.1, 0.15, 0.12],
        labels=['Var1', 'Var2', 'Var3'],
        title='Test Plot 3: Vertical',
        savepath=os.path.join(os.path.dirname(__file__), 'test_coefplot3.png'),
        show=False
    )
    print("✓ Test 3 passed: Vertical plot created")
except Exception as e:
    print(f"✗ Test 3 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Custom styling
print("\nTest 4: Custom styling...")
try:
    plotter = CoefPlot(horizontal=True)
    plotter.plot(
        coefs=[0.5, -0.3, 0.8],
        ses=[0.1, 0.15, 0.12],
        labels=['Var1', 'Var2', 'Var3'],
        colors=['red', 'blue', 'green'],
        markers=['o', 's', '^'],
        marker_size=10,
        ci_width=0.4,
        ci_style='line',
        title='Test Plot 4: Custom Styling',
        savepath=os.path.join(os.path.dirname(__file__), 'test_coefplot4.png'),
        show=False
    )
    print("✓ Test 4 passed: Custom styling works")
except Exception as e:
    print(f"✗ Test 4 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: CI with explicit bounds
print("\nTest 5: Explicit CI bounds...")
try:
    coefplot_py(
        coefs=[0.5, -0.3, 0.8],
        ci_lower=[0.3, -0.5, 0.6],
        ci_upper=[0.7, -0.1, 1.0],
        labels=['Var1', 'Var2', 'Var3'],
        title='Test Plot 5: Explicit CI',
        savepath=os.path.join(os.path.dirname(__file__), 'test_coefplot5.png'),
        show=False
    )
    print("✓ Test 5 passed: Explicit CI bounds work")
except Exception as e:
    print(f"✗ Test 5 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Multiple plots (simulated)
print("\nTest 6: Multiple plots...")
try:
    plotter = CoefPlot(horizontal=True)
    all_coefs = [0.5, 0.48, 0.47]  # Same coefficient from 3 models
    all_ses = [0.1, 0.095, 0.09]
    all_labels = ['Treatment'] * 3
    plot_labels = ['Model 1', 'Model 2', 'Model 3']
    
    plotter.plot(
        coefs=all_coefs,
        ses=all_ses,
        labels=all_labels,
        plot_labels=plot_labels,
        title='Test Plot 6: Multiple Models',
        savepath=os.path.join(os.path.dirname(__file__), 'test_coefplot6.png'),
        show=False
    )
    print("✓ Test 6 passed: Multiple plots work")
except Exception as e:
    print(f"✗ Test 6 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Check if files were created
print("\nTest 7: Checking output files...")
test_dir = os.path.dirname(__file__)
test_files = [
    os.path.join(test_dir, 'test_coefplot1.png'),
    os.path.join(test_dir, 'test_coefplot2.png'),
    os.path.join(test_dir, 'test_coefplot3.png'),
    os.path.join(test_dir, 'test_coefplot4.png'),
    os.path.join(test_dir, 'test_coefplot5.png'),
    os.path.join(test_dir, 'test_coefplot6.png')
]

created = []
missing_files = []
for f in test_files:
    if os.path.exists(f):
        created.append(f)
        size = os.path.getsize(f)
        print(f"✓ {f} created ({size} bytes)")
    else:
        missing_files.append(f)
        print(f"✗ {f} not found")

if missing_files:
    print(f"\n⚠ Warning: {len(missing_files)} file(s) not created")
else:
    print(f"\n✓ All {len(created)} test plots created successfully")

# Summary
print("\n" + "="*50)
print("TEST SUMMARY")
print("="*50)
if not missing_files and len(created) == len(test_files):
    print("✓ All tests passed!")
    print(f"✓ Created {len(created)} test plots")
    print("\nTo view plots, check the tests/test_coefplot*.png files")
else:
    print("⚠ Some tests had issues")
    if missing_files:
        print(f"✗ Missing files: {missing_files}")

print("\n" + "="*50)
print("Stata Integration Test")
print("="*50)
print("\nTo test Stata integration:")
print("1. Make sure coefplot_py.ado is in your Stata ado-path")
print("2. Make sure tools.py is accessible from Stata")
print("3. Run in Stata:")
print("   sysuse auto, clear")
print("   regress price mpg weight")
print("   coefplot_py, save(\"test_stata.png\")")

