#!/usr/bin/env python3

"""
This is the main file containing the task solution.
"""

import json
import re
import sys
from cgi import parse_multipart
from pathlib import Path
from pprint import pprint
from collections import OrderedDict

"""
Notes on the solution: the input format is quite similar to JSON already.
So it would be possible to focus only on adding the wrapping brackets and sorrounding key names in quotes.
I decided to parse it fully to add input validation.
"""


class ParsingError(Exception):
    pass


def main():
    task_A()


def task_A():
    # assumes input is a single line
    line = input()
    parsed = keyvalue_to_dict(line)
    print(dict_to_json(parsed))


def dict_to_json(d: dict) -> str:
    return json.dumps(d)


def keyvalue_to_dict(string: str) -> OrderedDict:
    """Parses a colon-delimtied key-value data into a dict.
    Validates the input.
    """

    result = OrderedDict()

    # regex describing a single key-value pair format
    single_pair_regex = r'[^:\s]+: ".*?(?<!\\)"'

    # validate that the whole input consists only of valid key-value pairs
    input_validation_regex = f"({single_pair_regex})?"
    if re.fullmatch(input_validation_regex, string) is None:
        raise ParsingError("Input is not a well-formed series of key-values")

    pairs = re.findall(single_pair_regex, string)

    # regex for separating the key from the value
    # The quotes are not checked for escape pattern, as the previous regex
    # guarantees the last quote to not be escaped
    parse_pair_regex = re.compile(r'([^:\s]+): "(.*)"$')

    for pair in pairs:
        matched = parse_pair_regex.match(pair)
        if matched is None:
            raise ParsingError(f"Could not separete key from value in string: {pair!r}")

        key, value = matched.groups()
        result[key] = value.replace('\\"', '"')

    return result


if __name__ == "__main__":
    sys.exit(main())
