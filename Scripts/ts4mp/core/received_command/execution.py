import time
import omega
import services

from ts4mp.core.received_command.message_types import ProtocolBufferMessage, HeartbeatMessage
from ts4mp.debug.log import ts4mp_log, Timer

from ts4mp.core.received_command.execute_command_mapping import PERFORM_COMMAND_FUNCTIONS
from ts4mp.core.received_command.preprocessing import  parse_all_args_except_for_function_name, replace_client_id_for_ui_commands, format_command_to_execute, create_and_append_pendable_command
from ts4mp.core.received_command.queue import commandQueue
client_online = False
time_since_last_update = time.time()


def attempt_command(function_name, parsed_args):
    try:
        _do_command(function_name, *parsed_args)
    except Exception as e:
        ts4mp_log("Execution Errors", str(e))


def _do_command(command_name, *args):
    if command_name in PERFORM_COMMAND_FUNCTIONS:
        PERFORM_COMMAND_FUNCTIONS[command_name](*args)

        ts4mp_log("commands", "There is a command named: {}. Executing it.".format(command_name))
    else:
        ts4mp_log("commands", "There is no such command named: {}!".format(command_name))


def client_sync():
    global time_since_last_update

    should_update = time.time() - time_since_last_update > 0.01
    if should_update:
        time_since_last_update = time.time()
    else:
        return


    client_manager = services.client_manager()
    client = None

    if client_manager is not None:
        client = client_manager.get_first_client()

        if client is None:
            return
    else:
        return
    while True:
        pop_element = commandQueue.pop_incoming_command()
        if not pop_element:
            # no more entries left in the queue.
            return False


        if isinstance(pop_element, ProtocolBufferMessage):
            omega.send(client.id, pop_element.msg_id, pop_element.msg)
        elif isinstance(pop_element, HeartbeatMessage):
            # we don't do anything with Heartbeats.
            ts4mp_log("latency", time.time() - pop_element.sent_time, force = True)
            pass


def server_sync():

    while True:
        with Timer("Server Sync"):
            pop_element = commandQueue.pop_incoming_command()
            if not pop_element:
                # no more entries left in the queue.
                return False

            # this is a server message coming from the client. Don't parse it.
            if isinstance(pop_element, ProtocolBufferMessage):
                continue
            current_line = pop_element.split(',')
            function_name = current_line[0]

            if not function_name:
                continue

            parsed_args = list()
            parse_all_args_except_for_function_name(current_line, function_name, parsed_args)

            stripped_function_name = function_name.strip()
            ts4mp_log("arg_handler", stripped_function_name)

            client_id = replace_client_id_for_ui_commands(stripped_function_name)
            parsed_args[-1] = client_id


            ts4mp_log("client_specific", "New function called {} recieved".format(stripped_function_name))

            create_and_append_pendable_command(client_id, stripped_function_name)

            attempt_command(stripped_function_name, parsed_args)






