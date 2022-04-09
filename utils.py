import os

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

