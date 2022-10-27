#!/usr/bin/env python3

"""
This is the main file containing the task solution.
"""

import bisect
import json
import re
import sys
from cgi import parse_multipart
from pathlib import Path
from pprint import pprint
from collections import OrderedDict
from typing import List

"""
Notes on the solution

Part A
I strived to implement input validation and raise errors on inputs not matching
the described format.  Based on the input example, I assumed that key values
must not contain whitespace.

I have decided to gather the input into a in-memory dict for later manipulation.
It allows using a well-tested JSON-encoding library for output and makes it
easier to write separate unit tests for parsing and encoding.

An alternative solution would be to transcode the input in a streaming fashion,
item by item, to avoid holding the whole event in memory. It is made easier by
the fact that the quoted value format is already compliant with JSON.


Part B
My first step was to decode the hint, which I did using the shell `base64 -d`
command.  It says "Hello, try XOR with 0x17F"

I tried inspecting the binary representation of the numbers before and after XOR
operation. I used the python shell:
```
>>> to_bin = lambda v: f'{v:016b}'
>>> vals = [0x154,  0x150, 0x14a, 0x144]
>>> xored = [(v ^ 0x17f) for v in vals]
>>> xored
[43, 47, 53, 59]
>>> [to_bin(v) for v in vals]
['0000000101010100', '0000000101010000', '0000000101001010', '0000000101000100']
>>> [to_bin(v) for v in xored]
['0000000000101011', '0000000000101111', '0000000000110101', '0000000000111011']
```

I did not observe a convincing pattern in the bit values. Then, I noticed that
the numbers are consecutive primes. Thus, the next number following the pattern
will be the next prime, 61. The code below replicates this reasoning. To obtain
the value for 'five', I need to reverse the xor (that is, once again perform XOR
0x17f) and convert the number to hexadecimal representation.

I hardcoded the prime numbers under 100, as they are well known. It would be
also possible to obtain the new value programmatically, for example by checking
each value larger than 59 with the Fermat probability test.
"""


XOR_PATTERN = 0x17F

PRIMES_UNDER_100 = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
]


class ParsingError(Exception):
    pass


def main():
    event = task_A()
    task_B(event)


def task_A():
    print("part A:")
    # assumes input is a single line
    line = input()
    parsed = keyvalue_to_dict(line)
    print(dict_to_json(parsed))

    return parsed


def task_B(original_event: OrderedDict):
    print("\npart B:")

    # The numbers in the original event are contiguous prime numbers.
    # Append a field 'five' with the next prime number.

    prev_prime = int(original_event["four"], 16) ^ XOR_PATTERN
    next_prime = find_first_prime_larger_than(prev_prime)

    # reverse the operations needed to obtain the prime series
    next_prime_xored = next_prime ^ XOR_PATTERN
    next_value = hex(next_prime_xored)

    # append obtained value to the original event
    new_event = OrderedDict((*original_event.items(), ("five", next_value)))
    serialized = dict_to_keyvalue(new_event)
    print(serialized)


def find_first_prime_larger_than(p: int) -> int:
    """Finds the next prime after given. Works for numbers < 100"""
    i = bisect.bisect_right(PRIMES_UNDER_100, p)
    return PRIMES_UNDER_100[i]


def dict_to_json(d: dict) -> str:
    """Encodes a dict as a JSON string"""
    return json.dumps(d)


def keyvalue_to_dict(string: str) -> OrderedDict:
    """Parses a key-value series into a dict.
    Raises `ParsingError` if the input format is invalid.
    Assumes that keys do not contain whitespace.
    """

    result = OrderedDict()

    remainder = string.strip()
    try:
        while remainder != "":
            key, remainder = remainder.split(": ", 1)

            # if there are multiple strings delimited by whitespace
            # before the next ': ', the input must be invalid
            if re.search("\s", key):
                raise ParsingError(f"Invalid key: {key!r}")

            if remainder[0] != '"':
                raise ParsingError("Value must start with a quote")
            # omit the leading "
            remainder = remainder[1:]

            value, remainder = re.split(r'(?<!\\)"', remainder, 1)

            # unescape quotes and store the result
            result[key] = value.replace('\\"', '"')

            if remainder != "" and remainder[0] != " ":
                # there must be a space between key-value items
                raise ParsingError("There must be a space after a closing quote")
            remainder = remainder.strip()

    except ValueError as e:
        # handles split() calls returning too few items
        raise ParsingError("Input is not a well-formed key-value series") from e

    return result


def dict_to_keyvalue(d: dict) -> str:
    return " ".join(f'{key}: "{escape_value(value)}"' for key, value in d.items())


def escape_value(s: str) -> str:
    return s.replace('"', r"\"")


if __name__ == "__main__":
    sys.exit(main())
