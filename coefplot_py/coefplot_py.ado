*! version 1.0.0  coefplot_py - Python implementation of coefplot
*! Wrapper command to call Python coefplot from Stata
*! Usage: coefplot_py [coeflist] [, options]
*! 
*! Example:
*!   regress y x1 x2 x3
*!   coefplot_py x1 x2, save("coefplot.png") title("My Results")

program define coefplot_py
    version 16
    
    syntax [anything(name=namelist)] [, ///
        HORizontal          /// Plot horizontally (default)
        VERTical            /// Plot vertically
        CILevel(real 95)    /// Confidence interval level
        Title(str)          /// Plot title
        Save(str)           /// Save path for figure
        ESTimates(str)      /// Use stored estimates
        COLors(str)         /// Colors (comma-separated)
        MARKers(str)        /// Markers (comma-separated)
        MARKerSize(real 6)  /// Marker size
        CIWidth(real 0.3)   /// CI width
        CIStyle(str)        /// CI style: line, bar, area
        NOZero               /// Don't draw zero line
        NOGrid               /// Don't show grid
        NOLEgend             /// Don't show legend
        XLabel(str)         /// X-axis label
        YLabel(str)         /// Y-axis label
        XLimit(str)         /// X-axis limits (min max)
        FIGSize(str)        /// Figure size (width height)
        DPI(real 300)       /// Resolution
        *                   /// Additional options
    ]
    
    // Check if estimation results exist
    if "`estimates'" == "" {
        if "`e(cmd)'" == "" {
            display as error "no estimation results found"
            display as error "either run an estimation command first, or use estimates() option"
            exit 301
        }
        local est_name "."
    }
    else {
        local est_name "`estimates'"
    }
    
    // Restore estimates if needed
    if "`estimates'" != "" {
        qui estimates restore `estimates'
    }
    
    // Determine orientation
    local orient = cond("`vertical'" != "", "False", "True")
    
    // Set defaults
    if "`cistyle'" == "" local cistyle "line"
    if "`title'" == "" local title "Coefficient Plot"
    if "`markersize'" == "" local markersize "6"
    if "`ciwidth'" == "" local ciwidth "0.3"
    if "`cilevel'" == "" local cilevel "95"
    if "`dpi'" == "" local dpi "300"
    
    // Add current directory to Python path
    local current_dir = c(pwd)
    local personal_dir = c(sysdir_personal)
    
    // Build coefficient names string for Python
    local coef_str "None"
    if "`namelist'" != "" {
        local coef_str "["
        local first 1
        foreach name of local namelist {
            if !`first' local coef_str `"`coef_str', "'
            local coef_str `"`coef_str'"`name'""'
            local first 0
        }
        local coef_str `"`coef_str']"'
    }
    
    // Build savepath string (absolute path rooted at current Stata dir)
    local save_str "None"
    if "`save'" != "" {
        // If path is already absolute (starts with / or ~ or drive letter), use as-is
        local firstchar = substr("`save'",1,1)
        local absflag 0
        if "`firstchar'" == "/" local absflag 1
        if "`firstchar'" == "~" local absflag 1
        if strpos("`save'", ":") == 2 local absflag 1
        if `absflag' {
            local save_abs `"`save'"'
        }
        else {
            local save_abs `"`c(pwd)'/`save'"'
        }
        local save_str `"r"`save_abs'""'
    }
    
    // Build colors string (accept comma- or space-separated)
    local colors_str "None"
    if "`colors'" != "" {
        // Replace commas with spaces and trim
        local colors_clean : subinstr local colors "," " " , all
        local colors_clean : list retokenize colors_clean
        local colors_str `"['
        local first 1
        foreach color of local colors_clean {
            if !`first' local colors_str `"`colors_str', '
            local colors_str `"`colors_str'r"`color'""'
            local first 0
        }
        local colors_str `"`colors_str']"'
    }
    
    // Build markers string (accept comma- or space-separated)
    local markers_str "None"
    if "`markers'" != "" {
        local markers_clean : subinstr local markers "," " " , all
        local markers_clean : list retokenize markers_clean
        local markers_str `"['
        local first 1
        foreach marker of local markers_clean {
            if !`first' local markers_str `"`markers_str', '
            local markers_str `"`markers_str'r"`marker'""'
            local first 0
        }
        local markers_str `"`markers_str']"'
    }
    
    // Build xlim string
    local xlim_str "None"
    if "`xlimit'" != "" {
        local xlim_parts : word count `xlimit'
        if `xlim_parts' == 2 {
            local xmin : word 1 of `xlimit'
            local xmax : word 2 of `xlimit'
            local xlim_str `"(`xmin', `xmax')"'
        }
    }
    
    // Build figsize string
    local figsize_str "None"
    if "`figsize'" != "" {
        local size_parts : word count `figsize'
        if `size_parts' == 2 {
            local width : word 1 of `figsize'
            local height : word 2 of `figsize'
            local figsize_str `"(`width', `height')"'
        }
    }
    
    // Build xlabel/ylabel strings
    local xlabel_str "None"
    if "`xlabel'" != "" {
        local xlabel_str `"r"`xlabel'""'
    }
    local ylabel_str "None"
    if "`ylabel'" != "" {
        local ylabel_str `"r"`ylabel'""'
    }
    
    // Execute Python code using exec to handle multi-line blocks properly
    python: import sys, os
    python: sys.path.insert(0, r"`current_dir'")
    python: sys.path.insert(0, r"`personal_dir'")
    python: coefplot_dir = os.path.join(r"`current_dir'", "coefplot_py")
    python: exec("if os.path.exists(coefplot_dir): sys.path.insert(0, coefplot_dir)")
    python: home_dir = os.path.expanduser("~")
    python: coefplot_home = os.path.join(home_dir, "coefplot_py")
    python: exec("if os.path.exists(coefplot_home): sys.path.insert(0, coefplot_home)")
    python: exec("try:\n    from tools import coefplot_from_stata\nexcept ImportError:\n    try:\n        from coefplot_py.tools import coefplot_from_stata\n    except ImportError:\n        print('Error: tools.py not found.')\n        print(f'Tried: {coefplot_home}')\n        print(f'Tried: {coefplot_dir}')\n        print(f'Current directory: {os.getcwd()}')\n        print(f'Python path: {sys.path}')\n        sys.exit(1)")
    python: coef_names = `coef_str'
    python: savepath = `save_str'
    python: # Ensure relative save paths are rooted at Stata's working directory
    python: import os
    python: if savepath is not None and not os.path.isabs(savepath):
    python:     savepath = os.path.join(r"`current_dir'", savepath)
    python: options = {'horizontal': `orient', 'ci_level': `cilevel', 'title': r"`title'", 'savepath': savepath, 'marker_size': `markersize', 'ci_width': `ciwidth', 'ci_style': r"`cistyle'", 'zero_line': `=cond("`nozero'"!="", "False", "True")', 'grid': `=cond("`nogrid'"!="", "False", "True")', 'legend': `=cond("`nolegend'"!="", "False", "True")', 'dpi': `dpi'}
    python: colors_opt = `colors_str'
    python: options['colors'] = colors_opt
    python: markers_opt = `markers_str'
    python: options['markers'] = markers_opt
    python: xlim_opt = `xlim_str'
    python: options['xlim'] = xlim_opt
    python: figsize_opt = `figsize_str'
    python: options['figsize'] = figsize_opt
    python: xlabel_opt = `xlabel_str'
    python: options['xlabel'] = xlabel_opt
    python: ylabel_opt = `ylabel_str'
    python: options['ylabel'] = ylabel_opt
    python: exec("try:\n    print(f'Saving to: {options.get('savepath')}')\n    coefplot_from_stata(est_name=r\".\", coefs=coef_names, **options)\n    print('Plot created successfully')\nexcept Exception as e:\n    print(f'Error creating plot: {e}')\n    import traceback\n    traceback.print_exc()\n    sys.exit(1)")
    
end
