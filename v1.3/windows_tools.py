"""Herramientas seguras para Windows.

v1.3 no ejecuta comandos arbitrarios. Solo expone operaciones explícitas.
"""

import os
import platform
import subprocess
from dataclasses import dataclass


@dataclass
class WindowsTools:
    """Acciones de escritorio con límites explícitos."""

    def status(self) -> str:
        return f"Sistema: {platform.system()} {platform.release()}"

    def open_app(self, app: str) -> str:
        """Abre únicamente aplicaciones permitidas por una lista fija."""
        if platform.system() != "Windows":
            return "Esta herramienta requiere Windows."

        allowed = {
            "notepad": ["notepad.exe"],
            "calculadora": ["calc.exe"],
            "calc": ["calc.exe"],
        }
        command = allowed.get(app.lower().strip())
        if not command:
            return "Aplicación no permitida. Usa: notepad, calculadora."

        subprocess.Popen(command, shell=False)
        return f"He abierto {app}."

    def open_folder(self, path: str) -> str:
        """Abre una carpeta existente mediante el explorador de Windows."""
        if platform.system() != "Windows":
            return "Esta herramienta requiere Windows."
        path = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(path):
            return "La carpeta indicada no existe."
        subprocess.Popen(["explorer.exe", path], shell=False)
        return f"He abierto la carpeta: {path}"
