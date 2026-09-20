from ai import DemoProvider


def answer(text):
    return DemoProvider().reply([{"role": "user", "content": text}])


def test_answers_identity_question():
    assert answer("¿Quién eres?") == "Soy Jarvis, tu asistente personal."


def test_answers_known_fact():
    assert answer("¿Cuál es la capital de México?") == "La capital de México es la Ciudad de México."


def test_calculates_arithmetic_safely():
    assert answer("¿Cuánto es 204 + 85 + 150?") == "El resultado es 439."


def test_calculates_numbers_spoken_in_spanish():
    question = "¿Cuánto es doscientos cuatro más ochenta y cinco más ciento cincuenta?"
    assert answer(question) == "El resultado es 439."


def test_calculates_mixed_spoken_and_numeric_values():
    assert answer("¿Cuánto es 204 más ochenta y cinco?") == "El resultado es 289."


def test_calculates_transcription_with_polite_prefix_and_symbols():
    assert answer("dime Cuánto es 200 + 80") == "El resultado es 280."


def test_unknown_answer_does_not_hallucinate():
    assert "no conozco" in answer("¿Quién ganará mañana?")
