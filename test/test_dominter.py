#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import json
import sys

from dominter.dom import Window, start_app
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
        slv = slice(0, 2147483647, None) if ispymaj(2) else slice(None, None, None)
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
        s3.removeProperty('topXxx')
        self.assertEqual(len(s3), 0)
        self.assertFalse(hasattr(s3, 'topXxx'))

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
        self.assertEqual(elm.attributes, {})
        self.assertEqual(type(elm._childList), domdom.ChildList)
        self.assertEqual(type(elm._classList), domdom.ClassList)
        self.assertEqual(type(elm._style), domdom.Style)
        self.assertIsNone(elm._onclick)
        self.assertIsNone(elm._onchange)
        self.assertEqual(elm._on, 0)
        #
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt-1]
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
            self.assertEqual(len(document.diffdat), ddcnt)
            ddd = document.diffdat[ddcnt-1]
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
        # __setattr__() id
        objdic = document.obj_dic
        self.assertEqual(len(objdic), 1)
        self.assertEqual(objdic[str(id(elm))], elm)

        def setid(preid, newid, ddcnt):
            elm.id = newid
            self.assertEqual(elm._id, newid)
            self.assertEqual(elm.id, newid)
            self.assertEqual(len(objdic), 1)
            self.assertEqual(objdic[newid], elm)
            ddcnt += 1
            self.assertEqual(len(document.diffdat), ddcnt)
            ddd = document.diffdat[ddcnt - 1]
            self.assertEqual(ddd['_objid_'], preid)
            self.assertEqual(ddd['id'], newid)
            return ddcnt
        ddcnt = setid(str(id(elm)), 'testid0', ddcnt)
        id1 = 'testid1'
        ddcnt = setid('testid0', id1, ddcnt)
        # __setattr__() className
        self.assertEqual(len(elm.classList), 0)
        cls1 = 'cls1'
        #
        elm.className = cls1
        self.assertEqual(elm.className, cls1)
        self.assertEqual(len(elm.classList), 1)
        self.assertEqual(elm.classList[0], cls1)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], cls1)
        cls2 = 'cls2'
        #
        elm.className = cls2
        self.assertEqual(elm.className, cls2)
        self.assertEqual(len(elm.classList), 1)
        self.assertEqual(elm.classList[0], cls2)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], cls2)
        cls3 = ''
        #
        elm.className = cls3
        self.assertEqual(elm.className, cls3)
        self.assertEqual(len(elm.classList), 0)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
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
            self.assertEqual(len(document.diffdat), lddcnt)
            ddd = document.diffdat[lddcnt - 1]
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
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], cls5b)
        # __setattr__() classList
        with self.assertRaises(TypeError):
            elm.classList = []
        # __setattr__() style
        elm.style = ''
        self.assertEqual(len(elm._style), 0)
        self.assertEqual(elm.style.cssText, '')
        self.assertEqual(elm.style, {})
        ddcnt += 0 # no change
        self.assertEqual(len(document.diffdat), ddcnt)
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
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], styl0)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], styl1)

        # __setattr__() onclick
        handlers = document.handlers
        self.assertEqual(len(handlers), 0)

        def onclick1(ev):
            pass
        #
        elm.onclick = onclick1
        self.assertEqual(elm._onclick, onclick1)
        self.assertEqual(elm.onclick, onclick1)
        self.assertEqual(handlers[repr(onclick1)], onclick1)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['onclick'], repr(onclick1))
        # __setattr__() onchange

        def onchange1(ev):
            pass
        #
        elm.onchange = onchange1
        self.assertEqual(elm._onchange, onchange1)
        self.assertEqual(elm.onchange, onchange1)
        self.assertEqual(handlers[repr(onchange1)], onchange1)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['onchange'], repr(onchange1))
        # __setattr__() others
        elm.foo = 'foovalue'
        self.assertEqual(elm.foo, 'foovalue')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['foo'], 'foovalue')
        #
        elm.bar = 'barvalue'
        self.assertEqual(elm.bar, 'barvalue')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['bar'], 'barvalue')
        #
        elm.baz = 'bazvalue'
        self.assertEqual(elm.baz, 'bazvalue')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
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
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)

        # childList append() to []
        elm.childList.append(chd2)
        self.assertEqual(elm.childList, [chd, chd2])
        self.assertEqual(chd2.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd2._id)

        # childList insert(0) to [x, y]
        elm.childList.insert(0, chd3)
        self.assertEqual(elm.childList, [chd3, chd, chd2])
        self.assertEqual(chd3.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd3._id, chd._id])

        # childList clear()
        elm.childList.clear()
        self.assertEqual(elm.childList, [])
        self.assertEqual(chd.parent, None)
        self.assertEqual(chd2.parent, None)
        self.assertEqual(chd3.parent, None)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearChild'], True)

        # childList set [x]
        elm.childList = [chd, ]
        self.assertEqual(elm.childList, [chd, ])
        self.assertEqual(chd.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)

        # childList insert(0) to [x]
        elm.childList.insert(0, chd2)
        self.assertEqual(elm.childList, [chd2, chd, ])
        self.assertEqual(chd2.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd2._id, chd._id])

        # childList insert(1) to [x, y]
        elm.childList.insert(1, chd3)
        self.assertEqual(elm.childList, [chd2, chd3, chd, ])
        self.assertEqual(chd3.parent, elm)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd3._id, chd._id])

        # childList clear()
        elm.childList.clear()
        self.assertEqual(elm.childList, [])
        self.assertEqual(chd.parent, None)
        self.assertEqual(chd2.parent, None)
        self.assertEqual(chd3.parent, None)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearChild'], True)

        # childList set [x, y]
        elm.childList = [chd, chd2]
        self.assertEqual(elm.childList, [chd, chd2])
        self.assertEqual(chd.parent, elm)
        self.assertEqual(chd2.parent, elm)
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd2._id)

        # childList append() to [x, y]
        elm.childList.append(chd3)
        self.assertEqual(elm.childList, [chd, chd2, chd3])
        self.assertEqual(chd3.parent, elm)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd3._id)

        # childList remove(y) from [x, y, z]
        elm.childList.remove(chd2)
        self.assertEqual(elm.childList, [chd, chd3])
        self.assertEqual(chd2.parent, None)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList remove(x) from [x, y]
        elm.childList.remove(chd)
        self.assertEqual(elm.childList, [chd3, ])
        self.assertEqual(chd.parent, None)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList extend([y, z]) to [x]
        elm.childList.extend([chd, chd2])
        self.assertEqual(elm.childList, [chd3, chd, chd2])
        self.assertEqual(chd.parent, elm)
        self.assertEqual(chd2.parent, elm)
        ddcnt += 2
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd2._id)

        # childList pop y from [x, y, z]
        chk = elm.childList.pop(1)
        self.assertEqual(chk, chd)
        self.assertEqual(elm.childList, [chd3, chd2])
        self.assertEqual(chd.parent, None)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList pop y from [x, y,]
        chk = elm.childList.pop(1)
        self.assertEqual(chk, chd2)
        self.assertEqual(elm.childList, [chd3, ])
        self.assertEqual(chd2.parent, None)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList pop x from [x,]
        chk = elm.childList.pop(0)
        self.assertEqual(chk, chd3)
        self.assertEqual(elm.childList, [])
        self.assertEqual(chd3.parent, None)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList set [x, y, z]
        elm.childList = [chd, chd2, chd3]
        self.assertEqual(elm.childList, [chd, chd2, chd3])
        self.assertEqual(chd.parent, elm)
        self.assertEqual(chd2.parent, elm)
        self.assertEqual(chd3.parent, elm)
        ddcnt += 3
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd2._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd3._id)

        # childList reverse()
        elm.childList.reverse()
        self.assertEqual(elm.childList, [chd3, chd2, chd])
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_reverseChild'], True)

        # childList sort()
        elm.childList.sort(lambda x: x.tagName)
        self.assertEqual(elm.childList, [chd2, chd3, chd])
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_sortChild'], [1, 0, 2, ])

        # childList set overwrite
        elm.childList = [chd, chd3]
        self.assertEqual(elm.childList, [chd, chd3])
        ddcnt += 3
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearChild'], True)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_appendChild'], chd3._id)

        # childList del 0 from [x, y]
        del elm.childList[0]
        self.assertEqual(elm.childList, [chd3])
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList del 0,1 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        del elm.childList[0:2]
        self.assertEqual(elm.childList, [chd3])
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList del 1,2 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        del elm.childList[1:3]
        self.assertEqual(elm.childList, [chd])
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList del 0 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        del elm.childList[0:1]
        self.assertEqual(elm.childList, [chd2, chd3])
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList del 1 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        del elm.childList[1]
        self.assertEqual(elm.childList, [chd, chd3])
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList del 2 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        del elm.childList[2:1000]
        self.assertEqual(elm.childList, [chd, chd2])
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList del -1 from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        del elm.childList[-1]
        self.assertEqual(elm.childList, [chd, chd2])
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList del -2: from [x, y, z]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        del elm.childList[-2:]
        self.assertEqual(elm.childList, [chd, ])
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem
        chd4 = document.createElement('chd4tag')
        chd5 = document.createElement('chd5tag')
        ddcnt += 2
        # childList setitem [0] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[0] = chd4
        self.assertEqual(elm.childList, [chd4, chd2, chd3])
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList setitem [-3] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[-3] = chd4
        self.assertEqual(elm.childList, [chd4, chd2, chd3])
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList setitem [1] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[1] = chd4
        self.assertEqual(elm.childList, [chd, chd4, chd3])
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [-2] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[1] = chd4
        self.assertEqual(elm.childList, [chd, chd4, chd3])
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [2] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[2] = chd4
        self.assertEqual(elm.childList, [chd, chd2, chd4])
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [-1] to [1,2,3]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[2] = chd4
        self.assertEqual(elm.childList, [chd, chd2, chd4])
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [1:5]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[1:5] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd4, chd5])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [-2:5]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[-2:5] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd4, chd5])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [1:]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[1:] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd4, chd5])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [-2:]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[-2:] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd4, chd5])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd2._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [0:2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[0:2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd5, chd3])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [-3:-1]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[-3:-1] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd5, chd3])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [:2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[:2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd5, chd3])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [:-1]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[:-1] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd5, chd3])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [0:3:2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[0:3:2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd2, chd5])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd3._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [-3::2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[-3::2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd4, chd2, chd5])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd3._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)

        # childList setitem [2:0:-1]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[2:0:-1] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd5, chd4])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [-1:0:-1]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[-1:0:-1] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd, chd5, chd4])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd2._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd2._id)

        # childList setitem [2::-2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[2::-2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd5, chd2, chd4])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # childList setitem [-1::-2]
        elm.childList = [chd, chd2, chd3]
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.childList[-1::-2] = [chd4, chd5]
        self.assertEqual(elm.childList, [chd5, chd2, chd4])
        ddcnt += 4
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd4.id, chd3._id])
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_insertBefore'], [chd5.id, chd._id])
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd3._id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeChild'], chd._id)

        # classList
        # classList clear by className
        elm.className = ''
        lst = elm.classList
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], '')
        self.assertEqual(len(lst), 0)

        # classList [].append(x)
        elm.classList.append('clsb1')
        self.assertEqual(len(lst), 1)
        self.assertEqual(lst[0], 'clsb1')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsb1', ])

        # classList [x].add(y)
        elm.classList.add('clsb2')
        self.assertEqual(len(lst), 2)
        self.assertEqual(lst[1], 'clsb2')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsb2', ])

        # classList [1,2].extend([3,4,5])
        elm.classList.extend(['clsb3', 'clsb4', 'clsb5'])
        self.assertEqual(len(lst), 5)
        self.assertEqual(lst[2], 'clsb3')
        self.assertEqual(lst[3], 'clsb4')
        self.assertEqual(lst[4], 'clsb5')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsb3', 'clsb4', 'clsb5'])

        # classList [1,2,3,4,5].insert(2, 1.5)
        elm.classList.insert(2, 'clsb1.5')
        self.assertEqual(len(lst), 6)
        self.assertEqual(elm.className, 'clsb1 clsb2 clsb1.5 clsb3 clsb4 clsb5')
        self.assertTrue(elm.classList.contains('clsb1'))
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsb1.5', ])

        # classList [1,2,1.5,3,4,5].remove(1)
        elm.classList.remove('clsb1')
        self.assertEqual(len(lst), 5)
        self.assertFalse(elm.classList.contains('clsb1'))
        self.assertTrue(elm.classList.contains('clsb4'))
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb1', ])

        # classList [2,1.5,3,4,5].remove(4)
        elm.classList.remove('clsb4')
        self.assertEqual(len(lst), 4)
        self.assertFalse(elm.classList.contains('clsb4'))
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3 clsb5')
        self.assertTrue(elm.classList.contains('clsb5'))
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb4', ])

        # classList [2,1.5,3,5].remove(5)
        elm.classList.remove('clsb5')
        self.assertEqual(len(lst), 3)
        self.assertFalse(elm.classList.contains('clsb5'))
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb5', ])

        # classList [2,1.5,3].toggle(6)
        elm.classList.toggle('clsb6')
        self.assertEqual(len(lst), 4)
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3 clsb6')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsb6', ])

        # classList [2,1.5,3,6].toggle(6)
        elm.classList.toggle('clsb6')
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb6', ])

        # classList [2,1.5,3].pop(1)
        cn = elm.classList.pop(1)
        self.assertEqual(cn, 'clsb1.5')
        self.assertEqual(len(lst), 2)
        self.assertEqual(elm.className, 'clsb2 clsb3')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb1.5', ])

        # classList [2,3].pop(1)
        cn = elm.classList.pop(1)
        self.assertEqual(cn, 'clsb3')
        self.assertEqual(len(lst), 1)
        self.assertEqual(elm.className, 'clsb2')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb3', ])

        # classList [2].pop(0)
        cn = elm.classList.pop(0)
        self.assertEqual(cn, 'clsb2')
        self.assertEqual(len(lst), 0)
        self.assertEqual(elm.className, '')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsb2', ])

        # classList setitem [0] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[0] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc2 clsc3')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', ])

        # classList setitem [-3] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[-3] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc2 clsc3')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', ])

        # classList setitem [1] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[1] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc3')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', ])

        # classList setitem [-2] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[-2] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc3')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', ])

        # classList setitem [2] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[2] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc2 clsc4')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', ])

        # classList setitem [-1] to [1,2,3]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[-1] = 'clsc4'
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc2 clsc4')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', ])

        # classList setitem [1:5]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[1:5] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc5')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList setitem [-2:5]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[-2:5] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc5')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList setitem [1:]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[1:] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc5')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList setitem [-2:]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[-2:] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc4 clsc5')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList setitem [0:2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[0:2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc5 clsc3')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc2', ])

        # classList setitem [-3:-1]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[-3:-1] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc5 clsc3')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc2', ])

        # classList setitem [:2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[:2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc5 clsc3')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc2', ])

        # classList setitem [:-1]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[:-1] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc5 clsc3')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc2', ])

        # classList setitem [0:3:2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[0:3:2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc2 clsc5')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc3', ])

        # classList setitem [-3::2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[-3::2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc4 clsc2 clsc5')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', 'clsc3', ])

        # classList setitem [2:0:-1]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[2:0:-1] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc5 clsc4')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', 'clsc2', ])

        # classList setitem [-1:0:-1]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[-1:0:-1] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc1 clsc5 clsc4')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', 'clsc2', ])

        # classList setitem [2::-2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[2::-2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc5 clsc2 clsc4')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', 'clsc1', ])

        # classList setitem [-1::-2]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList[-1::-2] = ['clsc4', 'clsc5', ]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc5 clsc2 clsc4')
        ddcnt += 2
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_addClass'], ['clsc4', 'clsc5', ])
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3', 'clsc1', ])

        # classList set by className
        elm.className = 'clsc1 clsc2 clsc3  clsc4'
        self.assertEqual(len(lst), 4)
        self.assertEqual(elm.className, 'clsc1 clsc2 clsc3 clsc4')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], 'clsc1 clsc2 clsc3  clsc4')
        # note: no className in dominter.js because className is treated like common properties

        # classList del[0] from [x,y,z,w]
        del elm.classList[0]
        self.assertEqual(len(lst), 3)
        self.assertEqual(elm.className, 'clsc2 clsc3 clsc4')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc1', ])

        # classList del 0,1 from [x,y,z]
        del elm.classList[0:2]
        self.assertEqual(len(lst), 1)
        self.assertEqual(elm.className, 'clsc4')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3',])

        # classList del 1,2,3,4 from [x,y,z]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        del elm.classList[1:5]
        self.assertEqual(len(lst), 1)
        self.assertEqual(elm.className, 'clsc1')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3',])

        # classList del -1 from [x,y,z]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        del elm.classList[-1]
        self.assertEqual(len(lst), 2)
        self.assertEqual(elm.className, 'clsc1 clsc2')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc3',])

        # classList del -2: from [x,y,z]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        del elm.classList[-2:]
        self.assertEqual(len(lst), 1)
        self.assertEqual(elm.className, 'clsc1')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList del -2: from [x,y,z]
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        del elm.classList[-2:]
        self.assertEqual(len(lst), 1)
        self.assertEqual(elm.className, 'clsc1')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_removeClass'], ['clsc2', 'clsc3', ])

        # classList reverse()
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList.reverse()
        self.assertEqual(elm.className, 'clsc3 clsc2 clsc1')
        ddcnt += 0
        self.assertEqual(len(document.diffdat), ddcnt)

        # classList reverse()
        elm.className = 'clsc1 clsc2 clsc3'
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        elm.classList.sort()
        self.assertEqual(elm.className, 'clsc1 clsc2 clsc3')
        ddcnt += 0
        self.assertEqual(len(document.diffdat), ddcnt)

        # classList clear()
        elm.classList.clear()
        self.assertEqual(elm.className, '')
        self.assertEqual(len(lst), 0)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearClass'], True)

        # style
        elm.style.cssText = ''
        ddcnt += 1
        #
        elm.style.color = 'red'
        self.assertEqual(len(elm.style), 1)
        self.assertEqual(elm.style.color, 'red')
        self.assertEqual(elm.style['color'], 'red')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'color': 'red'})
        #
        elm.style.zIndex = 3
        self.assertEqual(len(elm.style), 2)
        self.assertEqual(elm.style.zIndex, 3)
        self.assertEqual(elm.style['z-index'], 3)
        self.assertEqual(elm.style['zIndex'], 3)
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'z-index': 3})
        #
        elm.style['color'] = 'grey'
        self.assertEqual(len(elm.style), 2)
        self.assertEqual(elm.style.color, 'grey')
        self.assertEqual(elm.style['color'], 'grey')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'color': 'grey'})
        #
        elm.style = 'color: green; z-index: 11'
        self.assertEqual(len(elm.style), 2)
        self.assertEqual(elm.style.color, 'green')
        self.assertEqual(elm.style['color'], 'green')
        self.assertEqual(elm.style.zIndex, '11')
        self.assertEqual(elm.style['z-index'], '11')
        self.assertEqual(elm.style['zIndex'], '11')
        ddcnt += 3
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_clearStyle'], True)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'color': 'green'})
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['_setStyle'], {'z-index': '11'})

    def test_Element2(self):
        win = Window()
        document = win.document
        elm = document.createElement('elmtag')
        elm2 = document.createElement('elm2tag')
        chd = document.createElement('chdtag')
        chd2 = document.createElement('chd2tag')
        ddcnt = 4
        # removeChild appendChild
        self.assertEqual(len(document.diffdat), ddcnt)
        self.assertEqual(len(elm.childList), 0)
        with self.assertRaises(ValueError):
            elm.removeChild(chd)
        self.assertEqual(len(document.diffdat), ddcnt)
        self.assertEqual(len(elm.childList), 0)
        self.assertIsNone(chd.parent)

        elm.appendChild(chd)
        self.assertEqual(len(elm.childList), 1)
        self.assertEqual(elm.childList[0], chd)
        self.assertEqual(chd.parent, elm)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd.id)

        elm.removeChild(chd)
        self.assertEqual(len(elm.childList), 0)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_removeChild'], chd.id)

        elm.appendChild(chd)
        elm.appendChild(chd2)
        elm.appendChild(chd)
        self.assertEqual(len(elm.childList), 2)
        self.assertEqual(elm.childList[0], chd2)
        self.assertEqual(elm.childList[1], chd)
        ddcnt += 4
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd.id)
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd2.id)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_removeChild'], chd.id)
        ddd = document.diffdat[ddcnt - 1]
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
        ddcnt += 2
        self.assertEqual(len(elm.childList), 2)
        self.assertEqual(elm.childList[0], chd2)
        self.assertEqual(elm.childList[1], chd)
        self.assertEqual(len(elm2.childList), 0)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], elm2.id)
        self.assertEqual(ddd['_removeChild'], chd.id)
        ddd = document.diffdat[ddcnt - 1]
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
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_insertBefore'], [chd3.id, chd2.id])

        elm.insertBefore(chd4, chd)
        self.assertEqual(len(elm.childList), 4)
        self.assertEqual(elm.childList[0], chd3)
        self.assertEqual(elm.childList[1], chd2)
        self.assertEqual(elm.childList[2], chd4)
        self.assertEqual(elm.childList[3], chd)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
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
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd.id)
        elm.insertBefore(chd2, chd)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
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
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_appendChild'], chd3.id)

        elm.replaceChild(chd4, chd)
        self.assertIsNone(chd.parent)
        self.assertEqual(len(elm.childList), 3)
        self.assertEqual(elm.childList[0], chd2)
        self.assertEqual(elm.childList[1], chd4)
        self.assertEqual(elm.childList[2], chd3)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_replaceChild'], [chd4.id, chd.id])

        elm.replaceChild(chd2, chd3)
        self.assertIsNone(chd3.parent)
        self.assertEqual(len(elm.childList), 2)
        self.assertEqual(elm.childList[0], chd4)
        self.assertEqual(elm.childList[1], chd2)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_replaceChild'], [chd2.id, chd3.id])

        elm.replaceChild(chd3, chd4)
        self.assertIsNone(chd4.parent)
        self.assertEqual(len(elm.childList), 2)
        self.assertEqual(elm.childList[0], chd3)
        self.assertEqual(elm.childList[1], chd2)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_replaceChild'], [chd3.id, chd4.id])

        elm.replaceChild(chd4, chd2)
        self.assertIsNone(chd2.parent)
        self.assertEqual(len(elm.childList), 2)
        self.assertEqual(elm.childList[0], chd3)
        self.assertEqual(elm.childList[1], chd4)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_replaceChild'], [chd4.id, chd2.id])

        elm.replaceChild(chd4, chd3)
        self.assertIsNone(chd3.parent)
        self.assertEqual(len(elm.childList), 1)
        self.assertEqual(elm.childList[0], chd4)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['_replaceChild'], [chd4.id, chd3.id])

        ###elm.removeChild(chd2)

    def test_Element3(self):
        win = Window()
        document = win.document
        elm = document.createElement('elmtag')


if __name__ == "__main__":
    unittest.main()
