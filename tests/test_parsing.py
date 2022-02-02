import threading
import socket

import pytest

from llpserver.llp_server import LLPServer


@pytest.fixture(autouse=True)
def llp_server():
    server = LLPServer()
    with server as tcp_server:
        thread = threading.Thread(target=tcp_server.listen_for_traffic)
        thread.daemon = True
        thread.start()
        yield tcp_server
        thread.join()

def connect_send_message(message):
    HOST = '127.0.0.1'
    PORT = 8888

    data = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024) # Always the welcome message
        assert data.decode() == "Welcome to the Love Letter Server\n"
        s.sendall(message.encode())
        return s.recv(1024).decode().rstrip()



@pytest.mark.parametrize(
    "test_input",
    [
        "hello",
        "goodbye",
        "goodbye\n"
        "myn"
        "234567891234677"
    ]
)
def test_login_failures(test_input):
    assert connect_send_message(f"LOGIN {test_input}") == f"> OK - Hello {test_input}"

@pytest.mark.parametrize(
    "test_input",
    [
        "hello!!",
        "goodbye_",
        "my"
        "12345678912344556677"
    ]
)
def test_login_successes(test_input):
    assert connect_send_message(f"LOGIN {test_input}") == f"> ERROR - Invalid username, try again"
