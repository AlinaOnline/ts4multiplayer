import socket
import threading

import ts4mp
import ts4mp.core.client_utils
from ts4mp.debug.log import ts4mp_log, Timer
from ts4mp.core.networking import generic_send_loop, generic_listen_loop
from ts4mp.core.notifications import show_client_connect_on_client, show_client_connection_failure
from ts4mp.core.received_command.queue import commandQueue
class Client:
    def __init__(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.serversocket.settimeout(15)
        self.host = 0
        self.port = 0
        self.alive = True
        self.connected = False
        self.ever_recieved_data = False
    def listen(self):
        # Spawn networking stuff in a separate thread.
        threading.Thread(target=self.listen_loop, args=[]).start()

    def send(self):
        # Spawn networking stuff in a separate thread.

        threading.Thread(target=self.send_loop, args=[]).start()

    def send_loop(self):
        try:

            ts4mp_log("sockets", "Attempting to connect to server.")
            self.serversocket.connect((self.host, self.port))
            self.connected = True
            ts4mp_log("sockets", "Connected to Server")

            while self.alive:
                while True:
                    pop_element = commandQueue.pop_outgoing_command()
                    if not pop_element:
                        # no more entries left in the queue.
                        break
                    ts4mp_log("Messages", "Managed to pop an element from the command Queue.")
                    generic_send_loop(pop_element, self.serversocket)
                    ts4mp_log("Messages", "Sent a message.")

            ts4mp_log("sockets", "Client was disconnected.")

        except Exception as e:
            show_client_connection_failure()
            ts4mp_log("sockets", str(e))

            self.connected = False

    def listen_loop(self):
        serversocket = self.serversocket
        size = None
        data = b''
        while self.alive:
            if self.connected:
                try:
                    new_command, data, size = generic_listen_loop(serversocket, data, size)
                    if new_command is not None:
                        # if we've never received data, then this is the first time we've gotten data.
                        # obviously.
                        if not self.ever_recieved_data:
                            show_client_connect_on_client()

                            ts4mp.core.client_utils.on_successful_client_connect()
                            self.ever_recieved_data = True
                        commandQueue.queue_incoming_command(new_command)
                except socket.error as e:
                    ts4mp_log("sockets", "Catastrophic failure: {}".format(e), force=True)

                    show_client_connection_failure()
                    self.connected = False


            # time.sleep(1)

    def kill(self):
        self.alive = False
