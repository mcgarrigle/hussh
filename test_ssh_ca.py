#!/usr/bin/env python3

import os
import unittest
from sshkey_tools.keys import PublicKey, PrivateKey
from sshkey_tools.cert import SSHCertificate, CertificateFields
from datetime import datetime, timedelta
from ssh_ca import CA

class TestSSHCA(unittest.TestCase):

    def fixture(self, path):
        with open(path, "r") as f:
            return f.read()

    def setUp(self):
        here = os.path.dirname(os.path.realpath(__file__))
        self.ca = CA(here)

    def test_time_from(self):
        # return datetime.now() + timedelta(hours=8),
        now = datetime.now()
        self.assertEqual(self.ca.time_from(now, "1h"), now + timedelta(hours=1))
        self.assertEqual(self.ca.time_from(now, "1d"), now + timedelta(hours=24))
        self.assertEqual(self.ca.time_from(now, "2d"), now + timedelta(hours=48))
        self.assertEqual(self.ca.time_from(now, "1w"), now + timedelta(hours=24 * 7))
        self.assertEqual(self.ca.time_from(now, "2w"), now + timedelta(hours=24 * 14))

    def test_store_public_key(self):
        result = self.ca.store_public_key("this key name", "ssh public key")
        self.assertEqual(result["id"], "f7fd17cd432bc2587b2679cc05e1b8d55a2805eef1cc2f8a93bab243aff72b5d")
        self.assertEqual(result["name"], "this key name")

    def test_retrieve_public_key(self):
        result = self.ca.retrieve_public_key("f7fd17cd432bc2587b2679cc05e1b8d55a2805eef1cc2f8a93bab243aff72b5d")
        self.assertEqual(result, {'id': 'f7fd17cd432bc2587b2679cc05e1b8d55a2805eef1cc2f8a93bab243aff72b5d', 'name': 'this key name', 'key': 'ssh public key'})

    def test_sign(self):
        key  = self.fixture("fixtures/test_public_key.pub")
        profile = {'key_id': 1666,
                   'serial': 4, 
                   'principals': ['test'], 
                   'extensions': ['permit-X11-forwarding', 
                                  'permit-agent-forwarding', 
                                  'permit-port-forwarding', 
                                  'permit-pty',
                                  'permit-user-rc'],
                   'validity': '1d'}
        cert = self.ca.sign(key, profile)
        self.assertTrue("rsa-sha2-512-cert-v01@openssh.com" in cert)

if __name__ == '__main__':
    unittest.main()
