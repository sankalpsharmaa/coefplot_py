"""
Python implementation of Stata's coefplot functionality
Can be called from Stata using Python integration (Stata 16+)

Usage from Stata:
    python: import sys
    python: sys.path.append("path/to/coefplot_py")
    python: from tools import coefplot_py
    python: coefplot_py(coefs, ses, labels, ci_level=95, title="", savepath="")
    
Or use the coefplot_py Stata command directly after estimation.
"""

import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend by default
import matplotlib.pyplot as plt  # noqa: E402
from typing import List, Optional, Union, Tuple

# Configure LaTeX rendering (robust detection)
LATEX_AVAILABLE = False
try:
    import shutil
    if shutil.which('latex') is None:
        raise RuntimeError('latex not found')
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Computer Modern', 'Times', 'Palatino', 'New Century Schoolbook', 'Bookman', 'DejaVu Serif']
    plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
    # Force a render to ensure LaTeX is usable
    fig, ax = plt.subplots(figsize=(1, 1), dpi=72)
    ax.text(0.5, 0.5, r'$\alpha$', ha='center')
    fig.canvas.draw()
    plt.close(fig)
    LATEX_AVAILABLE = True
except Exception:
    # LaTeX not available, use regular text
    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times', 'Palatino', 'New Century Schoolbook', 'Bookman', 'DejaVu Serif']
    warnings.warn("LaTeX not available. Using regular text rendering. Install LaTeX for better quality.")

# Try to import Stata API if available
try:
    import sfi
    STATA_AVAILABLE = True
except ImportError:
    STATA_AVAILABLE = False
    warnings.warn("Stata API (sfi) not available. Some features may be limited.")


class CoefPlot:
    """
    Main class for creating coefficient plots similar to Stata's coefplot.
    
    This implementation focuses on the core plotting functionality:
    - Plotting coefficients with confidence intervals
    - Horizontal and vertical orientations
    - Multiple models/plots
    - Custom styling options
    """
    
    def __init__(self, 
                 horizontal: bool = True,
                 ci_level: float = 95,
                 figsize: Tuple[float, float] = None,
                 dpi: int = 300):
        """
        Initialize CoefPlot object.
        
        Parameters:
        -----------
        horizontal : bool
            If True, plot horizontally (default). If False, plot vertically.
        ci_level : float
            Confidence interval level (default 95)
        figsize : tuple
            Figure size (width, height). If None, uses default.
        dpi : int
            Resolution for saved figures (default 300)
        """
        self.horizontal = horizontal
        self.ci_level = ci_level
        self.figsize = figsize if figsize else (8, 6) if horizontal else (6, 8)
        self.dpi = dpi
        self.fig = None
        self.ax = None
        
    def plot(self,
             coefs: Union[List[float], np.ndarray, pd.Series],
             ses: Optional[Union[List[float], np.ndarray, pd.Series]] = None,
             labels: Optional[Union[List[str], np.ndarray]] = None,
             ci_lower: Optional[Union[List[float], np.ndarray]] = None,
             ci_upper: Optional[Union[List[float], np.ndarray]] = None,
             groups: Optional[Union[List[str], np.ndarray]] = None,
             plot_labels: Optional[Union[List[str], np.ndarray]] = None,
             title: str = "",
             xlabel: str = "",
             ylabel: str = "",
             xlim: Optional[Tuple[float, float]] = None,
             colors: Optional[Union[List[str], str]] = None,
             markers: Optional[Union[List[str], str]] = None,
             marker_size: float = 6,
             ci_width: float = 0.3,
             ci_colors: Optional[Union[List[str], str]] = None,
             ci_style: str = "line",  # "line", "bar", "area"
             zero_line: bool = True,
             grid: bool = True,
             legend: bool = True,
             legend_labels: Optional[List[str]] = None,
             legend_loc: str = "best",
             savepath: Optional[str] = None,
             show: bool = True,
             **kwargs):
        """
        Create coefficient plot.
        
        Parameters:
        -----------
        coefs : array-like
            Coefficient values to plot
        ses : array-like, optional
            Standard errors. Used to compute CI if ci_lower/ci_upper not provided
        labels : array-like, optional
            Labels for coefficients (y-axis if horizontal, x-axis if vertical)
        ci_lower : array-like, optional
            Lower bounds of confidence intervals
        ci_upper : array-like, optional
            Upper bounds of confidence intervals
        groups : array-like, optional
            Group identifiers for grouping coefficients
        plot_labels : array-like, optional
            Labels for different plots/models (for multiple plots)
        title : str
            Plot title
        xlabel : str
            X-axis label
        ylabel : str
            Y-axis label
        xlim : tuple, optional
            X-axis limits (min, max)
        colors : str or list
            Colors for coefficients. Can be single color or list.
        markers : str or list
            Marker styles. Can be single marker or list.
        marker_size : float
            Size of markers
        ci_width : float
            Width of confidence interval lines/bars
        ci_colors : str or list
            Colors for confidence intervals
        ci_style : str
            Style of CI: "line", "bar", or "area"
        zero_line : bool
            Whether to draw vertical/horizontal line at zero
        grid : bool
            Whether to show grid
        legend : bool
            Whether to show legend
        legend_labels : list
            Labels for legend
        legend_loc : str
            Legend location
        savepath : str, optional
            Path to save figure
        show : bool
            Whether to display figure
        **kwargs
            Additional matplotlib arguments
        """
        # Convert inputs to numpy arrays
        coefs = np.asarray(coefs)
        n_coefs = len(coefs)
        
        # Generate labels if not provided
        if labels is None:
            labels = [f"Coefficient {i+1}" for i in range(n_coefs)]
        # Ensure labels is a 1D array (handle 0-d arrays from Stata)
        labels = np.asarray(labels)
        if labels.ndim == 0:
            labels = np.array([labels.item()])
        elif labels.ndim > 1:
            labels = labels.flatten()
        
        # Compute confidence intervals if not provided
        if ci_lower is None or ci_upper is None:
            if ses is None:
                raise ValueError("Must provide either (ci_lower, ci_upper) or ses")
            z_score = self._get_z_score(self.ci_level)
            ci_lower = coefs - z_score * np.asarray(ses)
            ci_upper = coefs + z_score * np.asarray(ses)
        else:
            ci_lower = np.asarray(ci_lower)
            ci_upper = np.asarray(ci_upper)
        # Handle multiple plots/models
        if plot_labels is not None:
            plot_labels = np.asarray(plot_labels)
            self._plot_multiple(
                coefs,
                ci_lower,
                ci_upper,
                labels,
                plot_labels,
                groups,
                title,
                xlabel,
                ylabel,
                xlim,
                colors,
                markers,
                marker_size,
                ci_width,
                ci_colors,
                ci_style,
                zero_line,
                grid,
                legend,
                legend_labels,
                legend_loc,
                savepath,
                show,
                **kwargs,
            )
        else:
            self._plot_single(
                coefs,
                ci_lower,
                ci_upper,
                labels,
                groups,
                title,
                xlabel,
                ylabel,
                xlim,
                colors,
                markers,
                marker_size,
                ci_width,
                ci_colors,
                ci_style,
                zero_line,
                grid,
                legend,
                savepath,
                show,
                **kwargs,
            )
    
    def _format_latex_label(self, text: str) -> str:
        """
        Format text label for LaTeX rendering.
        Escapes special characters and handles common patterns.
        """
        if not text or text == "":
            return ""
        
        # If LaTeX is not available, return as-is
        if not LATEX_AVAILABLE:
            return text
        
        # If already wrapped in $, return as-is
        if text.strip().startswith('$') and text.strip().endswith('$'):
            return text
        
        # Escape special LaTeX characters
        text = str(text)
        # Common patterns that should be in math mode
        if any(char in text for char in ['_', '^', '{', '}', '\\']):
            # Check if it looks like a variable name (e.g., "post_treated")
            if '_' in text and not text.startswith('$'):
                # Wrap in math mode for subscripts
                parts = text.split('_')
                if len(parts) == 2:
                    return f"${parts[0]}_{{{parts[1]}}}$"
        
        # Escape special characters
        special_chars = ['#', '$', '%', '&', '~', '^', '\\']
        for char in special_chars:
            if char in text and not text.startswith('$'):
                text = text.replace(char, '\\' + char)
        
        return text
    
    def _plot_single(self, coefs, ci_lower, ci_upper, labels, groups,
                    title, xlabel, ylabel, xlim, colors, markers, marker_size,
                    ci_width, ci_colors, ci_style, zero_line, grid, legend,
                    savepath, show, **kwargs):
        """Plot single set of coefficients."""
        # Create figure
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # Set up colors and markers
        if colors is None:
            colors = plt.cm.tab10(np.linspace(0, 1, len(coefs)))
        elif isinstance(colors, str):
            colors = [colors] * len(coefs)
        
        if markers is None:
            markers = ['o'] * len(coefs)
        elif isinstance(markers, str):
            markers = [markers] * len(coefs)
        
        if ci_colors is None:
            ci_colors = colors
        
        # Y positions
        y_pos = np.arange(len(coefs))
        
        if self.horizontal:
            # Horizontal plot: coefficients on x-axis, labels on y-axis
            self._plot_horizontal(coefs, ci_lower, ci_upper, y_pos, labels,
                                 colors, markers, marker_size, ci_width,
                                 ci_colors, ci_style, zero_line, grid)
            self.ax.set_yticks(y_pos)
            # Format labels for LaTeX
            latex_labels = [self._format_latex_label(str(lbl)) for lbl in labels]
            self.ax.set_yticklabels(latex_labels)
            self.ax.set_xlabel(self._format_latex_label(xlabel if xlabel else "Coefficient"))
            self.ax.set_ylabel(self._format_latex_label(ylabel if ylabel else ""))
            if xlim:
                self.ax.set_xlim(xlim)
        else:
            # Vertical plot: coefficients on y-axis, labels on x-axis
            self._plot_vertical(coefs, ci_lower, ci_upper, y_pos, labels,
                              colors, markers, marker_size, ci_width,
                              ci_colors, ci_style, zero_line, grid)
            self.ax.set_xticks(y_pos)
            # Format labels for LaTeX
            latex_labels = [self._format_latex_label(str(lbl)) for lbl in labels]
            self.ax.set_xticklabels(latex_labels, rotation=45, ha='right')
            self.ax.set_xlabel(self._format_latex_label(xlabel if xlabel else ""))
            self.ax.set_ylabel(self._format_latex_label(ylabel if ylabel else "Coefficient"))
            if xlim:
                self.ax.set_ylim(xlim)
        
        self.ax.set_title(self._format_latex_label(title))
        
        if savepath:
            self.fig.savefig(savepath, dpi=self.dpi, bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def _plot_horizontal(self, coefs, ci_lower, ci_upper, y_pos, labels,
                        colors, markers, marker_size, ci_width, ci_colors,
                        ci_style, zero_line, grid):
        """Plot horizontally."""
        # Plot confidence intervals
        if ci_style == "line":
            for i, (y, ll, ul) in enumerate(zip(y_pos, ci_lower, ci_upper)):
                color = ci_colors[i] if isinstance(ci_colors, (list, np.ndarray)) else ci_colors
                self.ax.plot([ll, ul], [y, y], color=color, linewidth=2, alpha=0.7)
                self.ax.plot([ll, ll], [y - ci_width / 2, y + ci_width / 2],
                              color=color, linewidth=2, alpha=0.7)
                self.ax.plot([ul, ul], [y - ci_width / 2, y + ci_width / 2],
                              color=color, linewidth=2, alpha=0.7)
        elif ci_style == "bar":
            for i, (y, ll, ul) in enumerate(zip(y_pos, ci_lower, ci_upper)):
                color = ci_colors[i] if isinstance(ci_colors, (list, np.ndarray)) else ci_colors
                width = ul - ll
                self.ax.barh(y, width, left=ll, height=ci_width,
                             color=color, alpha=0.3, edgecolor=color)
        elif ci_style == "area":
            # Not implemented - use line instead
            self._plot_horizontal(coefs, ci_lower, ci_upper, y_pos, labels,
                                colors, markers, marker_size, ci_width,
                                ci_colors, "line", zero_line, grid)
            return
        
        # Plot coefficients
        for i, (y, coef, color, marker) in enumerate(zip(y_pos, coefs, colors, markers)):
            self.ax.scatter(coef, y, s=marker_size ** 2, color=color,
                            marker=marker, zorder=5, edgecolors='white', linewidths=1)
        
        # Zero line
        if zero_line:
            self.ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        
        # Grid
        if grid:
            self.ax.grid(True, alpha=0.3, axis='x')
        
        # Invert y-axis so top coefficient is at top
        self.ax.invert_yaxis()
    
    def _plot_vertical(self, coefs, ci_lower, ci_upper, y_pos, labels,
                     colors, markers, marker_size, ci_width, ci_colors,
                     ci_style, zero_line, grid):
        """Plot vertically."""
        # Plot confidence intervals
        if ci_style == "line":
            for i, (x, ll, ul) in enumerate(zip(y_pos, ci_lower, ci_upper)):
                color = ci_colors[i] if isinstance(ci_colors, (list, np.ndarray)) else ci_colors
                self.ax.plot([x, x], [ll, ul], color=color, linewidth=2, alpha=0.7)
                self.ax.plot([x - ci_width / 2, x + ci_width / 2], [ll, ll],
                              color=color, linewidth=2, alpha=0.7)
                self.ax.plot([x - ci_width / 2, x + ci_width / 2], [ul, ul],
                              color=color, linewidth=2, alpha=0.7)
        elif ci_style == "bar":
            for i, (x, ll, ul) in enumerate(zip(y_pos, ci_lower, ci_upper)):
                color = ci_colors[i] if isinstance(ci_colors, (list, np.ndarray)) else ci_colors
                height = ul - ll
                self.ax.bar(x, height, bottom=ll, width=ci_width,
                            color=color, alpha=0.3, edgecolor=color)
        elif ci_style == "area":
            # Not implemented - use line instead
            self._plot_vertical(coefs, ci_lower, ci_upper, y_pos, labels,
                              colors, markers, marker_size, ci_width,
                              ci_colors, "line", zero_line, grid)
            return
        
        # Plot coefficients
        for i, (x, coef, color, marker) in enumerate(zip(y_pos, coefs, colors, markers)):
            self.ax.scatter(x, coef, s=marker_size ** 2, color=color,
                            marker=marker, zorder=5, edgecolors='white', linewidths=1)
        
        # Zero line
        if zero_line:
            self.ax.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        
        # Grid
        if grid:
            self.ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_multiple(self, coefs, ci_lower, ci_upper, labels, plot_labels,
                     groups, title, xlabel, ylabel, xlim, colors, markers,
                     marker_size, ci_width, ci_colors, ci_style, zero_line,
                     grid, legend, legend_labels, legend_loc, savepath, show, **kwargs):
        """Plot multiple models/plots."""
        unique_plots = np.unique(plot_labels)
        n_plots = len(unique_plots)
        
        # Create subplots or single plot with offsets
        if n_plots > 1:
            fig, axes = plt.subplots(1, n_plots, figsize=(self.figsize[0]*n_plots, self.figsize[1]),
                                    sharey=True, dpi=self.dpi)
            if n_plots == 1:
                axes = [axes]
        else:
            fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
            axes = [ax] * n_plots
        
        self.fig = fig
        
        # Plot each model
        for plot_idx, plot_label in enumerate(unique_plots):
            mask = plot_labels == plot_label
            plot_coefs = coefs[mask]
            plot_ci_lower = ci_lower[mask]
            plot_ci_upper = ci_upper[mask]
            plot_coef_labels = labels[mask]
            
            ax = axes[plot_idx]
            self.ax = ax
            
            # Set up colors
            if colors is None:
                plot_colors = plt.cm.tab10(np.linspace(0, 1, len(plot_coefs)))
            elif isinstance(colors, str):
                plot_colors = [colors] * len(plot_coefs)
            else:
                plot_colors = np.asarray(colors)[mask]
            
            if markers is None:
                plot_markers = ['o'] * len(plot_coefs)
            elif isinstance(markers, str):
                plot_markers = [markers] * len(plot_coefs)
            else:
                plot_markers = np.asarray(markers)[mask]
            
            y_pos = np.arange(len(plot_coefs))
            
            if self.horizontal:
                self._plot_horizontal(plot_coefs, plot_ci_lower, plot_ci_upper,
                                    y_pos, plot_coef_labels, plot_colors,
                                    plot_markers, marker_size, ci_width,
                                    ci_colors, ci_style, zero_line, grid)
                ax.set_yticks(y_pos)
                latex_labels = [self._format_latex_label(str(lbl)) for lbl in plot_coef_labels]
                ax.set_yticklabels(latex_labels)
                ax.set_xlabel(self._format_latex_label(xlabel if xlabel else "Coefficient"))
                if plot_idx == 0:
                    ax.set_ylabel(self._format_latex_label(ylabel if ylabel else ""))
                if xlim:
                    ax.set_xlim(xlim)
            else:
                self._plot_vertical(
                    plot_coefs,
                    plot_ci_lower,
                    plot_ci_upper,
                    y_pos,
                    plot_coef_labels,
                    plot_colors,
                    plot_markers,
                    marker_size,
                    ci_width,
                    ci_colors,
                    ci_style,
                    zero_line,
                    grid,
                )
                ax.set_xticks(y_pos)
                latex_labels = [self._format_latex_label(str(lbl)) for lbl in plot_coef_labels]
                ax.set_xticklabels(latex_labels, rotation=45, ha='right')
                ax.set_xlabel(self._format_latex_label(xlabel if xlabel else ""))
                if plot_idx == 0:
                    ax.set_ylabel(self._format_latex_label(ylabel if ylabel else "Coefficient"))
                if xlim:
                    ax.set_ylim(xlim)
            
            plot_title = plot_label if title == "" else f"{title} - {plot_label}"
            ax.set_title(self._format_latex_label(plot_title))
        
        if title and n_plots == 1:
            fig.suptitle(self._format_latex_label(title))
        
        if savepath:
            fig.savefig(savepath, dpi=self.dpi, bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def _get_z_score(self, level: float) -> float:
        """Get z-score for confidence interval level."""
        try:
            from scipy import stats
            alpha = 1 - level / 100
            return stats.norm.ppf(1 - alpha/2)
        except ImportError:
            # Fallback to common z-scores if scipy not available
            z_scores = {90: 1.645, 95: 1.96, 99: 2.576, 99.9: 3.291}
            if level in z_scores:
                return z_scores[level]
            else:
                # Approximate using normal approximation
                warnings.warn(f"scipy not available. Using approximation for {level}% CI.")
                return 1.96 if level >= 95 else 1.645  # Default to 95% if unknown


def coefplot_py(coefs: Union[List[float], np.ndarray],
                ses: Optional[Union[List[float], np.ndarray]] = None,
                labels: Optional[Union[List[str], np.ndarray]] = None,
                ci_lower: Optional[Union[List[float], np.ndarray]] = None,
                ci_upper: Optional[Union[List[float], np.ndarray]] = None,
                horizontal: bool = True,
                ci_level: float = 95,
                title: str = "",
                savepath: Optional[str] = None,
                **kwargs) -> None:
    """
    Convenience function for creating coefficient plots.
    Can be called directly from Stata.
    
    Parameters:
    -----------
    coefs : array-like
        Coefficient values
    ses : array-like, optional
        Standard errors
    labels : array-like, optional
        Coefficient labels
    ci_lower : array-like, optional
        Lower CI bounds
    ci_upper : array-like, optional
        Upper CI bounds
    horizontal : bool
        Horizontal orientation (default True)
    ci_level : float
        CI level (default 95)
    title : str
        Plot title
    savepath : str, optional
        Path to save figure
    **kwargs
        Additional arguments passed to CoefPlot.plot()
    
    Examples:
    ---------
    From Python:
        coefplot_py([0.5, -0.3, 0.8], ses=[0.1, 0.15, 0.12],
                    labels=['Var1', 'Var2', 'Var3'])
    
    From Stata:
        python: from tools import coefplot_py
        python: coefplot_py([0.5, -0.3], ses=[0.1, 0.15], 
                            labels=['Var1', 'Var2'], savepath='coefplot.png')
    """
    plotter = CoefPlot(horizontal=horizontal, ci_level=ci_level)
    plotter.plot(coefs=coefs, ses=ses, labels=labels,
                ci_lower=ci_lower, ci_upper=ci_upper,
                title=title, savepath=savepath, **kwargs)


def coefplot_from_stata(est_name: Optional[str] = None,
                        coefs: Optional[List[str]] = None,
                        horizontal: bool = True,
                        ci_level: float = 95,
                        title: str = "",
                        savepath: Optional[str] = None,
                        **kwargs) -> None:
    """
    Create coefficient plot from Stata estimation results.
    
    Parameters:
    -----------
    est_name : str, optional
        Name of stored estimation result in Stata
    coefs : list of str, optional
        List of coefficient names to plot. If None, plots all coefficients.
    horizontal : bool
        Horizontal orientation
    ci_level : float
        CI level
    title : str
        Plot title
    savepath : str, optional
        Path to save figure
    **kwargs
        Additional arguments
    
    Examples:
    ---------
    From Stata:
        regress y x1 x2 x3
        python: from tools import coefplot_from_stata
        python: coefplot_from_stata(est_name='.', coefs=['x1', 'x2'], 
                                    savepath='coefplot.png')
    """
    if not STATA_AVAILABLE:
        raise ImportError("Stata API (sfi) not available. Cannot read Stata results.")
    
    # Get coefficient matrix
    if est_name == '.' or est_name is None:
        b = sfi.Matrix.get("e(b)")
        V = sfi.Matrix.get("e(V)")
    else:
        # Restore estimates
        sfi.Estimate.restore(est_name)
        b = sfi.Matrix.get("e(b)")
        V = sfi.Matrix.get("e(V)")
    
    # Extract coefficients
    coef_names_raw = sfi.Matrix.getRowNames("e(b)")[0]
    # Convert coef_names to list, handling 0-d arrays and scalars
    if isinstance(coef_names_raw, np.ndarray):
        if coef_names_raw.ndim == 0:
            coef_names_list = [str(coef_names_raw.item())]
        else:
            coef_names_list = coef_names_raw.tolist() if hasattr(coef_names_raw, 'tolist') else list(coef_names_raw)
    elif isinstance(coef_names_raw, list):
        coef_names_list = coef_names_raw
    else:
        coef_names_list = [str(coef_names_raw)]
    
    # Convert b to numpy array if it's a list
    b_array = np.array(b) if isinstance(b, list) else b
    coef_values = b_array[0, :] if b_array.ndim > 1 else b_array
    # Ensure coef_values is 1D
    if coef_values.ndim == 0:
        coef_values = np.array([coef_values.item()])
    elif coef_values.ndim > 1:
        coef_values = coef_values.flatten()
    
    # Filter coefficients if specified
    if coefs is not None and len(coefs) > 0:
        # Create mask: check if coefficient name matches any in coefs list
        # Handle factor variable notation (e.g., "1.religion_type" matches "religion_type:Protestant")
        mask = []
        for name in coef_names_list:
            matched = False
            name_str = str(name)
            for coef_pattern in coefs:
                pattern_str = str(coef_pattern)
                # Direct match
                if name_str == pattern_str:
                    matched = True
                    break
                # Factor variable match (e.g., "1.religion_type" matches "religion_type:Protestant")
                if '.' in pattern_str:
                    base_var = pattern_str.split('.')[1]
                    if base_var in name_str or name_str.startswith(base_var + ':'):
                        matched = True
                        break
            mask.append(matched)
        mask = np.array(mask, dtype=bool)
        if mask.sum() > 0:  # Only filter if we have matches
            coef_values = coef_values[mask]
            coef_names_list = [coef_names_list[i] for i in range(len(coef_names_list)) if mask[i]]
    
    coef_names = coef_names_list
    
    # Compute standard errors
    V_array = np.array(V) if isinstance(V, list) else V
    se_values = np.sqrt(np.diag(V_array))
    # Ensure se_values is 1D
    if se_values.ndim == 0:
        se_values = np.array([se_values.item()])
    elif se_values.ndim > 1:
        se_values = se_values.flatten()
    # Filter standard errors if coefficients were filtered
    if coefs is not None and len(coefs) > 0 and 'mask' in locals() and mask.sum() > 0:
        se_values = se_values[mask]
    
    # Ensure coef_names is a list (not a single string)
    if isinstance(coef_names, str):
        coef_names = [coef_names]
    elif not isinstance(coef_names, list):
        coef_names = list(coef_names)
    
    # Ensure lengths match
    if len(coef_values) != len(coef_names):
        # If mismatch, use default labels
        coef_names = [f"Coefficient {i+1}" for i in range(len(coef_values))]
    
    # Create plot
    coefplot_py(coef_values, ses=se_values, labels=coef_names,
               horizontal=horizontal, ci_level=ci_level,
               title=title, savepath=savepath, **kwargs)


# For backward compatibility and easy import
__all__ = ['CoefPlot', 'coefplot_py', 'coefplot_from_stata']
