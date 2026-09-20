from abc import ABC, abstractmethod
import ast
import datetime as dt
import operator
import re
import unicodedata

class AIProvider(ABC):
    @abstractmethod
    def reply(self, messages):
        raise NotImplementedError

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

    @staticmethod
    def _normalized(text):
        return "".join(
            char for char in unicodedata.normalize("NFD", text.lower())
            if unicodedata.category(char) != "Mn"
        ).strip(" ¿?¡!.,")

    @classmethod
    def _calculate(cls, expression):
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
