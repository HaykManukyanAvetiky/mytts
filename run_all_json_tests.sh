#!/bin/bash
# Run all JSON error handling tests
# This script executes all test files and provides a summary

echo "================================================================"
echo "JSON Error Handling - Complete Test Suite"
echo "================================================================"
echo ""
echo "Working Directory: $(pwd)"
echo "Date: $(date)"
echo ""

# Initialize counters
total_tests=0
passed_tests=0
failed_tests=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to run a test and track results
run_test() {
    local test_file=$1
    local test_name=$2

    echo "================================================================"
    echo "Running: $test_name"
    echo "================================================================"
    echo ""

    python3 "$test_file"
    local exit_code=$?

    total_tests=$((total_tests + 1))

    if [ $exit_code -eq 0 ]; then
        passed_tests=$((passed_tests + 1))
        echo -e "${GREEN}✓ $test_name PASSED${NC}"
    else
        failed_tests=$((failed_tests + 1))
        echo -e "${RED}✗ $test_name FAILED${NC}"
    fi

    echo ""
    return $exit_code
}

# Run all tests
run_test "test_json_error_handling.py" "Main Error Handling Test"
run_test "test_json_exact_example.py" "Exact Task Example Test"
run_test "test_json_error_edge_cases.py" "Edge Cases Test"

# Print summary
echo "================================================================"
echo "TEST SUITE SUMMARY"
echo "================================================================"
echo ""
echo "Total Tests:  $total_tests"
echo -e "Passed:       ${GREEN}$passed_tests${NC}"

if [ $failed_tests -gt 0 ]; then
    echo -e "Failed:       ${RED}$failed_tests${NC}"
else
    echo -e "Failed:       $failed_tests"
fi

echo ""

if [ $failed_tests -eq 0 ]; then
    echo -e "${GREEN}================================================================${NC}"
    echo -e "${GREEN}ALL TESTS PASSED! ✓${NC}"
    echo -e "${GREEN}================================================================${NC}"
    exit 0
else
    echo -e "${RED}================================================================${NC}"
    echo -e "${RED}SOME TESTS FAILED! ✗${NC}"
    echo -e "${RED}================================================================${NC}"
    exit 1
fi
