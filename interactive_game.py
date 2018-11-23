import argparse
import time
import logging
import socket
import select
import sys
from threading import *
import multiprocessing

import random
import time


class Client:

    def __init__(self, connection, address):
        self.address = address
        self.connection = connection
        self.send("\n\n\t\tWelcome\nThis is an interactive programming challenge\n\nTo get started, "
                             "please enter a username\n>>> ")
        self.name = self.receive()
        self.send(f"\nGreat! Your username has been set as {self.name}\n".encode())

    def client_thread(self):
        pass


    def send(self, *args):
        time.sleep(.2)
        mess = ""
        for i in args:
            mess += i
        try:
            self.connection.send(mess.encode())
            print("Sent <" + addr[0] + "> " + mess)
        except OSError:
            # cleanClose(conn, addr, "called from send")
            pass

    def receive(self):
        try:
            mess = self.connection.recv(1024)
            print("<" + addr[0] + "> " + mess.decode())
            return mess.decode()
        except ConnectionResetError:
            return False
        except OSError:
            return False


def get_args():
    debug = logging.WARNING

    logging.basicConfig(level=debug, format='%(asctime)s %levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Logging level: %d", debug)

    parser = argparse.ArgumentParser(description="Interactive Programming Game")

    parser.add_argument('-p', '--port', help='Port number to run the server on', type=int)
    parser.add_argument('-a', '--address', help='Address to run server on', default='127.0.0.1')
    parser.add_argument('-d', '--debug', action='count', help='Increase debug level for each -d')

    args = parser.parse_args()

    if args.debug:
        # Turn up the logging level
        debug -= args.debug * 10
        if debug < 0:
            debug = 0
        logging.getLogger().setLevel(debug)
        logging.warning('Updated log level to: %s(%d)', logging.getLevelName(debug), debug)

    return args





if __name__ == "__main__":
    args = get_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((args.address, args.port))
    server.listen(100)

    list_of_clients = []
    while True:
        conn, addr = server.accept()
        # list_of_clients.append(conn)

        new_client = Client(conn, addr)
        list_of_clients.append(new_client)

        Thread(target=new_client.client_thread).start()

