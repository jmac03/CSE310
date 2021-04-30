import socket
import select

# Constants
HEADER_SIZE = 16
FORMAT = "utf-8"
RECEIVE_COLOR = "\033[35m"
NORMAL_COLOR = "\033[32m"
ERROR_COLOR = "\033[31m"

# IP address of this computer
IP = socket.gethostbyname(socket.gethostname())
PORT = 1234
ADDR = (IP, PORT)

# Create the socket for clients to connect to
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Allow PORT to be reused
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Make a point for clients to be able to connect with server_socket
server_socket.bind(ADDR)

# List of connected sockets, including server
sockets_list = [server_socket]

# dictionary of connected client sockets
clients = {}


def display(data, color=None):
    """
    Prints colored text to the console
    Parameters:
        data(string): message to be printed
        color(string): color for message to be printed in
    """
    if color is not None:
        print(color + data)
    else:
        print(NORMAL_COLOR + data)


def receive_message(active_client_socket):
    """
    Receives message and returns it in two parts: header and data
    Parameters:
        active_client_socket(socket.socket): specific socket to receive message from
    Return: (dict) {"header": message_header, "data": data}
    """
    try:
        message_header = active_client_socket.recv(HEADER_SIZE)
        if not len(message_header):
            return False
        message_length = int(message_header.decode(FORMAT))
        data = active_client_socket.recv(message_length).decode(FORMAT)
        return {"header": message_header, "data": data}
    except Exception as e:
        display(str(e), ERROR_COLOR)
        return False


def start():
    """
    Starts the server
    """
    # Get ready to accept clients
    server_socket.listen()
    display(f"Listening on {IP}")

    while True:
        read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list)

        for specific_socket in read_sockets:
            # allow connections when checking the server
            if specific_socket == server_socket:
                client_socket, client_address = server_socket.accept()

                user = receive_message(client_socket)
                if user is False:
                    continue

                display(f"Accepted a connection from {user['data']}.")
                sockets_list.append(client_socket)

                # clients dict holds username
                clients[client_socket] = user

            else:
                message = receive_message(specific_socket)

                if not message:
                    display(f"Disconnected from {client_address}")
                    sockets_list.remove(specific_socket)
                    del clients[specific_socket]
                    continue
                # access the values for this user
                user = clients[specific_socket]

                display(f"{user['data']}: {message['data']}", RECEIVE_COLOR)

                username_list = []
                first_word_in_message = message["data"].split()[0]
                # display(first_word_in_message)

                # Creates a list of users to send message to
                for client_socket in clients:
                    # If username is in the first word in the message, add that username to the username_list
                    if clients[client_socket]["data"] in first_word_in_message:
                        username_list.append(clients[client_socket]["data"])

                # If no usernames were found in the first word of the message, add all users to the username_list
                if len(username_list) == 0:
                    for client_socket in clients:
                        username_list.append(clients[client_socket]["data"])

                for client_socket in clients:
                    # Send full message to all users found in username_list, except for the user that sent the message
                    if clients[client_socket]["data"] in username_list and clients[client_socket] != user:
                        client_socket.send(
                            user["header"] + user["data"].encode(FORMAT) + message["header"] + message["data"].encode(
                                FORMAT))

        for specific_socket in exception_sockets:
            sockets_list.remove(specific_socket)
            del clients[specific_socket]


start()
