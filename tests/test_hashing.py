import unittest
import json
import datetime
from src.core.hashing import SignedObject

class TestSignedObject(unittest.TestCase):

    def setUp(self):
        self.sample_data = {"key": "value", "numbers": [1, 2, 3]}
        self.obj = SignedObject(data=self.sample_data.copy(), version=1)

    def test_sign_and_verify_success(self):
        """Test that a valid signature verifies correctly."""
        self.obj.sign()
        self.assertIsNotNone(self.obj.signature)
        self.assertTrue(self.obj.verify())

    def test_verify_fails_without_signature(self):
        """Test that verify returns False if not signed."""
        self.assertIsNone(self.obj.signature)
        self.assertFalse(self.obj.verify())

    def test_tamper_data_fails(self):
        """Test that modifying data invalidates the signature."""
        self.obj.sign()
        self.obj.data["key"] = "hacked"
        self.assertFalse(self.obj.verify())

    def test_tamper_version_fails(self):
        """Test that modifying version invalidates the signature."""
        self.obj.sign()
        self.obj.version = 2
        self.assertFalse(self.obj.verify())

    def test_tamper_timestamp_fails(self):
        """Test that modifying timestamp invalidates the signature."""
        self.obj.sign()
        # Change timestamp slightly
        self.obj.timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.assertFalse(self.obj.verify())

    def test_determinism(self):
        """Test that identical objects produce identical signatures."""
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
        obj1 = SignedObject(data={"a": 1}, version=1, timestamp=ts)
        obj2 = SignedObject(data={"a": 1}, version=1, timestamp=ts)

        obj1.sign()
        obj2.sign()

        self.assertEqual(obj1.signature, obj2.signature)

    def test_json_key_sorting(self):
        """Test that key order in dictionary doesn't affect hash (determinism)."""
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
        # Different insertion order
        data1 = {"a": 1, "b": 2}
        data2 = {"b": 2, "a": 1}

        obj1 = SignedObject(data=data1, version=1, timestamp=ts)
        obj2 = SignedObject(data=data2, version=1, timestamp=ts)

        obj1.sign()
        obj2.sign()

        self.assertEqual(obj1.signature, obj2.signature)

if __name__ == '__main__':
    unittest.main()
