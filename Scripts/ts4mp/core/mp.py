import os.path

from ts4mp.core import multiplayer_client, multiplayer_server
from ts4mp.debug.log import ts4mp_log
from ts4mp.core.mp_utils import get_current_user_directory

try:
    # TODO: Implement a better way to test if user is a client/server
    is_client = False
    ts4mp_log("user_directory", get_current_user_directory(), force=True)
    if os.path.exists("{}client.txt".format(get_current_user_directory())):
        is_client = True
        ts4mp_log("user_directory", "Set to client.", force=True)

    if is_client:
        client_instance = multiplayer_client.Client()
        client_instance.listen()
        client_instance.send()
    else:
        server_instance = multiplayer_server.Server()
        server_instance.listen()
        server_instance.send()

except Exception as e:
    ts4mp_log("errors", str(e))
