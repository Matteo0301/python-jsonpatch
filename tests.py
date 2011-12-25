#!/usr/bin/env python
# -*- coding: utf-8 -*-

import doctest
import unittest
import jsonpatch


class ApplyPatchTestCase(unittest.TestCase):

    def test_add_object_key(self):
        obj = {'foo': 'bar'}
        jsonpatch.apply_patch(obj, [{'add': '/baz', 'value': 'qux'}])
        self.assertTrue('baz' in obj)
        self.assertEqual(obj['baz'], 'qux')

    def test_add_array_item(self):
        obj = {'foo': ['bar', 'baz']}
        jsonpatch.apply_patch(obj, [{'add': '/foo/1', 'value': 'qux'}])
        self.assertEqual(obj['foo'], ['bar', 'qux', 'baz'])

    def test_remove_object_key(self):
        obj = {'foo': 'bar', 'baz': 'qux'}
        jsonpatch.apply_patch(obj, [{'remove': '/baz'}])
        self.assertTrue('baz' not in obj)

    def test_remove_array_item(self):
        obj = {'foo': ['bar', 'qux', 'baz']}
        jsonpatch.apply_patch(obj, [{'remove': '/foo/1'}])
        self.assertEqual(obj['foo'], ['bar', 'baz'])

    def test_replace_object_key(self):
        obj = {'foo': 'bar', 'baz': 'qux'}
        jsonpatch.apply_patch(obj, [{'replace': '/baz', 'value': 'boo'}])
        self.assertTrue(obj['baz'], 'boo')

    def test_replace_array_item(self):
        obj = {'foo': ['bar', 'qux', 'baz']}
        jsonpatch.apply_patch(obj, [{'replace': '/foo/1', 'value': 'boo'}])
        self.assertEqual(obj['foo'], ['bar', 'boo', 'baz'])

    def test_move_object_key(self):
        obj = {'foo': {'bar': 'baz', 'waldo': 'fred'},
               'qux': {'corge': 'grault'}}
        jsonpatch.apply_patch(obj, [{'move': '/foo/waldo', 'to': '/qux/thud'}])
        self.assertEqual(obj, {'qux': {'thud': 'fred', 'corge': 'grault'},
                               'foo': {'bar': 'baz'}})

    def test_move_array_item(self):
        obj =  {'foo': ['all', 'grass', 'cows', 'eat']}
        jsonpatch.apply_patch(obj, [{'move': '/foo/1', 'to': '/foo/3'}])
        self.assertEqual(obj, {'foo': ['all', 'cows', 'eat', 'grass']})

    def test_test_success(self):
        obj =  {'baz': 'qux', 'foo': ['a', 2, 'c']}
        jsonpatch.apply_patch(obj, [{'test': '/baz', 'value': 'qux'},
                                    {'test': '/foo/1', 'value': 2}])

    def test_test_error(self):
        obj =  {'bar': 'qux'}
        self.assertRaises(AssertionError,
                          jsonpatch.apply_patch,
                          obj, [{'test': '/bar', 'value': 'bar'}])


class MakePatchTestCase(unittest.TestCase):

    def test_objects(self):
        src = {'foo': 'bar', 'boo': 'qux'}
        dst = {'baz': 'qux', 'foo': 'boo'}
        patch = jsonpatch.make_patch(src, dst)
        patch.apply(src)
        self.assertEqual(src, dst)

    def test_arrays(self):
        src = {'numbers': [1, 2, 3], 'other': [1, 3, 4, 5]}
        dst = {'numbers': [1, 3, 4, 5], 'other': [1, 3, 4]}
        patch = jsonpatch.make_patch(src, dst)
        patch.apply(src)
        self.assertEqual(src, dst)

    def test_complex_object(self):
        src = {'data': [
            {'foo': 1}, {'bar': [1, 2, 3]}, {'baz': {'1': 1, '2': 2}}
        ]}
        dst = {'data': [
            {'foo': [42]}, {'bar': []}, {'baz': {'boo': 'oom!'}}
        ]}
        patch = jsonpatch.make_patch(src, dst)
        patch.apply(src)
        self.assertEqual(src, dst)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite(jsonpatch))
    suite.addTest(unittest.makeSuite(ApplyPatchTestCase))
    suite.addTest(unittest.makeSuite(MakePatchTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
