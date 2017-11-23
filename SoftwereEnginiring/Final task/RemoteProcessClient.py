import socket
import struct
import json
import logging
from model.World import World

# create logger
logger = logging.getLogger('RemouteClient')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('RemouteClient.log')
fh.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


class RemoteProcessClient:
    BYTE_ORDER_FORMAT_STRING = "<"

    BYTE_FORMAT_STRING = BYTE_ORDER_FORMAT_STRING + "b"
    UNSIGNED_INT_FORMAT_STRING = BYTE_ORDER_FORMAT_STRING + "I"

    SIGNED_BYTE_SIZE_BYTES = 1
    UNSIGNED_INTEGER_SIZE_BYTES = 4

    ACTION = {"LOGIN": 1, "LOGOUT": 2, "MOVE": 3, "TURN": 5, "MAP": 10}

    RESULT = {
        "OKEY": 0,
        "BAD_COMMAND": 1,
        "RESOURCE_NOT_FOUND": 2,
        "PATH_NOT_FOUND": 3,
        "ACCESS_DENIED": 5
    }

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info("Create socket")
        self.socket.connect((host, port))
        logger.info("Connection done")
        self.socket.settimeout(5)
        self.read_buffer = bytes()
        self.read_index = 0

    def login(self, name):
        self.write_message('LOGIN', {"name" : name})
        return self.read_response()

    def logout(self):
        self.write_message('LOGOUT')
        return self.read_response()

    def move(self, line_idx, speed, train_idx):
        self.write_message('MOVE', {"line_idx": line_idx, "speed": speed, "train_idx": train_idx})
        return self.read_response()

    def turn(self):
        self.write_message('TURN')
        return self.read_response()

    def map(self, layer):
        self.write_message('MAP', {"layer": layer })
        return self.read_response()

    def write_message(self, action, data=None):
        if action in RemoteProcessClient.ACTION:
            self.write_uint(RemoteProcessClient.ACTION[action])
            logger.info("Action: %s", action)
        else:
            logger.error("write_message received wrong action=%s", action)
            raise ValueError("Received wrong action=%s" % action)
        self.write_string(json.dumps(data))
        logger.info("Loging message: %s", data)
        return self.read_response()

    def read_response(self):
        result = self.read_uint()
        data = self.read_string()
        logger.info("Result code: %d", result)
        if data:
            logger.info("Data: %s", data)
            return [result, json.loads(data)]
        return [result]

    def close(self):
        self.socket.close()
        logger.info("Close socket")

    def read_string(self):
        length = self.read_uint()
        if length == -1:
            return None

        byte_array = self.read_bytes(length)
        return byte_array.decode()

    def write_string(self, value):
        if value is None:
            return

        byte_array = value.encode()

        self.write_uint(len(byte_array))
        self.write_bytes(byte_array)

    def read_uint(self):
        byte_array = self.read_bytes(
            RemoteProcessClient.UNSIGNED_INTEGER_SIZE_BYTES)
        return struct.unpack(RemoteProcessClient.UNSIGNED_INT_FORMAT_STRING,
                             byte_array)[0]

    def write_uint(self, value):
        self.write_bytes(
            struct.pack(RemoteProcessClient.UNSIGNED_INT_FORMAT_STRING, value))

    def read_bytes(self, byte_count):
        byte_array = b''
        while len(byte_array) < byte_count:
            byte_array += self.socket.recv(byte_count - len(byte_array))

        if len(byte_array) != byte_count:
            raise IOError(
                "Error read %s bytes from input stream." % str(byte_count))

        return byte_array

    def write_bytes(self, byte_array):
        self.socket.sendall(byte_array)

    def read_world(self):
        layer = self.write_message('MAP', {"layer": 1})[1]
        posts = layer['post']
        trains = layer['train']
        return World(posts, trains)
