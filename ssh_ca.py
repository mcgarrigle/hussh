#!/usr/bin/env python3

import sys
import os
import re
import yaml

from datetime import datetime, timedelta
from sshkey_tools.keys import PublicKey, PrivateKey
from sshkey_tools.cert import SSHCertificate, CertificateFields

class CA:

    def __init__(self, base):
        self.base = base
        path = os.path.join(self.base, 'ca', "ssh_ca_user_key")
        self.ca_user_private_key = PrivateKey.from_file(path)

    def time_from(self, now: datetime, delta : str) -> datetime:
        m = re.match('(\d+)([hdw])', delta)
        n = int(m[1])
        if m[2] == "h":
            return now + timedelta(hours=n)
        if m[2] == "d":
            return now + timedelta(hours=n * 24)
        if m[2] == "w":
            return now + timedelta(hours=n * 24 * 7)
        if m[2] == "y":
            return now + timedelta(hours=n * 24 * 365)
        return now

    def validity(self, delta):
        return self.time_from(datetime.now(), delta)

    def user_public_key(self, username):
        path = os.path.join(self.base, 'keys', f"{username}.pub")
        return PublicKey.from_file(path)

    def profile(self, username):
        path = os.path.join(self.base, 'profiles', username)
        if not os.path.isfile(path):
            return None
        with open(path) as f:
            p = yaml.safe_load(f.read())
            p["username"] = username
            return p

    def sign(self, user_public_key, profile):
        key_id = profile["username"] + "@hussh"
        cert_fields = CertificateFields(
            serial=1234567890,
            cert_type=1,
            key_id=key_id,
            principals=profile["principals"],
            valid_after=datetime.now(),
            valid_before=self.validity(profile["validity"]),
            critical_options=[],
            extensions=profile["extensions"]
        )
        certificate = SSHCertificate.create(
            subject_pubkey=user_public_key,
            ca_privkey=self.ca_user_private_key,
            fields=cert_fields,
        )
        certificate.sign()
        return certificate.to_string()
