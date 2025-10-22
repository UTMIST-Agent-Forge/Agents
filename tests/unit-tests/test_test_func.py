from src.agents.test import test_func


def test_test_func_returns_success():
    assert test_func() == "success"
