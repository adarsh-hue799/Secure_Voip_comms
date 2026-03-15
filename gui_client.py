# gui_client.py
import threading
import tkinter as tk
from tkinter import messagebox
from client_core import VoipClient

class ClientGUI:
    def __init__(self, root):
        self.root = root
        root.title("Secure VoIP — Client")
        root.geometry("360x220")

        tk.Label(root, text="Server IP:").pack(pady=(10,0))
        self.ip_entry = tk.Entry(root)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.pack(pady=5)

        self.status = tk.Label(root, text="Status: Disconnected", fg="blue")
        self.status.pack(pady=6)

        self.btn_connect = tk.Button(root, text="Connect & Start Call", width=24, bg="#007bff", fg="white", command=self.connect_start)
        self.btn_connect.pack(pady=6)

        self.btn_disconnect = tk.Button(root, text="Disconnect", width=24, bg="#dc3545", fg="white", command=self.disconnect, state=tk.DISABLED)
        self.btn_disconnect.pack(pady=6)

        self.client = None

    def connect_start(self):
        ip = self.ip_entry.get().strip()
        if not ip:
            messagebox.showwarning("Input", "Please enter server IP")
            return
        self.client = VoipClient(server_ip=ip)
        threading.Thread(target=self._connect_thread, daemon=True).start()
        self.status.config(text="Status: Connecting...", fg="orange")
        self.btn_connect.config(state=tk.DISABLED)
        self.btn_disconnect.config(state=tk.NORMAL)

    def _connect_thread(self):
        try:
            self.client.connect()
            self.status.config(text="Status: In Call (sending audio)", fg="green")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            self.status.config(text="Status: Disconnected", fg="red")
            self.btn_connect.config(state=tk.NORMAL)
            self.btn_disconnect.config(state=tk.DISABLED)

    def disconnect(self):
        if self.client:
            self.client.stop()
        self.status.config(text="Status: Disconnected", fg="red")
        self.btn_connect.config(state=tk.NORMAL)
        self.btn_disconnect.config(state=tk.DISABLED)

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    app = ClientGUI(root)
    root.mainloop()
