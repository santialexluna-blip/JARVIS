"""HUD de escritorio ligero para JARVIS v2.1 usando Tkinter."""

import tkinter as tk


class JarvisHUD:
    def __init__(self, title: str = "JARVIS v2.1"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("700x420")
        self.root.minsize(520, 320)

        self.status = tk.StringVar(value="EN ESPERA")
        self.output = tk.StringVar(value="JARVIS listo.")

        tk.Label(self.root, text="JARVIS", font=("Segoe UI", 28, "bold")).pack(pady=(24, 4))
        tk.Label(self.root, textvariable=self.status, font=("Segoe UI", 11)).pack()
        tk.Label(
            self.root,
            textvariable=self.output,
            wraplength=620,
            justify="left",
            font=("Segoe UI", 13),
        ).pack(fill="both", expand=True, padx=40, pady=30)

        self.entry = tk.Entry(self.root, font=("Segoe UI", 12))
        self.entry.pack(fill="x", padx=40, pady=(0, 10))
        self.entry.bind("<Return>", lambda _event: self.submit())
        tk.Button(self.root, text="Enviar", command=self.submit).pack(pady=(0, 20))

        self.handler = None

    def set_handler(self, handler):
        self.handler = handler

    def submit(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, tk.END)
        self.status.set("PROCESANDO")
        try:
            result = self.handler(text) if self.handler else "Sin asistente conectado."
            self.output.set(result)
            self.status.set("LISTO")
        except Exception as exc:
            self.output.set(f"Error: {exc}")
            self.status.set("ERROR")

    def run(self):
        self.root.mainloop()
