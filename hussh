#!/usr/bin/env python3

import logging
import socket
import sys
import threading

import paramiko
import base64

from queue import Queue
from server  import Server
from command import Command


logging.basicConfig()
paramiko.util.log_to_file('logs/hussh.log', level='INFO')
logger = paramiko.util.get_logger("paramiko")

# ssh-keygen -f keys/host.rsa
host_key = paramiko.RSAKey(filename='keys/host.rsa')

session_queue = Queue()

def start_server(client):
    t = paramiko.Transport(client)
    t.set_gss_host(socket.getfqdn(""))
    t.load_server_moduli()
    t.add_server_key(host_key)
    server = Server()
    t.start_server(server=server)
    server.event.wait()     # wait for termination:
    t.close()

def accept_and_queue(sock):
    while True:
        try:
            client, _ = sock.accept()
        except Exception as e:
            logger.error(e)
        else:
            session_queue.put(client)

def wait_for_session():
    try:
        client = session_queue.get()
        threading.Thread(target=start_server, args=(client,), daemon=True).start()
    except KeyboardInterrupt:
        sys.exit(0)

def listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 5555))
    sock.listen(100)

    threading.Thread(target=accept_and_queue, args=(sock,), daemon=True).start()

    while True:
        wait_for_session()

if __name__ == '__main__':
    listener()
