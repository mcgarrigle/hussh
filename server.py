import threading
import paramiko
import base64

from command import Command


class Server(paramiko.ServerInterface):

    def __init__(self):
        self.event    = threading.Event()
        self.username = None
        self.key      = None

    def publickey(self, path):
        with open(path, "r") as f:
            key_parts = f.read().strip().split()
            key_type  = key_parts[0]
            key_bytes = base64.b64decode(key_parts[1])
            return paramiko.PKey.from_type_string(key_type, key_bytes)

    def check_auth_publickey(self, username, key):
        try:
            authorized_key = self.publickey(f"keys/{username}.pub")
            if key == authorized_key:
                self.username = username
                self.key      = key
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
        except Exception:
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
        command = Command(self.username)
        res = command.exec(cmd.decode()) 
        channel.send(res + "\n")
        self.event.set()
        return True

    def check_channel_shell_request(self, channel):
        return False
