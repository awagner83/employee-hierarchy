
from collections import namedtuple

from main import main


MockArgs = namedtuple("MockArgs", "input_file")


def test_main(capsys):

    main(MockArgs("test/fixtures/input.json"))

    actual = capsys.readouterr().out
    expected = str(open('test/fixtures/output').read())

    assert expected == actual


def test_main_empty_input(capsys):

    main(MockArgs("test/fixtures/empty_input.json"))

    actual = capsys.readouterr().out.strip()
    expected = "Total salary: 0"

    assert expected == actual
