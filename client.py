import socket
import threading
import argparse
import os

#Create a class to connect to the servers IP and port address
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    """In start method, the program will create the two-way communication between the client and the
    server. In here we also create and start the send and recieve threads"""
    def start(self):
        print("\nConnecting to {}:{}...\n".format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print("Connected successfully! ")

        print()
        name = input("What is your name? ")
        print()
        print("Welcome to the chat {}! ".format(name))

        #Create send and receive threads
        send = Send(self.sock, name)
        receive = Receive(self.sock, name)
        
        #Start threads
        send.start()
        receive.start()

        #Let other users know that someone has joined the chat
        self.sock.sendall("{} has joined the chat! ".format(name).encode("ascii"))
        print("\rType 'quit' at anytime to leave the chatroom")
        print("{}: ".format(name), end = "")

#Create a class to send messages
class Send(threading.Thread):
    """Create two class attributes for the socket object and the users inputted username"""
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    """In run method the program will listen for input from the user and send to the server.  The user can
    quit the program at any time by typing 'quit' in all lowercase."""
    def run(self):
        while True:
            msg = input("{}: ".format(self.name))

            if msg == "quit":
                self.sock.sendall("{} has left the chat.".format(self.name).encode("ascii"))
                break
            else:
                self.sock.sendall("{}: {}".format(self.name, msg).encode("ascii"))
            
        print("\nQuitting...")
        self.sock.close()
        os._exit(0)

#Create class to recieve any messages from the server
class Receive(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
    
    """In run method, the program will recieve any messages sent by the server and display them to all users.
    It will print the users username so that they can be identified"""
    def run(self):
        while True:
            msg = self.sock.recv(1024)
            if msg:
                print("\r{}\n{}: ".format(msg.decode("ascii"), self.name), end = "")
            else:
                #Client exits program, close
                print("\nLost connection to the server")
                print("\nQuitting...")
                self.sock.close()
                os._exit(0) 

#Get the host IP address from terminal and pass to Client class
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

client = Client(args.host, args.p)
client.start()