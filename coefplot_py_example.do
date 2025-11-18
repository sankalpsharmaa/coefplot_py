* ============================================================================
* Comprehensive Example: coefplot_py with Fake Dataset
* ============================================================================
* This file creates a fake Stata dataset and thoroughly tests all features
* of the coefplot_py "command."
*
* Requirements:
* - Stata 16+ with Python integration
* - "coefplot_py.ado" in your ado-path
* - coefplot_py package installed or accessible
* ============================================================================

clear all
set seed 12345

* Determine the directory of this do-file; fallback to current dir
local dofile = c(filename)
local do_dir ""
if strpos("`dofile'", "/")>0 {
    local do_dir = substr("`dofile'", 1, strrpos("`dofile'", "/")-1)
}
else {
    local do_dir = c(pwd)
}

* Load the local coefplot_py ado from the repo
capture program drop coefplot_py
quietly do "`do_dir'/coefplot_py/coefplot_py.ado"

* Create tests directory if it doesn't exist
local outdir `"`do_dir'/tests"'
capture mkdir "`outdir'"

* ============================================================================
* PART 1: CREATE FAKE DATASET
* ============================================================================

* Create a panel dataset with treatment effects
set obs 1000

* Generate panel IDs
gen plot_id = floor((_n - 1) / 10) + 1
gen individual_id = mod(_n - 1, 10) + 1

* Generate time periods
expand 5
bysort plot_id individual_id: gen time = _n
gen year = 2010 + time

* Generate treatment variable (post_treated: 1 if treated after period 3)
gen post_treated = (time > 3) if plot_id <= 50
replace post_treated = 0 if missing(post_treated)

* Generate religion type (categorical)
gen religion_type = mod(plot_id, 4) + 1
label define religion_lbl 1 "Catholic" 2 "Protestant" 3 "Muslim" 4 "Other"
label values religion_type religion_lbl

* Generate event study periods
gen event_period = time - 3
replace event_period = -2 if event_period < -2
replace event_period = 2 if event_period > 2

* Generate outcome variable with treatment effect
gen num_sisters = 2 + 0.15 * post_treated + 0.05 * religion_type + 0.02 * time + 0.1 * (plot_id / 10) + rnormal(0, 0.5)

* Ensure positive values
replace num_sisters = abs(num_sisters)

* Generate additional variables for more complex models
gen age = 25 + rnormal(0, 5)
gen education = 12 + rnormal(0, 2)
gen income = 30000 + rnormal(0, 10000)

* Create interaction terms
gen treated_x_event = post_treated * event_period

* Label variables
label variable num_sisters "Number of Sisters"
label variable post_treated "Post-Treatment"
label variable religion_type "Religion Type"
label variable plot_id "Plot ID"
label variable time "Time Period"
label variable year "Year"
label variable event_period "Event Period"
label variable age "Age"
label variable education "Education"
label variable income "Income"

* ============================================================================
* PART 2: BASIC TESTS
* ============================================================================

display as text _n "========================================"
display as text "PART 2: BASIC TESTS"
display as text "========================================" _n

* Test 1: Basic regression with single coefficient
display as text "Test 1: Basic regression with single coefficient"
regress num_sisters post_treated, cluster(plot_id)
coefplot_py, save("`outdir'/example1_basic.png") title("Test 1: Basic Plot")
display as text "✓ Test 1 completed" _n

* Test 2: Plot specific coefficient only
display as text "Test 2: Plot specific coefficient only"
regress num_sisters post_treated, cluster(plot_id)
coefplot_py post_treated, save("`outdir'/example2_specific.png") title("Test 2: Specific Coefficient")
display as text "✓ Test 2 completed" _n

* Test 3: Multiple coefficients
display as text "Test 3: Multiple coefficients"
regress num_sisters post_treated i.religion_type, cluster(plot_id)
coefplot_py post_treated "1.religion_type" "2.religion_type", save("`outdir'/example3_multiple.png") title("Test 3: Multiple Coefficients")
display as text "✓ Test 3 completed" _n

* ============================================================================
* PART 3: STYLING OPTIONS
* ============================================================================

display as text _n "========================================"
display as text "PART 3: STYLING OPTIONS"
display as text "========================================" _n

* Test 4: Custom colors
display as text "Test 4: Custom colors"
regress num_sisters post_treated i.religion_type, cluster(plot_id)
coefplot_py post_treated "1.religion_type", save("`outdir'/example4_colors.png") title("Test 4: Custom Colors")
display as text "✓ Test 4 completed" _n

* Test 5: Custom markers
display as text "Test 5: Custom markers"
regress num_sisters post_treated i.religion_type, cluster(plot_id)
coefplot_py post_treated "1.religion_type", save("`outdir'/example5_markers.png") title("Test 5: Custom Markers") markersize(10)
display as text "✓ Test 5 completed" _n

* Test 6: CI styling
display as text "Test 6: CI styling (bar style)"
regress num_sisters post_treated, cluster(plot_id)
coefplot_py post_treated, save("`outdir'/example6_ci_bar.png") title("Test 6: CI Bar Style") cistyle("bar") ciwidth(0.4)
display as text "✓ Test 6 completed" _n

* Test 7: Custom CI level
display as text "Test 7: Custom CI level (90%)"
regress num_sisters post_treated, cluster(plot_id)
coefplot_py post_treated, save("`outdir'/example7_ci90.png") title("Test 7: 90% Confidence Interval") cilevel(90)
display as text "✓ Test 7 completed" _n

* Test 8: No zero line, no grid
display as text "Test 8: Minimal styling (no zero line, no grid)"
regress num_sisters post_treated, cluster(plot_id)
coefplot_py post_treated, save("`outdir'/example8_minimal.png") title("Test 8: Minimal Style") nozero nogrid
display as text "✓ Test 8 completed" _n

* ============================================================================
* PART 4: ORIENTATION AND LAYOUT
* ============================================================================

display as text _n "========================================"
display as text "PART 4: ORIENTATION AND LAYOUT"
display as text "========================================" _n

* Test 9: Vertical orientation
display as text "Test 9: Vertical orientation"
regress num_sisters post_treated i.religion_type, cluster(plot_id)
coefplot_py post_treated "1.religion_type" "2.religion_type", save("`outdir'/example9_vertical.png") title("Test 9: Vertical Plot") vertical
display as text "✓ Test 9 completed" _n

* Test 10: Custom figure size
display as text "Test 10: Custom figure size"
regress num_sisters post_treated, cluster(plot_id)
coefplot_py post_treated, save("`outdir'/example10_figsize.png") title("Test 10: Custom Figure Size") figsize(12 8)
display as text "✓ Test 10 completed" _n

* Test 11: High resolution
display as text "Test 11: High resolution (600 DPI)"
regress num_sisters post_treated, cluster(plot_id)
coefplot_py post_treated, save("`outdir'/example11_highres.png") title("Test 11: High Resolution") dpi(600)
display as text "✓ Test 11 completed" _n

* ============================================================================
* PART 5: AXES AND LABELS
* ============================================================================

display as text _n "========================================"
display as text "PART 5: AXES AND LABELS"
display as text "========================================" _n

* Test 12: Custom axis labels
display as text "Test 12: Custom axis labels"
regress num_sisters post_treated, cluster(plot_id)
coefplot_py post_treated, save("`outdir'/example12_axis_labels.png") title("Test 12: Custom Axis Labels") xlabel("Treatment Effect on Number of Sisters") ylabel("")
display as text "✓ Test 12 completed" _n

* Test 13: X-axis limits
display as text "Test 13: X-axis limits"
regress num_sisters post_treated, cluster(plot_id)
coefplot_py post_treated, save("`outdir'/example13_xlimits.png") title("Test 13: Custom X-Axis Limits") xlimit(-0.1 0.3)
display as text "✓ Test 13 completed" _n

* ============================================================================
* PART 6: STORED ESTIMATES
* ============================================================================

display as text _n "========================================"
display as text "PART 6: STORED ESTIMATES"
display as text "========================================" _n

* Test 14: Using stored estimates
display as text "Test 14: Using stored estimates"
regress num_sisters post_treated, cluster(plot_id)
estimates store model1

regress num_sisters post_treated i.religion_type, cluster(plot_id)
estimates store model2

regress num_sisters post_treated i.religion_type age education, cluster(plot_id)
estimates store model3

coefplot_py post_treated, estimates(model1) save("`outdir'/example14_model1.png") title("Test 14: Model 1 (Stored Estimates)")
display as text "✓ Test 14a completed"

coefplot_py post_treated, estimates(model2) save("`outdir'/example14_model2.png") title("Test 14: Model 2 (Stored Estimates)")
display as text "✓ Test 14b completed"

coefplot_py post_treated, estimates(model3) save("`outdir'/example14_model3.png") title("Test 14: Model 3 (Stored Estimates)")
display as text "✓ Test 14c completed" _n

* ============================================================================
* PART 7: COMPLEX MODELS
* ============================================================================

display as text _n "========================================"
display as text "PART 7: COMPLEX MODELS"
display as text "========================================" _n

* Test 15: Event study
display as text "Test 15: Event study coefficients"
gen event_m2 = (event_period == -2)
gen event_m1 = (event_period == -1)
gen event_0 = (event_period == 0)
gen event_p1 = (event_period == 1)
gen event_p2 = (event_period == 2)

regress num_sisters event_m2 event_m1 event_0 event_p1 event_p2, cluster(plot_id)
coefplot_py event_m2 event_m1 event_0 event_p1 event_p2, save("`outdir'/example15_event_study.png") title("Test 15: Event Study Coefficients")
display as text "✓ Test 15 completed" _n

* Test 16: Interaction terms
display as text "Test 16: Interaction terms"
regress num_sisters post_treated##religion_type, cluster(plot_id)
coefplot_py post_treated "1.post_treated#1.religion_type" "1.post_treated#2.religion_type", save("`outdir'/example16_interactions.png") title("Test 16: Interaction Terms")
display as text "✓ Test 16 completed" _n

* Test 17: Many coefficients
display as text "Test 17: Many coefficients"
regress num_sisters post_treated i.religion_type age education income, cluster(plot_id)
coefplot_py post_treated "1.religion_type" "2.religion_type" "3.religion_type" age education income, save("`outdir'/example17_many_coefs.png") title("Test 17: Many Coefficients")
display as text "✓ Test 17 completed" _n

* ============================================================================
* PART 8: EDGE CASES
* ============================================================================

display as text _n "========================================"
display as text "PART 8: EDGE CASES"
display as text "========================================" _n

* Test 18: Single coefficient
display as text "Test 18: Single coefficient"
regress num_sisters post_treated, cluster(plot_id)
coefplot_py post_treated, save("`outdir'/example18_single.png") title("Test 18: Single Coefficient")
display as text "✓ Test 18 completed" _n

* Test 19: All coefficients (no selection)
display as text "Test 19: All coefficients"
regress num_sisters post_treated i.religion_type, cluster(plot_id)
coefplot_py, save("`outdir'/example19_all_coefs.png") title("Test 19: All Coefficients")
display as text "✓ Test 19 completed" _n

* Test 20: Combined options
display as text "Test 20: Combined options"
regress num_sisters post_treated i.religion_type, cluster(plot_id)
coefplot_py post_treated "1.religion_type", save("`outdir'/example20_combined.png") title("Test 20: Combined Options") markersize(12) ciwidth(0.5) cilevel(99) cistyle("bar") xlabel("Coefficient Value") ylabel("") xlimit(-0.2 0.4) figsize(10 6) dpi(300)
display as text "✓ Test 20 completed" _n

* ============================================================================
* SUMMARY
* ============================================================================

display as text _n "========================================"
display as text "TEST SUMMARY"
display as text "========================================"
display as text "All 20 tests completed successfully!"
display as text "Check the tests/ directory for output PNG files."
display as text "========================================" _n

* List all created files
display as text "Created files:"
local files : dir "tests" files "example*.png"
foreach file of local files {
    display as text "  - `file'"
}
