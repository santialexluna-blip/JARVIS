from pathlib import Path


def test_launcher_uses_delayed_expansion_for_ollama_inside_block():
    launcher = Path("JARVIS.bat").read_text(encoding="utf-8")
    assert "EnableDelayedExpansion" in launcher
    assert '"!OLLAMA_EXE!" pull qwen3:4b' in launcher
    assert 'start "" /min "!OLLAMA_EXE!" serve' in launcher
