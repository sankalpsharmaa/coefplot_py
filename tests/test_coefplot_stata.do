* Test script for coefplot_py Stata command
* ==========================================
*
* This script tests the coefplot_py command with various Stata estimation commands
* Run this after installing coefplot_py.ado and ensuring tools.py is accessible

* Check if Python is available
capture python query
if _rc != 0 {
    display as error "Python is not configured in Stata"
    display as error "Run: python set exec <path_to_python>"
    exit 199
}

display "Python is configured"
python query

* Test 1: Basic regression
display _n "Test 1: Basic regression"
sysuse auto, clear
regress price mpg weight
coefplot_py, save("test_stata1.png") title("Test 1: Basic Regression")
display "✓ Test 1 completed"

* Test 2: Specific coefficients
display _n "Test 2: Specific coefficients"
regress price mpg weight
coefplot_py mpg weight, save("test_stata2.png") title("Test 2: Selected Coefficients")
display "✓ Test 2 completed"

* Test 3: With clustering
display _n "Test 3: Clustered standard errors"
regress price mpg weight, cluster(rep78)
coefplot_py mpg, save("test_stata3.png") title("Test 3: Clustered SE")
display "✓ Test 3 completed"

* Test 4: Custom styling
display _n "Test 4: Custom styling"
regress price mpg weight
coefplot_py mpg weight, ///
    save("test_stata4.png") ///
    title("Test 4: Custom Style") ///
    colors("red, blue") ///
    markers("o, s") ///
    markersize(10) ///
    cilevel(90)
display "✓ Test 4 completed"

* Test 5: Vertical orientation
display _n "Test 5: Vertical orientation"
regress price mpg weight
coefplot_py mpg weight, ///
    save("test_stata5.png") ///
    title("Test 5: Vertical") ///
    vertical
display "✓ Test 5 completed"

* Test 6: Stored estimates
display _n "Test 6: Stored estimates"
regress price mpg
estimates store model1
regress price mpg weight
estimates store model2

coefplot_py mpg, estimates(model1) save("test_stata6a.png") title("Model 1")
coefplot_py mpg, estimates(model2) save("test_stata6b.png") title("Model 2")
display "✓ Test 6 completed"

* Test 7: Fixed effects (if reghdfe available)
capture which reghdfe
if _rc == 0 {
    display _n "Test 7: Fixed effects regression"
    sysuse auto, clear
    reghdfe price mpg, absorb(rep78) cluster(rep78)
    coefplot_py mpg, save("test_stata7.png") title("Test 7: Fixed Effects")
    display "✓ Test 7 completed"
}
else {
    display _n "Test 7: Skipped (reghdfe not available)"
}

* Summary
display _n "=========================================="
display "TEST SUMMARY"
display "=========================================="
display "All tests completed!"
display "Check test_stata*.png files for output"
display ""
display "If any tests failed, check:"
display "1. coefplot_py.ado is in your ado-path"
display "2. tools.py is accessible from Python"
display "3. Python packages are installed (matplotlib, numpy, pandas)"

