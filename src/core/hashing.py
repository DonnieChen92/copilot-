import hashlib
import json
import datetime

class SignedObject:
    """
    Represents a piece of data that can be cryptographically signed and verified.
    This implements the 'H · Hash' module concepts of the A-Z framework.
    """
    def __init__(self, data, version=1, timestamp=None, signature=None):
        """
        Initialize the SignedObject.

        Args:
            data (dict): The data payload to be signed.
            version (int): The version number of the data schema or object.
            timestamp (str, optional): ISO format timestamp. Defaults to current UTC time.
            signature (str, optional): The cryptographic signature. Defaults to None.
        """
        self.data = data
        self.version = version
        self.timestamp = timestamp or datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.signature = signature

    def _calculate_hash(self):
        """
        Calculates the SHA-256 hash of the object's contents.

        Returns:
            str: The hexadecimal representation of the hash.
        """
        # Ensure strict determinism for the data dictionary
        serialized_data = json.dumps(self.data, sort_keys=True)

        # specific delimiter to avoid concatenation collisions
        payload = f"{serialized_data}|{self.version}|{self.timestamp}"

        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def sign(self):
        """
        Generates the hash for the current state and stores it in self.signature.
        """
        self.signature = self._calculate_hash()

    def verify(self):
        """
        Verifies the integrity of the object by comparing the stored signature
        against a newly calculated hash of the current state.

        Returns:
            bool: True if the signature is valid and matches the data; False otherwise.
        """
        if self.signature is None:
            return False

        current_hash = self._calculate_hash()
        return self.signature == current_hash
