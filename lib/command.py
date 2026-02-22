import os
import paramiko

from lib.ssh_ca import CA
from lib.secret import Secret

class Command:

    def __init__(self, home, username):
        self.username = username
        self.home     = home
        self.ca       = CA(self.home)
        self.secret   = Secret(self.home)
        self.logger   = paramiko.util.get_logger("paramiko")

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
        raise ValueError("unknown command")

    def exec(self, line):
        args = line.split()
        if args[0] == "cert":
            return self.command_cert()
        if args[0] == "secret":
            return self.command_secret(line)
        else:
            raise ValueError(f"unknown command '{line}'")
