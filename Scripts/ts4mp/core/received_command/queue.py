from threading import Lock
from collections import deque

class CommandQueue:
    def __init__(self):
        self._incoming_lock = Lock()
        self._outgoing_lock = Lock()
        self._incoming_commands = deque()
        self._outgoing_commands = deque()

    def queue_incoming_command(self, command):
        with self._incoming_lock:
            self._incoming_commands.append(command)

    def queue_outgoing_command(self, command):
        with self._outgoing_lock:
            self._outgoing_commands.append(command)

    def pop_incoming_command(self):
        with self._incoming_lock:
            try:
                return self._incoming_commands.popleft()
            except IndexError:
                return False

    def pop_outgoing_command(self):
        with self._outgoing_lock:
            try:
                return self._outgoing_commands.popleft()
            except IndexError:
                return False

    def outgoing_queue_len(self):
        with self._outgoing_lock:
            return len(self._outgoing_commands)

commandQueue = CommandQueue()
