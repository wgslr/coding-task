import pytest
from collections import OrderedDict
from task import ParsingError, keyvalue_to_dict


def test_keyvalue_parsing():
    assert keyvalue_to_dict(r'time: "12:34:56"') == {"time": "12:34:56"}


def test_colon_space_in_value():
    assert keyvalue_to_dict(r'key: "not_a_key: not a value"') == {
        "key": "not_a_key: not a value"
    }


def test_escaping():
    assert keyvalue_to_dict(r'key: "not_a_key: \"not a value\""') == {
        "key": 'not_a_key: "not a value"'
    }


def test_ordering():
    assert keyvalue_to_dict(r'key0: "value0", key1: "value1"') == OrderedDict(
        (
            ("key0", "value0"),
            ("key1", "value1"),
        )
    )
    assert keyvalue_to_dict(r'key1: "value1", key0: "value0"') == OrderedDict(
        (
            ("key1", "value1"),
            ("key0", "value0"),
        )
    )


def test_invalid_input_is_rejected():
    with pytest.raises(ParsingError):
        keyvalue_to_dict(r'key: "value" dangling')

    with pytest.raises(ParsingError):
        keyvalue_to_dict(r"key: unqouted")
