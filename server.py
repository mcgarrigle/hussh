import threading
import paramiko
import base64

from command import Command


def publickey(path):
    with open(path, "r") as f:
        key_str   = f.read().strip().split()
        key_bytes = base64.b64decode(key_str[1])
        return paramiko.RSAKey(data=key_bytes)


class Server(paramiko.ServerInterface):

    def __init__(self):
        self.event    = threading.Event()
        self.username = None
        self.key      = None

    def check_auth_publickey(self, username, key):
        authorized_key = publickey(f"keys/{username}.pub")
        if key == authorized_key:
            self.username = username
            self.key      = key
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED

    def check_auth_password(self, username, password):
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'publickey'

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_exec_request(self, channel, cmd):
        command = Command(self.username, self.key, channel)
        command.exec(cmd.decode()) 
        self.event.set()
        return True

    def check_channel_shell_request(self, channel):
        return False
