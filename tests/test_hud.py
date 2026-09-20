from unittest.mock import patch


def test_hud_module_imports():
    with patch("tkinter.Tk"):
        from hud import JarvisHUD
        assert JarvisHUD is not None


def test_desktop_module_imports():
    from jarvis_gui import JarvisDesktop
    assert JarvisDesktop is not None
