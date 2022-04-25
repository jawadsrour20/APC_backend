import os
import subprocess
import shlex

def get_file_name_without_extension(file_name, extension='.py'):
    return file_name[:file_name.rindex(extension)]


def get_os():
    return os.name

# Returns True if the OS is MacOS or Linux, False otherwise (Windows)
def is_unix():
    return get_os() == 'posix'

def create_submissions_container_folder():
    if not os.path.exists("submissions"):
        os.mkdir("submissions")
        print("Directory submissions created.")
    else:
        print("Directory submissions already exists")

def create_folder(folder_name):

    if not os.path.exists("submissions"):
        create_submissions_container_folder()
    try:
        os.mkdir(f"submissions/{folder_name}")
        print("Directory ", folder_name, " created.")
    except FileExistsError:
        print("Directory " , folder_name ,  " already exists")


def get_function_prototype(directory, file_name):

    function_prototype = None
    with open(f"{directory}/{file_name}", "r") as f:
        for line in f:
            if line.startswith("def"):
                function_prototype = line
                break
    # returns None if File does not contain a function
    return function_prototype

def get_problem_difficulty(file_name):

    if is_unix():
        return get_problem_difficulty_unix(file_name)
    else:
        return get_problem_difficulty_windows(file_name)


# shell scripts need permission to be executed
# run the command --> chmod +rwx <shell_script_file_name>
def get_problem_difficulty_unix(file_name):
    TARGET_SCRIPT = "./radonHalstead.sh"
    FILE_PATH = "./input/"
    args = shlex.split(f"{TARGET_SCRIPT} {FILE_PATH} {file_name}")
    output = subprocess.check_output(args).decode('utf-8')
    difficulty = output.split(":")[1].strip()

    return convert_problem_difficulty_to_string(float(difficulty))

def get_problem_difficulty_windows(file_name):
    pass


def evaluate_passed_test_cases(file_path):

    if is_unix():
            return evaluate_passed_test_cases_unix(file_path)
    else:
        return evaluate_passed_test_cases_windows(file_path)


def evaluate_passed_test_cases_unix(file_path):
    TARGET_SCRIPT = "./test_runner.sh"
    args = shlex.split(f"{TARGET_SCRIPT} {file_path}")
    return subprocess.check_output(args).decode('utf-8')


def evaluate_passed_test_cases_windows(file_path):
    pass


def convert_problem_difficulty_to_string(problem_difficulty):
    if problem_difficulty <= 3:
        return "easy"
    elif problem_difficulty <= 5:
        return "medium"
    else:
        return "hard"

def count_test_cases(file_path):

    if not os.path.exists(file_path):
        return 0
    counter = 0
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("def"):
                counter += 1
    return counter


# print(get_problem_difficulty("speed_at_intersection.py"))