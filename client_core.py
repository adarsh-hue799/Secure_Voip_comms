# client_core.py
import socket
import threading
import pyaudio
from crypto_utils import load_private_key, rsa_decrypt, aes_encrypt, load_public_key
from net_utils import send_packet, recv_packet
from Crypto.PublicKey import RSA

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

class VoipClient:
    def __init__(self, server_ip="127.0.0.1", port=9999, key_prefix="client"):
        self.server_ip = server_ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.aes_key = None
        self.running = False
        self.privkey = load_private_key(f"keys/{key_prefix}_priv.pem")
        self.pubkey = load_public_key(f"keys/{key_prefix}_pub.pem")
        self.audio = pyaudio.PyAudio()
        self.record_stream = None

    def get_input_device_index(self):
        print("[Audio] Scanning input devices...")
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            print(f"  Device {i}: {info['name']} | Input channels: {info['maxInputChannels']}")
            if info.get("maxInputChannels", 0) > 0:
                print(f"[Audio] Selected input device {i}: {info['name']}")
                return i
        raise RuntimeError("No valid input device found. Connect a microphone.")

    def connect(self):
        self.sock.connect((self.server_ip, self.port))
        print(f"[Client] Connected to server {self.server_ip}:{self.port}")
        self.perform_handshake()
        in_idx = self.get_input_device_index()
        self.record_stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                                             input=True, input_device_index=in_idx,
                                             frames_per_buffer=CHUNK)
        self.running = True
        threading.Thread(target=self._send_loop, daemon=True).start()

    def perform_handshake(self):
        # send client public key PEM
        with open("keys/client_pub.pem", "rb") as f:
            send_packet(self.sock, f.read())
        # receive server public key (not used further here, but kept for protocol)
        server_pub_pem = recv_packet(self.sock)
        # receive RSA-encrypted AES session key
        enc_session = recv_packet(self.sock)
        # decrypt with client private key
        self.aes_key = rsa_decrypt(self.privkey, enc_session)
        print("[Client] Handshake complete. AES session key established.")

    def _send_loop(self):
        try:
            while self.running:
                frame = self.record_stream.read(CHUNK, exception_on_overflow=False)
                enc = aes_encrypt(self.aes_key, frame)
                send_packet(self.sock, enc)
        except Exception as e:
            print("[Client] Send loop error:", e)
        finally:
            self.stop()

    def stop(self):
        self.running = False
        try:
            if self.record_stream:
                self.record_stream.stop_stream(); self.record_stream.close()
        except:
            pass
        try:
            self.sock.close()
        except:
            pass
        try:
            self.audio.terminate()
        except:
            pass

if __name__ == "__main__":
    client = VoipClient()
    client.connect()
