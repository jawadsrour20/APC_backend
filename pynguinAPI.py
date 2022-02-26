import re
import subprocess
import shlex
import os
import utils

TARGET_SCRIPT = "./pynguinAPI.sh" if utils.is_unix() else "./pynguinAPI.ps"
# INPUT_DIR and OUTPUT_DIR are needed for the shell script to work properly
INPUT_DIR = "/input"
OUTPUT_DIR = "/output"
RELATIVE_INPUT_DIR = "./input/"
RELATIVE_OUTPUT_DIR = "./output/"
TEST_MODULE_PREFIX = "test_"
TEST_MODULE_FAILING_POSTFIX = "_failing"
FILE_EXTENSION = ".py"

def run(file_name):
    """Runs Pynguin on the given module name to generate unit test cases, and returns the results output

    Args:
        file_name (string): The name of the module to generate unit test cases for

    Returns:
        string: output results from running the PynguinAPI script
    """
    module_name = utils.get_file_name_without_extension(file_name)

    return run_unix(module_name) if utils.is_unix() else run_windows(module_name)

def run_unix(module_name):

    args = shlex.split(f"{TARGET_SCRIPT} {INPUT_DIR} {OUTPUT_DIR} {module_name}")
    return subprocess.check_output(args).decode('utf-8')

    # alternative:
    # stream = os.popen(f"{target_script} {input_dir} {output_dir} {module_name}")
    # output = stream.read()
    # return output

def run_windows(module_name):
    pass


def count_test_cases(file_path):

    if not os.path.exists(file_path):
        return 0
    counter = 0
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("def"):
                counter += 1
    return counter

def count_test_cases_passed(module_name):
    assert not module_name.endswith(FILE_EXTENSION)
    passed_test_cases_file = (
        f'{RELATIVE_OUTPUT_DIR}/{TEST_MODULE_PREFIX}{module_name}{FILE_EXTENSION}'
    )
    return count_test_cases(passed_test_cases_file)


def count_test_cases_failed(module_name):
    assert not module_name.endswith(FILE_EXTENSION)
    failed_test_cases_file = (
        f'{RELATIVE_OUTPUT_DIR}/{TEST_MODULE_PREFIX}{module_name}{TEST_MODULE_FAILING_POSTFIX}{FILE_EXTENSION}'
    )
    return count_test_cases(failed_test_cases_file)

def count_passed_and_failed_test_cases(file_name):
    module_name = utils.get_file_name_without_extension(file_name)
    return {
        "passed_test_cases": count_test_cases_passed(module_name),
        "failed_test_cases": count_test_cases_failed(module_name)
    }

