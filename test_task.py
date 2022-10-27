from task import keyvalue_to_dict


def test_keyvalue_parsing():
    assert keyvalue_to_dict(r'time: "12:34:56"') == {"time": "12:34:56"}


def test_colon_space_in_value():
    assert keyvalue_to_dict(r'time: "not_a_key: not a value"') == {
        "time": "not_a_key: not a value"
    }
