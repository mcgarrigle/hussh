import os

from ssh_ca import CA

class Command:

    def __init__(self, username, key, channel):
        self.username = username
        self.key      = key
        self.channel  = channel
        self.here     = os.path.dirname(os.path.realpath(__file__))
        self.ca       = CA(self.here)

    def cert(self):
        user_public_key = self.ca.user_public_key(self.username)
        profile = self.ca.profile(self.username)
        return self.ca.sign(user_public_key, profile) 

    def parse(self, cmd):
        if cmd == "cert":
            return self.cert()
        else:
            return f"ERROR: unknown command '{cmd}'"

    def exec(self, cmd):
        res = self.parse(cmd)
        self.channel.send(res + "\n")
