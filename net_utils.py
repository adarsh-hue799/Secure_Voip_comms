# net_utils.py
import struct
import socket

def send_packet(conn: socket.socket, data: bytes):
    conn.sendall(struct.pack(">I", len(data)) + data)

def recv_exact(conn: socket.socket, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Connection closed while receiving.")
        buf += chunk
    return buf

def recv_packet(conn: socket.socket) -> bytes:
    raw = recv_exact(conn, 4)
    (length,) = struct.unpack(">I", raw)
    return recv_exact(conn, length)
