#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import json
import sys

from dominter.dom import Window, start_app, Style
import dominter.dom as domdom


def ispymaj(v):
    return sys.version_info.major == v

class TestDominter(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDominter, self).__init__(*args, **kwargs)
        self.hl_return_val = True
        self.hl_return_pop = 'pop return'
        self.hl_add_elm = None
        self.hl_extend_lst = None
        self.hl_insert_idx = None
        self.hl_insert_elm = None
        self.hl_remove_elm = None
        self.hl_pop_idx = None
        self.hl_setitem_idx =None
        self.hl_setitem_value = None
        self.hl_delitem_idx = None
        self.hl_reverse_cnt = 0
        self.hl_sort_cnt = 0
        self.hl_sort_key = None
        self.hl_sort_reverse = None
        self.hl_clear_cnt = 0

    def hl_add_hook(self, elm):
        self.hl_add_elm = elm
        return self.hl_return_val

    def hl_extend_hook(self, lst):
        self.hl_extend_lst = lst
        return self.hl_return_val

    def hl_inserted_hook(self, idx, elm):
        self.hl_insert_idx = idx
        self.hl_insert_elm = elm
        return self.hl_return_val

    def hl_remove_hook(self, elm):
        self.hl_remove_elm = elm
        return self.hl_return_val

    def hl_pop_hook(self, idx):
        self.hl_pop_idx = idx
        return self.hl_return_val, self.hl_return_pop

    def hl_setitem_hook(self, idx, value):
        self.hl_setitem_idx = idx
        self.hl_setitem_value = value
        return self.hl_return_val

    def hl_delitem_hook(self, idx):
        self.hl_delitem_idx = idx
        return self.hl_return_val

    def hl_reverse_hook(self):
        self.hl_reverse_cnt += 1
        return self.hl_return_val

    def hl_sort_hook(self, key, reverse):
        self.hl_sort_cnt += 1
        self.hl_sort_key = key
        self.hl_sort_reverse = reverse
        return self.hl_return_val

    def hl_clear_hook(self):
        self.hl_clear_cnt += 1
        return self.hl_return_val

    def test_HookList(self):
        hl = domdom.HookList(init_val=None,
                             append_hook=self.hl_add_hook,
                             extend_hook=self.hl_extend_hook,
                             insert_hook=self.hl_inserted_hook,
                             remove_hook=self.hl_remove_hook,
                             pop_hook=self.hl_pop_hook,
                             setitem_hook=self.hl_setitem_hook,
                             delitem_hook=self.hl_delitem_hook,
                             reverse_hook=self.hl_reverse_hook,
                             sort_hook=self.hl_sort_hook,
                             clear_hook=self.hl_clear_hook, )
        # append
        self.hl_return_val = True
        hl._raw_append('test1')
        self.assertEqual(self.hl_add_elm, None)
        hl.append('test2')
        self.assertEqual(self.hl_add_elm, 'test2')
        self.assertEqual(hl, ['test1', 'test2'])
        self.hl_return_val = False
        hl.append('test3')
        self.assertEqual(self.hl_add_elm, 'test3')
        self.assertEqual(hl, ['test1', 'test2'])

        # add
        hl.add('test4')
        self.assertEqual(self.hl_add_elm, 'test4')
        self.assertEqual(hl, ['test1', 'test2'])
        self.hl_return_val = True
        hl.add('test5')
        self.assertEqual(self.hl_add_elm, 'test5')
        self.assertEqual(hl, ['test1', 'test2', 'test5'])

        # extend
        hl._raw_extend(['test6', 'test7'])
        self.assertEqual(self.hl_extend_lst, None)
        self.assertEqual(hl, ['test1', 'test2', 'test5', 'test6', 'test7'])
        hl.extend(['test8', ])
        self.assertEqual(self.hl_extend_lst, ['test8', ])
        self.assertEqual(hl, ['test1', 'test2', 'test5', 'test6', 'test7', 'test8'])
        self.hl_return_val = False
        hl.extend(['test9', 'test10', 'test11', ])
        self.assertEqual(self.hl_extend_lst, ['test9', 'test10', 'test11', ])
        self.assertEqual(hl, ['test1', 'test2', 'test5', 'test6', 'test7', 'test8'])

        # insert
        hl._raw_insert(1, 'test1.5')
        self.assertEqual(self.hl_insert_idx, None)
        self.assertEqual(self.hl_insert_elm, None)
        self.assertEqual(hl, ['test1', 'test1.5', 'test2', 'test5', 'test6', 'test7', 'test8'])
        hl.insert(2, 'test1.8')
        self.assertEqual(self.hl_insert_idx, 2)
        self.assertEqual(self.hl_insert_elm, 'test1.8')
        self.assertEqual(hl, ['test1', 'test1.5', 'test2', 'test5', 'test6', 'test7', 'test8'])
        self.hl_return_val = True
        hl.insert(0, 'test0.5')
        self.assertEqual(self.hl_insert_idx, 0)
        self.assertEqual(self.hl_insert_elm, 'test0.5')
        self.assertEqual(hl, ['test0.5', 'test1', 'test1.5', 'test2', 'test5', 'test6', 'test7', 'test8'])

        # remove
        hl._raw_remove('test8')
        self.assertEqual(self.hl_remove_elm, None)
        self.assertEqual(hl, ['test0.5', 'test1', 'test1.5', 'test2', 'test5', 'test6', 'test7', ])
        hl.remove('test1')
        self.assertEqual(self.hl_remove_elm, 'test1')
        self.assertEqual(hl, ['test0.5', 'test1.5', 'test2', 'test5', 'test6', 'test7', ])
        self.hl_return_val = False
        hl.remove('test2')
        self.assertEqual(self.hl_remove_elm, 'test2')
        self.assertEqual(hl, ['test0.5', 'test1.5', 'test2', 'test5', 'test6', 'test7', ])

        # pop
        elm = hl._raw_pop(2)
        self.assertEqual(elm, 'test2')
        self.assertEqual(self.hl_pop_idx, None)
        self.assertEqual(hl, ['test0.5', 'test1.5', 'test5', 'test6', 'test7', ])
        elm = hl.pop(0)
        self.assertEqual(elm, self.hl_return_pop)
        self.assertEqual(self.hl_pop_idx, 0)
        self.assertEqual(hl, ['test0.5', 'test1.5', 'test5', 'test6', 'test7', ])
        self.hl_return_val = True
        elm = hl.pop(3)
        self.assertEqual(elm, 'test6')
        self.assertEqual(self.hl_pop_idx, 3)
        self.assertEqual(hl, ['test0.5', 'test1.5', 'test5', 'test7', ])

        # delitem
        hl._raw_delitem(3)
        self.assertEqual(self.hl_delitem_idx, None)
        self.assertEqual(hl, ['test0.5', 'test1.5', 'test5', ])
        del hl[1]
        self.assertEqual(self.hl_delitem_idx, 1)
        self.assertEqual(hl, ['test0.5', 'test5', ])
        hl.extend(['test6', 'test7', 'test8', 'test9'])
        del hl[0:3]
        self.assertEqual(self.hl_delitem_idx, slice(0, 3, None))
        self.assertEqual(hl, ['test7', 'test8', 'test9'])
        self.hl_return_val = False
        del hl[1]
        self.assertEqual(self.hl_delitem_idx, 1)
        self.assertEqual(hl, ['test7', 'test8', 'test9'])
        del hl[0:3]
        self.assertEqual(self.hl_delitem_idx, slice(0, 3, None))
        self.assertEqual(hl, ['test7', 'test8', 'test9'])

        # reverse
        hl._raw_reverse()
        self.assertEqual(self.hl_reverse_cnt, 0)
        self.assertEqual(hl, ['test9', 'test8', 'test7'])
        hl.reverse()
        self.assertEqual(self.hl_reverse_cnt, 1)
        self.assertEqual(hl, ['test9', 'test8', 'test7'])
        self.hl_return_val = True
        hl.reverse()
        self.assertEqual(self.hl_reverse_cnt, 2)
        self.assertEqual(hl, ['test7', 'test8', 'test9'])

        # sort
        hl.extend(['test2', 'Test4', 'Test3'])
        hl._raw_sort(reverse=True)
        self.assertEqual(self.hl_sort_cnt, 0)
        self.assertEqual(self.hl_sort_key, None)
        self.assertEqual(self.hl_sort_reverse, None)
        self.assertEqual(hl, ['test9', 'test8', 'test7', 'test2', 'Test4', 'Test3'])
        hl._raw_sort()
        self.assertEqual(self.hl_sort_cnt, 0)
        self.assertEqual(self.hl_sort_key, None)
        self.assertEqual(self.hl_sort_reverse, None)
        self.assertEqual(hl, ['Test3', 'Test4', 'test2', 'test7', 'test8', 'test9'])
        hl._raw_sort(key=str.lower)
        self.assertEqual(self.hl_sort_cnt, 0)
        self.assertEqual(self.hl_sort_key, None)
        self.assertEqual(self.hl_sort_reverse, None)
        self.assertEqual(hl, ['test2', 'Test3', 'Test4', 'test7', 'test8', 'test9'])
        hl.sort(reverse=True)
        self.assertEqual(self.hl_sort_cnt, 1)
        self.assertEqual(self.hl_sort_key, None)
        self.assertEqual(self.hl_sort_reverse, True)
        self.assertEqual(hl, ['test9', 'test8', 'test7', 'test2', 'Test4', 'Test3'])
        hl.sort()
        self.assertEqual(self.hl_sort_cnt, 2)
        self.assertEqual(self.hl_sort_key, None)
        self.assertEqual(self.hl_sort_reverse, False)
        self.assertEqual(hl, ['Test3', 'Test4', 'test2', 'test7', 'test8', 'test9'])
        hl.sort(key=str.lower)
        self.assertEqual(self.hl_sort_cnt, 3)
        self.assertEqual(self.hl_sort_key, str.lower)
        self.assertEqual(self.hl_sort_reverse, False)
        self.assertEqual(hl, ['test2', 'Test3', 'Test4', 'test7', 'test8', 'test9'])
        self.hl_return_val = False
        hl.sort(reverse=True)
        self.assertEqual(self.hl_sort_cnt, 4)
        self.assertEqual(self.hl_sort_key, None)
        self.assertEqual(self.hl_sort_reverse, True)
        self.assertEqual(hl, ['test2', 'Test3', 'Test4', 'test7', 'test8', 'test9'])
        hl.sort()
        self.assertEqual(self.hl_sort_cnt, 5)
        self.assertEqual(self.hl_sort_key, None)
        self.assertEqual(self.hl_sort_reverse, False)
        self.assertEqual(hl, ['test2', 'Test3', 'Test4', 'test7', 'test8', 'test9'])
        hl.sort(key=str.lower)
        self.assertEqual(self.hl_sort_cnt, 6)
        self.assertEqual(self.hl_sort_key, str.lower)
        self.assertEqual(self.hl_sort_reverse, False)
        self.assertEqual(hl, ['test2', 'Test3', 'Test4', 'test7', 'test8', 'test9'])

        # contains
        self.assertTrue(hl.contains('test2'))
        self.assertTrue(hl.contains('Test3'))
        self.assertTrue(hl.contains('Test4'))
        self.assertTrue(hl.contains('test7'))
        self.assertTrue(hl.contains('test8'))
        self.assertTrue(hl.contains('test9'))
        self.assertFalse(hl.contains('Test2'))

        # toggle
        self.hl_return_val = True
        hl.toggle('Test4')
        self.assertEqual(hl, ['test2', 'Test3', 'test7', 'test8', 'test9'])
        hl.toggle('Test4')
        self.assertEqual(hl, ['test2', 'Test3', 'test7', 'test8', 'test9', 'Test4'])

        # clear
        self.hl_return_val = False
        hl._raw_clear()
        self.assertEqual(hl, [])
        hl._raw_extend(['test2', 'Test3', 'test7', 'test8', 'test9', 'Test4'])
        self.assertEqual(self.hl_clear_cnt, 0)
        hl.clear()
        self.assertEqual(self.hl_clear_cnt, 1)
        self.assertEqual(hl, ['test2', 'Test3', 'test7', 'test8', 'test9', 'Test4'])
        self.hl_return_val = True
        hl.clear()
        self.assertEqual(self.hl_clear_cnt, 2)
        self.assertEqual(hl, [])

        # setitem
        iv = ['test2', 'Test3', 'test7', 'test8', 'test9', 'Test4']
        self.hl_return_val = False
        hl._raw_clear()
        hl._raw_extend(iv)
        self.assertEqual(self.hl_setitem_idx, None)
        hl[0] = 'test2m'
        self.assertEqual(self.hl_setitem_idx, 0)
        self.assertEqual(self.hl_setitem_value, 'test2m')
        self.assertEqual(hl, iv)
        hl[:2] = ['testm0', 'testm1', ]
        slv = slice(0, 2, None) if ispymaj(2) else slice(None, 2, None)
        self.assertEqual(self.hl_setitem_idx, slv)
        self.assertEqual(self.hl_setitem_value, ['testm0', 'testm1', ])
        self.assertEqual(hl, iv)
        hl[-1:-3:-2] = ['testm0', ]
        self.assertEqual(self.hl_setitem_idx, slice(-1, -3, -2))
        self.assertEqual(self.hl_setitem_value, ['testm0', ])
        self.assertEqual(hl, iv)
        self.hl_return_val = True
        hl._raw_clear()
        hl._raw_extend(iv)
        hl[0] = 'test2m'
        self.assertEqual(self.hl_setitem_idx, 0)
        self.assertEqual(self.hl_setitem_value, 'test2m')
        self.assertEqual(hl, ['test2m', 'Test3', 'test7', 'test8', 'test9', 'Test4'])
        hl._raw_clear()
        hl._raw_extend(iv)
        hl[:2] = ['testm0', 'testm1', ]
        slv = slice(0, 2, None) if ispymaj(2) else slice(None, 2, None)
        self.assertEqual(self.hl_setitem_idx, slv)
        self.assertEqual(self.hl_setitem_value, ['testm0', 'testm1', ])
        self.assertEqual(hl, ['testm0', 'testm1', 'test7', 'test8', 'test9', 'Test4'])
        hl._raw_clear()
        hl._raw_extend(iv)
        hl[-1:-5:-2] = ['testm0', 'testm1', ]
        self.assertEqual(self.hl_setitem_idx, slice(-1, -5, -2))
        self.assertEqual(self.hl_setitem_value, ['testm0', 'testm1', ])
        self.assertEqual(hl, ['test2', 'Test3', 'test7', 'testm1', 'test9', 'testm0'])
        hl._raw_clear()
        hl._raw_extend(iv)
        hl[:] = [1, 2, 3, 4, 5, 6 ]
        slv = slice(0, sys.maxint, None) if ispymaj(2) else slice(None, None, None)
        self.assertEqual(self.hl_setitem_idx, slv)
        self.assertEqual(self.hl_setitem_value, [1, 2, 3, 4, 5, 6 ])
        self.assertEqual(hl, [1, 2, 3, 4, 5, 6 ])

        # init_val
        hl = domdom.HookList(init_val=[1, 2, 3, 4, ])
        self.assertEqual(hl, [1, 2, 3, 4, ])
        hl = domdom.HookList(init_val=None)  # no hooks
        self.hl_return_val = False

        # append
        hl._raw_append('test1')
        hl.append('test2')
        self.assertEqual(hl, ['test1', 'test2'])

        # add
        hl.add('test4')
        self.assertEqual(hl, ['test1', 'test2', 'test4'])

        # extend
        hl._raw_extend(['test6', 'test7'])
        hl.extend(['test8', ])
        self.assertEqual(hl, ['test1', 'test2', 'test4', 'test6', 'test7', 'test8'])

        # insert
        hl._raw_insert(1, 'test1.5')
        hl.insert(0, 'test0.5')
        self.assertEqual(hl, ['test0.5', 'test1', 'test1.5', 'test2', 'test4', 'test6', 'test7', 'test8'])

        # remove
        hl._raw_remove('test8')
        hl.remove('test1')
        self.assertEqual(hl, ['test0.5', 'test1.5', 'test2', 'test4', 'test6', 'test7', ])

        # pop
        elm = hl._raw_pop(2)
        self.assertEqual(elm, 'test2')
        elm = hl.pop(3)
        self.assertEqual(elm, 'test6')
        self.assertEqual(hl, ['test0.5', 'test1.5', 'test4', 'test7', ])

        # delitem
        hl._raw_delitem(3)
        del hl[1]
        self.assertEqual(hl, ['test0.5', 'test4', ])
        hl.extend(['test6', 'test7', 'test8', 'test9'])
        del hl[0:3]
        self.assertEqual(hl, ['test7', 'test8', 'test9'])

        # reverse
        hl._raw_reverse()
        self.assertEqual(hl, ['test9', 'test8', 'test7'])
        hl.reverse()
        self.assertEqual(hl, ['test7', 'test8', 'test9'])

        # sort
        hl.extend(['test2', 'Test4', 'Test3'])
        hl._raw_sort(reverse=True)
        self.assertEqual(hl, ['test9', 'test8', 'test7', 'test2', 'Test4', 'Test3'])
        hl._raw_sort()
        self.assertEqual(hl, ['Test3', 'Test4', 'test2', 'test7', 'test8', 'test9'])
        hl._raw_sort(key=str.lower)
        self.assertEqual(hl, ['test2', 'Test3', 'Test4', 'test7', 'test8', 'test9'])

    def test_ClassList(self):
        win = Window()
        document = win.document
        #
        elm = document.createElement('test')
        #
        self.assertEqual(elm.className, '')
        #
        elm.setAttribute('class', 'txt1')
        self.assertTrue(elm.classList.contains('txt1'))
        self.assertTrue(not elm.classList.contains('txt2'))
        self.assertEqual(elm.className, 'txt1')
        #
        elm.setAttribute('class', 'txt1 txt2 txt3')
        self.assertTrue(elm.classList.contains('txt1'))
        self.assertTrue(elm.classList.contains('txt2'))
        self.assertTrue(elm.classList.contains('txt3'))
        lst = elm.className.split(' ')
        self.assertTrue('txt1' in lst)
        self.assertTrue('txt2' in lst)
        self.assertTrue('txt3' in lst)
        #
        elm.removeAttribute('class')
        self.assertTrue(not elm.classList.contains('txt1'))
        self.assertTrue(not elm.classList.contains('txt2'))
        self.assertTrue(not elm.classList.contains('txt3'))
        self.assertEqual(elm.className, '')
        #
        elm.className = 'txt1'
        self.assertTrue(elm.classList.contains('txt1'))
        self.assertTrue(not elm.classList.contains('txt2'))
        self.assertEqual(elm.className, 'txt1')
        #
        elm.className = 'txt1 txt2 txt3'
        self.assertTrue(elm.classList.contains('txt1'))
        self.assertTrue(elm.classList.contains('txt2'))
        self.assertTrue(elm.classList.contains('txt3'))
        lst = elm.className.split(' ')
        self.assertTrue('txt1' in lst)
        self.assertTrue('txt2' in lst)
        self.assertTrue('txt3' in lst)
        #
        elm.className = ''
        self.assertTrue(not elm.classList.contains('txt1'))
        self.assertTrue(not elm.classList.contains('txt2'))
        self.assertTrue(not elm.classList.contains('txt3'))
        self.assertEqual(elm.className, '')
        #
        elm.classList.append('clsb1')
        elm.classList.add('clsb2')
        elm.classList.extend(['clsb3', 'clsb4', 'clsb5'])
        elm.classList.insert(2, 'clsb1.5')
        self.assertEqual(elm.className, 'clsb1 clsb2 clsb1.5 clsb3 clsb4 clsb5')
        self.assertTrue(elm.classList.contains('clsb1'))
        #
        elm.classList.remove('clsb1')
        self.assertFalse(elm.classList.contains('clsb1'))
        self.assertTrue(elm.classList.contains('clsb4'))
        #
        elm.classList.remove('clsb4')
        self.assertFalse(elm.classList.contains('clsb4'))
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3 clsb5')
        self.assertTrue(elm.classList.contains('clsb5'))
        #
        elm.classList.remove('clsb5')
        self.assertFalse(elm.classList.contains('clsb5'))
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3')
        #
        elm.classList.clear()
        self.assertEqual(elm.className, '')
        #
        elm.classList.extend(['clsc1', 'clsc2'])
        elm.classList.add('clsc3')
        elm.classList.append('clsc4')
        self.assertEqual(elm.className, 'clsc1 clsc2 clsc3 clsc4')
        #
        elm.classList.toggle('clsc1')
        self.assertEqual(elm.className, 'clsc2 clsc3 clsc4')
        #
        elm.classList.toggle('clsc5')
        self.assertEqual(elm.className, 'clsc2 clsc3 clsc4 clsc5')

    def test_Style(self):
        win = Window()
        document = win.document
        elm = document.createElement('test')
        #
        elm.setAttribute('style', 'color: red; background-color: grey')
        self.assertEqual(elm.style['color'], 'red')
        self.assertEqual(elm.style['background-color'], 'grey')
        style = elm.getAttribute('style')
        lst = style.split(';')
        items = [itm.split(':') for itm in lst if 0 < len(itm.strip())]
        dic = {x[0].strip(): x[1].strip() for x in items}
        self.assertEqual(dic['color'], 'red')
        self.assertEqual(dic['background-color'], 'grey')
        can0 = 'color: red; background-color: grey;'
        can1 = 'background-color: grey; color: red;'
        self.assertTrue(elm.style.cssText == can0 or elm.style.cssText == can1)
        self.assertEqual(elm.style.cssText, elm.style['cssText'])
        #
        elm.setAttribute('style', '')
        style = elm.getAttribute('style')
        self.assertEqual(style, '')
        self.assertEqual(elm.style.cssText, '')
        self.assertEqual(elm.style.cssText, elm.style['cssText'])
        # __init__()
        s0 = domdom.Style(elm)
        self.assertEqual(s0.elm, elm)
        self.assertEqual(len(s0), 0)
        #
        s1 = domdom.Style(elm, {})
        self.assertEqual(s1.elm, elm)
        self.assertEqual(len(s1), 0)
        #
        s2 = domdom.Style(elm, {'abc': 234})
        self.assertEqual(s2.elm, elm)
        self.assertEqual(len(s2), 1)
        self.assertEqual(s2.abc, 234)
        self.assertEqual(s2.abc, s2['abc'])
        #
        s3 = domdom.Style(elm, {'abc': 'zxy', 'right': 'rrq'})
        self.assertEqual(s3.elm, elm)
        self.assertEqual(len(s3), 2)
        self.assertEqual(s3.abc, 'zxy')
        self.assertEqual(s3.abc, s3['abc'])
        self.assertEqual(s3.right, 'rrq')
        self.assertEqual(s3.right, s3['right'])
        # __setitem__ __getitem__
        s3['color'] = 'yellow'
        self.assertEqual(len(s3), 3)
        self.assertEqual(s3.color, 'yellow')
        self.assertEqual(s3.color, s3['color'])
        s3['cssText'] = 'color: red; background-color: grey'
        self.assertEqual(len(s3), 2)
        self.assertEqual(s3.color, 'red')
        self.assertEqual(s3.color, s3['color'])
        self.assertEqual(s3.backgroundColor, 'grey')
        self.assertEqual(s3['background-color'], s3.backgroundColor)
        s3['zIndex'] = '15'
        self.assertEqual(len(s3), 3)
        self.assertEqual(s3.zIndex, '15')
        self.assertEqual(s3.zIndex, s3['z-index'])
        self.assertEqual(s3.zIndex, s3['zIndex'])
        s3['z-index'] = '12'
        self.assertEqual(len(s3), 3)
        self.assertEqual(s3.zIndex, '12')
        self.assertEqual(s3.zIndex, s3['z-index'])
        self.assertEqual(s3.zIndex, s3['zIndex'])
        # __delitem__
        self.assertTrue('color' in s3)
        del(s3['color'])
        self.assertEqual(len(s3), 2)
        self.assertFalse('color' in s3)
        #
        self.assertTrue('z-index' in s3)
        self.assertTrue('zIndex' in s3)
        del(s3['z-index'])
        self.assertEqual(len(s3), 1)
        self.assertFalse('z-index' in s3)
        self.assertFalse('zIndex' in s3)
        # __setattr__ __getattr__
        self.assertEqual(s3.elm, elm)
        elm2 = document.createElement('test2')
        s3.elm = elm2
        self.assertEqual(s3.elm, elm2)
        #
        s3.color = 'blue'
        self.assertEqual(len(s3), 2)
        self.assertEqual(s3.color, 'blue')
        self.assertEqual(s3.color, s3['color'])
        s3.zIndex = '7'
        self.assertEqual(len(s3), 3)
        self.assertEqual(s3.zIndex, '7')
        self.assertEqual(s3.zIndex, s3['z-index'])
        # __delattr__
        self.assertTrue(hasattr(s3, 'zIndex'))
        del s3.zIndex
        self.assertEqual(len(s3), 2)
        self.assertFalse(hasattr(s3, 'zIndex'))
        # copy 1
        s3bak = s3.copy()
        self.assertEqual(s3bak, s3)
        self.assertTrue(isinstance(s3bak, Style))
        # pop
        s3 = domdom.Style(elm, {
            'aBc': 'abc1',
            'd-ef': 'def2',
            'GHI': 'ghi3',
            'JKL': 'jkl4',
            'mNo': 'mno5',
            'p-qr': 'pqr6',
            'STU': 'stu7',
            'vWx': 'vwx8',
        })
        self.assertEqual(len(s3), 8)
        ddcnt = len(document._diffdat)
        x = s3.pop('aBc')
        self.assertEqual(len(s3), 7)
        self.assertEqual(x, 'abc1')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_deleteStyle'], ['a-bc', ])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        x = s3.pop('d-ef')
        self.assertEqual(len(s3), 6)
        self.assertEqual(x, 'def2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_deleteStyle'], ['d-ef', ])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        x = s3.pop('xxx', 'yyy')
        self.assertEqual(len(s3), 6)
        self.assertEqual(x, 'yyy')
        self.assertEqual(len(document._diffdat), ddcnt)
        x = s3.pop('JKL')
        self.assertEqual(len(s3), 5)
        self.assertEqual(x, 'jkl4')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_deleteStyle'], ['jkl', ])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        x = s3.pop('m-no')
        self.assertEqual(len(s3), 4)
        self.assertEqual(x, 'mno5')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_deleteStyle'], ['m-no', ])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        x = s3.pop('pQr')
        self.assertEqual(len(s3), 3)
        self.assertEqual(x, 'pqr6')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_deleteStyle'], ['p-qr', ])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        # setdefault
        x = s3.setdefault('GHI', 'uuu')
        self.assertEqual(x, 'ghi3')
        self.assertEqual(len(s3), 3)
        self.assertEqual(len(document._diffdat), ddcnt)
        x = s3.setdefault('ggg', 'uuu')
        self.assertEqual(x, 'uuu')
        self.assertEqual(len(s3), 4)
        self.assertEqual(s3['ggg'], 'uuu')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_setStyle'], {'ggg': 'uuu'})
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        s3bb = s3.copy()
        # popitem
        x = s3.popitem()
        self.assertEqual(len(s3), 3)
        self.assertTrue(x[1] in ['ghi3', 'stu7', 'vwx8', 'uuu'])
        self.assertTrue(s3bb[x[0]], x[1])
        self.assertFalse(x[0] in s3)
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_deleteStyle'], [x[0], ])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        # update
        s3bb = s3.copy()
        s3.update({'abCd': 'aa', 'ef-gh': 'bb'})
        self.assertEqual(len(s3), 5)
        self.assertTrue('abCd' in s3)
        self.assertTrue('ab-cd' in s3)
        self.assertEqual(s3['abCd'], 'aa')
        self.assertEqual(s3['ab-cd'], 'aa')
        self.assertTrue('ef-gh' in s3)
        self.assertTrue('efGh' in s3)
        self.assertEqual(s3['ef-gh'], 'bb')
        self.assertEqual(s3['efGh'], 'bb')
        ddd = document._diffdat[ddcnt]
        self.assertTrue((ddd['_setStyle'], {'ab-cd': 'aa'}) or (ddd['_setStyle'], {'ef-gh': 'bb'}))
        ddcnt += 1
        ddd = document._diffdat[ddcnt]
        self.assertTrue((ddd['_setStyle'], {'ab-cd': 'aa'}) or (ddd['_setStyle'], {'ef-gh': 'bb'}))
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        s3.update([('ijKl', 'cc'), ('mn-op', 'dd')])
        self.assertEqual(len(s3), 7)
        self.assertTrue('ijKl' in s3)
        self.assertTrue('ij-kl' in s3)
        self.assertEqual(s3['ijKl'], 'cc')
        self.assertEqual(s3['ij-kl'], 'cc')
        self.assertTrue('mn-op' in s3)
        self.assertTrue('mnOp' in s3)
        self.assertEqual(s3['mn-op'], 'dd')
        self.assertEqual(s3['mnOp'], 'dd')
        ddd = document._diffdat[ddcnt]
        self.assertTrue((ddd['_setStyle'] == {'ij-kl': 'cc'}) or (ddd['_setStyle'] == {'mn-op': 'dd'}))
        ddcnt += 1
        ddd = document._diffdat[ddcnt]
        self.assertTrue((ddd['_setStyle'] == {'ij-kl': 'cc'}) or (ddd['_setStyle'] == {'mn-op': 'dd'}))
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        # copy 2
        s3 = s3bak.copy()
        # clear
        self.assertTrue(s3.cssText == 'color: blue; background-color: grey;' or
                        s3.cssText == 'background-color: grey; color: blue;')
        s3.clear()
        self.assertEqual(s3.cssText, '')
        # setProperty removeProperty
        s3.setProperty('topXxx', '123')
        self.assertEqual(len(s3), 1)
        self.assertEqual(s3.topXxx, '123')
        self.assertEqual(s3.topXxx, s3['top-xxx'])
        self.assertTrue(hasattr(s3, 'topXxx'))
        s3.setProperty('color', 'blue')
        self.assertEqual(len(s3), 2)
        self.assertEqual(s3.color, 'blue')
        self.assertEqual(s3.color, s3['color'])
        self.assertTrue(hasattr(s3, 'color'))
        val = s3.removeProperty('topXxx')
        self.assertEqual(len(s3), 1)
        self.assertFalse(hasattr(s3, 'topXxx'))
        self.assertEqual(val, '123')
        val = s3.removeProperty('topXxx')
        self.assertEqual(len(s3), 1)
        self.assertFalse(hasattr(s3, 'topXxx'))
        self.assertEqual(val, None)
        val = s3.removeProperty('color')
        self.assertEqual(len(s3), 0)
        self.assertFalse(hasattr(s3, 'color'))
        self.assertEqual(val, 'blue')

    def test_Element1(self):
        win = Window()
        document = win.document
        ddcnt = 1
        tagname = 'asdf'
        elm = document.createElement(tagname)
        # __init__()
        self.assertFalse(elm._in_init_)
        self.assertEqual(elm._id, str(id(elm)))
        self.assertEqual(elm.document, document)
        self.assertEqual(elm.tagName, tagname)
        self.assertIsNone(elm.name)
        self.assertIsNone(elm.parent)
        self.assertEqual(elm._eventlisteners, [])
        self.assertEqual(type(elm._childList), domdom.ChildList)
        self.assertEqual(type(elm._classList), domdom.ClassList)
        self.assertEqual(type(elm._style), domdom.Style)
        self.assertIsNone(elm._onclick)
        self.assertIsNone(elm._onchange)
        self.assertEqual(elm._sortorder, 0)
        #
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt-1]
        self.assertEqual(ddd['_objid_'], str(id(elm)))
        self.assertTrue('_createElement' in ddd)
        dic = json.loads(ddd['_createElement'])
        self.assertEqual(len(dic), 2)
        self.assertEqual(dic['_id'], str(id(elm)))
        self.assertEqual(dic['tagName'], tagname)
        # _pre_setattr()
        key0 = 'ghkl0'
        val0 = 'uiop0'
        elm._pre_setattr(key0, val0)
        ddcnt += 1

        def chk0():
            self.assertEqual(len(document._diffdat), ddcnt)
            ddd = document._diffdat[ddcnt-1]
            self.assertEqual(ddd['_objid_'], str(id(elm)))
            self.assertEqual(ddd[key0], val0)
        chk0()
        # _in_init_ == True
        key1 = 'ghkl1'
        val1 = 'uiop1'
        elm._in_init_ = True
        elm._pre_setattr(key1, val1)
        chk0()
        elm._in_init_ = False
        # dif_excepts = ['parent', 'document', 'onclick', '_onclick', 'onchange', '_onchange',]
        elm._pre_setattr('parent', 'parent val')
        chk0()
        elm._pre_setattr('document', 'document val')
        chk0()
        elm._pre_setattr('_onclick', '_onclick val')
        chk0()
        elm._pre_setattr('_onchange', '_onchange val')
        chk0()
        elm._pre_setattr('onclick', 'onclick val')
        chk0()
        elm._pre_setattr('onchange', 'onchange val')
        chk0()
        # id
        objdic = document._obj_dic
        self.assertEqual(len(objdic), 1)
        self.assertEqual(objdic[str(id(elm))], elm)

        def setid(preid, newid, ddcnt):
            elm.id = newid
            self.assertEqual(elm._id, newid)
            self.assertEqual(elm.id, newid)
            self.assertEqual(len(objdic), 1)
            self.assertEqual(objdic[newid], elm)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)
            ddd = document._diffdat[ddcnt - 1]
            self.assertEqual(ddd['_objid_'], preid)
            self.assertEqual(ddd['id'], newid)
            return ddcnt
        ddcnt = setid(str(id(elm)), 'testid0', ddcnt)
        id1 = 'testid1'
        ddcnt = setid('testid0', id1, ddcnt)
        # className
        self.assertEqual(len(elm.classList), 0)
        cls1 = 'cls1'
        #
        elm.className = cls1
        self.assertEqual(elm.className, cls1)
        self.assertEqual(len(elm.classList), 1)
        self.assertEqual(elm.classList[0], cls1)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], cls1)
        cls2 = 'cls2'
        #
        elm.className = cls2
        self.assertEqual(elm.className, cls2)
        self.assertEqual(len(elm.classList), 1)
        self.assertEqual(elm.classList[0], cls2)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], cls2)
        cls3 = ''
        #
        elm.className = cls3
        self.assertEqual(elm.className, cls3)
        self.assertEqual(len(elm.classList), 0)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], cls3)
        cls4x, cls4y = 'cls4x', 'cls4y'
        cls4a = '{} {}'.format(cls4x, cls4y)
        elm.className = cls4a

        def chk_cls4(txt):
            self.assertEqual(elm.className, cls4a)
            self.assertEqual(len(elm.classList), 2)
            self.assertEqual(elm.classList[0], cls4x)
            self.assertEqual(elm.classList[1], cls4y)
            lddcnt = ddcnt + 1
            self.assertEqual(len(document._diffdat), lddcnt)
            ddd = document._diffdat[lddcnt - 1]
            self.assertEqual(ddd['_objid_'], id1)
            self.assertEqual(ddd['className'], txt)
            return lddcnt
        ddcnt = chk_cls4(cls4a)
        cls4b = '{}  {}'.format(cls4x, cls4y)
        #
        elm.className = cls4b
        ddcnt = chk_cls4(cls4b)
        cls4c = ' {} {}'.format(cls4x, cls4y)
        #
        elm.className = cls4c
        ddcnt = chk_cls4(cls4c)
        cls4d = '{} {} '.format(cls4x, cls4y)
        #
        elm.className = cls4d
        ddcnt = chk_cls4(cls4d)
        cls4e = '  {}  {}  '.format(cls4x, cls4y)
        #
        elm.className = cls4e
        ddcnt = chk_cls4(cls4e)
        cls5x, cls5y, cls5z = 'cls5x', 'cls5y', 'cls5z'
        cls5a = '{} {} {}'.format(cls5x, cls5y, cls5z)
        cls5b = ' {} {}  {}'.format(cls5x, cls5y, cls5z)
        #
        elm.className = cls5b
        self.assertEqual(elm.className, cls5a)
        self.assertEqual(len(elm.classList), 3)
        self.assertEqual(elm.classList[0], cls5x)
        self.assertEqual(elm.classList[1], cls5y)
        self.assertEqual(elm.classList[2], cls5z)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], cls5b)
        # classList
        with self.assertRaises(TypeError):
            elm.classList = []
        # style
        elm.style = ''
        self.assertEqual(len(elm._style), 0)
        self.assertEqual(elm.style.cssText, '')
        self.assertEqual(elm.style, {})
        ddcnt += 0 # no change
        self.assertEqual(len(document._diffdat), ddcnt)
        styl0 = {'top': '20'}
        styl1 = {'left': '30'}
        txt = '{}: {}; {}: {};'.format(list(styl0.keys())[0], list(styl0.values())[0],
                                      list(styl1.keys())[0], list(styl1.values())[0])
        txt2 = '{}: {}; {}: {};'.format(list(styl1.keys())[0], list(styl1.values())[0],
                                      list(styl0.keys())[0], list(styl0.values())[0])
        #
        elm.style = txt
        self.assertEqual(len(elm._style), 2)
        csstxt = elm.style.cssText
        self.assertTrue(csstxt == txt or csstxt == txt2)
        styls = dict(styl0)
        styls.update(styl1)
        self.assertEqual(elm.style, styls)
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], styl0)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], styl1)

        # __setattr__() others
        elm.foo = 'foovalue'
        self.assertEqual(elm.foo, 'foovalue')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['foo'], 'foovalue')
        #
        elm.bar = 'barvalue'
        self.assertEqual(elm.bar, 'barvalue')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['bar'], 'barvalue')
        #
        elm.baz = 'bazvalue'
        self.assertEqual(elm.baz, 'bazvalue')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['baz'], 'bazvalue')

        # childList
        chd = document.createElement('chdtag')
        chd2 = document.createElement('chd2tag')
        chd3 = document.createElement('chd3tag')
        ddcnt += 3

        # childList set []
        elm.childList = []
        elm.childList.append(chd)
        self.assertEqual(elm.childList, [chd, ])
        self.assertEqual(chd.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)

        # childList append() to []
        elm.childList.append(chd2)
        self.assertEqual(elm.childList, [chd, chd2])
        self.assertEqual(chd2.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd2._id)

        # childList insert(0) to [x, y]
        elm.childList.insert(0, chd3)
        self.assertEqual(elm.childList, [chd3, chd, chd2])
        self.assertEqual(chd3.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd3._id, chd._id])

        # childList clear()
        elm.childList.clear()
        self.assertEqual(elm.childList, [])
        self.assertEqual(chd.parent, None)
        self.assertEqual(chd2.parent, None)
        self.assertEqual(chd3.parent, None)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearChild'], True)

        # childList set [x]
        elm.childList = [chd, ]
        self.assertEqual(elm.childList, [chd, ])
        self.assertEqual(chd.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)

        # childList insert(0) to [x]
        elm.childList.insert(0, chd2)
        self.assertEqual(elm.childList, [chd2, chd, ])
        self.assertEqual(chd2.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd2._id, chd._id])

        # childList insert(1) to [x, y]
        elm.childList.insert(1, chd3)
        self.assertEqual(elm.childList, [chd2, chd3, chd, ])
        self.assertEqual(chd3.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd3._id, chd._id])

        # childList clear()
        elm.childList.clear()
        self.assertEqual(elm.childList, [])
        self.assertEqual(chd.parent, None)
        self.assertEqual(chd2.parent, None)
        self.assertEqual(chd3.parent, None)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearChild'], True)

        # childList set [x, y]
        elm.childList = [chd, chd2]
        self.assertEqual(elm.childList, [chd, chd2])
        self.assertEqual(chd.parent, elm)
        self.assertEqual(chd2.parent, elm)
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd2._id)

        # childList append() to [x, y]
        elm.childList.append(chd3)
        self.assertEqual(elm.childList, [chd, chd2, chd3])
        self.assertEqual(chd3.parent, elm)
        ddcnt += 1
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd3._id)

        # childList remove(y) from [x, y, z]
        elm.childList.remove(chd2)
        self.assertEqual(elm.childList, [chd, chd3])
        self.assertEqual(chd2.parent, None)
        ddcnt += 1
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList remove(x) from [x, y]
        elm.childList.remove(chd)
        self.assertEqual(elm.childList, [chd3, ])
        self.assertEqual(chd.parent, None)
        ddcnt += 1
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList extend([y, z]) to [x]
        elm.childList.extend([chd, chd2])
        self.assertEqual(elm.childList, [chd3, chd, chd2])
        self.assertEqual(chd.parent, elm)
        self.assertEqual(chd2.parent, elm)
        ddcnt += 2
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd2._id)

        # childList pop y from [x, y, z]
        chk = elm.childList.pop(1)
        self.assertEqual(chk, chd)
        self.assertEqual(elm.childList, [chd3, chd2])
        self.assertEqual(chd.parent, None)
        ddcnt += 1
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList pop y from [x, y,]
        chk = elm.childList.pop(1)
        self.assertEqual(chk, chd2)
        self.assertEqual(elm.childList, [chd3, ])
        self.assertEqual(chd2.parent, None)
        ddcnt += 1
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList pop x from [x,]
        chk = elm.childList.pop(0)
        self.assertEqual(chk, chd3)
        self.assertEqual(elm.childList, [])
        self.assertEqual(chd3.parent, None)
        ddcnt += 1
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList set [x, y, z]
        elm.childList = [chd, chd2, chd3]
        self.assertEqual(elm.childList, [chd, chd2, chd3])
        self.assertEqual(chd.parent, elm)
        self.assertEqual(chd2.parent, elm)
        self.assertEqual(chd3.parent, elm)
        ddcnt += 3
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd2._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd3._id)

        # childList reverse()
        elm.childList.reverse()
        self.assertEqual(elm.childList, [chd3, chd2, chd])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_reverseChild'], True)

        # childList sort()
        elm.childList.sort(lambda x: x.tagName)
        self.assertEqual(elm.childList, [chd2, chd3, chd])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_sortChild'], [1, 0, 2, ])

        # childList set overwrite
        elm.childList = [chd, chd3]
        self.assertEqual(elm.childList, [chd, chd3])
        ddcnt += 3
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearChild'], True)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd3._id)

        # childList del 0 from [x, y]
        del elm.childList[0]
        self.assertEqual(elm.childList, [chd3])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList del 0,1 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        del elm.childList[0:2]
        self.assertEqual(elm.childList, [chd3])
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList del 1,2 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        del elm.childList[1:3]
        self.assertEqual(elm.childList, [chd])
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList del 0 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        del elm.childList[0:1]
        self.assertEqual(elm.childList, [chd2, chd3])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList del 1 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        del elm.childList[1]
        self.assertEqual(elm.childList, [chd, chd3])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList del 2 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        del elm.childList[2:1000]
        self.assertEqual(elm.childList, [chd, chd2])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList del -1 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        del elm.childList[-1]
        self.assertEqual(elm.childList, [chd, chd2])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList del -2: from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        del elm.childList[-2:]
        self.assertEqual(elm.childList, [chd, ])
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem
        chd4 = document.createElement('chd4tag')
        chd5 = document.createElement('chd5tag')
        ddcnt += 2
        # childList setitem [0] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[0] = chd4
        self.assertEqual(elm.childList, [chd4, chd2, chd3])
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList setitem [-3] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[-3] = chd4
        self.assertEqual(elm.childList, [chd4, chd2, chd3])
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList setitem [1] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[1] = chd4
        self.assertEqual(elm.childList, [chd, chd4, chd3])
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [-2] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[1] = chd4
        self.assertEqual(elm.childList, [chd, chd4, chd3])
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [2] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[2] = chd4
        self.assertEqual(elm.childList, [chd, chd2, chd4])
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [-1] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[2] = chd4
        self.assertEqual(elm.childList, [chd, chd2, chd4])
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [1:5]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[1:5] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd4, chd5])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [-2:5]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[-2:5] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd4, chd5])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [1:]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[1:] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd4, chd5])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [-2:]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[-2:] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd4, chd5])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [0:2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[0:2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd5, chd3])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [-3:-1]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[-3:-1] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd5, chd3])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [:2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[:2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd5, chd3])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [:-1]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[:-1] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd5, chd3])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [0:3:2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[0:3:2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd2, chd5])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd3._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [-3::2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[-3::2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd2, chd5])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd3._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [2:0:-1]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[2:0:-1] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd5, chd4])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [-1:0:-1]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[-1:0:-1] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd5, chd4])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [2::-2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[2::-2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd5, chd2, chd4])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList setitem [-1::-2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.childList[-1::-2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd5, chd2, chd4])
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # classList
        # classList clear by className
        elm.className = ''
        lst = elm.classList
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], '')
        self.assertEqual(len(lst), 0)

        # classList [].append(x)
        elm.classList.append('clsb1')
        self.assertEqual(len(lst), 1)
        self.assertEqual(lst[0], 'clsb1')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsb1', ])

        # classList [x].add(y)
        elm.classList.add('clsb2')
        self.assertEqual(len(lst), 2)
        self.assertEqual(lst[1], 'clsb2')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsb2', ])

        # classList [1,2].extend([3,4,5])
        elm.classList.extend(['clsb3', 'clsb4', 'clsb5'])
        self.assertEqual(len(lst), 5)
        self.assertEqual(lst[2], 'clsb3')
        self.assertEqual(lst[3], 'clsb4')
        self.assertEqual(lst[4], 'clsb5')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsb3', 'clsb4', 'clsb5'])

        # classList [1,2,3,4,5].insert(2, 1.5)
        elm.classList.insert(2, 'clsb1.5')
        self.assertEqual(len(lst), 6)
        self.assertEqual(elm.className, 'clsb1 clsb2 clsb1.5 clsb3 clsb4 clsb5')
        self.assertTrue(elm.classList.contains('clsb1'))
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsb1.5', ])

        # classList [1,2,1.5,3,4,5].remove(1)
        elm.classList.remove('clsb1')
        self.assertEqual(len(lst), 5)
        self.assertFalse(elm.classList.contains('clsb1'))
        self.assertTrue(elm.classList.contains('clsb4'))
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb1', ])

        # classList [2,1.5,3,4,5].remove(4)
        elm.classList.remove('clsb4')
        self.assertEqual(len(lst), 4)
        self.assertFalse(elm.classList.contains('clsb4'))
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3 clsb5')
        self.assertTrue(elm.classList.contains('clsb5'))
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb4', ])

        # classList [2,1.5,3,5].remove(5)
        elm.classList.remove('clsb5')
        self.assertEqual(len(lst), 3)
        self.assertFalse(elm.classList.contains('clsb5'))
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb5', ])

        # classList [2,1.5,3].toggle(6)
        elm.classList.toggle('clsb6')
        self.assertEqual(len(lst), 4)
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3 clsb6')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsb6', ])

        # classList [2,1.5,3,6].toggle(6)
        elm.classList.toggle('clsb6')
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb6', ])

        # classList [2,1.5,3].pop(1)
        cn = elm.classList.pop(1)
        self.assertEqual(cn, 'clsb1.5')
        self.assertEqual(len(lst), 2)
        self.assertEqual(elm.className, 'clsb2 clsb3')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb1.5', ])

        # classList [2,3].pop(1)
        cn = elm.classList.pop(1)
        self.assertEqual(cn, 'clsb3')
        self.assertEqual(len(lst), 1)
        self.assertEqual(elm.className, 'clsb2')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb3', ])

        # classList [2].pop(0)
        cn = elm.classList.pop(0)
        self.assertEqual(cn, 'clsb2')
        self.assertEqual(len(lst), 0)
        self.assertEqual(elm.className, '')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb2', ])

        # classList setitem [0] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[0] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc2 clsc3')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', ])

        # classList setitem [-3] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[-3] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc2 clsc3')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', ])

        # classList setitem [1] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[1] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc3')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', ])

        # classList setitem [-2] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[-2] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc3')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', ])

        # classList setitem [2] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[2] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc2 clsc4')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', ])

        # classList setitem [-1] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[-1] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc2 clsc4')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', ])

        # classList setitem [1:5]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[1:5] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc5')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList setitem [-2:5]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[-2:5] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc5')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList setitem [1:]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[1:] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc5')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList setitem [-2:]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[-2:] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc5')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList setitem [0:2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[0:2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc5 clsc3')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc2', ])

        # classList setitem [-3:-1]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[-3:-1] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc5 clsc3')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc2', ])

        # classList setitem [:2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[:2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc5 clsc3')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc2', ])

        # classList setitem [:-1]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[:-1] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc5 clsc3')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc2', ])

        # classList setitem [0:3:2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[0:3:2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc2 clsc5')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc3', ])

        # classList setitem [-3::2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[-3::2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc2 clsc5')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc3', ])

        # classList setitem [2:0:-1]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[2:0:-1] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc5 clsc4')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', 'clsc2', ])

        # classList setitem [-1:0:-1]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[-1:0:-1] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc5 clsc4')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', 'clsc2', ])

        # classList setitem [2::-2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[2::-2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc5 clsc2 clsc4')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', 'clsc1', ])

        # classList setitem [-1::-2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList[-1::-2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc5 clsc2 clsc4')
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', 'clsc1', ])

        # classList set by className
        elm.className = 'clsc1 clsc2 clsc3  clsc4'
        self.assertEqual(len(lst), 4)
        self.assertEqual(elm.className, 'clsc1 clsc2 clsc3 clsc4')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], 'clsc1 clsc2 clsc3  clsc4')
        # note: no className in dominter.js because className is treated like common properties

        # classList del[0] from [x,y,z,w]
        del elm.classList[0]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc2 clsc3 clsc4')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', ])

        # classList del 0,1 from [x,y,z]
        del elm.classList[0:2]
        self.assertEqual(len(lst), 1)
        self.assertEqual(elm.className, 'clsc4')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3',])

        # classList del 1,2,3,4 from [x,y,z]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        del elm.classList[1:5]
        self.assertEqual(len(lst), 1)
        self.assertEqual(elm.className, 'clsc1')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3',])

        # classList del -1 from [x,y,z]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        del elm.classList[-1]
        self.assertEqual(len(lst), 2)
        self.assertEqual(elm.className, 'clsc1 clsc2')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3',])

        # classList del -2: from [x,y,z]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        del elm.classList[-2:]
        self.assertEqual(len(lst), 1)
        self.assertEqual(elm.className, 'clsc1')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList del -2: from [x,y,z]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        del elm.classList[-2:]
        self.assertEqual(len(lst), 1)
        self.assertEqual(elm.className, 'clsc1')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList reverse()
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList.reverse()
        self.assertEqual(elm.className, 'clsc3 clsc2 clsc1')
        ddcnt += 0
        self.assertEqual(len(document._diffdat), ddcnt)

        # classList reverse()
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        elm.classList.sort()
        self.assertEqual(elm.className, 'clsc1 clsc2 clsc3')
        ddcnt += 0
        self.assertEqual(len(document._diffdat), ddcnt)

        # classList clear()
        elm.classList.clear()
        self.assertEqual(elm.className, '')
        self.assertEqual(len(lst), 0)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearClass'], True)

        # style
        elm.style.cssText = ''
        ddcnt += 1

        # style setitem getitem
        elm.style['color'] = 'grey'
        self.assertEqual(len(elm.style), 1)
        self.assertEqual(elm.style.color, 'grey')
        self.assertEqual(elm.style['color'], 'grey')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'color': 'grey'})

        # style setattr getattr
        elm.style.color = 'red'
        self.assertEqual(len(elm.style), 1)
        self.assertEqual(elm.style.color, 'red')
        self.assertEqual(elm.style['color'], 'red')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'color': 'red'})

        # style attr2item_key
        elm.style.zIndex = 3
        self.assertEqual(len(elm.style), 2)
        self.assertEqual(elm.style, {'color': 'red', 'z-index': 3})
        self.assertEqual(elm.style.zIndex, 3)
        self.assertEqual(elm.style['z-index'], 3)
        self.assertEqual(elm.style['zIndex'], 3)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'z-index': 3})

        # style contains
        self.assertFalse('size' in elm.style)
        elm.style.size = 80
        self.assertTrue('size' in elm.style)
        self.assertEqual(len(elm.style), 3)
        self.assertEqual(elm.style, {'color': 'red', 'z-index': 3, 'size': 80})
        self.assertEqual(elm.style.size, 80)
        self.assertEqual(elm.style['size'], 80)
        self.assertTrue('z-index' in elm.style)
        self.assertTrue('zIndex' in elm.style)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'size': 80})

        # style delitem
        self.assertFalse('marginLeft' in elm.style)
        self.assertFalse('margin-left' in elm.style)
        elm.style['margin-left'] = 5
        self.assertEqual(len(elm.style), 4)
        self.assertEqual(elm.style, {'color': 'red', 'z-index': 3, 'size': 80, 'margin-left': 5, })
        ddcnt += 1
        self.assertTrue('marginLeft' in elm.style)
        self.assertTrue('margin-left' in elm.style)
        self.assertEqual(elm.style.marginLeft, 5)
        self.assertEqual(elm.style['margin-left'], 5)
        del elm.style['margin-left']
        self.assertEqual(len(elm.style), 3)
        self.assertEqual(elm.style, {'color': 'red', 'z-index': 3, 'size': 80, })
        self.assertFalse('marginLeft' in elm.style)
        self.assertFalse('margin-left' in elm.style)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_deleteStyle'], ['margin-left', ])
        del elm.style.zIndex
        self.assertEqual(len(elm.style), 2)
        self.assertEqual(elm.style, {'color': 'red', 'size': 80, })
        self.assertFalse('xIndex' in elm.style)
        self.assertFalse('z-index' in elm.style)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_deleteStyle'], ['z-index', ])

        # style setProperty 1
        elm.style.setProperty('color', 'grey')
        self.assertEqual(len(elm.style), 2)
        self.assertEqual(elm.style, {'color': 'grey', 'size': 80, })
        self.assertEqual(elm.style.color, 'grey')
        self.assertEqual(elm.style['color'], 'grey')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'color': 'grey'})

        # style setProperty 2
        elm.style.setProperty('margin-left', '20')
        self.assertEqual(len(elm.style), 3)
        self.assertEqual(elm.style, {'color': 'grey', 'size': 80, 'margin-left': '20', })
        self.assertEqual(elm.style.marginLeft, '20')
        self.assertEqual(elm.style['margin-left'], '20')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'margin-left': '20'})

        # style removeProperty
        elm.style.removeProperty('margin-left')
        self.assertEqual(len(elm.style), 2)
        self.assertEqual(elm.style, {'color': 'grey', 'size': 80, })
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_deleteStyle'], ['margin-left', ])


        # style cssText read
        self.assertTrue(elm.style.cssText=='color: grey; size: 80;' or
                        elm.style.cssText == 'size: 80; color: grey;')

        # style pop
        val = elm.style.pop('color')
        self.assertEqual(val, 'grey')
        self.assertEqual(len(elm.style), 1)
        self.assertEqual(elm.style, {'size': 80, })
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_deleteStyle'], ['color', ])

        # style cssText write
        elm.style.cssText = 'color: yellow; z-index: 12;'
        self.assertTrue(elm.style.cssText == 'color: yellow; z-index: 12;' or
                        elm.style.cssText == 'z-index: 12; color: yellow;'
                        )
        self.assertEqual(elm.style, {'color': 'yellow', 'z-index': '12'})
        ddcnt += 3
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearStyle'], True)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'color': 'yellow'})
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'z-index': '12'})

        # style clear
        elm.style.clear()
        self.assertEqual(len(elm.style), 0)
        self.assertEqual(elm.style, {})
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearStyle'], True)

        # style set 0
        elm.style = 'color: green; z-index: 11; special: a:b:c:de: ;'
        self.assertEqual(len(elm.style), 3)
        self.assertEqual(elm.style.color, 'green')
        self.assertEqual(elm.style['color'], 'green')
        self.assertEqual(elm.style.zIndex, '11')
        self.assertEqual(elm.style['z-index'], '11')
        self.assertEqual(elm.style['zIndex'], '11')
        self.assertEqual(elm.style.special, 'a:b:c:de:')
        ddcnt += 3
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'color': 'green'})
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'z-index': '11'})
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'special': 'a:b:c:de:'})

        # style set 1
        elm.style = 'color: green; z-index: 11; special: a:b:c:de: ;'
        self.assertEqual(len(elm.style), 3)
        self.assertEqual(elm.style.color, 'green')
        self.assertEqual(elm.style['color'], 'green')
        self.assertEqual(elm.style.zIndex, '11')
        self.assertEqual(elm.style['z-index'], '11')
        self.assertEqual(elm.style['zIndex'], '11')
        self.assertEqual(elm.style.special, 'a:b:c:de:')
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearStyle'], True)
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'color': 'green'})
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'z-index': '11'})
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'special': 'a:b:c:de:'})

        # onclick
        handlers = document._handlers
        self.assertEqual(len(handlers), 0)

        def onclick1(ev):
            pass
        #
        elm.onclick = onclick1
        self.assertEqual(elm._onclick, onclick1)
        self.assertEqual(elm.onclick, onclick1)
        self.assertEqual(handlers[repr(onclick1)], onclick1)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['onclick'], repr(onclick1))
        # onchange

        def onchange1(ev):
            pass
        #
        elm.onchange = onchange1
        self.assertEqual(elm._onchange, onchange1)
        self.assertEqual(elm.onchange, onchange1)
        self.assertEqual(handlers[repr(onchange1)], onchange1)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['onchange'], repr(onchange1))

    def test_Element2(self):
        win = Window()
        document = win.document
        elm = document.createElement('elmtag')
        elm2 = document.createElement('elm2tag')
        chd = document.createElement('chdtag')
        chd2 = document.createElement('chd2tag')
        ddcnt = 4
        # removeChild appendChild
        self.assertEqual(len(document._diffdat), ddcnt)
        self.assertEqual(len(elm.childList), 0)
        with self.assertRaises(ValueError):
            elm.removeChild(chd)
        self.assertEqual(len(document._diffdat), ddcnt)
        self.assertEqual(len(elm.childList), 0)
        self.assertIsNone(chd.parent)

        elm.appendChild(chd)
        self.assertEqual(len(elm.childList), 1)
        self.assertEqual(elm.childList[0], chd)
        self.assertEqual(chd.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd.id)

        elm.removeChild(chd)
        self.assertEqual(len(elm.childList), 0)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_removeChild'], chd.id)

        elm.appendChild(chd)
        elm.appendChild(chd2)
        elm.appendChild(chd)
        self.assertEqual(len(elm.childList), 2)
        self.assertEqual(elm.childList[0], chd2)
        self.assertEqual(elm.childList[1], chd)
        ddcnt += 4
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd.id)
        ddd = document._diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd2.id)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_removeChild'], chd.id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd.id)

        elm.removeChild(chd)
        elm.removeChild(chd2)
        ddcnt += 2
        elm.appendChild(chd2)
        elm2.appendChild(chd)
        ddcnt += 2
        self.assertEqual(len(elm.childList), 1)
        self.assertEqual(elm.childList[0], chd2)
        self.assertEqual(len(elm2.childList), 1)
        self.assertEqual(elm2.childList[0], chd)

        elm.appendChild(chd)
        self.assertEqual(len(elm.childList), 2)
        self.assertEqual(elm.childList[0], chd2)
        self.assertEqual(elm.childList[1], chd)
        self.assertEqual(len(elm2.childList), 0)
        ddcnt += 2
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], elm2.id)
        self.assertEqual(ddd['_removeChild'], chd.id)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd.id)

        chd3 = document.createElement('chd3tag')
        chd4 = document.createElement('chd4tag')
        ddcnt += 2
        # insertBefore()
        elm.insertBefore(chd3, chd2)
        self.assertEqual(len(elm.childList), 3)
        self.assertEqual(elm.childList[0], chd3)
        self.assertEqual(elm.childList[1], chd2)
        self.assertEqual(elm.childList[2], chd)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_insertBefore'], [chd3.id, chd2.id])

        elm.insertBefore(chd4, chd)
        self.assertEqual(len(elm.childList), 4)
        self.assertEqual(elm.childList[0], chd3)
        self.assertEqual(elm.childList[1], chd2)
        self.assertEqual(elm.childList[2], chd4)
        self.assertEqual(elm.childList[3], chd)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd.id])
        elm.childList.clear()
        ddcnt += 1

        with self.assertRaises(ValueError):
            elm.insertBefore(None, chd)

        with self.assertRaises(ValueError):
            elm.insertBefore(chd, chd2)
        #elm.appendChild(chd)
        elm.insertBefore(chd, None)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd.id)
        elm.insertBefore(chd2, chd)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(len(elm.childList), 2)
        self.assertEqual(elm.childList[0], chd2)
        self.assertEqual(elm.childList[1], chd)
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_insertBefore'], [chd2.id, chd.id])

        # replaceChild
        elm.replaceChild(chd3, None)
        self.assertEqual(len(elm.childList), 3)
        self.assertEqual(elm.childList[0], chd2)
        self.assertEqual(elm.childList[1], chd)
        self.assertEqual(elm.childList[2], chd3)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd3.id)

        elm.replaceChild(chd4, chd)
        self.assertIsNone(chd.parent)
        self.assertEqual(len(elm.childList), 3)
        self.assertEqual(elm.childList[0], chd2)
        self.assertEqual(elm.childList[1], chd4)
        self.assertEqual(elm.childList[2], chd3)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_replaceChild'], [chd4.id, chd.id])

        elm.replaceChild(chd2, chd3)
        self.assertIsNone(chd3.parent)
        self.assertEqual(len(elm.childList), 2)
        self.assertEqual(elm.childList[0], chd4)
        self.assertEqual(elm.childList[1], chd2)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_replaceChild'], [chd2.id, chd3.id])

        elm.replaceChild(chd3, chd4)
        self.assertIsNone(chd4.parent)
        self.assertEqual(len(elm.childList), 2)
        self.assertEqual(elm.childList[0], chd3)
        self.assertEqual(elm.childList[1], chd2)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_replaceChild'], [chd3.id, chd4.id])

        elm.replaceChild(chd4, chd2)
        self.assertIsNone(chd2.parent)
        self.assertEqual(len(elm.childList), 2)
        self.assertEqual(elm.childList[0], chd3)
        self.assertEqual(elm.childList[1], chd4)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_replaceChild'], [chd4.id, chd2.id])

        elm.replaceChild(chd4, chd3)
        self.assertIsNone(chd3.parent)
        self.assertEqual(len(elm.childList), 1)
        self.assertEqual(elm.childList[0], chd4)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_replaceChild'], [chd4.id, chd3.id])

    def test_Element3(self):
        win = Window()
        document = win.document
        elm = document.createElement('elmtag')
        ddcnt = 1
        # setAttribute() getAttribute 1
        elm.setAttribute('abc', 1234)
        v = elm.getAttribute('abc')
        self.assertEqual(v, 1234)
        self.assertTrue('abc' in elm.__dict__)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_setAttributes'], {'abc': 1234})

        # setAttribute() getAttribute 2
        elm.setAttribute('def', 567)
        v = elm.getAttribute('def')
        self.assertEqual(v, 567)
        self.assertTrue('def' in elm.__dict__)
        v = elm.getAttribute('abc')
        self.assertEqual(v, 1234)
        self.assertTrue('abc' in elm.__dict__)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_setAttributes'], {'def': 567})

        # removeAttribute()
        elm.removeAttribute('abc')
        v = elm.getAttribute('abc')
        self.assertEqual(v, None)
        v = elm.getAttribute('def')
        self.assertEqual(v, 567)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_removeAttributes'], ['abc', ])

        # addEventListener
        def fnc1(ev):
            pass
        self.assertEqual(elm._eventlisteners, [])
        elm.addEventListener('mousemove', fnc1)
        self.assertEqual(elm._eventlisteners, [('mousemove', fnc1), ])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_addEventListener'], ['mousemove', repr(fnc1), ])
        # removeEventListener
        elm.removeEventListener('mousemove', fnc1)
        self.assertEqual(elm._eventlisteners, [])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_removeEventListener'], ['mousemove', repr(fnc1), ])

    def test_Element_dumps(self):
        win = Window()
        document = win.document
        elm = document.createElement('elmtag')
        ddcnt = 1
        s = elm._dumps()
        d = json.loads(s)
        self.assertEqual(d, {'tagName': 'elmtag', '_id': elm._id})
        elm.test01 = '1234'
        s = elm._dumps()
        d = json.loads(s)
        self.assertEqual(d, {'tagName': 'elmtag', '_id': elm._id, 'test01': '1234'})
        elm.__dict__['test02'] = "246"
        s = elm._dumps()
        d = json.loads(s)
        self.assertEqual(d, {'tagName': 'elmtag', '_id': elm._id, 'test01': '1234',
                             'test02': '246'})

    def test_Document(self):
        win = Window()
        document = win.document
        # __init__
        self.assertTrue(document._dirty_cache)
        self.assertFalse(document._dirty_diff)
        self.assertEqual(document._obj_dic, {})
        self.assertEqual(document._diffdat, [])
        self.assertEqual(document._handlers, {})
        self.assertEqual(type(document.head), domdom.Element)
        self.assertEqual(document.head.document, document)
        self.assertEqual(document.head.tagName, 'head')
        self.assertEqual(type(document.body), domdom.Element)
        self.assertEqual(document.body.document, document)
        self.assertEqual(document.body.tagName, 'body')
        self.assertIsNone(document._cache)

        # _add_diff _clean_diff
        document._dirty_diff = False
        document._add_diff('diffdat1')
        self.assertTrue(document._dirty_diff)
        self.assertEqual(document._diffdat, ['diffdat1', ])
        document._dirty = False
        document._add_diff('diffdat2')
        self.assertTrue(document._dirty_diff)
        self.assertEqual(document._diffdat, ['diffdat1', 'diffdat2', ])
        document._clean_diff()
        self.assertFalse(document._dirty_diff)
        self.assertEqual(document._diffdat, [])

        # getElementById
        elm1 = document.tag('input type="text" id="id001"')
        elm2 = document.button('this is a button', id_='id002')
        elm3 = document.createElement('button')
        elm3.id = 'id003'
        v = document.getElementById('id001')
        self.assertEqual(v, elm1)
        v = document.getElementById('id002')
        self.assertEqual(v, elm2)
        v = document.getElementById('id003')
        self.assertEqual(v, elm3)
        v = document.getElementById('id000')
        self.assertEqual(v, None)

        # getElementsByName
        elm1.name = 'nameA'
        elm2.name = 'nameB'
        elm3.name = 'nameA'
        lst = document.getElementsByName('nameA')
        self.assertTrue(lst == [elm1, elm3] or lst == [elm3, elm1])
        lst = document.getElementsByName('nameB')
        self.assertEqual(lst, [elm2, ])

        # getElementsByTagName
        lst = document.getElementsByTagName('input')
        self.assertEqual(lst, [elm1, ])
        lst = document.getElementsByTagName('button')
        self.assertTrue(lst == [elm2, elm3] or lst == [elm3, elm2])

        # getElementsByClassName
        elm1.className = 'clsA clsB'
        elm2.className = 'clsB clsC'
        elm3.className = 'clsC clsD'
        lst = document.getElementsByClassName('clsA')
        self.assertEqual(lst, [elm1, ])
        lst = document.getElementsByClassName('clsB')
        self.assertTrue(lst == [elm1, elm2] or lst == [elm2, elm1])
        lst = document.getElementsByClassName('clsC')
        self.assertTrue(lst == [elm2, elm3] or lst == [elm3, elm2])
        lst = document.getElementsByClassName('clsD')
        self.assertEqual(lst, [elm3, ])

        # createElement
        ddcnt = len(document._diffdat)
        elm4 = document.createElement('tagname')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm4._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm4._id, 'tagName': 'tagname'})
        self.assertTrue(elm4._id in document._obj_dic)
        self.assertEqual(document._obj_dic[elm4._id], elm4)

        # tag
        del document._diffdat[:]
        ddcnt = 0
        with self.assertRaises(TypeError):
            elm = document.tag()
        with self.assertRaises(TypeError):
            elm = document.tag(1234)
        with self.assertRaises(TypeError):
            elm = document.tag('')
        # tag without option arg
        elm = document.tag('tagwoopt')
        self.assertEqual(elm.tagName, 'tagwoopt')
        self.assertEqual(type(elm), domdom.Element)
        self.assertFalse('textContent' in elm.__dict__)
        self.assertIsNone(elm.onclick)
        self.assertIsNone(elm.onchange)
        self.assertEqual(elm._eventlisteners, [])
        self.assertEqual(elm.childList, [])
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)
        ddd = document._diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'tagwoopt'})
        self.assertTrue(elm._id in document._obj_dic)
        self.assertEqual(document._obj_dic[elm._id], elm)

        # tag with option arg
        del document._diffdat[:]
        ddcnt = 0
        def clickfnc(ev):
            pass
        def changefnc(ev):
            pass
        def fnc1(ev):
            pass
        def fnc2(ev):
            pass
        def fnc3(ev):
            pass
        elm = document.tag('tagwopt', textContent='ttttt',
                           attrs={'atr1': 'aval1', 'atr2': 'aval2'},
                           onclick=clickfnc, onchange=changefnc,
                           handler=(('event1', fnc1), ('event2', fnc2), ('event3', fnc3)),
                           childList=[elm1, elm2, elm3])
        self.assertEqual(elm.tagName, 'tagwopt')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.textContent, 'ttttt')
        self.assertEqual(elm.onclick, clickfnc)
        self.assertEqual(elm.onchange, changefnc)
        self.assertEqual(len(elm._eventlisteners), 3)
        self.assertTrue(('event1', fnc1) in elm._eventlisteners)
        self.assertTrue(('event2', fnc2) in elm._eventlisteners)
        self.assertTrue(('event3', fnc3) in elm._eventlisteners)
        self.assertEqual(elm.childList, [elm1, elm2, elm3])
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'tagwopt'})
        self.assertTrue(elm._id in document._obj_dic)
        self.assertEqual(document._obj_dic[elm._id], elm)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'ttttt'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setAttributes': {'atr1': 'aval1'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setAttributes': {'atr2': 'aval2'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onclick': repr(clickfnc)} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(changefnc)} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_addEventListener': ['event1', repr(fnc1)]} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_addEventListener': ['event2', repr(fnc2)]} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_addEventListener': ['event3', repr(fnc3)]} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # tag with tagtext
        del document._diffdat[:]
        ddcnt = 0
        elm = document.tag('tagtxt atr3="aval3" atr4="aval4" atr5'
                           + ' id="ididid"'
                           + ' class="cls1 cls2  cls3"'
                           + ' style="background-color: green; font-size: 14;"'
                           + ' _=vvv')
        self.assertEqual(elm.tagName, 'tagtxt')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.atr3, 'aval3')
        self.assertEqual(elm.atr4, 'aval4')
        self.assertEqual(elm.atr5, True)
        self.assertEqual(elm.id, 'ididid')
        self.assertEqual(elm.className, 'cls1 cls2 cls3')
        self.assertEqual(elm.style, {'background-color': 'green', 'font-size': '14'})
        self.assertEqual(elm.style.backgroundColor, 'green')
        self.assertEqual(elm.style.fontSize, '14')
        self.assertEqual(elm.textContent, 'vvv')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        self.assertEqual(ddd['_objid_'], preid)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'tagtxt'})
        self.assertTrue(elm._id in document._obj_dic)
        self.assertEqual(document._obj_dic[elm.id], elm)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'atr3': 'aval3'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'atr4': 'aval4'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'ididid'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': 'ididid', 'className': 'cls1 cls2  cls3'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': 'ididid', '_setStyle': {'background-color': 'green'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': 'ididid', '_setStyle': {'font-size': '14'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': 'ididid', 'textContent': 'vvv'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # add_handler
        del document._diffdat[:]
        ddcnt = 0
        elm = document.tag('tagwopt', handler=('event2', fnc2))
        self.assertEqual(elm.tagName, 'tagwopt')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(len(elm._eventlisteners), 1)
        self.assertTrue(('event2', fnc2) in elm._eventlisteners)
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'tagwopt'})
        self.assertTrue(elm._id in document._obj_dic)
        self.assertEqual(document._obj_dic[elm._id], elm)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_addEventListener': ['event2', repr(fnc2)]} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # create_with without arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.create_with('cwtag')
        self.assertEqual(elm.tagName, 'cwtag')
        self.assertEqual(type(elm), domdom.Element)
        self.assertFalse('type' in elm.__dict__)
        self.assertFalse('value' in elm.__dict__)
        self.assertFalse('src' in elm.__dict__)
        self.assertFalse('textContent' in elm.__dict__)
        self.assertFalse('checked' in elm.__dict__)
        self.assertFalse('selectedIndex' in elm.__dict__)
        self.assertEqual(elm.name, None)
        self.assertFalse('min' in elm.__dict__)
        self.assertFalse('max' in elm.__dict__)
        self.assertFalse('step' in elm.__dict__)
        self.assertFalse('minlength' in elm.__dict__)
        self.assertFalse('maxlength' in elm.__dict__)
        self.assertFalse('pattern' in elm.__dict__)
        self.assertFalse('multiple' in elm.__dict__)
        self.assertFalse('size' in elm.__dict__)
        self.assertFalse('label' in elm.__dict__)
        self.assertFalse('selected' in elm.__dict__)
        self.assertFalse('rows' in elm.__dict__)
        self.assertFalse('cols' in elm.__dict__)
        self.assertFalse('alt' in elm.__dict__)
        self.assertFalse('width' in elm.__dict__)
        self.assertFalse('height' in elm.__dict__)
        self.assertFalse('href' in elm.__dict__)
        self.assertFalse('rel' in elm.__dict__)
        self.assertFalse('integrity' in elm.__dict__)
        self.assertFalse('media' in elm.__dict__)
        self.assertFalse('scoped' in elm.__dict__)
        self.assertFalse('crossorigin' in elm.__dict__)
        self.assertFalse('longdesc' in elm.__dict__)
        self.assertFalse('sizes' in elm.__dict__)
        self.assertFalse('referrerpolicy' in elm.__dict__)
        self.assertFalse('srcset' in elm.__dict__)
        self.assertFalse('download' in elm.__dict__)
        self.assertFalse('target' in elm.__dict__)
        self.assertFalse('readonly' in elm.__dict__)
        self.assertFalse('disabled' in elm.__dict__)
        self.assertFalse('placeholder' in elm.__dict__)
        self.assertFalse('for_' in elm.__dict__)
        self.assertFalse('id' in elm.__dict__)
        self.assertFalse('accesskey' in elm.__dict__)
        self.assertFalse('hidden' in elm.__dict__)
        self.assertFalse('tabindex' in elm.__dict__)
        self.assertFalse('title' in elm.__dict__)
        self.assertEqual(elm.className, '')
        self.assertEqual(elm.style, {})
        self.assertEqual(elm.childList, [])
        self.assertFalse('onclick' in elm.__dict__)
        self.assertFalse('onchange' in elm.__dict__)
        self.assertEqual(len(elm._eventlisteners), 0)
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'cwtag'})
        self.assertTrue(elm._id in document._obj_dic)
        self.assertEqual(document._obj_dic[elm._id], elm)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # create_with with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.create_with('cwtagid', id_='vid')
        self.assertEqual(elm.tagName, 'cwtagid')
        self.assertEqual(type(elm), domdom.Element)
        self.assertFalse('type' in elm.__dict__)
        self.assertFalse('value' in elm.__dict__)
        self.assertFalse('src' in elm.__dict__)
        self.assertFalse('textContent' in elm.__dict__)
        self.assertFalse('checked' in elm.__dict__)
        self.assertFalse('selectedIndex' in elm.__dict__)
        self.assertEqual(elm.name, None)
        self.assertFalse('min' in elm.__dict__)
        self.assertFalse('max' in elm.__dict__)
        self.assertFalse('step' in elm.__dict__)
        self.assertFalse('minlength' in elm.__dict__)
        self.assertFalse('maxlength' in elm.__dict__)
        self.assertFalse('pattern' in elm.__dict__)
        self.assertFalse('multiple' in elm.__dict__)
        self.assertFalse('size' in elm.__dict__)
        self.assertFalse('label' in elm.__dict__)
        self.assertFalse('selected' in elm.__dict__)
        self.assertFalse('rows' in elm.__dict__)
        self.assertFalse('cols' in elm.__dict__)
        self.assertFalse('alt' in elm.__dict__)
        self.assertFalse('width' in elm.__dict__)
        self.assertFalse('height' in elm.__dict__)
        self.assertFalse('href' in elm.__dict__)
        self.assertFalse('rel' in elm.__dict__)
        self.assertFalse('integrity' in elm.__dict__)
        self.assertFalse('media' in elm.__dict__)
        self.assertFalse('scoped' in elm.__dict__)
        self.assertFalse('crossorigin' in elm.__dict__)
        self.assertFalse('longdesc' in elm.__dict__)
        self.assertFalse('sizes' in elm.__dict__)
        self.assertFalse('referrerpolicy' in elm.__dict__)
        self.assertFalse('srcset' in elm.__dict__)
        self.assertFalse('download' in elm.__dict__)
        self.assertFalse('target' in elm.__dict__)
        self.assertFalse('readonly' in elm.__dict__)
        self.assertFalse('disabled' in elm.__dict__)
        self.assertFalse('placeholder' in elm.__dict__)
        self.assertFalse('for_' in elm.__dict__)
        self.assertEqual(elm.id, 'vid')
        self.assertFalse('accesskey' in elm.__dict__)
        self.assertFalse('hidden' in elm.__dict__)
        self.assertFalse('tabindex' in elm.__dict__)
        self.assertFalse('title' in elm.__dict__)
        self.assertEqual(elm.className, '')
        self.assertEqual(elm.style, {})
        self.assertEqual(elm.childList, [])
        self.assertFalse('onclick' in elm.__dict__)
        self.assertFalse('onchange' in elm.__dict__)
        self.assertEqual(len(elm._eventlisteners), 0)
        ddcnt += 1
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['id'], 'vid')
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # create_with with arg wighout id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.create_with('cwtagwa', type_='vtype', value='vvalue',
                                   src='vsrc', name='vname',
                                   textContent='vtextContent',
                                   checked='vchecked', selectedIndex=123,
                                   min=-100, max=200, step=12,
                                   minlength=6, maxlength=11, pattern='vpattern',
                                   multiple='vmultiple',
                                   size=98, label='vlabel', selected='vselected',
                                   rows=77, cols=88,
                                   alt='valt', width=99, height=111,
                                   href='vhref', rel='vrel',
                                   integrity='vintegrity', media='vmedia',
                                   scoped='vscoped', crossorigin='vcrossorigin',
                                   longdesc='vlongdesc', sizes='vsizes',
                                   referrerpolicy='vreferrerpolicy',
                                   srcset='vsrcset', download='vdownload',
                                   target='vtarget',
                                   readonly='vreadonly', disabled='vdisabled',
                                   placeholder='vplaceholder', for_='vfor',
                                   accesskey='vaccesskey',
                                   hidden='vhidden', tabindex='vtabindex',
                                   title='vtitle',
                                   style='vstyle: vs', className='vclassName',
                                   childList=[elm1, elm2],
                                   onclick=fnc1, onchange=fnc2, handler=('mousemove', fnc3))
        self.assertEqual(elm.tagName, 'cwtagwa')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.type, 'vtype')
        self.assertEqual(elm.value, 'vvalue')
        self.assertEqual(elm.src, 'vsrc')
        self.assertEqual(elm.textContent, 'vtextContent')
        self.assertEqual(elm.checked, 'vchecked')
        self.assertEqual(elm.selectedIndex, 123)
        self.assertEqual(elm.name, 'vname')
        self.assertEqual(elm.min, -100)
        self.assertEqual(elm.max, 200)
        self.assertEqual(elm.step, 12)
        self.assertEqual(elm.minlength, 6)
        self.assertEqual(elm.maxlength, 11)
        self.assertEqual(elm.pattern, 'vpattern')
        self.assertEqual(elm.multiple, 'vmultiple')
        self.assertEqual(elm.size, 98)
        self.assertEqual(elm.label, 'vlabel')
        self.assertEqual(elm.selected, 'vselected')
        self.assertEqual(elm.rows, 77)
        self.assertEqual(elm.cols, 88)
        self.assertEqual(elm.alt, 'valt')
        self.assertEqual(elm.width, 99)
        self.assertEqual(elm.height, 111)
        self.assertEqual(elm.href, 'vhref')
        self.assertEqual(elm.rel, 'vrel')
        self.assertEqual(elm.integrity, 'vintegrity')
        self.assertEqual(elm.media, 'vmedia')
        self.assertEqual(elm.scoped, 'vscoped')
        self.assertEqual(elm.crossorigin, 'vcrossorigin')
        self.assertEqual(elm.longdesc, 'vlongdesc')
        self.assertEqual(elm.sizes, 'vsizes')
        self.assertEqual(elm.referrerpolicy, 'vreferrerpolicy')
        self.assertEqual(elm.srcset, 'vsrcset')
        self.assertEqual(elm.download, 'vdownload')
        self.assertEqual(elm.target, 'vtarget')
        self.assertEqual(elm.readonly, 'vreadonly')
        self.assertEqual(elm.disabled, 'vdisabled')
        self.assertEqual(elm.placeholder, 'vplaceholder')
        self.assertEqual(elm.for_, 'vfor')
        self.assertEqual(elm.accesskey, 'vaccesskey')
        self.assertEqual(elm.hidden, 'vhidden')
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.className, 'vclassName')
        self.assertEqual(elm.style.cssText, 'vstyle: vs;')
        self.assertEqual(elm.childList, [elm1, elm2])
        self.assertEqual(elm.onclick, fnc1)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm._eventlisteners, [('mousemove', fnc3),])
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'vtype'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'vvalue'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'src': 'vsrc'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'vtextContent'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'checked': 'vchecked'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'selectedIndex': 123} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'name': 'vname'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'min': -100} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'max': 200} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'step': 12} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'minlength': 6} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'maxlength': 11} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'pattern': 'vpattern'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'multiple': 'vmultiple'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'size': 98} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'label': 'vlabel'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'selected': 'vselected'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'rows': 77} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'cols': 88} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'alt': 'valt'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'width': 99} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'height': 111} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'href': 'vhref'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'rel': 'vrel'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'integrity': 'vintegrity'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'media': 'vmedia'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'scoped': 'vscoped'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'crossorigin': 'vcrossorigin'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'longdesc': 'vlongdesc'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'sizes': 'vsizes'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'referrerpolicy': 'vreferrerpolicy'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'srcset': 'vsrcset'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'download': 'vdownload'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'target': 'vtarget'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': 'vreadonly'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': 'vdisabled'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'placeholder': 'vplaceholder'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'for_': 'vfor'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'accesskey': 'vaccesskey'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'hidden': 'vhidden'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'vclassName'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'vstyle': 'vs'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_appendChild': elm1._id} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_appendChild': elm2._id} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onclick': repr(fnc1)} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_addEventListener': ['mousemove', repr(fnc3)]} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        def test_textcontent_id(fnc, name):
            # fnc no arg
            del document._diffdat[:]
            ddcnt = 0
            elm = fnc('{}text'.format(name))
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.textContent, '{}text'.format(name))
            ddd = document._diffdat[ddcnt]
            self.assertEqual(ddd['_objid_'], elm._id)
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': elm._id, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'textContent': '{}text'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)

            # fnc with id
            elm = fnc('{}text'.format(name), id_='id{}'.format(name))
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.textContent, '{}text'.format(name))
            self.assertEqual(elm.id, 'id{}'.format(name))
            ddd = document._diffdat[ddcnt]
            preid = ddd['_objid_']
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': preid, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': preid, 'textContent': '{}text'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': preid, 'id': 'id{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)
            return ddcnt

        def test_noarg_tag_id(fnc, name):
            # fnc no arg
            del document._diffdat[:]
            ddcnt = 0
            elm = fnc()
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            ddd = document._diffdat[ddcnt]
            self.assertEqual(ddd['_objid_'], elm._id)
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': elm._id, 'tagName': name})
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)

            # fnc with id
            elm = fnc(id_='id{}'.format(name))
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.id, 'id{}'.format(name))
            ddd = document._diffdat[ddcnt]
            preid = ddd['_objid_']
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': preid, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': preid, 'id': 'id{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)
            return ddcnt

        def test_text_type_id(fnc, name, typ):
            # no arg
            del document._diffdat[:]
            ddcnt = 0
            elm = fnc('t{}'.format(name))
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.type, typ)
            self.assertEqual(elm.textContent, 't{}'.format(name))
            ddd = document._diffdat[ddcnt]
            self.assertEqual(ddd['_objid_'], elm._id)
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': elm._id, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'type': typ} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'textContent': 't{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)

            # with id
            del document._diffdat[:]
            ddcnt = 0
            elm = fnc('t{}'.format(name), id_='id{}'.format(name))
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.type, typ)
            self.assertEqual(elm.textContent, 't{}'.format(name))
            self.assertEqual(elm.id, 'id{}'.format(name))
            ddd = document._diffdat[ddcnt]
            preid = ddd['_objid_']
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': preid, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': preid, 'type': typ} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': preid, 'textContent': 't{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': preid, 'id': 'id{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)
            return ddcnt

        def test_value_type_id(fnc, name, typ):
            # no arg
            del document._diffdat[:]
            ddcnt = 0
            elm = fnc('v{}'.format(name))
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.type, typ)
            self.assertEqual(elm.value, 'v{}'.format(name))
            ddd = document._diffdat[ddcnt]
            self.assertEqual(ddd['_objid_'], elm._id)
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': elm._id, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'type': typ} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'value': 'v{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)

            # with id
            del document._diffdat[:]
            ddcnt = 0
            elm = fnc('v{}'.format(name), id_='id{}'.format(name))
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.type, typ)
            self.assertEqual(elm.value, 'v{}'.format(name))
            self.assertEqual(elm.id, 'id{}'.format(name))
            ddd = document._diffdat[ddcnt]
            preid = ddd['_objid_']
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': preid, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': preid, 'type': typ} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': preid, 'value': 'v{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': preid, 'id': 'id{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)
            return ddcnt

        def test_value_id(fnc, name):
            # no arg
            del document._diffdat[:]
            ddcnt = 0
            elm = fnc('v{}'.format(name))
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.value, 'v{}'.format(name))
            ddd = document._diffdat[ddcnt]
            self.assertEqual(ddd['_objid_'], elm._id)
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': elm._id, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'value': 'v{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)

            # with id
            del document._diffdat[:]
            ddcnt = 0
            elm = fnc('v{}'.format(name), id_='id{}'.format(name))
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.value, 'v{}'.format(name))
            self.assertEqual(elm.id, 'id{}'.format(name))
            ddd = document._diffdat[ddcnt]
            preid = ddd['_objid_']
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': preid, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': preid, 'value': 'v{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': preid, 'id': 'id{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)
            return ddcnt

        def test_title(fnc, name):
            return test_textcontent_id(fnc, name)
        ddcnt = test_title(document.title, 'title')

        # style no arg
        ddcnt = test_text_type_id(document.style, 'style', 'text/css')

        # style with arg
        del document._diffdat[:]
        ddcnt = 0
        name = 'style'
        typ = 'text/css'
        elm = document.style('t{}'.format(name), media='wmedia', scoped='wscoped')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, name)
        self.assertEqual(elm.type, typ)
        self.assertEqual(elm.textContent, 't{}'.format(name))
        self.assertEqual(elm.media, 'wmedia')
        self.assertEqual(elm.scoped, 'wscoped')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': name})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': typ} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 't{}'.format(name)} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'media': 'wmedia'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'scoped': 'wscoped'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # link no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.link('wlink')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'link')
        self.assertEqual(elm.href, 'wlink')
        self.assertEqual(elm.rel, 'stylesheet')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'link'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'href': 'wlink'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'rel': 'stylesheet'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # link with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.link('wlink', id_='id0003')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'link')
        self.assertEqual(elm.href, 'wlink')
        self.assertEqual(elm.rel, 'stylesheet')
        self.assertEqual(elm.id, 'id0003')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'link'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'href': 'wlink'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'rel': 'stylesheet'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'id0003'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # link with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.link('wlink', integrity='wintegrity', media='wmedia')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'link')
        self.assertEqual(elm.href, 'wlink')
        self.assertEqual(elm.rel, 'stylesheet')
        self.assertEqual(elm.integrity, 'wintegrity')
        self.assertEqual(elm.media, 'wmedia')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'link'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'href': 'wlink'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'rel': 'stylesheet'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'integrity': 'wintegrity'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'media': 'wmedia'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # script no arg
        ddcnt = test_text_type_id(document.script, 'script', 'text/javascript')

        # script with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.script('wscript', src='wsrc', crossorigin='wcrossorigin')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'script')
        self.assertEqual(elm.type, 'text/javascript')
        self.assertEqual(elm.textContent, 'wscript')
        self.assertEqual(elm.src, 'wsrc')
        self.assertEqual(elm.crossorigin, 'wcrossorigin')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'script'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'text/javascript'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'src': 'wsrc'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'wscript'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'crossorigin': 'wcrossorigin'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # br no arg
        ddcnt = test_noarg_tag_id(document.br, 'br')

        # p no arg
        ddcnt = test_textcontent_id(document.p, 'p')

        # p with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.p('wp', tabindex='vtabindex', title='vtitle',
                         style='color: black', className='cls1 cls2')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'p')
        self.assertEqual(elm.textContent, 'wp')
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'p'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'wp'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # span no arg
        ddcnt = test_textcontent_id(document.span, 'span')

        # span with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.span('wspan', tabindex='vtabindex', title='vtitle',
                            style='color: black', className='cls1 cls2')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'span')
        self.assertEqual(elm.textContent, 'wspan')
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'span'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'wspan'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # div no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.div('wdiv')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'div')
        self.assertEqual(elm.textContent, 'wdiv')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'div'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'wdiv'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # div with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.div('wdiv', id_='id0009')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'div')
        self.assertEqual(elm.textContent, 'wdiv')
        self.assertEqual(elm.id, 'id0009')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'div'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'textContent': 'wdiv'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'id0009'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # div with arg
        del document._diffdat[:]
        ddcnt = 0
        elm1 = document.createElement('button')
        elm2 = document.createElement('button')
        elm3 = document.createElement('button')
        ddcnt += 3
        elm = document.div('wdiv', tabindex='vtabindex', title='vtitle',
                           style='color: black', className='cls1 cls2',
                           childList=[elm1, elm3])
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'div')
        self.assertEqual(elm.textContent, 'wdiv')
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'div'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'wdiv'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_appendChild': elm1._id} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_appendChild': elm3._id} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # button no arg & with id
        ddcnt = test_text_type_id(document.button, 'button', 'button')

        # button with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.button('wbutton', name='nbutton', value='vbutton',
                              disabled=True, onclick=fnc1,
                              tabindex='vtabindex', title='vtitle',
                              style='color: black', className='cls1 cls2')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'button')
        self.assertEqual(elm.type, 'button')
        self.assertEqual(elm.textContent, 'wbutton')
        self.assertEqual(elm.name, 'nbutton')
        self.assertEqual(elm.value, 'vbutton')
        self.assertEqual(elm.disabled, True)
        self.assertEqual(elm.onclick, fnc1)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'button'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'button'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'vbutton'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'wbutton'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'name': 'nbutton'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onclick': repr(fnc1)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # text no arg
        ddcnt = test_value_type_id(document.text, 'input', 'text')

        # text with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.text('wtext', readonly=True, disabled=False,
                            placeholder='ptext', pattern='vpattern',
                            minlength='vminlength', maxlength='vmaxlength',
                            size='vsize', tabindex='vtabindex', title='vtitle',
                            style='color: black', className='cls1 cls2',
                            onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'text')
        self.assertEqual(elm.value, 'wtext')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.placeholder, 'ptext')
        self.assertEqual(elm.pattern, 'vpattern')
        self.assertEqual(elm.minlength, 'vminlength')
        self.assertEqual(elm.maxlength, 'vmaxlength')
        self.assertEqual(elm.size, 'vsize')
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'text'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wtext'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'placeholder': 'ptext'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'pattern': 'vpattern'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'minlength': 'vminlength'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'maxlength': 'vmaxlength'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'size': 'vsize'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # checkbox no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.checkbox()
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'checkbox')
        self.assertEqual(elm.checked, False)
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'checkbox'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'checked': False} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # checkbox with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.checkbox(id_='id0012')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'checkbox')
        self.assertEqual(elm.id, 'id0012')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'type': 'checkbox'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'checked': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'id0012'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # checkbox with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.checkbox(checked=True, value='vcheckbox',
                                readonly=True, disabled=False,
                                tabindex='vtabindex', title='vtitle',
                                style='color: black', className='cls1 cls2',
                                onchange=fnc3)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'checkbox')
        self.assertEqual(elm.checked, True)
        self.assertEqual(elm.value, 'vcheckbox')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc3)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'checkbox'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'vcheckbox'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'checked': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc3)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # radio no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.radio('nradio', 'vradio')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'radio')
        self.assertEqual(elm.value, 'vradio')
        self.assertEqual(elm.checked, False)
        self.assertEqual(elm.name, 'nradio')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'radio'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'vradio'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'checked': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'name': 'nradio'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # radio with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.radio('nradio', 'vradio', id_='id0013')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'radio')
        self.assertEqual(elm.value, 'vradio')
        self.assertEqual(elm.checked, False)
        self.assertEqual(elm.name, 'nradio')
        self.assertEqual(elm.id, 'id0013')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'type': 'radio'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'value': 'vradio'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'checked': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'name': 'nradio'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'id0013'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # radio with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.radio('nradio', 'vradio', checked=True,
                            readonly=True, disabled=False,
                             tabindex='vtabindex', title='vtitle',
                            style='color: black', className='cls1 cls2',
                            onchange=fnc3)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'radio')
        self.assertEqual(elm.value, 'vradio')
        self.assertEqual(elm.checked, True)
        self.assertEqual(elm.name, 'nradio')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc3)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'radio'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'vradio'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'checked': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'name': 'nradio'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc3)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # color no arg
        ddcnt = test_value_type_id(document.color, 'input', 'color')

        # color with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.color('wcolor', readonly=True, disabled=False,
                             tabindex='vtabindex', title='vtitle',
                             style='color: black', className='cls1 cls2',
                             onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'color')
        self.assertEqual(elm.value, 'wcolor')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'color'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wcolor'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # date no arg
        ddcnt = test_value_type_id(document.date, 'input', 'date')

        # date with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.date('wdate', readonly=True, disabled=False,
                            tabindex='vtabindex', title='vtitle',
                            style='color: black', className='cls1 cls2',
                            onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'date')
        self.assertEqual(elm.value, 'wdate')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'date'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wdate'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # datetime_local no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.datetime_local('wdatetime_local')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'datetime-local')
        self.assertEqual(elm.step, '1')
        self.assertEqual(elm.value, 'wdatetime_local')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'datetime-local'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wdatetime_local'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'step': '1'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # datetime_local with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.datetime_local('wdatetime_local', id_='id0016')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'datetime-local')
        self.assertEqual(elm.step, '1')
        self.assertEqual(elm.value, 'wdatetime_local')
        self.assertEqual(elm.id, 'id0016')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'type': 'datetime-local'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'value': 'wdatetime_local'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'step': '1'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'id0016'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # datetime_local with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.datetime_local('wdatetime_local', readonly=True, disabled=False,
                                      tabindex='vtabindex', title='vtitle',
                                      style='color: black', className='cls1 cls2',
                                      onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'datetime-local')
        self.assertEqual(elm.step, '1')
        self.assertEqual(elm.value, 'wdatetime_local')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'datetime-local'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wdatetime_local'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'step': '1'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # month no arg
        ddcnt = test_value_type_id(document.month, 'input', 'month')

        # month with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.month('wmonth', readonly=True, disabled=False,
                            tabindex='vtabindex', title='vtitle',
                            style='color: black', className='cls1 cls2',
                            onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'month')
        self.assertEqual(elm.value, 'wmonth')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'month'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wmonth'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # time no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.time('wtime')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'time')
        self.assertEqual(elm.step, '1')
        self.assertEqual(elm.value, 'wtime')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'time'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wtime'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'step': '1'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # time with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.time('wtime', id_='idtime')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'time')
        self.assertEqual(elm.step, '1')
        self.assertEqual(elm.value, 'wtime')
        self.assertEqual(elm.id, 'idtime')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'type': 'time'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'value': 'wtime'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'step': '1'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'idtime'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # time with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.time('wtime', readonly=True, disabled=False,
                            tabindex='vtabindex', title='vtitle',
                            style='color: black', className='cls1 cls2',
                            onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'time')
        self.assertEqual(elm.step, '1')
        self.assertEqual(elm.value, 'wtime')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'time'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wtime'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'step': '1'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # week no arg & with id
        ddcnt = test_value_type_id(document.week, 'input', 'week')

        # week with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.week('wweek', readonly=True, disabled=False,
                            tabindex='vtabindex', title='vtitle',
                            style='color: black', className='cls1 cls2',
                            onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'week')
        self.assertEqual(elm.value, 'wweek')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'week'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wweek'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # file no arg & with id
        ddcnt = test_value_type_id(document.file, 'input', 'file')

        # file with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.file('wfile', readonly=True, disabled=False,
                            tabindex='vtabindex', title='vtitle',
                            style='color: black', className='cls1 cls2',
                            onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'file')
        self.assertEqual(elm.value, 'wfile')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'file'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wfile'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # number no arg & with id
        ddcnt = test_value_type_id(document.number, 'input', 'number')

        # number with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.number('wnumber', min=-555, max=444, step=12,
                              readonly=True, disabled=False,
                              tabindex='vtabindex', title='vtitle',
                              style='color: black', className='cls1 cls2',
                              onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'number')
        self.assertEqual(elm.min, -555)
        self.assertEqual(elm.max, 444)
        self.assertEqual(elm.step, 12)
        self.assertEqual(elm.value, 'wnumber')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'number'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wnumber'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'min': -555} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'max': 444} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'step': 12} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # password no arg & with id
        ddcnt = test_value_type_id(document.password, 'input', 'password')

        # password with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.password('wpassword', readonly=True, disabled=False,
                                tabindex='vtabindex', title='vtitle',
                                style='color: black', className='cls1 cls2',
                                onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'password')
        self.assertEqual(elm.value, 'wpassword')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'password'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wpassword'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # range no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.range('wrange')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'range')
        self.assertEqual(elm.value, 'wrange')
        self.assertEqual(elm.min, '0')
        self.assertEqual(elm.max, '100')
        self.assertEqual(elm.step, '1')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'range'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wrange'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'min': '0'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'max': '100'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'step': '1'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # range with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.range('wrange', id_='idrange')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'range')
        self.assertEqual(elm.value, 'wrange')
        self.assertEqual(elm.min, '0')
        self.assertEqual(elm.max, '100')
        self.assertEqual(elm.step, '1')
        self.assertEqual(elm.id, 'idrange')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'type': 'range'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'value': 'wrange'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'min': '0'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'max': '100'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'step': '1'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'idrange'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # range with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.range('wrange', min=-555, max=444, step=12,
                             readonly=True, disabled=False,
                             tabindex='vtabindex', title='vtitle',
                             style='color: black', className='cls1 cls2',
                             onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'input')
        self.assertEqual(elm.type, 'range')
        self.assertEqual(elm.min, -555)
        self.assertEqual(elm.max, 444)
        self.assertEqual(elm.step, 12)
        self.assertEqual(elm.value, 'wrange')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'input'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'type': 'range'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wrange'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'min': -555} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'max': 444} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'step': 12} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # select no arg & with id
        ddcnt = test_value_id(document.select, 'select')

        # select with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.select('wselect', selectedIndex=19, name='nselect',
                              multiple='mselect', size=91,
                              readonly=True, disabled=False,
                              tabindex='vtabindex', title='vtitle',
                              style='color: black', className='cls1 cls2',
                              onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'select')
        self.assertEqual(elm.selectedIndex, 19)
        self.assertEqual(elm.name, 'nselect')
        self.assertEqual(elm.multiple, 'mselect')
        self.assertEqual(elm.size, 91)
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'select'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'wselect'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'selectedIndex': 19} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'name': 'nselect'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'multiple': 'mselect'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'size': 91} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # option no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.option('voption', 'coption')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'option')
        self.assertEqual(elm.value, 'voption')
        self.assertEqual(elm.textContent, 'coption')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'option'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'voption'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'coption'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # option with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.option('voption', 'coption', id_='idoption')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'option')
        self.assertEqual(elm.value, 'voption')
        self.assertEqual(elm.textContent, 'coption')
        self.assertEqual(elm.id, 'idoption')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'option'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'value': 'voption'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'textContent': 'coption'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'idoption'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # option with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.option('voption', 'coption',
                              label='loption', selected=True,
                              readonly=True, disabled=False,
                              tabindex='vtabindex', title='vtitle',
                              style='color: black', className='cls1 cls2',
                              onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'option')
        self.assertEqual(elm.value, 'voption')
        self.assertEqual(elm.textContent, 'coption')
        self.assertEqual(elm.label, 'loption')
        self.assertEqual(elm.selected, True)
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'option'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'voption'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'coption'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'label': 'loption'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'selected': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # textarea no arg
        ddcnt = test_value_id(document.textarea, 'textarea')

        # textarea with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.textarea('vtextarea',
                                rows=89, cols=76,
                                readonly=True, disabled=False,
                                tabindex='vtabindex', title='vtitle',
                                style='color: black', className='cls1 cls2',
                                onchange=fnc2)
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'textarea')
        self.assertEqual(elm.value, 'vtextarea')
        self.assertEqual(elm.rows, 89)
        self.assertEqual(elm.cols, 76)
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.onchange, fnc2)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'textarea'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'value': 'vtextarea'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'rows': 89} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'cols': 76} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'onchange': repr(fnc2)} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # table no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.table()
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'table')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'table'})
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # table with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.table(id_='idtable')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'table')
        self.assertEqual(elm.id, 'idtable')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'table'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'idtable'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # table with arg
        elm1 = document.createElement('button')
        elm2 = document.createElement('button')
        elm3 = document.createElement('button')
        ddcnt += 3
        del document._diffdat[:]
        ddcnt = 0
        elm = document.table(readonly=True, disabled=False,
                             tabindex='vtabindex', title='vtitle',
                             style='color: black', className='cls1 cls2',
                             childList=[elm1, elm2])
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'table')
        self.assertEqual(elm.readonly, True)
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        self.assertEqual(elm.childList, [elm1, elm2])
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'table'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'readonly': True} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_appendChild': elm1._id} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_appendChild': elm2._id} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # tr no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.tr()
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'tr')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'tr'})
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # tr with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.tr(id_='idtr')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'tr')
        self.assertEqual(elm.id, 'idtr')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'tr'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'idtr'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # tr with arg
        del document._diffdat[:]
        ddcnt = 0
        elm1 = document.createElement('button')
        elm2 = document.createElement('button')
        elm3 = document.createElement('button')
        ddcnt += 3
        elm = document.tr(tabindex='vtabindex', title='vtitle',
                          style='color: black', className='cls1 cls2',
                          childList=[elm3, elm2])
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'tr')
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        self.assertEqual(elm.childList, [elm3, elm2])
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'tr'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_appendChild': elm3._id} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_appendChild': elm2._id} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # th no arg & with id
        ddcnt = test_textcontent_id(document.th, 'th')

        # th with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.th('thtext', tabindex='vtabindex', title='vtitle',
                          style='color: black', className='cls1 cls2')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'th')
        self.assertEqual(elm.textContent, 'thtext')
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'th'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'thtext'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # td no arg & with id
        ddcnt = test_textcontent_id(document.td, 'td')

        # td with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.td('tdtext', tabindex='vtabindex', title='vtitle',
                          style='color: black', className='cls1 cls2')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'td')
        self.assertEqual(elm.textContent, 'tdtext')
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'td'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'tdtext'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # fieldset no arg & with id
        ddcnt = test_textcontent_id(document.fieldset, 'fieldset')

        # fieldset with arg
        elm1 = document.createElement('button')
        elm2 = document.createElement('button')
        elm3 = document.createElement('button')
        ddcnt += 3
        del document._diffdat[:]
        ddcnt = 0
        elm = document.fieldset(textContent='cfieldset', disabled=False,
                                tabindex='vtabindex', title='vtitle',
                                style='color: black', className='cls1 cls2',
                                childList=[elm1, elm2])
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'fieldset')
        self.assertEqual(elm.textContent, 'cfieldset')
        self.assertEqual(elm.disabled, False)
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        self.assertEqual(elm.childList, [elm1, elm2])
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'fieldset'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'cfieldset'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'disabled': False} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_appendChild': elm1._id} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_appendChild': elm2._id} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # legend no arg & with id
        ddcnt = test_textcontent_id(document.legend, 'legend')

        # legend with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.legend('legendtext', tabindex='vtabindex', title='vtitle',
                              style='color: black', className='cls1 cls2')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'legend')
        self.assertEqual(elm.textContent, 'legendtext')
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'legend'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'legendtext'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # img no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.img('simg')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'img')
        self.assertEqual(elm.src, 'simg')
        self.assertEqual(elm.alt, '')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'img'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'src': 'simg'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'alt': ''} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # img with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.img('simg', id_='idimg')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'img')
        self.assertEqual(elm.src, 'simg')
        self.assertEqual(elm.alt, '')
        self.assertEqual(elm.id, 'idimg')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'img'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'src': 'simg'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'alt': ''} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'idimg'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # img with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.img('simg', alt='aimg', width=123, height=45,
                           crossorigin='cimg', longdesc='limg', sizes='szimg',
                           referrerpolicy='rpimg', srcset='ssimg',
                           tabindex='vtabindex', title='vtitle',
                           style='color: black', className='cls1 cls2')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'img')
        self.assertEqual(elm.src, 'simg')
        self.assertEqual(elm.alt, 'aimg')
        self.assertEqual(elm.width, 123)
        self.assertEqual(elm.height, 45)
        self.assertEqual(elm.crossorigin, 'cimg')
        self.assertEqual(elm.longdesc, 'limg')
        self.assertEqual(elm.sizes, 'szimg')
        self.assertEqual(elm.referrerpolicy, 'rpimg')
        self.assertEqual(elm.srcset, 'ssimg')
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'img'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'src': 'simg'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'alt': 'aimg'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'width': 123} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'height': 45} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'crossorigin': 'cimg'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'longdesc': 'limg'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'sizes': 'szimg'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'referrerpolicy': 'rpimg'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'srcset': 'ssimg'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # a no arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.a('wa', 'ca')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'a')
        self.assertEqual(elm.href, 'wa')
        self.assertEqual(elm.textContent, 'ca')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'a'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'ca'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'href': 'wa'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # a with id
        del document._diffdat[:]
        ddcnt = 0
        elm = document.a('wa', 'ca', id_='ida')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'a')
        self.assertEqual(elm.textContent, 'ca')
        self.assertEqual(elm.href, 'wa')
        self.assertEqual(elm.id, 'ida')
        ddd = document._diffdat[ddcnt]
        preid = ddd['_objid_']
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': preid, 'tagName': 'a'})
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'textContent': 'ca'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'href': 'wa'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': preid, 'id': 'ida'} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # a with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.a('wa', 'ca', download='da', rel='ra',
                         target='ta', referrerpolicy='rpa',
                         tabindex='vtabindex', title='vtitle',
                         style='color: black', className='cls1 cls2')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'a')
        self.assertEqual(elm.textContent, 'ca')
        self.assertEqual(elm.href, 'wa')
        self.assertEqual(elm.rel, 'ra')
        self.assertEqual(elm.target, 'ta')
        self.assertEqual(elm.referrerpolicy, 'rpa')
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'a'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'ca'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'href': 'wa'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'rel': 'ra'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'referrerpolicy': 'rpa'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'download': 'da'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'target': 'ta'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        # label no arg & with id
        ddcnt = test_textcontent_id(document.label, 'label')

        # label with arg
        del document._diffdat[:]
        ddcnt = 0
        elm = document.label('labeltext', for_='flabel',
                             tabindex='vtabindex', title='vtitle',
                             style='color: black', className='cls1 cls2')
        self.assertEqual(type(elm), domdom.Element)
        self.assertEqual(elm.tagName, 'label')
        self.assertEqual(elm.textContent, 'labeltext')
        self.assertEqual(elm.for_, 'flabel')
        self.assertEqual(elm.tabindex, 'vtabindex')
        self.assertEqual(elm.title, 'vtitle')
        self.assertEqual(elm.style, {'color': 'black'})
        self.assertEqual(elm.className, 'cls1 cls2')
        ddd = document._diffdat[ddcnt]
        self.assertEqual(ddd['_objid_'], elm._id)
        s = ddd['_createElement']
        j = json.loads(s)
        self.assertEqual(j, {'_id': elm._id, 'tagName': 'label'})
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'textContent': 'labeltext'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'for_': 'flabel'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'tabindex': 'vtabindex'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'title': 'vtitle'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2'} in document._diffdat)
        ddcnt += 1
        self.assertTrue({'_objid_': elm._id, '_setStyle': {'color': 'black'}} in document._diffdat)
        ddcnt += 1
        self.assertEqual(len(document._diffdat), ddcnt)

        def test_h1(fnc, name):
            # h1 no arg & with id
            test_textcontent_id(fnc, name)

            # h1 with arg
            del document._diffdat[:]
            ddcnt = 0
            elm = fnc('{}text'.format(name), accesskey='a{}'.format(name),
                      hidden='h{}'.format(name),
                      tabindex='t{}'.format(name),
                      title='tt{}'.format(name),
                      style='{}: black'.format(name),
                      className='cls1 cls2 {}'.format(name))
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.textContent, '{}text'.format(name))
            self.assertEqual(elm.accesskey, 'a{}'.format(name))
            self.assertEqual(elm.tabindex, 't{}'.format(name))
            self.assertEqual(elm.title, 'tt{}'.format(name))
            self.assertEqual(elm.style, {name: 'black'})
            self.assertEqual(elm.className, 'cls1 cls2 {}'.format(name))
            ddd = document._diffdat[ddcnt]
            self.assertEqual(ddd['_objid_'], elm._id)
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': elm._id, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'textContent': '{}text'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'accesskey': 'a{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'hidden': 'h{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'tabindex': 't{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'title': 'tt{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2 {}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, '_setStyle': {name: 'black'}} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)
            return ddcnt

        test_h1(document.h1, 'h1')
        test_h1(document.h2, 'h2')
        test_h1(document.h3, 'h3')
        test_h1(document.h4, 'h4')
        test_h1(document.h5, 'h5')
        test_h1(document.h6, 'h6')

        def test_ol(fnc, name):
            # ol no arg & with id
            test_noarg_tag_id(fnc, name)
            # ol with arg
            elm1 = document.createElement('button')
            elm2 = document.createElement('button')
            del document._diffdat[:]
            ddcnt = 0
            elm = fnc(accesskey='a{}'.format(name),
                      hidden='h{}'.format(name),
                      tabindex='t{}'.format(name),
                      title='tt{}'.format(name),
                      style='{}: black'.format(name),
                      className='cls1 cls2 {}'.format(name),
                      childList=[elm1, elm2])
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.accesskey, 'a{}'.format(name))
            self.assertEqual(elm.tabindex, 't{}'.format(name))
            self.assertEqual(elm.title, 'tt{}'.format(name))
            self.assertEqual(elm.style, {name: 'black'})
            self.assertEqual(elm.className, 'cls1 cls2 {}'.format(name))
            self.assertEqual(elm.childList, [elm1, elm2])
            ddd = document._diffdat[ddcnt]
            self.assertEqual(ddd['_objid_'], elm._id)
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': elm._id, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'accesskey': 'a{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'hidden': 'h{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'tabindex': 't{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'title': 'tt{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2 {}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, '_setStyle': {name: 'black'}} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, '_appendChild': elm1.id} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, '_appendChild': elm2.id} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)
            return ddcnt
        test_ol(document.ol, 'ol')
        test_ol(document.ul, 'ul')

        def test_li(fnc, name):
            # li no arg & with id
            test_textcontent_id(fnc, name)
            # li with arg
            elm1 = document.createElement('button')
            elm2 = document.createElement('button')
            del document._diffdat[:]
            ddcnt = 0
            elm = fnc('{}text'.format(name), accesskey='a{}'.format(name),
                      hidden='h{}'.format(name),
                      tabindex='t{}'.format(name),
                      title='tt{}'.format(name),
                      style='{}: black'.format(name),
                      className='cls1 cls2 {}'.format(name),
                      childList=[elm1, elm2])
            self.assertEqual(type(elm), domdom.Element)
            self.assertEqual(elm.tagName, name)
            self.assertEqual(elm.textContent, '{}text'.format(name))
            self.assertEqual(elm.accesskey, 'a{}'.format(name))
            self.assertEqual(elm.tabindex, 't{}'.format(name))
            self.assertEqual(elm.title, 'tt{}'.format(name))
            self.assertEqual(elm.style, {name: 'black'})
            self.assertEqual(elm.className, 'cls1 cls2 {}'.format(name))
            self.assertEqual(elm.childList, [elm1, elm2])
            ddd = document._diffdat[ddcnt]
            self.assertEqual(ddd['_objid_'], elm._id)
            s = ddd['_createElement']
            j = json.loads(s)
            self.assertEqual(j, {'_id': elm._id, 'tagName': name})
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'textContent': '{}text'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'accesskey': 'a{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'hidden': 'h{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'tabindex': 't{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'title': 'tt{}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, 'className': 'cls1 cls2 {}'.format(name)} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, '_setStyle': {name: 'black'}} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, '_appendChild': elm1.id} in document._diffdat)
            ddcnt += 1
            self.assertTrue({'_objid_': elm._id, '_appendChild': elm2.id} in document._diffdat)
            ddcnt += 1
            self.assertEqual(len(document._diffdat), ddcnt)
            return ddcnt
        test_li(document.li, 'li')
        test_ol(document.section, 'section')
        test_ol(document.header, 'header')
        test_ol(document.footer, 'footer')


if __name__ == "__main__":
    unittest.main()
