import socket
import struct
import json
import logging

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
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

class RemoteProcessClient:
    BUFFER_SIZE_BYTES = 1 << 20
    BYTE_ORDER_FORMAT_STRING = "<"

    BYTE_FORMAT_STRING = BYTE_ORDER_FORMAT_STRING + "b"
    UNSIGNED_INT_FORMAT_STRING = BYTE_ORDER_FORMAT_STRING + "I"

    SIGNED_BYTE_SIZE_BYTES = 1
    UNSIGNED_INTEGER_SIZE_BYTES = 4

    ACTION = {
        "LOGIN" : 1,
        "LOGOUT" : 2,
        "MOVE" : 3,
        "TURN" : 5,
        "MAP" : 10
        }

    RESULT= {
        "OKEY" : 0,
        "BAD_COMMAND" : 1,
        "RESOURCE_NOT_FOUND" : 2,
        "PATH_NOT_FOUND" : 3,
        "ACCESS_DENIED" : 5
        }


    def __init__(self, host, port):
        self.socket = socket.socket()
        logger.info("Create socket")
        self.socket.connect((host, port))
        logger.info("Connection done")
        self.read_buffer = bytes()
        self.read_index = 0


    def write_message(self, action, data=""):
        if action in RemoteProcessClient.ACTION:
            self.write_uint(RemoteProcessClient.ACTION[action])
            logger.info("Action: %s", action)
        else:
            logger.error("write_message received wrong action=%s", action)
            raise ValueError("Received wrong action=%s" % action)
        self.write_string(json.dumps(data))
        logger.info("Loging message: %s", data)

    def read_response(self):
        result = self.read_enum(RemoteProcessClient.Result)
        data = self.read_string()
        logger.info("Result code: %d", result)
        logger.info("Data: %s", data)

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
        byte_array = self.read_bytes(RemoteProcessClient.UNSIGNED_INTEGER_SIZE_BYTES)
        return struct.unpack(RemoteProcessClient.UNSIGNED_INT_FORMAT_STRING, byte_array)[0]

    def write_uint(self, value):
        self.write_bytes(struct.pack(RemoteProcessClient.UNSIGNED_INT_FORMAT_STRING, value))


    def read_bytes(self, byte_count):
        if len(self.read_buffer) - self.read_index < byte_count:
            self.read_buffer = self.read_buffer[self.read_index:]
            self.read_index = 0

        while len(self.read_buffer) - self.read_index < byte_count:
            chunk = self.socket.recv(max(
                RemoteProcessClient.BUFFER_SIZE_BYTES - len(self.read_buffer),
                byte_count - len(self.read_buffer) + self.read_index
            ))

            if not len(chunk):
                break

            self.read_buffer += chunk

        if len(self.read_buffer) - self.read_index < byte_count:
            raise IOError("Can't read %s bytes from input stream." % str(byte_count))

        byte_array = self.read_buffer[self.read_index:self.read_index + byte_count]
        self.read_index += byte_count
        return byte_array

    def write_bytes(self, byte_array):
        self.socket.sendall(byte_array)
