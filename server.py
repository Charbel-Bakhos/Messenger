import socket
import threading
import argparse
import os

"""Server class will inherit from the threading method to create a thread"""
class Server(threading.Thread):

    """On initialisation, get the host IP and port and create a list to store connections."""
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.connection = []

    """Create the listening socket and bind to the host IP and port. Will use IPv4 netowrk and 
    TCP stream. Create an option to reuse the port if a connection is closed. Listen for a max
    of 5 as per recommendation in documentation"""
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(5)

        """Create infinite loop to listen for and accept new connections. Return the address
        of the connected client and the address to which the socket is bound. Create a 
        new thread and add to existing connections. Store all active connections in connection list"""
        while True:
            client_sock, sockname = sock.accept()
            print("Accepted a new connection from {} to {}".format(client_sock.getpeername(), client_sock.getsockname()))
            server_socket = ServerSock(client_sock, sockname, self)
            server_socket.start()
            self.connection.append(server_socket)
            print("Ready to receive messages from", client_sock.getpeername())
    
    """Create functionality to send messages to all clients that are connected to the server"""
    def send_message(self, msg, source):
        for connections in self.connection:
            if connections.sockname != source:
                connections.send(msg)


class ServerSock(threading.Thread):

    def __init__(self, client_sock, sockname, server):
        super().__init__()
        self.client_sock = client_sock
        self.sockname = sockname
        self.server = server
    
    def run(self):
        while True:
            msg = self.client_sock.recv(1024).decode("ascii")
            if msg:
                print("{} says {!r}".format(self.sockname, msg))
                self.server.send_message(msg, self.sockname)
            else:
                #Exit thread when client has closed connection
                print("{} has closed their connection". format(self.sockname))
                self.client_sock.close()
                server.remove_connection(self)
                return
    
    def send(self, msg):
        self.client_sock.sendall(msg.encode("ascii"))
    

def exit(server):
    while True:
        ipt = input("")
        if ipt == "quit chat":
            print("Closing all connections...")
            for connections in server.connection:
                connections.client_sock.close()
            print("Shutting down the server...")
            os._exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    # Create and start server thread
    server = Server(args.host, args.p)
    server.start()

    exit = threading.Thread(target = exit, args = (server,))
    exit.start()

