# 🔐 Secure VoIP Comms

> **Real-time encrypted voice communication over TCP — RSA handshake + AES-128 session encryption, with a clean Tkinter GUI.**

---

## 📡 What is this?

**Secure VoIP Comms** is a peer-to-peer voice call application built in Python that encrypts all audio end-to-end. Unlike regular VoIP apps, every audio frame is encrypted before it leaves your machine using AES-128 (EAX mode), and the session key itself is securely exchanged using RSA-2048 public-key cryptography.

It works over any TCP network — LAN or internet — and comes with a simple GUI for both the server and client sides.

---

## ✨ Features

- 🔒 **RSA-2048 Handshake** — Server generates a unique AES session key and delivers it to the client encrypted with the client's RSA public key
- 🛡️ **AES-128 EAX Encryption** — Every audio chunk is encrypted with authentication (nonce + tag + ciphertext), preventing tampering and replay attacks
- 🎙️ **Real-time Audio Streaming** — 16kHz mono PCM audio captured and streamed over TCP using PyAudio
- 🖥️ **Dual GUI** — Separate Tkinter windows for Server and Client, no terminal needed
- 🔑 **Key Generation Script** — One command to generate fresh RSA key pairs for both sides
- 📦 **Lightweight** — Only 2 external dependencies: `pycryptodome` and `PyAudio`

---

## 🏗️ Project Structure

```
Secure_Voip_comms/
│
├── gui_server.py        # Server GUI — start/stop listening for a call
├── gui_client.py        # Client GUI — enter IP and connect to server
│
├── server_core.py       # Server logic — handshake, decrypt, play audio
├── client_core.py       # Client logic — handshake, record, encrypt, send
│
├── crypto_utils.py      # RSA + AES encrypt/decrypt helpers
├── net_utils.py         # Length-prefixed TCP packet send/receive
├── generate_keys.py     # Generates RSA key pairs into keys/ folder
├── test.py              # Basic tests
│
├── requirements.txt     # Python dependencies
└── .gitignore
```

---

## 🔐 How the Encryption Works

```
CLIENT                                    SERVER
  |                                          |
  |--- sends client_pub.pem --------------->|
  |<-- receives server_pub.pem -------------|
  |                                          |  generates AES session key
  |<-- receives RSA-encrypted AES key -------|
  |    (decrypts with client_priv.pem)       |
  |                                          |
  |=== AES-128 EAX encrypted audio ========>|
  |    (nonce + tag + ciphertext per frame)  |
```

Every audio frame is independently encrypted. If a packet is corrupted or tampered with, the AES-EAX tag verification fails and that frame is silently dropped — the call continues.

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/adarsh-hue799/Secure_Voip_comms.git
cd Secure_Voip_comms
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Generate RSA key pairs

```bash
python generate_keys.py
```

This creates a `keys/` folder with:
- `server_priv.pem` / `server_pub.pem`
- `client_priv.pem` / `client_pub.pem`

> ⚠️ **Never share or commit the `_priv.pem` files.** The `keys/` folder is already in `.gitignore`.

### 4. Run the Server

```bash
python gui_server.py
```

Click **Start Server** — it will listen on port `9999`.

### 5. Run the Client

```bash
python gui_client.py
```

Enter the server's IP address (use `127.0.0.1` for localhost), then click **Connect & Start Call**.

---

## 📋 Requirements

| Requirement | Version |
|---|---|
| Python | 3.10+ |
| pycryptodome | latest |
| PyAudio | latest |
| OS | Windows / macOS / Linux |

> **Note for macOS/Linux users:** You may need to install PortAudio before PyAudio:
> ```bash
> # macOS
> brew install portaudio
>
> # Ubuntu/Debian
> sudo apt-get install portaudio19-dev
> ```

---

## 🛠️ Running Without GUI (Terminal Mode)

**Server:**
```bash
python server_core.py
```

**Client:**
```bash
python client_core.py
```

---

## 📁 Key Files Explained

| File | Purpose |
|---|---|
| `crypto_utils.py` | AES-128 EAX encrypt/decrypt + RSA PKCS1-OAEP encrypt/decrypt |
| `net_utils.py` | Framed TCP packets using 4-byte length prefix (`struct.pack(">I", ...)`) |
| `generate_keys.py` | Generates 2048-bit RSA key pairs using PyCryptodome |
| `gui_server.py` | Tkinter GUI wrapping `VoipServer` in a background thread |
| `gui_client.py` | Tkinter GUI wrapping `VoipClient` in a background thread |

---

## ⚙️ Configuration

Default settings in `client_core.py` and `server_core.py`:

```python
CHUNK    = 1024       # Audio frames per buffer
FORMAT   = paInt16    # 16-bit PCM
CHANNELS = 1          # Mono
RATE     = 16000      # 16 kHz sample rate
PORT     = 9999       # TCP port
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
