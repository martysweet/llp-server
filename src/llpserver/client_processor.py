import logging
import re

class ClientProcessor:
    # This class is responsible for parsing messages from a client
    # passing them to the server process and returning responses.

    def __init__(self, connection, address):
        self.connection = connection
        self.logger = logging.getLogger(address[0] + ':' + str(address[1]))
        self.logger.info('Client connected')
        connection.send(str.encode('Welcome to the Love Letter Server\n'))

        # TODO: Activity: What happens if a client disconnects without running LOGOUT?
        # TODO: What happens to the socket?
        # Here we need to read until a linebreak
        #
        target_char = "\n"
        fragments = []

        self.listen = True
        while self.listen:
            print("Listen")
            try:
                a = self.recv_basic()
                self.parse_input(a)
            except Exception as e:
                self.logger.error(e)

    def recv_basic(self):
        total_data = []
        while True:
            data = self.connection.recv(1).decode()
            if not data:
                break
            total_data.append(data)
            if total_data[-1] == "\n":
                break
        return ''.join(total_data)


    def send(self, status, data):   # TODO Typing
        message = f'> {status} - {data}\n'    # We need to add a newline here
        self.connection.sendall(str.encode(message))

    def parse_input(self, data):
        if data.startswith('LOGIN'):
            self.parse_login(str.rstrip(data))  # Remove linebreak
        elif data.startswith('LOGOUT'):
            self.handle_logout()

    def handle_logout(self):
        self.listen = False
        self.send('OK', "Goodbye xoxo")
        self.connection.close()

    def parse_login(self, data):
        # The command we expect is LOGIN something
        # we can remove the first 6 characters, then check the string for valid characters

        username = data[6:]
        if not re.match("^[a-zA-Z0-9]{3,15}$", username):
            self.logger.error(f"Invalid username given: '{username}'")
            self.send("ERROR", "Invalid username, try again")
            return

        # Assign with server
        self.send("OK", f"Hello {username}")