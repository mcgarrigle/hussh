#!/usr/bin/env python3

import os
import unittest
from datetime import datetime, timedelta
from ssh_ca import CA

class TestSSHCA(unittest.TestCase):

    def setUp(self):
        here = os.path.dirname(os.path.realpath(__file__))
        fixtures = os.path.join(here, "fixtures")
        self.ca = CA(fixtures)

    def test_time_from(self):
        now = datetime.now()
        self.assertEqual(self.ca.time_from(now, "1h"), now + timedelta(hours=1))
        self.assertEqual(self.ca.time_from(now, "1d"), now + timedelta(hours=24))
        self.assertEqual(self.ca.time_from(now, "2d"), now + timedelta(hours=48))
        self.assertEqual(self.ca.time_from(now, "1w"), now + timedelta(hours=24 * 7))
        self.assertEqual(self.ca.time_from(now, "2w"), now + timedelta(hours=24 * 14))

    def test_sign(self):
        key     = self.ca.user_public_key("test")
        profile = self.ca.profile("test")
        cert    = self.ca.sign(key, profile)
        self.assertTrue("rsa-sha2-512-cert-v01@openssh.com" in cert)

if __name__ == '__main__':
    unittest.main()
