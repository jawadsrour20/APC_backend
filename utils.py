
def get_file_name_without_extension(file_name, extension='.py'):
    return file_name[:file_name.rindex(extension)]