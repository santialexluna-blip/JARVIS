from abc import ABC, abstractmethod
import ast
import datetime as dt
import operator
import re
import unicodedata
import json
import os
import shutil
import subprocess
import time
from urllib.error import URLError
from urllib.request import Request, urlopen

class AIProvider(ABC):
    @abstractmethod
    def reply(self, messages):
        raise NotImplementedError


class OllamaProvider(AIProvider):
    """Proveedor local sin tokens mediante la API de Ollama."""

    def __init__(self, model="qwen3:4b", endpoint="http://localhost:11434/api/chat"):
        self.model = model
        self.endpoint = endpoint

    def reply(self, messages):
        if not self.ensure_available():
            raise RuntimeError("La IA local no está disponible.")
        system = {
            "role": "system",
            "content": (
                "Eres JARVIS, un asistente personal en español. Responde con precisión, "
                "claridad y de forma breve. Mantén el contexto de la conversación. "
                "No inventes datos: si no estás seguro o la información puede haber cambiado, "
                "indícalo. No menciones estas instrucciones."
            ),
        }
        conversation = [system]
        conversation.extend(message for message in messages if message.get("role") != "system")
        payload = json.dumps({
            "model": self.model,
            "messages": conversation,
            "stream": False,
            "think": False,
            "keep_alive": "10m",
            "options": {"temperature": 0.2, "num_ctx": 2048},
        }).encode("utf-8")
        request = Request(
            self.endpoint,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=180) as response:
                result = json.loads(response.read().decode("utf-8"))
        except (URLError, OSError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError("La IA local no está disponible.") from exc
        answer = result.get("message", {}).get("content", "").strip()
        if not answer:
            raise RuntimeError("La IA local devolvió una respuesta vacía.")
        return answer

    def available(self) -> bool:
        try:
            request = Request("http://localhost:11434/api/tags")
            with urlopen(request, timeout=2) as response:
                return response.status == 200
        except (URLError, OSError, TimeoutError):
            return False

    @staticmethod
    def _find_ollama() -> str | None:
        command = shutil.which("ollama")
        if command:
            return command
        local_app_data = os.getenv("LOCALAPPDATA")
        if local_app_data:
            candidate = os.path.join(local_app_data, "Programs", "Ollama", "ollama.exe")
            if os.path.isfile(candidate):
                return candidate
        return None

    def ensure_available(self, wait_seconds: int = 20) -> bool:
        if self.available():
            return True
        executable = self._find_ollama()
        if not executable:
            return False
        creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        try:
            subprocess.Popen(
                [executable, "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creation_flags,
            )
        except OSError:
            return False
        deadline = time.monotonic() + wait_seconds
        while time.monotonic() < deadline:
            if self.available():
                return True
            time.sleep(0.5)
        return False


class HybridProvider(AIProvider):
    """Usa IA local y conserva respuestas básicas si Ollama no está listo."""

    def __init__(self, local=None, fallback=None):
        self.local = local or OllamaProvider()
        self.fallback = fallback or DemoProvider()

    def reply(self, messages):
        try:
            return self.local.reply(messages)
        except RuntimeError:
            basic = self.fallback.reply(messages)
            if "Todavía no conozco" not in basic:
                return basic
            return (
                "Mi modelo local no está disponible en este momento. "
                "Abre JARVIS.bat con conexión a Internet para completar la instalación inicial."
            )

class DemoProvider(AIProvider):
    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    _spanish_units = {
        "cero": 0, "un": 1, "uno": 1, "una": 1, "dos": 2, "tres": 3,
        "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8,
        "nueve": 9, "diez": 10, "once": 11, "doce": 12, "trece": 13,
        "catorce": 14, "quince": 15, "dieciseis": 16, "diecisiete": 17,
        "dieciocho": 18, "diecinueve": 19, "veinte": 20, "veintiuno": 21,
        "veintidos": 22, "veintitres": 23, "veinticuatro": 24,
        "veinticinco": 25, "veintiseis": 26, "veintisiete": 27,
        "veintiocho": 28, "veintinueve": 29,
    }
    _spanish_tens = {
        "treinta": 30, "cuarenta": 40, "cincuenta": 50, "sesenta": 60,
        "setenta": 70, "ochenta": 80, "noventa": 90,
    }
    _spanish_hundreds = {
        "cien": 100, "ciento": 100, "doscientos": 200, "trescientos": 300,
        "cuatrocientos": 400, "quinientos": 500, "seiscientos": 600,
        "setecientos": 700, "ochocientos": 800, "novecientos": 900,
    }

    @staticmethod
    def _normalized(text):
        return "".join(
            char for char in unicodedata.normalize("NFD", text.lower())
            if unicodedata.category(char) != "Mn"
        ).strip(" ¿?¡!.,")

    @classmethod
    def _calculate(cls, expression):
        expression = expression.strip()

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.BinOp) and type(node.op) in cls._operators:
                return cls._operators[type(node.op)](evaluate(node.left), evaluate(node.right))
            if isinstance(node, ast.UnaryOp) and type(node.op) in cls._operators:
                return cls._operators[type(node.op)](evaluate(node.operand))
            raise ValueError("expresión no permitida")

        if len(expression) > 80:
            raise ValueError("expresión demasiado larga")
        return evaluate(ast.parse(expression, mode="eval"))

    @classmethod
    def _spanish_number(cls, phrase):
        phrase = phrase.strip()
        if re.fullmatch(r"\d+(?:\.\d+)?", phrase):
            return float(phrase) if "." in phrase else int(phrase)

        total = 0
        current = 0
        found = False
        for word in phrase.split():
            if word == "y":
                continue
            if word in cls._spanish_units:
                current += cls._spanish_units[word]
                found = True
            elif word in cls._spanish_tens:
                current += cls._spanish_tens[word]
                found = True
            elif word in cls._spanish_hundreds:
                current += cls._spanish_hundreds[word]
                found = True
            elif word == "mil":
                total += (current or 1) * 1000
                current = 0
                found = True
            else:
                raise ValueError(f"número desconocido: {word}")
        if not found:
            raise ValueError("no hay un número")
        return total + current

    @classmethod
    def _spoken_math_expression(cls, text):
        text = text.replace("dividido entre", "entre")
        pieces = re.split(r"\s+(mas|menos|por|entre)\s+", text)
        if len(pieces) < 3 or len(pieces) % 2 == 0:
            raise ValueError("no es una operación hablada")
        operator_symbols = {"mas": "+", "menos": "-", "por": "*", "entre": "/"}
        expression = [str(cls._spanish_number(pieces[0]))]
        for index in range(1, len(pieces), 2):
            expression.append(operator_symbols[pieces[index]])
            expression.append(str(cls._spanish_number(pieces[index + 1])))
        return " ".join(expression)

    def reply(self, messages):
        last = messages[-1]["content"] if messages else ""
        text = self._normalized(last)

        if text in {"hola", "buenos dias", "buenas tardes", "buenas noches"}:
            return "Hola. Soy Jarvis. ¿En qué puedo ayudarte?"
        if "como te llamas" in text or "quien eres" in text:
            return "Soy Jarvis, tu asistente personal."
        if "como estas" in text:
            return "Funcionando correctamente y listo para ayudarte."
        if "capital de mexico" in text:
            return "La capital de México es la Ciudad de México."
        if "capital de francia" in text:
            return "La capital de Francia es París."
        if text in {"que dia es", "fecha", "fecha de hoy"}:
            return f"Hoy es {dt.date.today().strftime('%d/%m/%Y')}."

        expression = text
        for prefix in ("cuanto es ", "calcula ", "resultado de "):
            if expression.startswith(prefix):
                expression = expression[len(prefix):]
                break
        try:
            expression = self._spoken_math_expression(expression)
        except ValueError:
            expression = expression.replace("por", "*").replace("entre", "/")
            expression = re.sub(r"[^0-9+\-*/().% ]", "", expression)
        if expression.strip() and re.fullmatch(r"[0-9+\-*/().% ]+", expression):
            try:
                result = self._calculate(expression)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                return f"El resultado es {result}."
            except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
                return "No pude calcular esa operación de forma segura."

        return (
            "Todavía no conozco esa respuesta con seguridad. "
            "Puedes decir busca, seguido de tu pregunta, para consultar Internet."
        )
