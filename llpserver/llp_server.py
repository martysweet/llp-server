import socket
import logging
from _thread import *

from .client_processor import ClientProcessor
from netifaces import interfaces, ifaddresses, AF_INET


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
        logging.info("Starting listening on port 8888")
        self._sock.bind(('0.0.0.0', 8888))
        self._sock.listen(30)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._sock.close()

    def single_conn_listen(self):   # Used for tests
        connection, address = self._sock.accept()
        start_new_thread(threaded_client, (connection, address, self.core_server))

    # TODO: Task - Improve this to show
    # Interfacename: IP IP IP
    # Hide empty interfaces
    def log_ipv4_addresses(self):
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
            logging.info(" ".join(addresses))
        return addresses

    def listen_for_traffic(self):
        logging.info("Listening for connections")
        self.log_ipv4_addresses()
        while True:
            connection, address = self._sock.accept()
            start_new_thread(threaded_client, (connection, address, self.core_server))





