import pickle
from struct import unpack, pack

from ts4mp.debug.log import ts4mp_log


def generic_send_loop(data, socket):
    try:
        data = pickle.dumps(data)
        length = pack('>Q', len(data))
        ts4mp_log("networking state", "Sending length")

        socket.sendall(length)
        ts4mp_log("networking state", "Sending data")

        socket.sendall(data)
    except Exception as e:
        ts4mp_log("critical error", str(e))
def generic_listen_loop(socket, data, size):
    try:
        new_command = None
        if size is None:
            ts4mp_log("networking state", "Receiving length")

            size = socket.recv(8)
            (size,) = unpack('>Q', size)
            ts4mp_log("networking state", "Received length is {}".format(size))

            size = int(size)
        elif size > len(data):
            bytes_to_receive = size - len(data)
            ts4mp_log("networking state", "Receiving data")

            new_data = socket.recv(bytes_to_receive)
            data += new_data
        elif size == len(data):
            data = pickle.loads(data)
            new_command = data
            size = None
            data = b''

        return new_command, data, size
    except Exception as e:
        ts4mp_log("critical error", str(e))