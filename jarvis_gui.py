"""Interfaz HUD de escritorio y conversación por voz de JARVIS."""

import math
import queue
import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from assistant import Assistant
from voice import VoiceEngine
from voice_app import VoiceConversation

BG, PANEL = "#02090a", "#061719"
CYAN, CYAN_SOFT, CYAN_DARK = "#31f4ee", "#137e82", "#08383d"
TEXT, MUTED, RED = "#d7ffff", "#579398", "#ff6275"


class JarvisDesktop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS v2.5 · HUD")
        self.root.geometry("1080x720")
        self.root.minsize(900, 620)
        self.root.configure(bg=BG)
        self.voice = VoiceEngine(language="es-MX", profile="cinematic")
        self.conversation = VoiceConversation(assistant=Assistant(), voice=self.voice)
        self.events, self.stop_event = queue.Queue(), threading.Event()
        self.listening, self.worker, self.voice_ids = False, None, {}
        self.angle, self.pulse = 0, 0
        self.status = tk.StringVar(value="INICIANDO")
        self.voice_name = tk.StringVar(value="JARVIS cinematográfico")
        self._build_styles()
        self._build_ui()
        self._load_voices()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(50, self._animate)
        self.root.after(100, self._poll_events)
        self.root.after(700, self.start_listening)

    def _build_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Jarvis.TCombobox", fieldbackground=PANEL, background=PANEL,
                        foreground=TEXT, arrowcolor=CYAN, bordercolor=CYAN_DARK)

    def _build_ui(self):
        self.hud = tk.Canvas(self.root, bg=BG, highlightthickness=0)
        self.hud.pack(fill="both", expand=True)
        self.hud.bind("<Configure>", lambda _event: self._draw_hud())
        self.status_label = tk.Label(self.root, textvariable=self.status, bg=BG, fg=MUTED,
                                     font=("Consolas", 12, "bold"))
        self.status_window = self.hud.create_window(28, 58, anchor="nw", window=self.status_label)
        self.title_window = self.hud.create_text(540, 20, text="J  A  R  V  I  S", fill=TEXT,
                                                 font=("Consolas", 15, "bold"))
        self.version_window = self.hud.create_text(540, 44, text="HUD 2.5  ·  IA LOCAL", fill=MUTED,
                                                   font=("Consolas", 8))
        self.info_button = self._round_button("i", self.show_info)
        self.info_window = self.hud.create_window(0, 0, window=self.info_button)

        self.transcript_frame = tk.Frame(self.root, bg=PANEL, highlightbackground=CYAN_DARK,
                                         highlightthickness=1)
        tk.Label(self.transcript_frame, text="REGISTRO DE CONVERSACIÓN", bg=PANEL, fg=CYAN,
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=16, pady=(13, 4))
        self.transcript = ScrolledText(self.transcript_frame, bg=PANEL, fg=TEXT,
                                       insertbackground=TEXT, relief="flat", borderwidth=0,
                                       font=("Segoe UI", 10), wrap="word", state="disabled")
        self.transcript.pack(fill="both", expand=True, padx=10, pady=5)
        for tag, color in (("user", CYAN), ("jarvis", TEXT), ("system", MUTED)):
            self.transcript.tag_configure(tag, foreground=color, spacing1=7)
        input_row = tk.Frame(self.transcript_frame, bg=PANEL)
        input_row.pack(fill="x", padx=12, pady=(4, 12))
        self.entry = tk.Entry(input_row, bg="#092327", fg=TEXT, insertbackground=TEXT,
                              relief="flat", font=("Segoe UI", 10))
        self.entry.pack(side="left", fill="x", expand=True, ipady=7)
        self.entry.bind("<Return>", lambda _event: self.send_text())
        tk.Button(input_row, text="ENVIAR", command=self.send_text, bg=CYAN_DARK, fg=CYAN,
                  activebackground=CYAN_SOFT, relief="flat", cursor="hand2").pack(side="left", padx=(8, 0), ipady=5)
        self.transcript_window = self.hud.create_window(0, 0, window=self.transcript_frame, state="hidden")

        self.settings_frame = tk.Frame(self.root, bg=PANEL, highlightbackground=CYAN_DARK, highlightthickness=1)
        tk.Label(self.settings_frame, text="PERFIL DE VOZ", bg=PANEL, fg=CYAN,
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=16, pady=(14, 8))
        self.voice_box = ttk.Combobox(self.settings_frame, textvariable=self.voice_name,
                                      state="readonly", style="Jarvis.TCombobox")
        self.voice_box.pack(fill="x", padx=15)
        self.voice_box.bind("<<ComboboxSelected>>", self._change_voice)
        tk.Button(self.settings_frame, text="PROBAR VOZ", command=self._preview_voice,
                  bg=CYAN_DARK, fg=CYAN, activebackground=CYAN_SOFT, relief="flat",
                  cursor="hand2").pack(fill="x", padx=15, pady=12, ipady=5)
        self.settings_window = self.hud.create_window(0, 0, window=self.settings_frame, state="hidden")

        self.mic_button = self._round_button("MIC", self.toggle_listening, 12)
        self.mic_window = self.hud.create_window(0, 0, window=self.mic_button)
        self.log_button = self._nav_button("REGISTRO", self.toggle_transcript)
        self.log_window = self.hud.create_window(0, 0, window=self.log_button)
        self.voice_button = self._nav_button("VOZ", self.toggle_settings)
        self.voice_window = self.hud.create_window(0, 0, window=self.voice_button)
        self.close_button = self._nav_button("SALIR", self.close)
        self.close_window = self.hud.create_window(0, 0, window=self.close_button)
        self.help_button = self._round_button("?", self.show_info)
        self.help_window = self.hud.create_window(0, 0, window=self.help_button)
        self._append("system", "Sistema preparado. Di “Jarvis” para comenzar o escribe un mensaje.")

    def _round_button(self, text, command, size=13):
        return tk.Button(self.root, text=text, command=command, bg=CYAN_DARK, fg=CYAN,
                         activebackground=CYAN_SOFT, activeforeground="white", relief="flat",
                         bd=0, font=("Consolas", size, "bold"), cursor="hand2", width=4, height=2)

    def _nav_button(self, text, command):
        return tk.Button(self.root, text=text, command=command, bg=BG, fg=MUTED,
                         activebackground=CYAN_DARK, activeforeground=CYAN, relief="flat",
                         font=("Consolas", 9, "bold"), cursor="hand2", width=12, height=2)

    def _draw_hud(self):
        width, height = self.hud.winfo_width(), self.hud.winfo_height()
        if width < 10 or height < 10:
            return
        self.hud.delete("hud-shape")
        cx, cy = width / 2, height * .47
        radius = min(width * .25, height * .31)
        self.hud.create_line(20, 40, width-20, 40, fill=CYAN_DARK, tags="hud-shape")
        self.hud.create_line(0, height-92, width, height-92, fill=CYAN_DARK, width=2, tags="hud-shape")
        self.hud.create_rectangle(0, height-91, width, height, fill="#031113", outline="", tags="hud-shape")
        for scale, color, line in ((1.28, "#06292d", 1), (1.08, CYAN_DARK, 3), (.82, CYAN_SOFT, 2), (.55, CYAN, 2)):
            r = radius * scale
            self.hud.create_oval(cx-r, cy-r, cx+r, cy+r, outline=color, width=line, tags="hud-shape")
        for i in range(72):
            a = math.radians(i*5)
            inner, outer = radius*(.9 if i%3 else .84), radius*(1.02 if i%3 else 1.08)
            self.hud.create_line(cx+inner*math.cos(a), cy+inner*math.sin(a),
                                 cx+outer*math.cos(a), cy+outer*math.sin(a),
                                 fill=CYAN_DARK if i%3 else CYAN_SOFT, tags="hud-shape")
        self.hud.create_text(cx, cy-radius*.18, text="VOICE INTERFACE", fill=MUTED,
                             font=("Consolas", 9), tags="hud-shape")
        self.hud.tag_lower("hud-shape")
        for item, xy in ((self.title_window, (width/2, 20)), (self.version_window, (width/2, 44)),
                         (self.status_window, (25, 54)), (self.info_window, (width-48, 70)),
                         (self.help_window, (width-48, height-128)), (self.mic_window, (width/2, height-50)),
                         (self.log_window, (width/2-180, height-47)), (self.voice_window, (width/2+180, height-47)),
                         (self.close_window, (width-100, height-47)), (self.transcript_window, (width-265, height/2)),
                         (self.settings_window, (200, height/2))):
            self.hud.coords(item, *xy)
        self.hud.itemconfigure(self.transcript_window, width=430, height=max(300, height-190))
        self.hud.itemconfigure(self.settings_window, width=320, height=150)

    def _animate(self):
        if not self.root.winfo_exists():
            return
        width, height = self.hud.winfo_width(), self.hud.winfo_height()
        cx, cy = width/2, height*.47
        radius = min(width*.25, height*.31)
        self.hud.delete("animation")
        color = CYAN if self.listening else CYAN_SOFT
        for offset, extent, scale, line in ((0, 52, 1.18, 2), (120, 82, .96, 4), (240, 38, .70, 2)):
            r = radius*scale
            self.hud.create_arc(cx-r, cy-r, cx+r, cy+r, start=self.angle+offset,
                                extent=extent, style="arc", outline=color, width=line, tags="animation")
        pulse_r = radius*(.42+.025*math.sin(self.pulse))
        self.hud.create_oval(cx-pulse_r, cy-pulse_r, cx+pulse_r, cy+pulse_r,
                             outline=color, width=2, tags="animation")
        self.hud.create_text(cx, cy+radius*.18, text="ESCUCHANDO" if self.listening else "EN PAUSA",
                             fill=color, font=("Consolas", 10, "bold"), tags="animation")
        self.angle, self.pulse = (self.angle+(2.2 if self.listening else .6))%360, self.pulse+.18
        self.root.after(50, self._animate)

    def _append(self, role, message):
        labels = {"user": "TÚ", "jarvis": "JARVIS", "system": "SISTEMA"}
        self.transcript.configure(state="normal")
        self.transcript.insert("end", f"{labels[role]}  {message}\n", role)
        self.transcript.configure(state="disabled")
        self.transcript.see("end")

    def _load_voices(self):
        voices = self.voice.list_voices()
        self.voice_ids = {item["name"]: item["id"] for item in voices}
        self.voice_box["values"] = ["JARVIS cinematográfico", "Voz española automática", *self.voice_ids]
        self.voice_name.set("JARVIS cinematográfico")

    def _change_voice(self, _event=None):
        selected = self.voice_name.get()
        if selected == "JARVIS cinematográfico": self.voice.set_profile("cinematic")
        elif selected == "Voz española automática": self.voice.set_profile("spanish")
        else: self.voice.set_profile("custom", self.voice_ids.get(selected))
        self._append("system", f"Voz seleccionada: {selected}.")

    def _preview_voice(self):
        was_listening = self.listening
        self.listening = False
        def preview():
            time.sleep(.4)
            self.voice.speak("Buenas tardes. Soy Jarvis. Todos los sistemas están preparados.")
            self.listening = was_listening
        threading.Thread(target=preview, daemon=True).start()

    def _set_status(self, text, color=CYAN):
        self.status.set(f"LISTENING  {text}")
        self.status_label.configure(fg=color)

    def start_listening(self):
        self.listening = True
        self.mic_button.configure(bg=CYAN_SOFT, fg="white")
        self._set_status("ON")
        if not self.worker or not self.worker.is_alive():
            self.worker = threading.Thread(target=self._voice_loop, daemon=True)
            self.worker.start()

    def toggle_listening(self):
        self.listening = not self.listening
        self.mic_button.configure(bg=CYAN_SOFT if self.listening else CYAN_DARK,
                                  fg="white" if self.listening else CYAN)
        self._set_status("ON" if self.listening else "OFF", CYAN if self.listening else MUTED)
        if self.listening and (not self.worker or not self.worker.is_alive()):
            self.worker = threading.Thread(target=self._voice_loop, daemon=True)
            self.worker.start()

    def toggle_transcript(self):
        current = self.hud.itemcget(self.transcript_window, "state")
        self.hud.itemconfigure(self.transcript_window, state="hidden" if current == "normal" else "normal")

    def toggle_settings(self):
        current = self.hud.itemcget(self.settings_window, "state")
        self.hud.itemconfigure(self.settings_window, state="hidden" if current == "normal" else "normal")

    def show_info(self):
        self.toggle_transcript()
        self._append("system", "MIC activa o pausa la escucha. REGISTRO muestra la conversación. VOZ cambia el perfil.")

    def _voice_loop(self):
        welcome = "Sistema listo. Di Jarvis para activarme."
        self.events.put(("jarvis", welcome))
        self.voice.speak(welcome)
        while not self.stop_event.is_set() and self.conversation.running:
            if not self.listening:
                time.sleep(.1)
                continue
            try: heard = self.voice.listen(timeout=1, phrase_time_limit=12)
            except RuntimeError as exc:
                self.events.put(("error", str(exc)))
                return
            if heard:
                self.events.put(("user", heard))
                response = self.conversation.process_text(heard)
                if response:
                    self.events.put(("jarvis", response))
                    self.voice.speak(response)
        self.events.put(("closed", None))

    def send_text(self):
        message = self.entry.get().strip()
        if not message: return
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
                if event == "user": self._append("user", payload)
                elif event == "jarvis": self._append("jarvis", payload)
                elif event == "error":
                    self._append("system", payload)
                    self._set_status("ERROR", RED)
                elif event == "closed":
                    self.close()
                    return
        except queue.Empty: pass
        self.root.after(100, self._poll_events)

    def close(self):
        self.stop_event.set()
        self.conversation.running = False
        self.root.destroy()

    def run(self): self.root.mainloop()


def main(): JarvisDesktop().run()


if __name__ == "__main__": main()
