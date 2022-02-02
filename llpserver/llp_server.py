import select
import socket
import logging
from _thread import *

from .client_processor import ClientProcessor


# Handle the incoming connection
from .core_server import CoreServer


def threaded_client(connection, address, core_server):
    ClientProcessor(connection, address, core_server) # x will block until it's closed
    logging.info("Client closed")


class LLPServer:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET,
                                   socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET,
                              socket.SO_REUSEADDR, 1)
        self.core_server = CoreServer()

    def __enter__(self):
        self._sock.bind(('0.0.0.0', 8888))
        self._sock.listen(5)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._sock.close()

    def single_conn_listen(self):   # Used for tests
        connection, address = self._sock.accept()
        start_new_thread(threaded_client, (connection, address, self.core_server))

    def listen_for_traffic(self):
        logging.info("Listening for connections")
        while True:
            connection, address = self._sock.accept()
            start_new_thread(threaded_client, (connection, address, self.core_server))





