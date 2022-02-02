# Love Letter Protocol Client Server

The Lover Letter Protocol Client Server is designed to be an education example of the client-server model taught for
A-Level computer science.

The project implements a fictional "Love Letter" Application Layer protocol, which operates over the Transmission Control Protocol (TCP).

The user must use the client application and communicate with the server, using the defined protocol.


## Love Letter Protocol
### Introduction
The objectives of LLP are 1) promote love while learning about networking, 2) send messages between clients, 3) highlight
the concepts of the client-server model. LLP, though usable using an ASCII terminal, can be implemented into a graphical
interface or used by other programs.

The LLP protocol is designed to be easily used by a simple ASCII TCP client, such as Telnet.

The TCP/IP Layer when using LLP is as follows:

- Application Layer - Love Letter Protocol (LLP)
- Transport Layer - Transmission Control protocol (TCP)
- Network Layer - Internet Protocol V4 (IPV4)

### Response Codes
Upon processing a message, the server will return one of the following status codes followed by a descriptive message.
- ERROR
- OK

### LLP Model

TODO Diagram of components

### Client Commands
The following table shows a list of commands which can be used. Further details for each command are documented below.

| Command | Description |
|---------|-------------|
|```LOGIN <username>``` | Used to attach a username to the opened TCP/IP session.|
|```LIST``` | Used to list all clients which are connected to the server. |
|```MESSAGE <username>``` | Sends a message to another user on the server. |
|```BLOCK <username>``` | Blocks a username from sending love messages to the calling client. |
|```XOXOXO``` | Indicates the end of a message. |


#### LOGIN
Used to attach a username to the opened TCP/IP session. 
Usernames must be between 3-15 characters. 
Valid characters: a-z A-Z 0-9

```
LOGIN bob
> OK bob, xoxo
```

```
LOGIN %^&
> ERROR Username invalid
```


#### BLOCK <username>
The sender will receive the following error message:
```
> ERROR Message not sent. Your love was not desired.
```
