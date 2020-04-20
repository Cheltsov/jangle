from abc import abstractmethod
from hashlib import sha256

class IEncoder():
    @abstractmethod
    def encode(self, text: str):
        pass

class SHA256Encoder(IEncoder):
    def encode(self, text: str) -> str:
        return sha256(text.encode('utf-8')).hexdigest()
