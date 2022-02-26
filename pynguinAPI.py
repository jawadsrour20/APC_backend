import subprocess
import shlex
import os
import utils


target_script = './pynguinAPI.sh' if utils.is_unix() else "./pynguinAPI.ps"
input_dir = '/input'
output_dir = '/output'

def run(module_name):
    """Runs Pynguin on the given module name to generate unit test cases, and returns the results output

    Args:
        module_name (string): The name of the module to generate unit test cases for

    Returns:
        string: output results from running the PynguinAPI script
    """

    return run_unix(module_name) if utils.is_unix() else run_windows(module_name)

def run_unix(module_name):

    args = shlex.split(f"{target_script} {input_dir} {output_dir} {module_name}")
    return subprocess.check_output(args).decode('utf-8')

    # alternative:
    # stream = os.popen(f"{target_script} {input_dir} {output_dir} {module_name}")
    # output = stream.read()
    # return output

def run_windows(module_name):
    pass