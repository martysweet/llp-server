# Love Letter Protocol Client Server

The Lover Letter Protocol Client Server is designed to be an education example of the client-server model taught for
A-Level computer science.

The project implements a fictional "Love Letter" Application Layer protocol, which operates over the Transmission Control Protocol (TCP).

The user can use an ASCII client (such as telnet or [PuTTY Telnet](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)) and communicate with the server, using the defined protocol.

Students are encouraged to run the code locally and experiment with how it works, there are snippets throughout the codebase where improvements could be made. Submit a Pull Request for new additions.

## Getting Started
To get started, run `main.py` within python 3.8 or greater, the server should start.
```bash
$ python3.8 main.py 
root - INFO - Starting listening on port 8888
root - INFO - Listening for connections
root - INFO - 172.19.0.1
```

Then connect with your telnet client to the IP listed and port 8888.
```bash
$ telnet 127.0.0.1 8888
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
> OK - Welcome to the Love Letter Server
Supported commands are: LOGIN, LOGOUT, LIST, MESSAGE


LOGIN olivia
> OK - Hello olivia
```

Refer to this document for commands you can use. You can also launch multiple clients from the same machine.
Use the LIST command to see connected users and ports in use!

## Love Letter Protocol
### Introduction
The objectives of LLP are 1) promote love while learning about networking and protocols, 2) send messages between clients, 3) highlight
the concepts of the client-server model. LLP, though usable using an ASCII terminal, can be implemented into a graphical
interface or used by other programs.

The LLP protocol is designed to be easily used by a simple ASCII TCP client, such as telnet or [PuTTY Telnet](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)).

The TCP/IP Layer when using LLP is as follows:

- Application Layer - Love Letter Protocol (LLP) - _defined by this document_
- Transport Layer - Transmission Control protocol (TCP)
- Network Layer - Internet Protocol V4 (IPV4)

### Response Codes
Upon processing a message, the server will return one of the following status codes followed by a descriptive message.
- ERROR
- OK

For example: 
```
> OK - Hello user
```

### Server Model
- **llp_server.py** - Run's a socket server which listens for connections. Spawns a ClientProcessor in a new Thread upon a new connection.
- **client_processor.py** - Handles the income LLP messages from the clients text based terminal, parsing the message and making calls to the CoreServer.
- **core_server.py** - Maintains the central state of the server, allows clients to message each other by maintaining a map of clients.


### Client Commands
The following table shows a list of commands which can be used. Further details for each command are documented below.

| Command | Description |
|---------|-------------|
|```LOGIN <username>``` | Used to attach a username to the opened TCP/IP session.|
|```LIST``` | Used to list all clients which are connected to the server. |
|```MESSAGE <username>``` | Sends a message to another user on the server. |
|```XOXOXO``` | Indicates the end of a message. |


#### LOGIN
Used to attach a username to the opened TCP/IP session. 
Usernames must be between 3-15 characters. 
Valid characters: a-z A-Z 0-9

```
LOGIN bob
> OK - Hello bob
```

```
LOGIN %^&
> ERROR - Invalid username, try again
```


#### LIST
Outputs all the clients logged into the server.
```
LIST
> OK - Data Available...
192.168.69.165:58628 | bob
127.0.0.1:55430 | olivia
```

Use this command to discover usernames to send messages to.

#### MESSAGE
Used to send a message to a user
```
MESSAGE bob
> OK - Send Message, end with XOXOXO
hello, happy valentines
XOXOXO
```

It will be displayed in the recipients console like
```
> OK - Hello mms
> INBOUND MESSAGE - SENDER: olivia
> RECIPIENT: bob
> hello, happy valentines
> XOXOXO
```

## Learning?
New to opensource? Try opening a Pull-Request and improve the codebase? There is lots that can be done!
- Better/full test coverage
- Unified error messages/handling
- BLOCK functionality
- BROADCAST functionality to send a message to everyone on the server