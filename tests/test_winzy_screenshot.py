import pytest
import winzy_screenshot as w

from argparse import Namespace, ArgumentParser

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args([])
    assert result.bbox is None

    result = parser.parse_args(["-b", "0", "10", "20", "50"])
    assert result.bbox == [[0,10,20,50]]

def test_plugin(capsys):
    w.screenshot_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
