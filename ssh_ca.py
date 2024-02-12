#!/usr/bin/env python3

import sys
import os
import hashlib
from datetime import datetime, timedelta
import yaml
from sshkey_tools.keys import PublicKey, PrivateKey
from sshkey_tools.cert import SSHCertificate, CertificateFields

class CA:

    def __init__(self, base):
        self.base = base
        path = os.path.join(self.base, 'ca', "user_ca_key")
        self.ca_user_private_key = PrivateKey.from_file(path)

    def profile(self, name):
        path = os.path.join(self.base, 'users', name)
        if not os.path.isfile(path):
            return None
        with open(path) as f:
            return yaml.safe_load(f.read())

    def store_public_key(self, public_key_text):
        digest = hashlib.sha256(public_key_text).hexdigest()
        path   = os.path.join(self.base, 'keys', f"{digest}.pub")
        with open(path, "wb") as f:
            f.write(public_key_text)
        return digest

    def retrieve_public_key(self, digest):
        path = os.path.join(self.base, 'keys', f"{digest}.pub")
        return PublicKey.from_file(path)

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
    this = CA(here)

    profile = this.profile("1e8212feddf3b955a6bae28ee62a2225fb55c4034389498f3703b8289a1fbc51")
    keyfile = sys.argv[1]

    key  = PublicKey.from_file(keyfile)
    cert = this.sign(key, profile)
    print(cert)
