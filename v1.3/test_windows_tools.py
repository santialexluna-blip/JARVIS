from unittest.mock import patch

from windows_tools import WindowsTools


def test_status():
    result = WindowsTools().status()
    assert "Sistema:" in result


def test_unknown_app_is_rejected():
    with patch("windows_tools.platform.system", return_value="Windows"):
        result = WindowsTools().open_app("cmd")
    assert "no permitida" in result
