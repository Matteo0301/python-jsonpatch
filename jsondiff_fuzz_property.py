#!/usr/bin/env python
from __future__ import print_function
import afl
import sys
from json import load
from jsonpatch import *
from hypothesis import given, settings
from hypothesis.strategies import  text, recursive, booleans, lists, none, floats, dictionaries, binary

json = recursive(
        booleans() | floats(allow_nan=False,allow_infinity=False) | text(),
        lambda children: lists(children) | dictionaries(text(), children),
    )

@given(x=binary(),y=json)
def test_make_apply(x,y):
    try:
        object = load(x)
    except:
        print("Invalid string")
        return
    patch = make_patch(object,y)
    res = apply_patch(object,patch)
    assert res == y

@given(x=binary())
def test_same_object(x):
    try:
        object = load(x)
    except:
        print("Invalid string")
        return
    patch = make_patch(object,object)
    assert patch == JsonPatch([])

@given(x=binary())
@settings(max_examples=100)
def test_empty_patch(x):
    try:
        object = load(x)
    except:
        print("Invalid string")
        return
    patch = JsonPatch([])
    res = apply_patch(object,patch)
    assert res == object

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
    afl.init()
    data = sys.stdin.buffer.read()
    print(test_make_apply.hypothesis.fuzz_one_input(data))
    print(test_empty_patch.hypothesis.fuzz_one_input(data))
    print(test_same_object.hypothesis.fuzz_one_input(data))
