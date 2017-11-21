import socket
import struct
import json
import logging

logger = logging.getLogger("Socket")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class Client():
    def __init__(self, address='wgforge-srv.wargaming.net', port=443):
        # wgforge-srv.wargaming.net: 443
        self.socket = socket.socket()
        self.socket.connect((address, port))
        self.conn = self.socket
        self._timeout = None
        self._address = address
        self._port = port

    def send_data(self, code, data):
        msg = json.dumps(data)
        msg = bytes(msg, 'utf-8')
        if self.socket:
            frmt = "%ds" % len(msg)
            packedMsg = struct.pack('<LL'+frmt, code, len(msg), msg)

            self.conn.sendall(packedMsg)


    def _read(self, size):
        data = b''
        while len(data) < size:
            dataTmp = self.conn.recv(size - len(data))
            data += dataTmp
            if dataTmp == '':
                raise RuntimeError("socket connection broken")
        return data

    def read_data(self):
        hdr = self._read(8)
        res_code, size = struct.unpack('<LL', hdr)
        data = self._read(size)
        frmt = "=%ds" % size
        msg = struct.unpack(frmt, data)
        return [res_code, size, json.loads(msg[0])]

    def close(self):
        logger.debug("closing main socket")
        self._closeSocket()
        if self.socket is not self.conn:
            logger.debug("closing connection socket")
            self._closeConnection()

    def _closeSocket(self):
        self.socket.close()

    def _closeConnection(self):
        self.conn.close()

    def _get_timeout(self):
        return self._timeout

    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.socket.settimeout(timeout)

    def _get_address(self):
        return self._address

    def _set_address(self, address):
        pass

    def _get_port(self):
        return self._port

    def _set_port(self, port):
        pass

    timeout = property(
        _get_timeout, _set_timeout, doc='Get/set the socket timeout')
    address = property(
        _get_address, _set_address, doc='read only property socket address')
    port = property(_get_port, _set_port, doc='read only property socket port')



if __name__ == '__main__':

    client = Client()

    msg = [1, {"name": "Mickey"}]

    client.send_data(*msg)
    print(client.read_data())

    client.close()