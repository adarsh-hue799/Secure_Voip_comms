# gui_server.py
import threading
import tkinter as tk
from tkinter import messagebox
from server_core import VoipServer

class ServerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Secure VoIP — Server")
        root.geometry("360x180")
        self.server = None

        self.status = tk.Label(root, text="Status: Idle", fg="blue")
        self.status.pack(pady=10)

        self.btn_start = tk.Button(root, text="Start Server", width=20, bg="#28a745", fg="white", command=self.start_server)
        self.btn_start.pack(pady=8)

        self.btn_stop = tk.Button(root, text="Stop Server", width=20, bg="#dc3545", fg="white", command=self.stop_server, state=tk.DISABLED)
        self.btn_stop.pack(pady=8)

    def start_server(self):
        self.server = VoipServer()
        threading.Thread(target=self._start_thread, daemon=True).start()
        self.status.config(text="Status: Listening...", fg="orange")
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)

    def _start_thread(self):
        try:
            self.server.start_listen()
            self.status.config(text=f"Status: Connected to client", fg="green")
        except Exception as e:
            messagebox.showerror("Server Error", str(e))
            self.status.config(text="Status: Idle", fg="red")
            self.btn_start.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)

    def stop_server(self):
        if self.server:
            self.server.stop()
        self.status.config(text="Status: Stopped", fg="red")
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()
