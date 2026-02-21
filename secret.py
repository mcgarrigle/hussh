import os

from glob import glob
from cryptography.fernet import Fernet

class Secret:

    def __init__(self, here):
        self.here = here
        path = os.path.join(self.here, 'keys', 'aes.key')
        with open(path, 'r') as k:
            self.aes_key = k.read()

    def secret(self, key, mode):
        path = os.path.join(self.here, 'secrets', key)
        return open(path, mode)

    def ls(self):
        path = os.path.join(self.here, 'secrets', '*')
        secrets = map(os.path.basename, glob(path))
        return '\n'.join(secrets)

    def set(self, key, plaintext):
        f = Fernet(self.aes_key)
        cyphertext = f.encrypt(bytes(plaintext, encoding='utf8'))
        with self.secret(key, 'wb') as s:
            s.write(cyphertext)
        return f"set {key}"

    def get(self, key):
        f = Fernet(self.aes_key)
        with self.secret(key, 'rb') as s:
            cyphertext = s.read()
            plaintext  = f.decrypt(cyphertext)
        return plaintext.decode('utf-8')
