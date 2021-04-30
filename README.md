# Overview

This program is made to demonstrate how to send and receive text messages in a local network. 

This is a Server/Client program, with each message sent from a client to the server, 
and from the server to the recipient client.

To start the Server, change directories to the directory of server.py, then run server.py with python. 
Start the client program after the server program by changing directories to the directory of client.py, 
then run client.py with python.

[Walk through video](https://youtu.be/iOBKUoi1SDg)

# Network Communication

This program uses the Server/Client architecture and allows multiple clients to join at once.

This program uses TCP with the port number: 1234.

The messages sent between the server and the client are text messages encoded and decoded with UTF-8.

# Development Environment

* PyCharm/Visual Studio Code
* Python 3.8
* Socket
* Select
* Errno
* Sys

# Useful Websites

* [Sentdex Sockets Tutorials](https://www.youtube.com/watch?v=Lbfe3-v7yE0&list=PLQVvvaa0QuDdzLB_0JSTTcl8E8jsJLhR5&index=1)
* [Tech With Tim Socket Tutorial](https://www.youtube.com/watch?v=3QiPPX-KeSc)
* [Pythontic Send function of Socket](https://pythontic.com/modules/socket/send)
* [Stackoverflow Server/Client Socket](https://stackoverflow.com/questions/22737838/raspberry-pi-server-client-socket-in-python)

# Future Work

* Item 1: Add text colors for each user, instead of simply receive color, error color, and normal color.
* Item 2: Make the server publicly accessible, usable from anywhere in the world.
* Item 3: Add a Graphical User Interface (GUI).
* Item 4: Allow clients to see messages while inputting their message. 