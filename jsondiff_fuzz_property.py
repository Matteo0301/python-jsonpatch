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

def test_make_apply(x,y):
    patch = make_patch(x,y)
    res = apply_patch(x,patch)
    assert res == y


def test_same_object(x):
    patch = make_patch(x,x)
    assert patch == JsonPatch([])

def test_empty_patch(x):
    patch = JsonPatch([])
    res = apply_patch(x,patch)
    assert res == x

@given(x=binary(),y=json)
def test_properties(x,y):
    try:
        object = load(x)
    except:
        print("Invalid string")
        return
    test_make_apply(object,y)
    test_same_object(object)
    test_empty_patch(object)


if __name__ == "__main__":
    afl.init()
    data = sys.stdin.buffer.read()
    print(test_properties.hypothesis.fuzz_one_input(data))