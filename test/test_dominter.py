#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import json

from dominter.dom import Window, start_app
import dominter.dom as domdom


class TestDominter(unittest.TestCase):
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
        self.assertEqual(elm._id, id(elm))
        self.assertEqual(elm.document, document)
        self.assertEqual(elm.tagName, 'asdf')
        self.assertIsNone(elm.name)
        self.assertIsNone(elm.parent)
        self.assertEqual(elm.eventlisteners, [])
        self.assertEqual(elm.attributes, {})
        self.assertEqual(elm.elements, [])
        self.assertEqual(type(elm._classList), domdom.ClassList)
        self.assertEqual(type(elm._style), domdom.Style)
        self.assertIsNone(elm._onclick)
        self.assertIsNone(elm._onchange)
        #
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt-1]
        self.assertEqual(ddd['_objid_'], id(elm))
        self.assertTrue('createElement' in ddd)
        dic = json.loads(ddd['createElement'])
        self.assertEqual(len(dic), 2)
        self.assertEqual(dic['_id'], id(elm))
        self.assertEqual(dic['tagName'], tagname)
        # pre_setattr()
        key0 = 'ghkl0'
        val0 = 'uiop0'
        elm.pre_setattr(key0, val0)
        ddcnt += 1

        def chk0():
            self.assertEqual(len(document.diffdat), ddcnt)
            ddd = document.diffdat[ddcnt-1]
            self.assertEqual(ddd['_objid_'], id(elm))
            self.assertEqual(ddd[key0], val0)
        chk0()
        # _in_init_ == True
        key1 = 'ghkl1'
        val1 = 'uiop1'
        elm._in_init_ = True
        elm.pre_setattr(key1, val1)
        chk0()
        elm._in_init_ = False
        # dif_excepts = ['parent', 'document', 'onclick', '_onclick', 'onchange', '_onchange',]
        elm.pre_setattr('parent', 'parent val')
        chk0()
        elm.pre_setattr('document', 'document val')
        chk0()
        elm.pre_setattr('_onclick', '_onclick val')
        chk0()
        elm.pre_setattr('_onchange', '_onchange val')
        chk0()
        elm.pre_setattr('onclick', 'onclick val')
        chk0()
        elm.pre_setattr('onchange', 'onchange val')
        chk0()
        # __setattr__() id
        objdic = document.obj_dic
        self.assertEqual(len(objdic), 1)
        self.assertEqual(objdic[id(elm)], elm)

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
        ddcnt = setid(id(elm), 'testid0', ddcnt)
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
        self.assertEqual(ddd['setStyle'], styl0)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['setStyle'], styl1)
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
        # id done
        # className done
        # classList
        elm.className = ''
        lst = elm.classList
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['className'], '')
        self.assertEqual(len(lst), 0)
        #
        elm.classList.append('clsb1')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['addClass'], ['clsb1', ])
        self.assertEqual(len(lst), 1)
        self.assertEqual(lst[0], 'clsb1')
        #
        elm.classList.add('clsb2')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['addClass'], ['clsb2', ])
        self.assertEqual(len(lst), 2)
        self.assertEqual(lst[1], 'clsb2')
        #
        elm.classList.extend(['clsb3', 'clsb4', 'clsb5'])
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['addClass'], ['clsb3', 'clsb4', 'clsb5'])
        self.assertEqual(len(lst), 5)
        self.assertEqual(lst[2], 'clsb3')
        self.assertEqual(lst[3], 'clsb4')
        self.assertEqual(lst[4], 'clsb5')
        #
        elm.classList.insert(2, 'clsb1.5')
        self.assertEqual(elm.className, 'clsb1 clsb2 clsb1.5 clsb3 clsb4 clsb5')
        self.assertTrue(elm.classList.contains('clsb1'))
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['addClass'], ['clsb1.5', ])
        self.assertEqual(len(lst), 6)
        #
        elm.classList.remove('clsb1')
        self.assertFalse(elm.classList.contains('clsb1'))
        self.assertTrue(elm.classList.contains('clsb4'))
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['removeClass'], ['clsb1', ])
        self.assertEqual(len(lst), 5)
        #
        elm.classList.remove('clsb4')
        self.assertFalse(elm.classList.contains('clsb4'))
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3 clsb5')
        self.assertTrue(elm.classList.contains('clsb5'))
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['removeClass'], ['clsb4', ])
        self.assertEqual(len(lst), 4)
        #
        elm.classList.remove('clsb5')
        self.assertFalse(elm.classList.contains('clsb5'))
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['removeClass'], ['clsb5', ])
        self.assertEqual(len(lst), 3)
        #
        elm.classList.toggle('clsb6')
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3 clsb6')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['addClass'], ['clsb6', ])
        self.assertEqual(len(lst), 4)
        #
        elm.classList.toggle('clsb6')
        self.assertEqual(elm.className, 'clsb2 clsb1.5 clsb3')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['removeClass'], ['clsb6', ])
        self.assertEqual(len(lst), 3)
        #
        elm.classList.clear()
        self.assertEqual(elm.className, '')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['clearClass'], True)
        self.assertEqual(len(lst), 0)
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
        self.assertEqual(ddd['setStyle'], {'color': 'red'})
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
        self.assertEqual(ddd['setStyle'], {'z-index': 3})
        #
        elm.style['color'] = 'grey'
        self.assertEqual(len(elm.style), 2)
        self.assertEqual(elm.style.color, 'grey')
        self.assertEqual(elm.style['color'], 'grey')
        ddcnt += 1
        self.assertEqual(len(document.diffdat), ddcnt)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['setStyle'], {'color': 'grey'})
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
        self.assertEqual(ddd['clearStyle'], True)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['setStyle'], {'color': 'green'})
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], id1)
        self.assertEqual(ddd['setStyle'], {'z-index': '11'})


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
        self.assertEqual(len(elm.elements), 0)
        with self.assertRaises(ValueError):
            elm.removeChild(chd)
        self.assertEqual(len(document.diffdat), ddcnt)
        self.assertEqual(len(elm.elements), 0)
        self.assertIsNone(chd.parent)
        #
        elm.appendChild(chd)
        self.assertEqual(len(elm.elements), 1)
        self.assertEqual(elm.elements[0], chd)
        self.assertEqual(chd.parent, elm)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['appendChild'], chd.id)
        #
        elm.removeChild(chd)
        self.assertEqual(len(elm.elements), 0)
        ddcnt += 1
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['removeChild'], chd.id)
        #
        elm.appendChild(chd)
        elm.appendChild(chd2)
        elm.appendChild(chd)
        self.assertEqual(len(elm.elements), 2)
        self.assertEqual(elm.elements[0], chd2)
        self.assertEqual(elm.elements[1], chd)
        ddcnt += 4
        ddd = document.diffdat[ddcnt - 4]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['appendChild'], chd.id)
        ddd = document.diffdat[ddcnt - 3]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['appendChild'], chd2.id)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['removeChild'], chd.id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['appendChild'], chd.id)
        #
        elm.removeChild(chd)
        elm.removeChild(chd2)
        ddcnt += 2
        elm.appendChild(chd2)
        elm2.appendChild(chd)
        ddcnt += 2
        self.assertEqual(len(elm.elements), 1)
        self.assertEqual(elm.elements[0], chd2)
        self.assertEqual(len(elm2.elements), 1)
        self.assertEqual(elm2.elements[0], chd)
        #
        elm.appendChild(chd)
        ddcnt += 2
        self.assertEqual(len(elm.elements), 2)
        self.assertEqual(elm.elements[0], chd2)
        self.assertEqual(elm.elements[1], chd)
        self.assertEqual(len(elm2.elements), 0)
        ddd = document.diffdat[ddcnt - 2]
        self.assertEqual(ddd['_objid_'], elm2.id)
        self.assertEqual(ddd['removeChild'], chd.id)
        ddd = document.diffdat[ddcnt - 1]
        self.assertEqual(ddd['_objid_'], elm.id)
        self.assertEqual(ddd['appendChild'], chd.id)


    def test_Element3(self):
        win = Window()
        document = win.document
        elm = document.createElement('elmtag')


if __name__ == "__main__":
    unittest.main()
