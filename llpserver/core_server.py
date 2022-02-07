import logging


class CoreServer:
    """
    Responsible for core logic. No data formatting should occur here.
    Activity: It might be nice to move error messages out into constants
    Activity: Is there any need for multithreaded consideration here?
    """
    def __init__(self):
        self.logger = logging.getLogger("LLP Server Started")
        self.clients = {}

    def list_clients(self):
        return [c for k, c in self.clients.items()]

    def is_username_available(self, username):
        return self.clients.get(username) is None

    def add_client(self, client):
        self.clients[client.get_username()] = client

    def send_message(self, sender_username, recipient_username, message):
        # Find the target username
        target = self.clients.get(recipient_username)
        if target is None:
            return "ERROR", "Recipient does not exist"

        # Activity: Implement blocking

        target.push_love_message(sender_username, message)
        return "OK", "Message Delivered"

