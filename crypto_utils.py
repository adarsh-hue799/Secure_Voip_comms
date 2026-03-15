# crypto_utils.py
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

# AES - EAX mode helpers (nonce + tag)
def generate_aes_key():
    return get_random_bytes(16)  # 128-bit

def aes_encrypt(key: bytes, plaintext: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return cipher.nonce + tag + ciphertext  # nonce(16) + tag(16) + ciphertext

def aes_decrypt(key: bytes, data: bytes) -> bytes:
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

# RSA helpers using PyCryptodome RSA
def load_private_key(path: str):
    return RSA.import_key(open(path, "rb").read())

def load_public_key(path: str):
    return RSA.import_key(open(path, "rb").read())

def rsa_encrypt(pubkey, data: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(pubkey)
    return cipher.encrypt(data)

def rsa_decrypt(privkey, data: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(privkey)
    return cipher.decrypt(data)
