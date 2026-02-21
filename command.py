import os

from ssh_ca import CA
from secret import Secret

class Command:

    def __init__(self, username):
        self.username = username
        self.here     = os.path.dirname(os.path.realpath(__file__))
        self.ca       = CA(self.here)
        self.secret   = Secret(self.here)

    def command_cert(self):
        user_public_key = self.ca.user_public_key(self.username)
        profile = self.ca.profile(self.username)
        return self.ca.sign(user_public_key, profile) 

    def command_secret(self, line):
        args = line.split(" ", 3)
        if args[1] == "list":
            return self.secret.ls()
        if args[1] == "set":
            return self.secret.set(args[2], args[3])
        if args[1] == "get":
            return self.secret.get(args[2])

    def dispatch(self, line):
        args = line.split()
        if args[0] == "cert":
            return self.command_cert()
        if args[0] == "secret":
            return self.command_secret(line)
        else:
            return f"ERROR: unknown command '{cmd}'"

    def exec(self, cmd):
        return self.dispatch(cmd)
