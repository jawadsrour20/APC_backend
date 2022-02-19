import subprocess
import shlex
import os
target_script = './pynguinAPI.sh'
input_dir = '/input'
output_dir = '/output'

def run(module_name):
    """
    Runs the given command and returns the output.
    :param command: The command to be run.
    :return: The output of the command.
    """
    args = shlex.split(f"{target_script} {input_dir} {output_dir} {module_name}")
    return subprocess.check_output(args).decode('utf-8')

    # alternative:
    # stream = os.popen(f"{target_script} {input_dir} {output_dir} {module_name}")
    # output = stream.read()
    # return output


