import pprint

function1 = 'ReachIntersection' # takes 4 input parameters
function2 = 'SpeedAtIntersection' # takes 3 input parameters
function3 = 'SetFinalSpeed' # takes 4 input parameters


data_set = {
        function1: [],
        function2: [],
        function3: [],
        }


def find_functions_body(file_name):

    # a file starts at line_number = 1
    start_line = 1
    end_line = 1
    count_lines = 1

    number_of_functions = sum(1 for line in open(f'{file_name}', 'r') if line.startswith('def'))
    functions = list()
    num_lines = sum(1 for line in open(f'{file_name}', 'r'))


    for function_index in range(number_of_functions):
        function_name = 'test_case_' + str(function_index)
        # get total number of lines in file
        # Find the start_line for a function
        with open(f'{file_name}', 'r') as file:
            for line in file.readlines():
                if len(line.split()) != 0:
                    if line.split()[0] == "def" and line[slice(4, line.index('('))] == function_name:
                        start_line = count_lines
                count_lines += 1

        # print("Start line = ", start_line)
        count_lines = 1
        # Find the end_line for a function

        with open(f'{file_name}', 'r') as file:
            for line in file.readlines():

                # The first time count_lines is greater than start_line is inside the function's body
                if count_lines > start_line:

                    # \n inserted --> function ended
                    if len(line.split()) == 0:
                        end_line = count_lines - 1
                        break
                    # case statement returns a value
                    elif line.split()[0] == 'return':
                        end_line = count_lines
                        break
                    # case statement has no return value
                    elif not line.split('\t')[0][0].isspace():
                        end_line = count_lines - 1
                    # case E.O.F
                    elif count_lines == num_lines:
                        end_line = count_lines
                        break

                # TODO
                # case of nested loops in a function and return value has multiple tabs inserted before it
                # case of nested loops and no return value
                # case func calling itself
                # case func calling funcs several times

                count_lines += 1

        # print("End line = ", end_line)

        # reset counter
        count_lines = 1
        func_body = list()
        with open(f'{file_name}', 'r') as file:
            for line in file.readlines():

                if start_line <= count_lines <= end_line:
                    func_body.append(line)

                count_lines += 1

        func_body = [line.strip() for line in func_body]
        functions.append(func_body)

        # reset counters
        start_line = 1
        end_line = 1
        count_lines = 1

    return functions


def get_functions_parameters(file_name):
    functions = find_functions_body(file_name)

    for function in functions:
        function1_calls = list()
        function2_calls = list()
        function3_calls = list()
        for function_line in function:
            if function1 in function_line:
                function1_calls.append(function_line)
            if function2 in function_line:
                function2_calls.append(function_line)
            if function3 in function_line:
                function3_calls.append(function_line)
        # print(function1_calls)
        # print(function2_calls)
        # print(function3_calls)


        for function1_call in function1_calls:
            input_parameters = function1_call[function1_call.rindex('(')+1:function1_call.rindex(')')].split(',')
            input_parameters = [input_parameter.strip() for input_parameter in input_parameters]
            input_parameter1 = input_parameters[0] + " ="
            input_parameter2 = input_parameters[1] + " ="
            input_parameter3 = input_parameters[2] + " ="
            input_parameter4 = input_parameters[3] + " ="
            input_parameter1_value, input_parameter2_value, input_parameter3_value, input_parameter4_value = 0, 0, 0, 0
            for function_line in function:
                if input_parameter1 in function_line:
                    input_parameter1_value = function_line.split("=")[1].strip()
                if input_parameter2 in function_line:
                    input_parameter2_value = function_line.split("=")[1].strip()
                if input_parameter3 in function_line:
                    input_parameter3_value = function_line.split("=")[1].strip()
                if input_parameter4 in function_line:
                    input_parameter4_value = function_line.split("=")[1].strip()

            data_set[function1].append([input_parameter1_value, input_parameter2_value, input_parameter3_value, input_parameter4_value])

        for function2_call in function2_calls:
            input_parameters = function2_call[function2_call.rindex('(')+1:function2_call.rindex(')')].split(',')
            input_parameters = [input_parameter.strip() for input_parameter in input_parameters]
            input_parameter1 = input_parameters[0] + " ="
            input_parameter2 = input_parameters[1] + " ="
            input_parameter3 = input_parameters[2] + " ="
            input_parameter1_value, input_parameter2_value, input_parameter3_value = 0, 0, 0
            for function_line in function:
                if input_parameter1 in function_line:
                    input_parameter1_value = function_line.split("=")[1].strip()
                if input_parameter2 in function_line:
                    input_parameter2_value = function_line.split("=")[1].strip()
                if input_parameter3 in function_line:
                    input_parameter3_value = function_line.split("=")[1].strip()

            data_set[function2].append([input_parameter1_value, input_parameter2_value, input_parameter3_value])

        for function3_call in function3_calls:
            input_parameters = function3_call[function3_call.rindex('(')+1:function3_call.rindex(')')].split(',')
            input_parameters = [input_parameter.strip() for input_parameter in input_parameters]
            input_parameter1 = input_parameters[0] + " ="
            input_parameter2 = input_parameters[1] + " ="
            input_parameter3 = input_parameters[2] + " ="
            input_parameter4 = input_parameters[3] + " ="
            input_parameter1_value, input_parameter2_value, input_parameter3_value, input_parameter4_value = 0, 0, 0, 0
            for function_line in function:
                if input_parameter1 in function_line:
                    input_parameter1_value = function_line.split("=")[1].strip()
                if input_parameter2 in function_line:
                    input_parameter2_value = function_line.split("=")[1].strip()
                if input_parameter3 in function_line:
                    input_parameter3_value = function_line.split("=")[1].strip()
                if input_parameter4 in function_line:
                    input_parameter4_value = function_line.split("=")[1].strip()

            data_set[function3].append([input_parameter1_value, input_parameter2_value, input_parameter3_value, input_parameter4_value])    



if __name__ == '__main__':
    functions = get_functions_parameters('test.py')
    pprint.pprint(data_set)
