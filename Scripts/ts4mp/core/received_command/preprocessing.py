import re
from server_commands.argument_helpers import RequiredTargetParam
from ts4mp.core.pending_client_commands import pending_commands_lock, pendable_functions, pending_commands
from ts4mp.debug.log import ts4mp_log
import services
from ts4mp.debug.log import Timer
ALPHABETIC_REGEX = re.compile('[a-zA-Z]')


def format_command_to_execute(function_name, parsed_args):
    function_to_execute = "{}({})".format(function_name, str(parsed_args).replace('[', '').replace(']', ''))
    return function_to_execute

def parse_all_args_except_for_function_name(current_line, function_name, parsed_args):
    for arg_index in range(1, len(current_line)):
        arg = remove_unneeded_symbols_from_command(arg_index, current_line)

        parsed_arg = _parse_arg(arg)
        parsed_arg = replace_RequiredTargetParam_argument_in_command(arg_index, function_name, parsed_arg)
        parsed_args.append(parsed_arg)

def replace_RequiredTargetParam_argument_in_command(arg_index, function_name, parsed_arg):
    if arg_index == 1 and function_name.strip() == "find_career":
        parsed_arg = RequiredTargetParam(str(parsed_arg))
    return parsed_arg

def remove_unneeded_symbols_from_command(arg_index, current_line):
    arg = current_line[arg_index].replace(')', '').replace('{}', '').replace('(', '').replace("[", "").replace("]",
                                                                                                               "")
    ts4mp_log("arg_handler", str(arg) + "\n", force=False)
    if "'" not in arg and "True" not in arg and "False" not in arg:
        with Timer("regex"):
          arg = ALPHABETIC_REGEX.sub('', arg)
        arg = arg.replace('<._ = ', '').replace('>', '')
    return arg

def create_and_append_pendable_command(client_id, function_name):
    if function_name in pendable_functions:
        with pending_commands_lock:
            if function_name not in pending_commands:
                pending_commands[function_name] = []
            if client_id not in pending_commands[function_name]:
                pending_commands[function_name].append(client_id)


def replace_client_id_for_ui_commands(stripped_function_name):
    if stripped_function_name == "ui_dialog_pick_result" or stripped_function_name == "ui_dialog_respond":
        client_id = services.get_first_client().id
    else:
        client_id = 1000
    return client_id


def _parse_arg(arg):
    #Horrible, hacky way of parsing arguments from the client commands.
    #DO NOT EVER CHANGE THESE LINES OF CODE.
    #IT WILL SCREW UP OBJECT IDS AND VERY LONG NUMBERS, EVEN THOUGH IT SEEMS THAT THIS CODE IS COMPLETELY
    #USELESS. THE ASSIGNING OF THE VARIABLE TO ANOTHER VARIABLE CAUSES IT TO BREAK IF REMOVED
    new_arg = arg
    bool_arg = None
    if "True" in new_arg:
        bool_arg = True
    elif "False" in new_arg:
        bool_arg = False
    if bool_arg is not None:
        return bool_arg


    orig_arg = new_arg.replace('"', "").replace("(", "").replace(")", "").replace("'", "").strip()
    new_arg = orig_arg
    ts4mp_log("arg_handler", "First pass: " + str(new_arg) + "\n", force=False)



    try:
        new_arg = float(orig_arg)

        try:
            new_arg = int(orig_arg)
        except BaseException:
            pass
    except BaseException:
        pass
    ts4mp_log("arg_handler", "Second pass: " +  str(new_arg) + "\n", force=False)

    return new_arg