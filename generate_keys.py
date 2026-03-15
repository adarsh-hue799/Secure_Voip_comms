# generate_keys.py
from Crypto.PublicKey import RSA
import os

os.makedirs("keys", exist_ok=True)

def gen_pair(prefix):
    key = RSA.generate(2048)
    with open(f"keys/{prefix}_priv.pem", "wb") as f:
        f.write(key.export_key())
    with open(f"keys/{prefix}_pub.pem", "wb") as f:
        f.write(key.publickey().export_key())

if __name__ == "__main__":
    gen_pair("server")
    gen_pair("client")
    print("✅ RSA keys generated in ./keys/")
