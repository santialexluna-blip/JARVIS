"""Interfaz de escritorio y conversación por voz de JARVIS."""

import queue
import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from assistant import Assistant
from voice import VoiceEngine
from voice_app import VoiceConversation


BG = "#07111f"
PANEL = "#0d1b2e"
PANEL_2 = "#10243d"
CYAN = "#46d9ff"
BLUE = "#248cff"
TEXT = "#e9f5ff"
MUTED = "#8ba7bf"
GREEN = "#57e6a5"


class JarvisDesktop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS v2.4")
        self.root.geometry("920x680")
        self.root.minsize(760, 560)
        self.root.configure(bg=BG)

        self.voice = VoiceEngine(language="es-MX")
        self.conversation = VoiceConversation(assistant=Assistant(), voice=self.voice)
        self.events = queue.Queue()
        self.stop_event = threading.Event()
        self.listening = False
        self.worker = None
        self.voice_ids = {}

        self.status = tk.StringVar(value="PREPARANDO")
        self.voice_name = tk.StringVar(value="Voz automática")
        self._build_styles()
        self._build_ui()
        self._load_voices()

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(100, self._poll_events)
        self.root.after(600, self.start_listening)

    def _build_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "Jarvis.TCombobox",
            fieldbackground=PANEL_2,
            background=PANEL_2,
            foreground=TEXT,
            arrowcolor=CYAN,
            bordercolor="#244c6f",
        )

    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=34, pady=(26, 12))
        tk.Label(header, text="JARVIS", bg=BG, fg=TEXT, font=("Segoe UI", 30, "bold")).pack(side="left")
        tk.Label(header, text="  v2.4 · IA LOCAL", bg=BG, fg=CYAN, font=("Segoe UI", 11, "bold")).pack(side="left", pady=(12, 0))
        tk.Label(header, textvariable=self.status, bg=BG, fg=GREEN, font=("Segoe UI", 11, "bold")).pack(side="right", pady=(12, 0))

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=34, pady=8)

        side = tk.Frame(body, bg=PANEL, width=230, highlightbackground="#183957", highlightthickness=1)
        side.pack(side="left", fill="y", padx=(0, 16))
        side.pack_propagate(False)

        self.orb = tk.Canvas(side, width=150, height=150, bg=PANEL, highlightthickness=0)
        self.orb.pack(pady=(35, 16))
        self.orb.create_oval(20, 20, 130, 130, outline="#174b70", width=3)
        self.orb_id = self.orb.create_oval(40, 40, 110, 110, fill=BLUE, outline=CYAN, width=2)
        self.orb.create_text(75, 75, text="J", fill="white", font=("Segoe UI", 30, "bold"))

        tk.Label(side, text="VOZ", bg=PANEL, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=22, pady=(10, 6))
        self.voice_box = ttk.Combobox(side, textvariable=self.voice_name, state="readonly", style="Jarvis.TCombobox")
        self.voice_box.pack(fill="x", padx=20)
        self.voice_box.bind("<<ComboboxSelected>>", self._change_voice)
        tk.Button(side, text="PROBAR VOZ", command=self._preview_voice, bg="#16283c", fg=CYAN, activebackground="#223b56", relief="flat", font=("Segoe UI", 9, "bold"), cursor="hand2").pack(fill="x", padx=20, pady=(8, 0), ipady=6)

        self.listen_button = tk.Button(side, text="PAUSAR MICRÓFONO", command=self.toggle_listening, bg=BLUE, fg="white", activebackground=CYAN, relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2")
        self.listen_button.pack(fill="x", padx=20, pady=(26, 10), ipady=8)
        tk.Button(side, text="CERRAR JARVIS", command=self.close, bg="#16283c", fg=TEXT, activebackground="#223b56", relief="flat", font=("Segoe UI", 10), cursor="hand2").pack(fill="x", padx=20, ipady=8)

        main = tk.Frame(body, bg=PANEL, highlightbackground="#183957", highlightthickness=1)
        main.pack(side="left", fill="both", expand=True)
        tk.Label(main, text="CONVERSACIÓN", bg=PANEL, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=22, pady=(18, 8))

        self.transcript = ScrolledText(main, bg=PANEL, fg=TEXT, insertbackground=TEXT, selectbackground=BLUE, relief="flat", borderwidth=0, font=("Segoe UI", 12), wrap="word", state="disabled", padx=14, pady=14)
        self.transcript.pack(fill="both", expand=True, padx=8, pady=(0, 10))
        self.transcript.tag_configure("user", foreground=CYAN, spacing1=10)
        self.transcript.tag_configure("jarvis", foreground=TEXT, spacing1=8, spacing3=4)
        self.transcript.tag_configure("system", foreground=MUTED, spacing1=8)

        input_row = tk.Frame(main, bg=PANEL)
        input_row.pack(fill="x", padx=18, pady=(0, 18))
        self.entry = tk.Entry(input_row, bg=PANEL_2, fg=TEXT, insertbackground=TEXT, relief="flat", font=("Segoe UI", 12))
        self.entry.pack(side="left", fill="x", expand=True, ipady=10)
        self.entry.bind("<Return>", lambda _event: self.send_text())
        tk.Button(input_row, text="ENVIAR", command=self.send_text, bg=BLUE, fg="white", activebackground=CYAN, relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2").pack(side="left", padx=(10, 0), ipadx=18, ipady=8)

        self._append("system", "Sistema preparado. Di “Jarvis” para comenzar o escribe un mensaje.")

    def _append(self, role, message):
        labels = {"user": "TÚ", "jarvis": "JARVIS", "system": "SISTEMA"}
        self.transcript.configure(state="normal")
        self.transcript.insert("end", f"{labels[role]}  {message}\n", role)
        self.transcript.configure(state="disabled")
        self.transcript.see("end")

    def _load_voices(self):
        voices = self.voice.list_voices()
        self.voice_ids = {item["name"]: item["id"] for item in voices}
        names = ["Voz automática", *self.voice_ids]
        self.voice_box["values"] = names
        self.voice_name.set("Voz automática")

    def _change_voice(self, _event=None):
        selected = self.voice_name.get()
        self.voice.preferred_voice_id = self.voice_ids.get(selected)
        self._append("system", f"Voz seleccionada: {selected}.")

    def _preview_voice(self):
        was_listening = self.listening
        self.listening = False

        def preview():
            time.sleep(1.1)
            self.voice.speak("Hola. Soy Jarvis. Esta será mi nueva voz.")
            self.listening = was_listening

        threading.Thread(target=preview, daemon=True).start()

    def _set_status(self, text, color=GREEN):
        self.status.set(text)
        for widget in self.root.winfo_children()[0].winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("textvariable") == str(self.status):
                widget.configure(fg=color)

    def start_listening(self):
        self.listening = True
        self.listen_button.configure(text="PAUSAR MICRÓFONO")
        self._set_status("ESCUCHANDO")
        if not self.worker or not self.worker.is_alive():
            self.worker = threading.Thread(target=self._voice_loop, daemon=True)
            self.worker.start()

    def toggle_listening(self):
        self.listening = not self.listening
        if self.listening:
            self.listen_button.configure(text="PAUSAR MICRÓFONO")
            self._set_status("ESCUCHANDO")
        else:
            self.listen_button.configure(text="ACTIVAR MICRÓFONO")
            self._set_status("PAUSADO", MUTED)

    def _voice_loop(self):
        welcome = "Sistema listo. Di Jarvis para activarme."
        self.events.put(("jarvis", welcome))
        self.voice.speak(welcome)
        while not self.stop_event.is_set() and self.conversation.running:
            if not self.listening:
                time.sleep(0.1)
                continue
            try:
                heard = self.voice.listen(timeout=1, phrase_time_limit=12)
            except RuntimeError as exc:
                self.events.put(("error", str(exc)))
                return
            if not heard:
                continue
            self.events.put(("user", heard))
            response = self.conversation.process_text(heard)
            if response:
                self.events.put(("jarvis", response))
                self.voice.speak(response)
        self.events.put(("closed", None))

    def send_text(self):
        message = self.entry.get().strip()
        if not message:
            return
        self.entry.delete(0, "end")
        self._append("user", message)
        self.conversation.active = True

        def work():
            response = self.conversation.process_text(message)
            if response:
                self.events.put(("jarvis", response))
                self.voice.speak(response)

        threading.Thread(target=work, daemon=True).start()

    def _poll_events(self):
        try:
            while True:
                event, payload = self.events.get_nowait()
                if event == "user":
                    self._append("user", payload)
                elif event == "jarvis":
                    self._append("jarvis", payload)
                elif event == "error":
                    self._append("system", payload)
                    self._set_status("ERROR", "#ff6b7a")
                elif event == "closed":
                    self.close()
                    return
        except queue.Empty:
            pass
        self.root.after(100, self._poll_events)

    def close(self):
        self.stop_event.set()
        self.conversation.running = False
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    JarvisDesktop().run()


if __name__ == "__main__":
    main()
