#!/usr/bin/env python3

import sys
import os
import hashlib
from datetime import datetime, timedelta
import yaml
import json
from schema import Schema
from sshkey_tools.keys import PublicKey, PrivateKey
from sshkey_tools.cert import SSHCertificate, CertificateFields

class CA:

    def __init__(self, base):
        self.base = base
        path = os.path.join(self.base, 'ca', "user_ca_key")
        self.ca_user_private_key = PrivateKey.from_file(path)
        self.public_key_schema = Schema(name=str, key=str)

    def key_store_path(self, digest):
        return os.path.join(self.base, 'keys', f"{digest}.json")

    def profile(self, name):
        path = os.path.join(self.base, 'users', name)
        if not os.path.isfile(path):
            return None
        with open(path) as f:
            return yaml.safe_load(f.read())

    def store_public_key(self, name,  public_key_text):
        digest = hashlib.sha256(public_key_text.encode(encoding="utf-8")).hexdigest()
        path = self.key_store_path(digest)
        obj = { "id":digest, "name":name, "key":public_key_text }
        with open(path, "w") as f:
            f.write(json.dumps(obj))
        return digest

    def retrieve_public_key(self, digest):
        path = self.key_store_path(digest)
        with open(path, "r") as f:
            return json.loads(f.read())

    def sign(self, subject_public_key, profile):
        cert_fields = CertificateFields(
            serial=1234567890,
            cert_type=1,
            key_id="someuser@somehost",
            principals=profile["principals"],
            valid_after=datetime.now(),
            valid_before=datetime.now() + timedelta(hours=8),
            critical_options=[],
            extensions=profile["extensions"]
        )
        certificate = SSHCertificate.create(
            subject_pubkey=subject_public_key,
            ca_privkey=self.ca_user_private_key,
            fields=cert_fields,
        )
        certificate.sign()
        return certificate.to_string()

if __name__ == "__main__":

    here = os.path.dirname(os.path.realpath(__file__))
    ca = CA(here)

    profile = ca.profile("1e8212feddf3b955a6bae28ee62a2225fb55c4034389498f3703b8289a1fbc51")
    keyfile = sys.argv[1]

    digest = ca.store_public_key(keyfile, "ssh public key")
    print(digest)

    keyblob = ca.retrieve_public_key("f7fd17cd432bc2587b2679cc05e1b8d55a2805eef1cc2f8a93bab243aff72b5d")
    print(keyblob)
    
    #key  = PublicKey.from_string(keyfile)
    #cert = ca.sign(key, profile)
    #print(cert)
