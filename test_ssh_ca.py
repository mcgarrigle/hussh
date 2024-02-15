import os
import unittest
from ssh_ca import CA

class TestSSHCA(unittest.TestCase):

    def setUp(self):
        here = os.path.dirname(os.path.realpath(__file__))
        self.ca = CA(here)

    def test_test_store_public_key(self):
        digest = self.ca.store_public_key("this key name", "ssh public key")
        print(digest)
        self.assertEqual(digest, "f7fd17cd432bc2587b2679cc05e1b8d55a2805eef1cc2f8a93bab243aff72b5d")

    def test_test_retrieve_public_key(self):
        keyblob = self.ca.retrieve_public_key("f7fd17cd432bc2587b2679cc05e1b8d55a2805eef1cc2f8a93bab243aff72b5d")
        print(keyblob)
        self.assertEqual(keyblob, {'id': 'f7fd17cd432bc2587b2679cc05e1b8d55a2805eef1cc2f8a93bab243aff72b5d', 'name': 'this key name', 'key': 'ssh public key'})

if __name__ == '__main__':
    unittest.main()

    # profile = ca.profile("1e8212feddf3b955a6bae28ee62a2225fb55c4034389498f3703b8289a1fbc51")
    # keyfile = sys.argv[1]

    # digest = ca.store_public_key(keyfile, "ssh public key")
    # print(digest)

    # keyblob = ca.retrieve_public_key("f7fd17cd432bc2587b2679cc05e1b8d55a2805eef1cc2f8a93bab243aff72b5d")
    # print(keyblob)

    #key  = PublicKey.from_string(keyfile)
    #cert = ca.sign(key, profile)
    #print(cert)

