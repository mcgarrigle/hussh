#!/usr/bin/env python3

import sys
import os
import re
import yaml
import hashlib
import subprocess
from itertools import chain
from pprint import pprint

class ca:

    def __init__(self, base):
        self.base = base

    def profile(self, name):
        path = os.path.join(self.base, 'users', name)
        if not os.path.isfile(path):
            return None
        with open(path) as f:
            return yaml.safe_load(f.read())

    def key(self, data):
        digest = hashlib.sha256(data).hexdigest()
        path = os.path.join(self.base, 'keys', f"{digest}.pub")
        with open(path, "w") as f:
            f.write(data.decode("utf-8"))
        return digest

    def sign(self, keyfile, profile):
        principals = ",".join(profile["principals"])
        args = [
          "ssh-keygen",
          "-s", "ca/user_ca_key",
          "-V", profile["validity"],
          "-I", str(profile["key_id"]),
          "-z", str(profile["serial"]),
          "-n", principals,
          "-O", "clear"
        ]
        options = [ ("-O", f"extension:{option}") for option in profile["extensions"] ]
        args = args + list(chain(*options))
        args.append(keyfile)
        result = subprocess.run(args, shell=False, capture_output=True, text=True)
        match = re.match(r'Signed user key (.*?):', result.stderr)
        certfile =  match.group(1)
        return certfile

if __name__ == "__main__":

    base = os.path.dirname(os.path.realpath(__file__))
    this = ca(base)

    profile = this.profile("1e8212feddf3b955a6bae28ee62a2225fb55c4034389498f3703b8289a1fbc51")
    keyfile = sys.argv[1]

    cert = this.sign(keyfile, profile)
    print(cert)
