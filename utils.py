import os

def get_file_name_without_extension(file_name, extension='.py'):
    return file_name[:file_name.rindex(extension)]


def get_os():
    return os.name

# Returns True if the OS is MacOS or Linux, False otherwise (Windows)
def is_unix():
    return get_os() == 'posix'