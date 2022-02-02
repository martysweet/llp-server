import socket

import pytest


def connect_send_message(message):
    HOST = '127.0.0.1'
    PORT = 8888

    data = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)  # Always the welcome message
        assert data.decode() == "Welcome to the Love Letter Server\n"
        s.sendall(f"{message}\n".encode())
        d = s.recv(1024).decode().rstrip()
        s.close()
        return d

@pytest.mark.parametrize(
    "test_input",
    [
        "hello",
        "goodbye",
        "goodbye",
        "myn",
        "234567891234677",
    ]
)
def test_login_failures(test_input):
    assert connect_send_message(f"LOGIN {test_input}") == f"> OK - Hello {test_input}"


@pytest.mark.parametrize(
    "test_input",
    [
        "hello!!",
        "goodbye_",
        "my",
        "12345678912344556677",
    ]
)
def test_login_successes(test_input):
    assert connect_send_message(f"LOGIN {test_input}") == f"> ERROR - Invalid username, try again"


# def test_login_and_list():
#     s = connect()
#     s.send("LIST")
#     asserts.recv()