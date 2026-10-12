from unittest.mock import patch


def test_hud_module_imports():
    with patch("tkinter.Tk"):
        from hud import JarvisHUD
        assert JarvisHUD is not None


def test_desktop_module_imports():
    from jarvis_gui import JarvisDesktop
    assert JarvisDesktop is not None


def test_manual_activation_bypasses_wake_word():
    from unittest.mock import Mock
    from jarvis_gui import JarvisDesktop

    desktop = JarvisDesktop.__new__(JarvisDesktop)
    desktop.conversation = Mock(active=False)
    desktop.start_listening = Mock()
    desktop._append = Mock()
    desktop.activate_conversation()
    assert desktop.conversation.active is True
    desktop.start_listening.assert_called_once_with()
