import unittest
from schema import Schema

class TestSchema(unittest.TestCase):

    def setUp(self):
        self.schema = Schema(name=str, age=int)

    def test_validate(self):
        # matches schema
        self.assertTrue(self.schema.validate({"name":"foo","age":42}))
        # both have wrong types
        self.assertFalse(self.schema.validate({"name":42,"age":"foo"}))
        # age has wrong type
        self.assertFalse(self.schema.validate({"name":"foo","age":42.1}))
        # key "age" is missing
        self.assertFalse(self.schema.validate({"name":"foo"}))
        # key "age" is missing and other key substituted
        self.assertFalse(self.schema.validate({"name":"foo","beast":666}))
        # extra key that is not in the schema
        self.assertFalse(self.schema.validate({"name":"foo","age":42,"unwanted":True}))

    def test_equals(self):
        self.assertTrue({"name":"foo","age":42} == self.schema)

    def test_not_equals(self):
        self.assertTrue({"name":42,"age":"foo"} != self.schema)

if __name__ == '__main__':
    unittest.main()
