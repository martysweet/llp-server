import select
import socket
import logging
from _thread import *

from client_processor import ClientProcessor


# Handle the incoming connection
def threaded_client(connection, address):
    ClientProcessor(connection, address) # x will block until it's closed
    logging.info("Client closed")


class LLPServer:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET,
                                   socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET,
                              socket.SO_REUSEADDR, 1)

    def __enter__(self):
        self._sock.bind(('0.0.0.0', 8888))
        self._sock.listen(5)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._sock.close()

    def listen_for_traffic(self):
        logging.info("Listening for connections")
        while True:
            connection, address = self._sock.accept()
            start_new_thread(threaded_client, (connection, address))





