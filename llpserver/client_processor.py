import logging
import re


class ClientProcessor:
    """
     This class is responsible for parsing messages from a client
     passing them to the server process and returning responses.
    """
    def __init__(self, connection, address, core_server):
        self.connection = connection
        self.endpoint = f"{address[0]}:{address[1]}"
        self.logger = logging.getLogger(self.endpoint)
        self.logger.info('Client connected')
        self.username = None
        self.server = core_server
        self.client = None # Assigned when LOGIN called
        self.message_expecting_data = False
        self.message_recipient = ""
        self.message_data = ""
        connection.send(str.encode('Welcome to the Love Letter Server\n'))

        # Activity: What happens if a client disconnects without running LOGOUT?
        # What happens to the socket?
        self.listen = True
        while self.listen:
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

    def send(self, status, data):
        message = f'> {status} - {data}\n'    # We need to add a newline here
        self.connection.sendall(str.encode(message))

    def parse_input(self, data):

        if data.startswith('LOGIN'):
            self.parse_login(str.rstrip(data))  # Remove linebreak
            return

        # Users must login before doing anything else
        if self.username:
            if self.message_expecting_data:
                self.handle_message_data(data)
                return
            if data.startswith('LOGOUT'):
                self.handle_logout()
                return
            elif data.startswith('LIST'):
                self.process_list_clients()
                return
            elif data.startswith('MESSAGE'):
                self.process_send_message(str.rstrip(data))
                return

        # Catch-All Unhandled
        self.send("ERROR", "Unknown Command. Check the documentation or use LOGIN <username> first.")

    def process_send_message(self, data):
        # Find the recipient
        username = data[8:]
        if not re.match("^[a-zA-Z0-9]{3,15}$", username):
            self.logger.error(f"Invalid recipient username given: '{username}'")
            self.send("ERROR", "Invalid recipient username, try again")
            return

        # Activity: Check if the recipient is logged in

        # Flag we are expecting data
        self.message_recipient = username
        self.message_data = ""
        self.message_expecting_data = True

        self.send("OK", "Send Message, end with XOXOXO")

    def handle_message_data(self, data):
        # Activity: Fix the bug here, we don't want XOXOXO in the final message
        self.message_data += data
        self.logger.info(data)
        if data.rstrip().endswith("XOXOXO"):
            self.logger.info("Ready to send...")
            self.message_expecting_data = False
            success, msg = self.server.send_message(self.username, self.message_recipient, self.message_data)
            self.send(success, msg)


    def handle_logout(self):
        self.listen = False
        self.send('OK', "Goodbye xoxo")
        self.connection.close()

    def parse_login(self, data):
        # The command we expect is LOGIN something
        # we can remove the first 6 characters, then check the string for valid characters

        if self.username:
            self.send("ERROR", "You are already logged in")
            return

        username = data[6:]
        if not re.match("^[a-zA-Z0-9]{3,15}$", username):
            self.logger.error(f"Invalid username given: '{username}'")
            self.send("ERROR", "Invalid username, try again")
            return

        # Add the client to the server
        if self.server.is_username_available(username):
            self.username = username
            self.server.add_client(self)    # Add myself to the server
            self.send("OK", f"Hello {username}")
        else:
            self.send("ERROR", "Username is use")

    def process_list_clients(self):
        buf = "Data Available..."
        for c in self.server.list_clients():
            buf += f"\n{c.get_endpoint()} | {c.get_username()}"
        self.send("OK", buf)

    def get_endpoint(self):
        return self.endpoint

    def get_username(self):
        return self.username

    def push_love_message(self, sender, message):
        buf = f"SENDER: {sender}\nRECIPIENT: {self.username}\n{message}"
        buf = buf.replace("\n", "\n> ")
        self.send("INBOUND MESSAGE", buf)
