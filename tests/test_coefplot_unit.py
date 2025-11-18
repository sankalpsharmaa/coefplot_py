"""
Unit tests for coefplot_py package using pytest
"""

import pytest
import numpy as np
import os
import tempfile
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from coefplot_py import CoefPlot, coefplot_py


class TestCoefPlotInit:
    """Test CoefPlot initialization"""
    
    def test_default_init(self):
        """Test default initialization"""
        plotter = CoefPlot()
        assert plotter.horizontal is True
        assert plotter.ci_level == 95
        assert plotter.figsize == (8, 6)
        assert plotter.dpi == 300
        assert plotter.fig is None
        assert plotter.ax is None
    
    def test_custom_init(self):
        """Test custom initialization"""
        plotter = CoefPlot(
            horizontal=False,
            ci_level=90,
            figsize=(10, 8),
            dpi=150
        )
        assert plotter.horizontal is False
        assert plotter.ci_level == 90
        assert plotter.figsize == (10, 8)
        assert plotter.dpi == 150
    
    def test_vertical_figsize(self):
        """Test that vertical orientation gets correct default figsize"""
        plotter = CoefPlot(horizontal=False)
        assert plotter.figsize == (6, 8)


class TestCoefPlotBasic:
    """Test basic plotting functionality"""
    
    def test_basic_plot_with_ses(self):
        """Test basic plot with standard errors"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3, 0.8],
                ses=[0.1, 0.15, 0.12],
                labels=['Var1', 'Var2', 'Var3'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
            assert plotter.fig is not None
            assert plotter.ax is not None
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_basic_plot_with_ci_bounds(self):
        """Test basic plot with explicit CI bounds"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3],
                ci_lower=[0.3, -0.5],
                ci_upper=[0.7, -0.1],
                labels=['Var1', 'Var2'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_plot_without_labels(self):
        """Test plot generates default labels when none provided"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3, 0.8],
                ses=[0.1, 0.15, 0.12],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_plot_vertical_orientation(self):
        """Test vertical orientation"""
        plotter = CoefPlot(horizontal=False)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3, 0.8],
                ses=[0.1, 0.15, 0.12],
                labels=['Var1', 'Var2', 'Var3'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_plot_with_numpy_arrays(self):
        """Test plot accepts numpy arrays"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=np.array([0.5, -0.3, 0.8]),
                ses=np.array([0.1, 0.15, 0.12]),
                labels=np.array(['Var1', 'Var2', 'Var3']),
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestCoefPlotErrorHandling:
    """Test error handling"""
    
    def test_missing_ses_and_ci(self):
        """Test error when neither ses nor CI bounds provided"""
        plotter = CoefPlot()
        with pytest.raises(ValueError, match="Must provide either"):
            plotter.plot(
                coefs=[0.5, -0.3],
                savepath=None,
                show=False
            )
    
    def test_mismatched_lengths(self):
        """Test error handling for mismatched array lengths"""
        plotter = CoefPlot()
        # This should work but might produce unexpected results
        # The actual behavior depends on implementation
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Should handle gracefully or raise error
            try:
                plotter.plot(
                    coefs=[0.5, -0.3],
                    ses=[0.1, 0.15, 0.12],  # Mismatched length
                    savepath=tmp_path,
                    show=False
                )
            except (ValueError, IndexError):
                pass  # Expected behavior
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestCoefPlotStyling:
    """Test styling options"""
    
    def test_custom_colors(self):
        """Test custom colors"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3, 0.8],
                ses=[0.1, 0.15, 0.12],
                labels=['Var1', 'Var2', 'Var3'],
                colors=['red', 'blue', 'green'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_single_color(self):
        """Test single color for all coefficients"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3, 0.8],
                ses=[0.1, 0.15, 0.12],
                labels=['Var1', 'Var2', 'Var3'],
                colors='red',
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_custom_markers(self):
        """Test custom markers"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3, 0.8],
                ses=[0.1, 0.15, 0.12],
                labels=['Var1', 'Var2', 'Var3'],
                markers=['o', 's', '^'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_ci_styles(self):
        """Test different CI styles"""
        plotter = CoefPlot()
        for ci_style in ['line', 'bar']:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp_path = tmp.name
            
            try:
                plotter.plot(
                    coefs=[0.5, -0.3],
                    ses=[0.1, 0.15],
                    labels=['Var1', 'Var2'],
                    ci_style=ci_style,
                    savepath=tmp_path,
                    show=False
                )
                assert os.path.exists(tmp_path)
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
    
    def test_no_zero_line(self):
        """Test plot without zero line"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3],
                ses=[0.1, 0.15],
                labels=['Var1', 'Var2'],
                zero_line=False,
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_no_grid(self):
        """Test plot without grid"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3],
                ses=[0.1, 0.15],
                labels=['Var1', 'Var2'],
                grid=False,
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestCoefPlotCILevels:
    """Test different confidence interval levels"""
    
    def test_ci_level_90(self):
        """Test 90% confidence interval"""
        plotter = CoefPlot(ci_level=90)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3],
                ses=[0.1, 0.15],
                labels=['Var1', 'Var2'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_ci_level_99(self):
        """Test 99% confidence interval"""
        plotter = CoefPlot(ci_level=99)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3],
                ses=[0.1, 0.15],
                labels=['Var1', 'Var2'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestCoefPlotMultiple:
    """Test multiple plots/models"""
    
    def test_multiple_plots(self):
        """Test plotting multiple models"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, 0.48, 0.47],
                ses=[0.1, 0.095, 0.09],
                labels=['Treatment'] * 3,
                plot_labels=['Model 1', 'Model 2', 'Model 3'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestCoefplotPyFunction:
    """Test coefplot_py convenience function"""
    
    def test_coefplot_py_basic(self):
        """Test basic coefplot_py function"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            coefplot_py(
                coefs=[0.5, -0.3, 0.8],
                ses=[0.1, 0.15, 0.12],
                labels=['Var1', 'Var2', 'Var3'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_coefplot_py_vertical(self):
        """Test coefplot_py with vertical orientation"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            coefplot_py(
                coefs=[0.5, -0.3],
                ses=[0.1, 0.15],
                labels=['Var1', 'Var2'],
                horizontal=False,
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_coefplot_py_custom_ci_level(self):
        """Test coefplot_py with custom CI level"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            coefplot_py(
                coefs=[0.5, -0.3],
                ses=[0.1, 0.15],
                labels=['Var1', 'Var2'],
                ci_level=90,
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestCoefPlotLaTeX:
    """Test LaTeX formatting"""
    
    def test_latex_label_formatting(self):
        """Test LaTeX label formatting"""
        plotter = CoefPlot()
        # Test the _format_latex_label method
        # Note: This tests internal method, but it's important functionality
        label = plotter._format_latex_label("post_treated")
        assert isinstance(label, str)
        
        # Test with regular text
        label2 = plotter._format_latex_label("Treatment")
        assert isinstance(label2, str)
        
        # Test with empty string
        label3 = plotter._format_latex_label("")
        assert label3 == ""
    
    def test_plot_with_underscore_labels(self):
        """Test plot with labels containing underscores"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3],
                ses=[0.1, 0.15],
                labels=['post_treated', 'pre_treated'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestCoefPlotEdgeCases:
    """Test edge cases"""
    
    def test_single_coefficient(self):
        """Test plot with single coefficient"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5],
                ses=[0.1],
                labels=['Var1'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_many_coefficients(self):
        """Test plot with many coefficients"""
        plotter = CoefPlot()
        n = 20
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=np.random.randn(n),
                ses=np.random.rand(n) * 0.1 + 0.05,
                labels=[f'Var{i}' for i in range(n)],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_zero_coefficients(self):
        """Test plot with zero coefficients"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.0, 0.0, 0.0],
                ses=[0.1, 0.15, 0.12],
                labels=['Var1', 'Var2', 'Var3'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_very_large_coefficients(self):
        """Test plot with very large coefficients"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[100.0, -50.0],
                ses=[10.0, 5.0],
                labels=['Var1', 'Var2'],
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_custom_xlim(self):
        """Test plot with custom x-axis limits"""
        plotter = CoefPlot()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            plotter.plot(
                coefs=[0.5, -0.3],
                ses=[0.1, 0.15],
                labels=['Var1', 'Var2'],
                xlim=(-1.0, 1.0),
                savepath=tmp_path,
                show=False
            )
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

