import os
import sys
import logging
import socket
import threading
import paramiko
import base64

from queue       import Queue
from lib.server  import Server
from lib.command import Command

class HUSSH:

    def __init__(self, home):
        self.home = home
        path = os.path.join(self.home, 'keys', 'host.rsa')
        self.host_key = paramiko.RSAKey(filename=path)
        self.session_queue = Queue()
        self.logger = paramiko.util.get_logger("paramiko")

    def start_session(self, client):
        t = paramiko.Transport(client)
        t.set_gss_host(socket.getfqdn(""))
        t.load_server_moduli()
        t.add_server_key(self.host_key)
        server = Server(self.home)
        t.start_server(server=server)
        server.event.wait()     # wait for termination:
        t.close()

    def accept_and_queue(self, sock):
        while True:
            try:
                client, _ = sock.accept()
            except Exception as e:
                self.logger.error(e)
            else:
                self.session_queue.put(client)

    def wait_for_session(self):
        try:
            client = self.session_queue.get()
            threading.Thread(target=self.start_session, args=(client,), daemon=True).start()
        except KeyboardInterrupt:
            sys.exit(0)

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 5555))
        sock.listen(100)

        threading.Thread(target=self.accept_and_queue, args=(sock,), daemon=True).start()

        while True:
            self.wait_for_session()
