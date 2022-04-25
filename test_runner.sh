#!/bin/bash
# Script that runs the Python unit tests.
# It is used to run the unit tests against student code submissions
FILE_PATH=$1
passed_test_cases_count=$(python ${FILE_PATH})
echo ${passed_test_cases_count}