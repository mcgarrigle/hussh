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
        return obj

    def retrieve_public_key(self, digest):
        path = self.key_store_path(digest)
        with open(path, "r") as f:
            return json.loads(f.read())

    def sign(self, subject_public_key_text, profile):
        subject_public_key = PublicKey.from_string(subject_public_key_text)
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
