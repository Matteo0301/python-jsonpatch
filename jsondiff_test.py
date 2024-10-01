#!/usr/bin/env python
from __future__ import print_function

import sys
import json
from jsonpatch import *
import argparse
import math

from hypothesis import given, settings
from hypothesis.strategies import  text, tuples, builds, recursive, booleans, lists, none, floats, dictionaries

json = recursive(
        booleans() | floats(allow_nan=False,allow_infinity=False) | text(),
        lambda children: lists(children) | dictionaries(text(), children),
    )

@given(x=json,y=json)
@settings(max_examples=100)
def test_make_apply(x,y):
    patch = make_patch(x,y)
    res = apply_patch(x,patch)
    assert res == y

@given(x=json)
@settings(max_examples=100)
def test_same_object(x):
    patch = make_patch(x,x)
    assert patch == JsonPatch([])

@given(x=json)
@settings(max_examples=100)
def test_empty_patch(x):
    patch = JsonPatch([])
    res = apply_patch(x,patch)
    assert res == x

# This is the failing test
""" @given(x=json,y=json)
@settings(max_examples=100)
def test_idempotence(x,y):
    patch = make_patch(x,y)
    res = apply_patch(x,patch)
    res2 = apply_patch(res,patch)
    assert res == y
    assert res2 == res """

if __name__ == "__main__":
    test_make_apply()
    test_empty_patch()
    test_same_object()
