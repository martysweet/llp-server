import pytest
import threading
from llpserver.llp_server import LLPServer



@pytest.fixture(autouse=True)
def llp_server():
    server = LLPServer()
    with server as tcp_server:
        thread = threading.Thread(target=tcp_server.single_conn_listen)
        thread.daemon = True
        thread.start()
        yield tcp_server
        thread.join()