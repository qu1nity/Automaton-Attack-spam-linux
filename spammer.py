import string
import threading
import time
import tkinter as tk

from pynput import keyboard


INTERVAL = 0 


class DotaSpammerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automaton Attack abuse")
        self.root.geometry("350x150")
        self.root.attributes("-topmost", True)

        self.letters = string.ascii_lowercase
        self.current_index = 0

        self.running = threading.Event()
        self.shutdown = threading.Event()
        self.controller = keyboard.Controller()

        self.status_label = tk.Label(
            root,
            text="Статус: Выключен",
            fg="red",
            font=("Arial", 16, "bold"),
        )
        self.status_label.pack(pady=15)

        self.info_label = tk.Label(
            root,
            text="Горячие клавиши:\n[ 1 ] — Старт\n[ 2 ] — Стоп",
            font=("Arial", 12),
        )
        self.info_label.pack(pady=5)

        self.listener = keyboard.Listener(on_release=self.on_key_release)
        self.listener.start()

        self.spam_thread = threading.Thread(target=self.spam_loop, daemon=True)
        self.spam_thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def on_key_release(self, key):
        """Вызывается при отпускании клавиши."""
        try:
            char = key.char
        except AttributeError:
            return

        if char == "1":
            self.start_script()
        elif char == "2":
            self.stop_script()

    def start_script(self):
        if not self.running.is_set():
            self.running.set()
            self.root.after(
                0,
                lambda: self.status_label.config(
                    text="Статус: Работает", fg="green"
                ),
            )

    def stop_script(self):
        if self.running.is_set():
            self.running.clear()
            self.root.after(
                0,
                lambda: self.status_label.config(
                    text="Статус: Выключен", fg="red"
                ),
            )

    def spam_loop(self):
        while not self.shutdown.is_set():
            if not self.running.wait(timeout=0.1):
                continue

            if self.shutdown.is_set() or not self.running.is_set():
                continue

            char = self.letters[self.current_index]
            key = keyboard.KeyCode.from_char(char)

            self.controller.press(key)
            self.controller.release(key)

            self.current_index = (self.current_index + 1) % len(self.letters)
            time.sleep(INTERVAL)

    def close(self):
        self.shutdown.set()
        self.running.clear()
        self.listener.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DotaSpammerApp(root)
    root.mainloop()
