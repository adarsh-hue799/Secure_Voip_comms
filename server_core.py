# server_core.py
import socket
import threading
import pyaudio
from crypto_utils import generate_aes_key, rsa_encrypt, load_private_key, aes_decrypt, load_public_key
from net_utils import send_packet, recv_packet

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

class VoipServer:
    def __init__(self, host="0.0.0.0", port=9999, key_prefix="server"):
        self.host = host
        self.port = port
        self.sock = None
        self.conn = None
        self.addr = None
        self.aes_key = None
        self.running = False
        self.privkey = load_private_key(f"keys/{key_prefix}_priv.pem")
        self.pubkey = load_public_key(f"keys/{key_prefix}_pub.pem")
        self.audio = pyaudio.PyAudio()
        self.play_stream = None

    def get_output_device_index(self):
        """Return first device index with output channels (>0)."""
        print("[Audio] Scanning output devices...")
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            # info fields: name, maxOutputChannels
            print(f"  Device {i}: {info['name']} | Output channels: {info['maxOutputChannels']}")
            if info.get("maxOutputChannels", 0) > 0:
                print(f"[Audio] Selected output device {i}: {info['name']}")
                return i
        raise RuntimeError("No valid output device found. Connect headphones or speakers.")

    def start_listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print(f"[Server] Listening on {self.host}:{self.port}")
        self.conn, self.addr = self.sock.accept()
        print(f"[Server] Connected by {self.addr}")
        self.perform_handshake()

        out_idx = self.get_output_device_index()
        self.play_stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                                           output=True, output_device_index=out_idx,
                                           frames_per_buffer=CHUNK)
        self.running = True
        threading.Thread(target=self._recv_loop, daemon=True).start()

    def perform_handshake(self):
        # receive client's public key PEM
        client_pub_pem = recv_packet(self.conn)
        client_pub = load_public_key_from_pem_bytes(client_pub_pem)
        # send server public key
        with open("keys/server_pub.pem", "rb") as f:
            send_packet(self.conn, f.read())
        # create AES session key and send RSA-encrypted to client
        self.aes_key = generate_aes_key()
        enc_session = rsa_encrypt(client_pub, self.aes_key)
        send_packet(self.conn, enc_session)
        print("[Server] Handshake complete. AES session key established.")

    def _recv_loop(self):
        import random
        try:
            while self.running:
                pkt = recv_packet(self.conn)
# 💥 Simulate network corruption (1 in 10 packets)
            if random.random() < 0.1:
                pkt = b"tampered" + pkt
                try:
                    plain = aes_decrypt(self.aes_key, pkt)
                    # Play raw PCM bytes
                    self.play_stream.write(plain)
                except Exception as e:
                    print("[Server] Decrypt/playback error:", e)
        except ConnectionError:
            print("[Server] Connection closed.")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        try:
            if self.conn:
                self.conn.close()
        except:
            pass
        try:
            if self.sock:
                self.sock.close()
        except:
            pass
        try:
            if self.play_stream:
                self.play_stream.stop_stream(); self.play_stream.close()
        except:
            pass
        try:
            self.audio.terminate()
        except:
            pass

# helper: load public key from PEM bytes using PyCryptodome
from Crypto.PublicKey import RSA
def load_public_key_from_pem_bytes(pem_bytes):
    return RSA.import_key(pem_bytes)

if __name__ == "__main__":
    server = VoipServer()
    server.start_listen()
