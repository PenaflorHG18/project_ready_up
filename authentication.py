from cryptography.fernet import Fernet
from passlib.hash import argon2
from passlib.hash import bcrypt_sha256

class Hasher:
    def __init__(self, pepper_key):
        self.pepper = Fernet(pepper_key)

    def hash(self, pwd):
        # hash with argon2
        hash = argon2.using(rounds=10).hash(pwd)
        # convert this unicode hash string into bytes before encryption
        hashb = hash.encode('utf-8')
        # encrypt this hash using the global pepper
        pep_hash = self.pepper.encrypt(hashb)
        return pep_hash

    def check(self, pwd, pep_hash):
        # decrypt the hash using the global pepper
        hashb = self.pepper.decrypt(pep_hash)
        # convert this hash back into a unicode string
        hash = hashb.decode('utf-8')
        # check if the given password matches this hash
        return argon2.verify(pwd, hash)

    @staticmethod
    def random_pepper():
        return Fernet.generate_key()