#!/bin/bash
# Script to run coefplot_py examples in Stata
# Usage: ./run_examples.sh [stata_executable]
# Example: ./run_examples.sh stata-mp

# Default Stata executable
STATA_EXEC="${1:-stata-mp}"

# Check if Stata executable exists
if ! command -v "$STATA_EXEC" &> /dev/null; then
    echo "Error: Stata executable '$STATA_EXEC' not found"
    echo "Please provide the path to your Stata executable:"
    echo "  ./run_examples.sh /path/to/stata"
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
EXAMPLE_FILE="$PROJECT_DIR/coefplot_py_example.do"

# Check if example file exists
if [ ! -f "$EXAMPLE_FILE" ]; then
    echo "Error: Example file not found: $EXAMPLE_FILE"
    exit 1
fi

# Create tests directory if it doesn't exist
mkdir -p "$SCRIPT_DIR"

# Change to project directory
cd "$PROJECT_DIR"

echo "=========================================="
echo "Running coefplot_py examples"
echo "=========================================="
echo "Stata executable: $STATA_EXEC"
echo "Example file: $EXAMPLE_FILE"
echo "Output directory: $SCRIPT_DIR"
echo "=========================================="
echo ""

# Run Stata in batch mode
"$STATA_EXEC" -b do "$EXAMPLE_FILE"

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Examples completed successfully!"
    echo "=========================================="
    echo "Check $SCRIPT_DIR for output PNG files"
    
    # First, copy any outputs that Stata may have saved under the user's home directory
    if [ -d "$HOME/tests" ]; then
        # Copy example*.png from ~/tests into the repo tests directory
        cp -f "$HOME"/tests/example*.png "$SCRIPT_DIR" 2>/dev/null || true
    fi

    # Count output files in the repo tests directory
    FILE_COUNT=$(ls -1 "$SCRIPT_DIR"/example*.png 2>/dev/null | wc -l)
    echo "Created $FILE_COUNT PNG files"
else
    echo ""
    echo "=========================================="
    echo "Error: Examples failed to run"
    echo "=========================================="
    exit 1
fi
