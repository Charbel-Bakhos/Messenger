import socket
import threading
import argparse
import os

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start(self):
        print("\nConnecting to {}:{}...".format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print("Connected successfully! ")

        print()
        name = input("What is your name? ")
        print()
        print("Welcome {}! ".format(name))

        #Create send and receive threads
        send = Send(self.sock, name)
        receive = Receive(self.sock, name)
        
        #Start threads
        send.start()
        receive.start()

        self.sock.sendall("{} has joined the chat! ".format(name).encode("ascii"))
        print("\rType 'quit' at anytime to leave the chatroom")
        print("{}: ".format(name), end = " ")


class Send(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

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

class Receive(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
    
    def run(self):
        while True:
            msg = self.sock.recv(1024)
            if msg:
                print("\r{}\n{} ".format(msg.decode("ascii"), self.name), end = " ")
            else:
                #Client exits program, close
                print("\nLost connection to the server")
                print("\nQuitting...")
                self.sock.close()
                os._exit(0) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

client = Client(args.host, args.p)
client.start()