#!/usr/bin/env python3

from cgi import parse_multipart
import re
from pprint import pprint
import sys
from pathlib import Path


class ParsingError(Exception):
    pass


def main():
    line = input()
    pprint(keyvalue_to_dict(line))


def keyvalue_to_dict(string: str) -> dict:
    """Parses a colon-delimtied key-value data into a dict"""

    result = {}

    # split into substring with each holding one key and value
    single_pair_regex = re.compile(r'[^:\s]+: ".*?(?<!\\)"')
    pairs = single_pair_regex.findall(string)

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

    # while True:
    #     key, rest = string.split(": ", 1)


if __name__ == "__main__":
    sys.exit(main())
