import socket
import errno
import sys

# Constants
HEADER_LENGTH = 16
FORMAT = "utf-8"
RECEIVE_COLOR = "\033[35m"
NORMAL_COLOR = "\033[32m"
ERROR_COLOR = "\033[31m"

# IP address of this computer
IP = socket.gethostbyname(socket.gethostname())
PORT = 1234
ADDR = (IP, PORT)

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)
client_socket.setblocking(False)

username = my_username.encode(FORMAT)
username_header = f"{len(username):<{HEADER_LENGTH}}".encode(FORMAT)
client_socket.send(username_header + username)


def display(data, color=None):
    """
   Prints colored text to the console
   Parameters:
       data(string): message to be printed
       color(string): color for message to be printed in
   """
    if color is not None:
        print(color + data + NORMAL_COLOR)
    else:
        print(NORMAL_COLOR + data)


# Display blank message to set text color
display("", NORMAL_COLOR)

while True:
    # Message to be sent to server
    message = input(f"{my_username} > ")
    # If a message was entered prepare and send message to server
    if message:
        message = message.encode(FORMAT)
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode(FORMAT)
        client_socket.send(message_header + message)

    # receive all messages loop
    try:
        while True:
            # Receive username header
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                display("Connection closed by the server.", ERROR_COLOR)
                sys.exit()
            username_length = int(username_header.decode(FORMAT))
            # Receive username
            username = client_socket.recv(username_length).decode(FORMAT)

            # Receive message header
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode(FORMAT))
            # Receive message
            message = client_socket.recv(message_length).decode(FORMAT)
            # Prepare and display message
            display_message = f"{username} > {message}"
            display(display_message, RECEIVE_COLOR)
    except IOError as e:
        # If the IOError error was not expected, display the error and stop the client program
        if e.errno != errno.EAGAIN and e.errnor != errno.EWOULDBLOCK:
            display(f"Reading error {str(e)}", ERROR_COLOR)
            sys.exit()
        continue

    except Exception as e:
        # If there is any non-IOError, display it
        display(f"General error {str(e)}", ERROR_COLOR)
        sys.exit()
