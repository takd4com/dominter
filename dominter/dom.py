# -*- coding: utf-8 -*-
"""
dominter: Simple Python GUI (Graphical User Interface) package for small asynchronous web application.
Copyright (c) 2017 Tamini Bean
License: MIT
"""
import sys
import os
import json
import shlex
import re
import collections
from inspect import isclass
from logging import (getLogger, basicConfig, DEBUG, INFO, WARN, ERROR)

import tornado.ioloop
import tornado.web
import tornado.websocket


logger = getLogger(__name__)

_OBJKEY_ = '_objid_'


class HookList(list):
    def __init__(self, init_val=None, append_hook=None, extend_hook=None,
                 insert_hook=None, remove_hook=None, pop_hook=None,
                 setitem_hook=None, delitem_hook=None,
                 reverse_hook=None, sort_hook=None, clear_hook=None):
        if init_val is None:
            super(HookList, self).__init__()
        else:
            super(HookList, self).__init__(init_val)
        self.append_hook = append_hook
        self.extend_hook = extend_hook
        self.insert_hook = insert_hook
        self.remove_hook = remove_hook
        self.pop_hook = pop_hook
        self.setitem_hook = setitem_hook
        self.delitem_hook = delitem_hook
        self.reverse_hook = reverse_hook
        self.sort_hook = sort_hook
        self.clear_hook = clear_hook

    def _raw_append(self, txt):
        super(HookList, self).append(txt)

    def append(self, txt):
        if callable(self.append_hook):
            if self.append_hook(txt):
                super(HookList, self).append(txt)
        else:
            super(HookList, self).append(txt)

    def add(self, txt):
        self.append(txt)

    def _raw_extend(self, lst):
        super(HookList, self).extend(lst)

    def extend(self, lst):
        if callable(self.extend_hook):
            if self.extend_hook(lst):
                super(HookList, self).extend(lst)
        else:
            super(HookList, self).extend(lst)

    def _raw_insert(self, index, p_object):
        super(HookList, self).insert(index, p_object)

    def insert(self, index, p_object):
        if callable(self.insert_hook):
            if self.insert_hook(index, p_object):
                super(HookList, self).insert(index, p_object)
        else:
            super(HookList, self).insert(index, p_object)

    def _raw_remove(self, txt):
        super(HookList, self).remove(txt)

    def remove(self, txt):
        if callable(self.remove_hook):
            if self.remove_hook(txt):
                super(HookList, self).remove(txt)
        else:
            super(HookList, self).remove(txt)

    def _raw_pop(self, idx=None):
        if idx is None:
            return super(HookList, self).pop()
        else:
            return super(HookList, self).pop(idx)

    def pop(self, idx=None):
        if callable(self.pop_hook):
            res, elm = self.pop_hook(idx)
            if res:
                elm = self._raw_pop(idx)
            return elm
        else:
            return self._raw_pop(idx)

    def _raw_setitem(self, idx, value):
        super(HookList, self).__setitem__(idx, value)

    def __setitem__(self, idx, value):
        if callable(self.setitem_hook):
            if self.setitem_hook(idx, value):
                super(HookList, self).__setitem__(idx, value)
        else:
            super(HookList, self).__setitem__(idx, value)

    # setslice is python2 only
    def _raw_setslice(self, i, j, value):
        super(HookList, self).__setslice__(i, j, value)

    def __setslice__(self, i, j, value):
        if callable(self.setitem_hook):
            if self.setitem_hook(slice(i, j, None), value):
                super(HookList, self).__setslice__(i, j, value)
        else:
            super(HookList, self).__setslice__(i, j, value)

    def _raw_delitem(self, idx):
        super(HookList, self).__delitem__(idx)

    def __delitem__(self, idx):
        if callable(self.delitem_hook):
            if self.delitem_hook(idx):
                super(HookList, self).__delitem__(idx)
        else:
            super(HookList, self).__delitem__(idx)

    # delslice is python2 only
    def _raw_delslice(self, i=None, j=None):
        super(HookList, self).__delslice__(i, j)

    def __delslice__(self, i=None, j=None):
        if callable(self.delitem_hook):
            if self.delitem_hook(slice(i, j)):
                super(HookList, self).__delslice__(i, j)
        else:
            super(HookList, self).__delslice__(i, j)

    def _raw_reverse(self):
        super(HookList, self).reverse()

    def reverse(self):
        if callable(self.reverse_hook):
            if self.reverse_hook():
                super(HookList, self).reverse()
        else:
            super(HookList, self).reverse()

    def _raw_sort(self, key=None, reverse=False):
        super(HookList, self).sort(key=key, reverse=reverse)

    def sort(self, key=None, reverse=False):
        if callable(self.sort_hook):
            if self.sort_hook(key, reverse):
                super(HookList, self).sort(key=key, reverse=reverse)
        else:
            super(HookList, self).sort(key=key, reverse=reverse)

    def contains(self, txt):
        return txt in self

    def toggle(self, txt):
        if self.contains(txt):
            self.remove(txt)
        else:
            self.append(txt)

    def _raw_clear(self):
        if sys.version_info.major == 2:
            self._raw_delslice(0, len(self))
        else:
            self._raw_delitem(slice(None, None))

    def clear(self):
        if callable(self.clear_hook):
            if self.clear_hook():
                self._raw_clear()
        else:
            self._raw_clear()


class ChildList(HookList):
    def __init__(self, elm, init_val=None):
        if init_val is None:
            init_val = []
        super(ChildList, self).__init__(
            init_val=init_val,
            append_hook=elm._childList_append,
            extend_hook=elm._childList_extend,
            insert_hook=elm._childList_insert,
            remove_hook=elm._childList_remove,
            pop_hook=elm._childList_pop,
            setitem_hook=elm._childList_setitem,
            delitem_hook=elm._childList_delitem,
            reverse_hook=elm._childList_reverse,
            sort_hook=elm._childList_sort,
            clear_hook=elm._childList_clear,
        )


class ClassList(HookList):
    # element.class property class
    def __init__(self, elm, init_val=None):
        if init_val is None:
            init_val = []
        super(ClassList, self).__init__(
            init_val=init_val,
            append_hook=elm._classList_append,
            extend_hook=elm._classList_extend,
            insert_hook=elm._classList_insert,
            remove_hook=elm._classList_remove,
            pop_hook=elm._classList_pop,
            setitem_hook=elm._classList_setitem,
            delitem_hook=elm._classList_delitem,
            clear_hook=elm._classList_clear,
        )

    def _set_class_name(self, txt):
        # When className is set, diffdat is sent as it is, and classList is decomposed and stored. no need to call self.elm._classList_xxx
        self._raw_clear()
        lst = [x for x in txt.split(' ') if 0 < len(x)]
        super(ClassList, self)._raw_extend(lst)


class Style(dict):
    """
    element.style property class
    """
    re1 = re.compile(r'(.)([A-Z][a-z]+)')
    re2 = re.compile(r'([a-z0-9])([A-Z])')

    def __init__(self, elm, init_val=None):
        if init_val is None:
            dic = {}
        else:
            dic = {self.attr2item_key(k): v for k, v in init_val.items()}
        super(Style, self).__init__(dic)
        self.elm = elm

    def __setitem__(self, key, value):
        if 'cssText' == key:
            self.set_text(value)
        else:
            ik = self.attr2item_key(key)
            super(Style, self).__setitem__(ik, value)
            self.elm._style_set(ik, value)

    def __getitem__(self, key):
        if 'cssText' == key:
            return self.__str__()
        else:
            ik = self.attr2item_key(key)
            return super(Style, self).__getitem__(ik)

    def __delitem__(self, key):
        ik = self.attr2item_key(key)
        super(Style, self).__delitem__(ik)
        self.elm._style_delete(ik)

    def __contains__(self, key):
        ik = self.attr2item_key(key)
        return super(Style, self).__contains__(ik)


    def attr2item_key(self, key):
        s1 = self.re1.sub(r'\1-\2', key)
        return self.re2.sub(r'\1-\2', s1).lower()

    def __setattr__(self, key, value):
        if 'elm' == key:
            super(Style, self).__setattr__(key, value)
        else:
            self.__setitem__(key, value)

    def __getattr__(self, key):
        if 'elm' == key:
            return super(Style, self).__getattr__(key)
        else:
            try:
                return self[key]
            except KeyError as e:
                raise AttributeError

    def __delattr__(self, key):
        self.__delitem__(key)

    def pop(self, key, *args):
        if key in self:
            val = self[key]
            self.__delitem__(key)
            return val
        else:
            if 0 < len(args):
                return args[0]
            else:
                raise TypeError

    def clear(self):
        if 0 < len(self):
            super(Style, self).clear()
            self.elm._style_clear()

    def __str__(self):
        return ' '.join(('{}: {};'.format(k, v) for k, v in self.items()
                         if k != 'elm'))

    def set_text(self, txt):
        self.clear()
        for s in txt.split(';'):
            if 0 == len(s.strip()):
                continue
            kv = s.split(':')
            if 2 == len(kv):
                key = kv[0].strip()
                value = kv[1].strip()
                self.__setitem__(key, value)
            else:
                raise ValueError()

    @property
    def cssText(self):
        return self.__str__()

    def setProperty(self, key, value):
        self[key] = value

    def removeProperty(self, key):
        self.__delitem__(key)


class Element(object):
    """
    virtual element class
    """
    def __init__(self, document, tag):
        self._in_init_ = True
        self._id = str(id(self))
        self.document = document
        self.tagName = tag
        self.name = None
        self.parent = None
        self._eventlisteners = []
        self.attributes = {}
        self._childList = ChildList(self)
        self._classList = ClassList(self)
        self._style = Style(self)
        self._onclick = None
        self._onchange = None
        self._in_init_ = False
        self._on = 0 # to sort childList
        #self.onblur = None
        #self.onfocus = None
        #self.onclose = None
        #self.ondblclick = None
        #self.ondrag = None
        #self.ondragend = None
        #self.ondragenter = None
        #self.ondragexit = None
        #self.ondragleave = None
        #self.ondragover = None
        #self.ondragstart = None
        #self.ondrop = None
        #self.onkeydown = None
        #self.onkeypress = None
        #self.onkeyup = None
        #self.onload = None
        #self.onselect = None
        #self.onsubmit = None
        #self.onreset = None
        #self.onabort = None
        #self.onunload = None
        #self.onmouseout = None
        #self.onmouseover = None
        #self.onmouseup = None
        #self.onmousedown = None
        #self.onmousemove = None

    # dif_dat除外
    dif_excepts = ['_in_init_', '_on', 'classList', '_classList', 'style',
                   'childList', '_childList',
                   'parent', 'document',
                   'onclick', '_onclick',
                   'onchange', '_onchange', ]
    ser_excepts = ['_in_init_', '_on', 'parent', 'document', ]

    def _pre_setattr(self, key, value):
        if 'document' in self.__dict__:
            if (not self._in_init_) and (key not in self.dif_excepts):
                self.document.add_diff({_OBJKEY_: self._id, key: value})

    def __setattr__(self, key, value):
        self._pre_setattr(key, value)
        super(Element, self).__setattr__(key, value)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._set_id(value)

    def _set_id(self, txt):
        orgid = self._id
        self.__dict__['_id'] = txt
        objdic = self.document.obj_dic
        if orgid in objdic:
            del(objdic[orgid])
        objdic[txt] = self

    @property
    def childList(self):
        return self._childList

    @childList.setter
    def childList(self, lst):
        if 0 < len(self._childList):
            self._childList.clear()
        for elm in lst:
            self.appendChild(elm)

    @property
    def className(self):
        return ' '.join(self._classList)

    @className.setter
    def className(self, value):
        self._set_class_name(value)

    def _set_class_name(self, txt):
        classlist = self._classList
        classlist._set_class_name(txt)

    @property
    def classList(self):
        return self._classList

    @classList.setter
    def classList(self, value):
        raise TypeError('readonly')

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        self._style.cssText = value

    def addhandler(self, fnc):
        name = repr(fnc)
        self.document.handlers[name] = fnc
        return name

    @property
    def onclick(self):
        return self._onclick

    @onclick.setter
    def onclick(self, value):
        self._set_onclick(value)

    def _set_onclick(self, fnc):
        self.__dict__['_onclick'] = fnc
        name = self.addhandler(fnc)
        self.document.add_diff({_OBJKEY_: self.id, 'onclick': name})

    @property
    def onchange(self):
        return self._onchange

    @onchange.setter
    def onchange(self, value):
        self._set_onchange(value)

    def _set_onchange(self, fnc):
        self.__dict__['_onchange'] = fnc
        name = self.addhandler(fnc)
        self.document.add_diff({_OBJKEY_: self._id, 'onchange': name})

    def removeChild(self, elm):
        if elm not in self._childList:
            raise ValueError('not child')
        self.document.add_diff({_OBJKEY_: self._id, '_removeChild': elm.id})
        elm.parent = None
        self._childList._raw_remove(elm)

    def appendChild(self, elm):
        if elm.parent is not None:
            elm.parent.removeChild(elm)
        self.childList._raw_append(elm)
        elm.parent = self
        self.document.add_diff({_OBJKEY_: self._id, '_appendChild': elm.id})
        # check childList recursively
        if 0 == len(elm._childList):
            return
        que = collections.deque()
        for chd in elm._childList:
            que.append((elm, chd))
        while True:
            try:
                parent, chd = que.popleft()
            except IndexError:
                break
            if chd.parent is None:
                chd.parent = parent
                self.document.add_diff({_OBJKEY_: parent._id, '_appendChild': chd.id})
            for gson in chd.childList:
                que.append((chd, gson))

    def insertBefore(self, new_elm, ref_elm):
        """
        inserts the specified element before the reference element as a child of the current node.
        :param new_elm:
        :param ref_elm:
        :return:
        """
        if ref_elm is None:
            self.appendChild(new_elm)
        else:
            pos = self.childList.index(ref_elm)
            self.childList._raw_insert(pos, new_elm)
            new_elm.parent = self
            self.document.add_diff({_OBJKEY_: self._id, '_insertBefore': [new_elm._id, ref_elm._id]})

    def replaceChild(self, new_elm, old_elm):
        if old_elm is None:
            self.appendChild(new_elm)
        else:
            if new_elm.parent is not None:
                new_elm.parent.childList._raw_remove(new_elm)
                new_elm.parent = None
            pos = self.childList.index(old_elm)
            self.childList._raw_remove(old_elm)
            old_elm.parent = None
            self.childList._raw_insert(pos, new_elm)
            new_elm.parent = self
            self.document.add_diff({_OBJKEY_: self._id, '_replaceChild': [new_elm._id, old_elm._id]})

    def getAttribute(self, name):
        if 'style' == name:
            return str(self._style)
        elif 'class' == name:
            return self.className
        elif name in self.attributes.keys():
            return self.attributes[name]

    def setAttribute(self, name, value):
        if 'style' == name:
            # self._style.set_text(value)
            self.style.cssText = value
        elif 'class' == name:
            self.className = value
        else:
            self.attributes[name] = value
            self.document.add_diff({_OBJKEY_: self._id, '_setAttributes': {name: value}})

    def removeAttribute(self, name):
        if 'style' == name:
            self._style.clear()
        elif 'class' == name:
            self.className = ''
        elif name in self.attributes.keys():
            del(self.attributes[name])
            self.document.add_diff({_OBJKEY_: self._id, '_removeAttributes': [name, ]})

    def addEventListener(self, type_, listener):
        self._eventlisteners.append((type_, listener))
        self.document.add_diff({_OBJKEY_: self._id, '_addEventListener': [listener, ]})
        self.addhandler(listener)

    def removeEventListener(self, type_, listener):
        tpl = (type_, listener)
        if tpl in self._eventlisteners:
            self._eventlisteners.remove(tpl)
            self.document.add_diff({_OBJKEY_: self._id, '_removeEventListener': [listener, ]})
            name = repr(listener)
            del(self.document.handlers[name])

    def dumps(self):
        # self.onload()
        str = json.dumps(self, default=self.serializer, indent=2)
        # print(str)
        return str

    @staticmethod
    def serializer(obj):
        if isinstance(obj, Element):
            dic = obj.__dict__.copy()
            # delete reference to other elements to avoid circular reference
            # 他のelementへの参照を含めるてしまうと循環参照エラーが発生するため削除する
            for nm in Element.ser_excepts:
                del (dic[nm])
            items = list(dic.items())
            for k, v in items:
                if v is None:
                    del(dic[k])
                elif isinstance(v, list):
                    if 0 == len(v):
                        del(dic[k])
                elif isinstance(v, dict):
                    if 0 == len(v):
                        del(dic[k])
            return dic
        elif isinstance(obj, Style):
            dic = obj.__dict__.copy()
            # delete reference to other elements to avoid circular reference
            # 他のelementへの参照を含めるてしまうと循環参照エラーが発生するため削除する
            del (dic['elm'])
            return dic
        elif callable(obj):
            name = repr(obj)
            return name
        raise TypeError(repr(obj) + " is not serializable!")

    def _childList_append(self, elm):
        self.appendChild(elm)
        return False

    def _childList_insert(self, index, elm):
        self.insertBefore(elm, self.childList[index])
        return False

    def _childList_extend(self, lst):
        for elm in lst:
            self.appendChild(elm)
        return False

    def _childList_remove(self, elm):
        self.removeChild(elm)
        return False

    def _childList_pop(self, idx):
        elm = None
        if 0 <= idx < len(self._childList):
            elm = self._childList[idx]
            self.removeChild(elm)
        return False, elm

    def _childList_setitem(self, idx, value):
        if isinstance(idx, int):
            elm = self._childList[idx]
            if not isinstance(value, Element):
                raise TypeError('can only assign an Element')
            self.insertBefore(value, elm)
            if elm:
                self.removeChild(elm)
        elif isinstance(idx, slice):
            lst = self._childList[idx]
            if (not isinstance(value, list)) and (not isinstance(value, tuple)):
                raise TypeError('can only assign an iterable')
            stp = idx.step
            if (stp is not None) and (stp != 1):
                siz = len(self._childList)
                def pn(val, isst):
                    if val is None:
                        if 0 < stp:
                            return 0 if isst else siz
                        else:
                            return siz - 1 if isst else -1
                    elif 0 > val:
                        return siz + val
                    else:
                        return val
                bg = pn(idx.start, True)
                ed = pn(idx.stop, False)
                # force 0 > step
                if 0 < stp:
                    bg, ed, stp = ed - 1, bg - 1, -stp
                    value.reverse()
                cnt = 0
                for j in range(bg, ed, stp):
                    elm = value[cnt]
                    cnt += 1
                    ref = self._childList[j]
                    self.insertBefore(elm, ref)
                for elm in lst:
                    self.removeChild(elm)
            elif 0 == len(lst):
                for elm in value:
                    self.appendChild(elm)
            else:
                ref = lst[0]
                for elm in value:
                    self.insertBefore(elm, ref)
                for elm in lst:
                    self.removeChild(elm)
        else:
            raise TypeError('bad value type')
        return False

    def _childList_delitem(self, idx):
        lst = self._childList[idx]
        if lst:
            if isinstance(lst, Element):
                self.removeChild(lst)
            else:
                for elm in lst:
                    self.removeChild(elm)
        return False

    def _childList_reverse(self):
        self.document.add_diff({_OBJKEY_: self._id, '_reverseChild': True})
        return True

    def _childList_sort(self, key=None, reverse=False):
        for j, elm in enumerate(self.childList):
            elm._on = j
        self.childList._raw_sort(key=key, reverse=reverse)
        ordr = list([elm._on for elm in self.childList])
        self.document.add_diff({_OBJKEY_: self._id, '_sortChild': ordr})
        return False

    def _childList_clear(self):
        self.document.add_diff({_OBJKEY_: self._id, '_clearChild': True})
        for elm in self.childList:
            elm.parent = None
        return True

    def _classList_append(self, txt):
        self.document.add_diff({_OBJKEY_: self._id, '_addClass': [txt, ]})
        return True

    def _classList_insert(self, index, txt):
        self.document.add_diff({_OBJKEY_: self._id, '_addClass': [txt, ]})
        return True

    def _classList_extend(self, lst):
        self.document.add_diff({_OBJKEY_: self._id, '_addClass': lst})
        return True

    def _classList_remove(self, txt):
        self.document.add_diff({_OBJKEY_: self._id, '_removeClass': [txt, ]})
        return True

    def _classList_pop(self, idx):
        if 0 <= idx < len(self._classList):
            txt = self._classList[idx]
            self.document.add_diff({_OBJKEY_: self._id, '_removeClass': [txt, ]})
        return True, None

    def _classList_setitem(self, idx, value):
        if isinstance(idx, int):
            elm = self._classList[idx]
            if not isinstance(value, str):
                raise TypeError('can only assign an str')
            self.document.add_diff({_OBJKEY_: self._id, '_addClass': [value, ]})
            if elm:
                self.document.add_diff({_OBJKEY_: self._id, '_removeClass': [elm, ]})
        elif isinstance(idx, slice):
            lst = self._classList[idx]
            if (not isinstance(value, list)) and (not isinstance(value, tuple)):
                raise TypeError('can only assign an iterable')
            if 0 == len(lst):
                for elm in value:
                    self.document.add_diff({_OBJKEY_: self._id, '_addClass': elm})
            else:
                ref = lst[0]
                self.document.add_diff({_OBJKEY_: self._id, '_addClass': value})
                self.document.add_diff({_OBJKEY_: self._id, '_removeClass': lst})
        else:
            raise TypeError('bad value type')
        return True

    def _classList_delitem(self, idx):
        lst = self._classList[idx]
        if lst:
            if isinstance(lst, str):
                lst = [lst,]
            self.document.add_diff({_OBJKEY_: self._id, '_removeClass': lst})
        return True

    def _classList_clear(self):
        self.document.add_diff({_OBJKEY_: self._id, '_clearClass': True})
        return True

    def _style_set(self, key, value):
        self.document.add_diff({_OBJKEY_: self._id, '_setStyle': {key: value}})
        return True

    def _style_delete(self, key):
        self.document.add_diff({_OBJKEY_: self._id, '_deleteStyle': [key, ]})
        return True

    def _style_clear(self):
        self.document.add_diff({_OBJKEY_: self._id, '_clearStyle': True})
        return True


class Document(object):
    """
    virtual document class
    """
    def __init__(self):
        #super().__init__('document')
        self.dirty = True
        self.obj_dic = {}
        self.diffdat = []
        self.handlers = {}
        self.head = Element(self, 'head')
        self.body = Element(self, 'body')
        self.cache = None

    def clean_diff(self):
        self.diffdat = []

    def add_diff(self, dat):
        self.dirty = True
        self.diffdat.append(dat)

    def getElementById(self, eid):
        if isinstance(eid, int):
            eid = str(eid)
        return self.obj_dic.get(eid, None)

    def getElementsByName(self, name):
        return [elm for key, elm in self.obj_dic.items()
                if elm.name == name]

    def getElementsByTagName(self, tag):
        return [elm for key, elm in self.obj_dic.items()
                if elm.tagName == tag]

    def getElementsByClassName(self, cls):
        return [elm for key, elm in self.obj_dic.items()
                if cls in elm.classList]

    def createElement(self, tag):
        elm = Element(self, tag)
        dat = elm.dumps()
        self.add_diff({_OBJKEY_: elm._id, '_createElement': dat})
        self.obj_dic[elm._id] = elm
        return elm

    """ not supported. use span
    def createTextNode(self, txt):
        pass
    """

    def tag(self, tagtxt, textContent=None, innerHTML=None, attrs=None,
            onclick=None, onchange=None, handler=None, childList=None):
        """
        create a tag with a specification method similar to html.

        :param tagtxt:
        :param textContent:
        :param innerHTML:
        :param attrs:
        :param onclick:
        :param onchange:
        :param childList:
        :return:
        """
        if not isinstance(tagtxt, str) or 0 == len(tagtxt):
            raise TypeError('needs string')
        lst = shlex.split(tagtxt)
        tag = lst[0]
        elm = self.createElement(tag)
        for j, p in enumerate(lst):
            if (0 == j) or (0 == len(p)):
                continue
            if (p == '=') or (p == '_'):
                raise ValueError('spaces on both sides of {} are not allowed'.format(p))
            d = p.split('=')
            if 1 == len(d):
                # like readonly. set true
                elm.__dict__[d] = True
            else:
                if 2 == len(d):
                    k, v = d
                else:
                    k = d[0]
                    v = '='.join(d[1:])
                if k == '_':
                    # special key
                    elm.textContent = v
                elif k == 'id':
                    elm.id = v
                elif k == 'class':
                    elm.className = v
                elif k == 'style':
                    elm.style.cssText = v
                else:
                    elm._pre_setattr(k, v)
                    elm.__dict__[k] = v
        if textContent is not None:
            elm.textContent = textContent
        if innerHTML is not None:
            elm.innerHTML = innerHTML
        if attrs is not None:
            for key, val in attrs:
                if val is not None:
                    elm.setAttribute(key, val)
        if onclick is not None:
            elm.onclick = onclick
        if onchange is not None:
            elm.onchange = onchange
        self.add_handler(elm, handler)
        if childList is not None:
            if isinstance(childList, list) or isinstance(childList, tuple):
                elm._childList = ChildList(elm, childList)
            else:
                elm._childList = ChildList(elm, [childList, ])
        return elm

    def add_handler(self, elm, handler):
        if handler is not None:
            if isinstance(handler[0], str):
                elm.addEventListener(handler[0], handler[1])
            else:
                for hdr in handler:
                    elm.addEventListener(hdr[0], hdr[1])

    def create_with(self, tag, type_=None,
                    value=None, src=None, name=None, textContent=None,
                    checked=None, selectedIndex=None,
                    min=None, max=None, step=None, multiple=None, size=None,
                    label=None, selected=None, rows=None, cols=None,
                    alt=None, width=None, height=None, href=None, rel=None,
                    integrity=None, media=None, scoped=None, crossorigin=None,
                    longdesc=None, sizes=None, referrerpolicy=None,
                    srcset=None, download=None, target=None,
                    readonly=None, disabled=None, placeholder=None, for_=None,
                    id_=None, accesskey=None, hidden=None, tabindex=None,
                    style=None, className=None, childList=None,
                    onclick=None, onchange=None, handler=None):
        elm = self.createElement(tag)
        if type_ is not None:
            elm.type = type_
        if value is not None:
            elm.value = value
        if src is not None:
            elm.src = src
        if textContent is not None:
            elm.textContent = textContent
        if checked is not None:
            elm.checked = checked
        if selectedIndex is not None:
            elm.selectedIndex = selectedIndex
        if name is not None:
            elm.name = name
        if min is not None:
            elm.min = min
        if max is not None:
            elm.max = max
        if step is not None:
            elm.step = step
        if multiple is not None:
            elm.multiple = multiple
        if size is not None:
            elm.size = size
        if label is not None:
            elm.label = label
        if selected is not None:
            elm.selected = selected
        if rows is not None:
            elm.rows = rows
        if cols is not None:
            elm.cols = cols
        if alt is not None:
            elm.alt = alt
        if width is not None:
            elm.width = width
        if height is not None:
            elm.height = height
        if href is not None:
            elm.href = href
        if rel is not None:
            elm.rel = rel
        if integrity is not None:
            elm.integrity = integrity
        if media is not None:
            elm.media = media
        if scoped is not None:
            elm.scoped = scoped
        if crossorigin is not None:
            elm.crossorigin = crossorigin
        if longdesc is not None:
            elm.longdesc = longdesc
        if sizes is not None:
            elm.sizes = sizes
        if referrerpolicy is not None:
            elm.referrerpolicy = referrerpolicy
        if srcset is not None:
            elm.srcset = srcset
        if download is not None:
            elm.download = download
        if target is not None:
            elm.target = target
        if readonly is not None:
            elm.readonly = readonly
        if disabled is not None:
            elm.disabled = disabled
        if placeholder is not None:
            elm.placeholder = placeholder
        if for_ is not None:
            elm.for_ = for_
        if id_ is not None:
            elm.id = id_
        if accesskey is not None:
            elm.accesskey = accesskey
        if hidden is not None:
            elm.hidden = hidden
        if tabindex is not None:
            elm.tabindex = tabindex
        if className is not None:
            elm.className = className
        if style is not None:
            elm.style.cssText = style
        if childList is not None:
            elm.childList = childList
        if onclick is not None:
            elm.onclick = onclick
        if onchange is not None:
            elm.onchange = onchange
        self.add_handler(elm, handler)

        return elm

    @staticmethod
    def filter_none(lst):
        res = []
        for key, val in lst:
            if val is not None:
                res[key] = val

    def title(self, text, id_=None):
        return self.create_with('title', textContent=text, id_=id_)

    def style(self, textContent, type_='text/css', media=None, scoped=None, id_=None):
        return self.create_with('style', textContent=textContent, type_=type_,
                                media=media, scoped=scoped, id_=id_)

    def link(self, href, rel='stylesheet', integrity=None, media=None, id_=None):
        return self.create_with('link', href=href, rel=rel, integrity=integrity,
                                media=media, id_=id_)

    def script(self, textContent='', type='text/javascript', src=None,
               crossorigin=None, id_=None):
        return self.create_with('script', textContent=textContent, type_=type,
                                src=src, crossorigin=crossorigin, id_=id_)

    def br(self, id_=None):
        return self.create_with('br', id_=id_)

    def p(self, textContent, id_=None, style=None, className=None):
        return self.create_with('p', textContent=textContent,
                                id_=id_, style=style, className=className)

    def span(self, textContent, id_=None, style=None, className=None):
        return self.create_with('span', textContent=textContent,
                                id_=id_, style=style, className=className)

    def div(self, textContent=None, id_=None, style=None, className=None,
            childList=None):
        return self.create_with('div', textContent=textContent,
                                id_=id_, style=style, className=className,
                                childList=childList)

    def button(self, textContent='', type_='button', name=None, value=None,
               disabled=None, onclick=None,
               id_=None, style=None, className=None):
        return self.create_with('button', textContent=textContent,
                                type_=type_, name=name, value=value,
                                disabled=disabled, onclick=onclick,
                                id_=id_, style=style, className=className)

    def input(self, value='', onchange=None,
             readonly=None, disabled=None, placeholder=None,
             id_=None, style=None, className=None):
        return self.create_with('input', value=value,
                                onchange=onchange, readonly=readonly,
                                disabled=disabled, placeholder=placeholder,
                                id_=id_, style=style, className=className)

    def text(self, value='', type_='text', onchange=None,
             readonly=None, disabled=None, placeholder=None,
             id_=None, style=None, className=None):
        return self.create_with('input', type_=type_, value=value,
                                onchange=onchange, readonly=readonly,
                                disabled=disabled, placeholder=placeholder,
                                id_=id_, style=style, className=className)

    def checkbox(self, checked=False, value=None, onchange=None,
                 readonly=None, disabled=None,
                 id_=None, style=None, className=None):
        return self.create_with('input', type_='checkbox', value=value,
                                checked=checked, readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def radio(self, name, value, checked=False, onchange=None,
              readonly=None, disabled=None,
              id_=None, style=None, className=None):
        return self.create_with('input', type_='radio', name=name, value=value,
                                checked=checked, readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def color(self, value='', onchange=None, readonly=None, disabled=None,
              id_=None, style=None, className=None):
        return self.create_with('input', type_='color', value=value,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def date(self, value='', onchange=None, readonly=None, disabled=None,
             id_=None, style=None, className=None):
        return self.create_with('input', type_='date', value=value,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def datetime_local(self, value='', onchange=None, step='1',
                       readonly=None, disabled=None,
                       id_=None, style=None, className=None):
        return self.create_with('input', type_='datetime-local', value=value,
                                step=step, readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def month(self, value='', onchange=None, readonly=None, disabled=None,
              id_=None, style=None, className=None):
        return self.create_with('input', type_='month', value=value,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def time(self, value='', onchange=None, step='1',
             readonly=None, disabled=None,
             id_=None, style=None, className=None):
        return self.create_with('input', type_='time', value=value,
                                step=step, readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def week(self, value='', onchange=None, readonly=None, disabled=None,
             id_=None, style=None, className=None):
        return self.create_with('input', type_='week', value=value,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def file(self, value='', onchange=None, readonly=None, disabled=None,
             id_=None, style=None, className=None):
        return self.create_with('input', type_='file', value=value,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def number(self, value='', min=None, max=None, step=None, onchange=None,
               readonly=None, disabled=None,
               id_=None, style=None, className=None):
        return self.create_with('input', type_='number', value=value,
                                min=min, max=max, step=step,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def password(self, value='', onchange=None, readonly=None, disabled=None,
                 id_=None, style=None, className=None):
        return self.create_with('input', type_='password', value=value,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def range(self, value='', min='0', max='100', step='1', onchange=None,
              readonly=None, disabled=None,
              id_=None, style=None, className=None):
        return self.create_with('input', type_='range', value=value,
                                min=min, max=max, step=step,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def select(self, value=None, selectedIndex=None, name=None, onchange=None,
               multiple=None, size=None, readonly=None, disabled=None,
               id_=None, style=None, className=None):
        return self.create_with('select', value=value, name=name,
                                selectedIndex=selectedIndex, multiple=multiple,
                                size=size, readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def option(self, value, textContent, label=None, selected=None,
               onchange=None, readonly=None, disabled=None,
               id_=None, style=None, className=None):
        return self.create_with('option', value=value, textContent=textContent,
                                label=label, selected=selected,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def textarea(self, value, rows=None, cols=None, onchange=None,
                 readonly=None, disabled=None,
                 id_=None, style=None, className=None):
        return self.create_with('textarea', value=value, rows=rows, cols=cols,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, style=style, className=className)

    def table(self, readonly=None, disabled=None,
              id_=None, style=None, className=None, childList=None):
        return self.create_with('table',
                                readonly=readonly, disabled=disabled,
                                id_=id_, style=style, className=className,
                                childList=childList)

    def tr(self, id_=None, style=None, className=None, childList=None):
        return self.create_with('tr',
                                id_=id_, style=style, className=className,
                                childList=childList)

    def th(self, textContent, id_=None, style=None, className=None):
        return self.create_with('th', textContent=textContent,
                                id_=id_, style=style, className=className)

    def td(self, textContent, id_=None, style=None, className=None):
        return self.create_with('td', textContent=textContent,
                                id_=id_, style=style, className=className)

    def fieldset(self, textContent='', disabled=None,
                 id_=None, style=None, className=None, childList=None):
        return self.create_with('fieldset', textContent=textContent,
                                disabled=disabled,
                                id_=id_, style=style, className=className,
                                childList=childList)

    def legend(self, textContent, disabled=None,
               id_=None, style=None, className=None):
        return self.create_with('legend', textContent=textContent,
                                disabled=disabled,
                                id_=id_, style=style, className=className)

    def img(self, src, alt='', width=None, height=None, onclick=None,
            crossorigin=None, longdesc=None, sizes=None, referrerpolicy=None,
            srcset=None, id_=None, style=None, className=None):
        return self.create_with('img', src=src, alt=alt, width=width, height=height,
                                onclick=onclick, crossorigin=crossorigin,
                                longdesc=longdesc, sizes=sizes,
                                referrerpolicy=referrerpolicy, srcset=srcset,
                                id_=id_, style=style, className=className)

    def a(self, href, textContent, download=None, rel=None, target=None,
          referrerpolicy=None, id_=None, style=None, className=None):
        return self.create_with('a', href=href, textContent=textContent,
                                download=download, rel=rel, target=target,
                                referrerpolicy=referrerpolicy,
                                id_=id_, style=style, className=className)

    def label(self, textContent, for_=None,
              id_=None, style=None, className=None):
        return self.create_with('label', textContent=textContent, for_=for_,
                                id_=id_, style=style, className=className)

    def h1(self, textContent, id_=None, accesskey=None, hidden=None,
           tabindex=None, style=None, className=None):
        return self.create_with('h1', textContent=textContent,
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex,
                                style=style, className=className)

    def ol(self, textContent=None, id_=None, accesskey=None, hidden=None,
           tabindex=None, style=None, className=None, childList=None):
        return self.create_with('ol', textContent=textContent,
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex,
                                style=style, className=className,
                                childList=childList)

    def li(self, textContent=None, id_=None, accesskey=None, hidden=None,
           tabindex=None, style=None, className=None, childList=None):
        return self.create_with('li', textContent=textContent,
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex,
                                style=style, className=className,
                                childList=childList)

    def ul(self, id_=None, accesskey=None, hidden=None, tabindex=None,
                style=None, className=None, childList=None):
        return self.create_with('ul', id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex,
                                style=style, className=className,
                                childList=childList)

    def section(self, id_=None, accesskey=None, hidden=None, tabindex=None,
                style=None, className=None, childList=None):
        return self.create_with('section', id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex,
                                style=style, className=className,
                                childList=childList)

    def header(self, id_=None, accesskey=None, hidden=None, tabindex=None,
                style=None, className=None, childList=None):
        return self.create_with('header',
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex,
                                style=style, className=className,
                                childList=childList)

    def footer(self, id_=None, accesskey=None, hidden=None, tabindex=None,
                style=None, className=None, childList=None):
        return self.create_with('footer',
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex,
                                style=style, className=className,
                                childList=childList)


class Window(object):
    """
    virtual window class
    """
    def __init__(self):
        self.document = Document()
        #self.location = ''
        #self.name = ''

    def _dumps(self):
        if self.document.dirty:
            logger.debug('create cache')
            s = json.dumps(self.document, default=self._serializer, indent=2)
            self.document.cache = s
            self.document.dirty = False
        else:
            s = self.document.cache
        return s

    @staticmethod
    def _serializer(obj):
        if isinstance(obj, Document):
            return {'head': obj.head, 'body': obj.body}
        if isinstance(obj, Element):
            return Element.serializer(obj)
        if callable(obj):
            name = repr(obj)
            return name
        raise TypeError(repr(obj) + " is not serializable!")


class GetHandler(tornado.web.RequestHandler):
    """
    get handler for '/indexN.html' and '/dominter.js'
    """
    def initialize(self, filename=None, wspath='/_ws'):
        self.filename = filename
        self.wspath = wspath

    def get(self):
        param = {'wspath': self.wspath,}
        if self.filename is None:
            self.render(self.get_default_filename(), param=param)
        else:
            self.render(self.filename, param=param)

    def get_default_filename(self):
        return 'index.html'


class HtmlGetHandler(GetHandler):
    def get_default_filename(self):
        fn = 'dominter.html'
        mypath = os.path.dirname(__file__)
        return os.path.join(mypath, fn)


class JsGetHandler(GetHandler):
    def get_default_filename(self):
        fn = 'dominter.js'
        mypath = os.path.dirname(__file__)
        return os.path.join(mypath, fn)


class WsHandler(tornado.websocket.WebSocketHandler):
    """
    dominter websocket server handler
    """
    clients = {}

    def initialize(self, window=None):
        """
        initialize
        :param window: window class or instance. if class is given, it acts
        as multiple instance. if instance is given, it acts as single instance.
        :return: None
        """
        self.ismulti = False
        if isclass(window):
            self.ismulti = True
            self.window = window()
        else:
            self.window = window

    def open(self):
        logger.debug('open connection: {}'.format(self))
        wins = str(self.window)
        if wins not in self.clients:
            self.clients[wins] = []
        if self not in self.clients[wins]:
            self.clients[wins].append(self)
        if self.window is not None:
            dat = self.window._dumps()
            self.write_message(dat)

    def on_message(self, msg):
        dic = json.loads(msg)
        type_ = dic['type']
        id_ = dic['id']
        logger.debug('id: {} type:{}'.format(id_, type_))
        # system handler
        if 'change' == type_:
            objdic = self.window.document.obj_dic
            if id_ in objdic:
                obj = objdic[id_]
                if 'value' in dic:
                    obj.value = dic['value']
                if 'selectedIndex' in dic:
                    obj.selectedIndex = dic['selectedIndex']
                if 'checked' in dic:
                    obj.checked = dic['checked']
                    if obj.type == 'radio' and obj.checked:
                        # radiobuttonのcheckedは自分ではずさないといけない
                        group = self.window.document.getElementsByName(obj.name)
                        if group is not None:
                            for elm in group:
                                elm.checked = elm is obj
            if not self.ismulti:
                # boradcast if single instance
                self.broadcast(msg)
        # user handler
        if self.window is not None:
            doc = self.window.document
            if id_ in self.window.document.handlers:
                fnc = self.window.document.handlers[id_]
                if callable(fnc):
                    doc.clean_diff()
                    fnc(dic)
                    if 0 < len(doc.diffdat):
                        # self.write_message({'diff': doc.diffdat})
                        logger.debug('broadcast diff: {}'.format(len(doc.diffdat)))
                        self.broadcast({'diff': doc.diffdat})
                        doc.clean_diff()

    def broadcast(self, msg):
        cnt = 0
        wins = str(self.window)
        if self.ismulti:
            self.write_message(msg)
            cnt = 1
        else:
            # boradcast if single instance
            for cli in self.clients[wins]:
                cli.write_message(msg)
                cnt += 1
        logger.debug('broadcast count: {}'.format(cnt))

    def on_close(self):
        logger.debug('close connection: {}'.format(self))
        wins = str(self.window)
        if self in self.clients[wins]:
            self.clients[wins].remove(self)
        else:
            logger.warn('illegal :{}'.format(self))


def make_one(idx, dat, ws_path_pre, html_pre, html_post, silent):
    """
    make tornado app list for one window
    :param idx: window index
    :param dat: window class or window instance or dictionary contains window
    and other info.
    :param ws_path_pre: websocket server path prefix. (add window index for each window)
    :param html_pre: html path prefix
    :param html_post: html path suffix
    :return: app list for tornado
    """
    # win = {'window': window, 'path': html_path,}
    if isinstance(dat, dict):
        dic = dat
        win = dic.get('window')
    else:
        dic = {}
        win = dat
    if win is None:
        raise ValueError('no window')
    ws_path = '{}{}'.format(ws_path_pre, idx)
    # if no path passed, default paths are idex.html, index1.html, index2.html, ...
    html_default = '{}{}{}'.format(html_pre, '' if 0 == idx else idx, html_post)
    html_path = dic.get('path', html_default)
    inst = 'multiple' if isclass(win) else 'single'
    if not silent:
        print('dominter window {}: instance={} path={}'.format(idx, inst, html_path))
    return win, [
        (ws_path, WsHandler, {'window': win}),
        (html_path, HtmlGetHandler, {'wspath': ws_path}), ]


def make_app(wins, js_path="/dominter.js", ws_path_pre='/_ws',
             html_pre='/index', html_post='.html', silent=False):
    """
    make tornado app list for dominter
    :param wins:
    :param js_path:
    :param ws_path_pre:
    :param html_pre:
    :param html_post:
    :return: ([app list], [window list])
    """
    applst = [(js_path, JsGetHandler), ]
    winlst = []
    if isinstance(wins, dict):
        win, d = make_one(0, wins, ws_path_pre=ws_path_pre,
                          html_pre=html_pre, html_post=html_post,
                          silent=silent)
        winlst.append(win)
        applst.extend(d)
    else:
        try:
            iterator = iter(wins)
        except TypeError:
            win, d = make_one(0, wins, ws_path_pre=ws_path_pre,
                              html_pre=html_pre, html_post=html_post,
                              silent=silent)
            winlst.append(win)
            applst.extend(d)
        else:
            for j, dat in enumerate(wins):
                win, d = make_one(j, dat, ws_path_pre=ws_path_pre,
                                  html_pre=html_pre, html_post=html_post,
                                  silent=silent)
                winlst.append(win)
                applst.extend(d)
    return applst, winlst


def start_app(wins, port=8888, template_path=None, static_path=None,
              js_path="/dominter.js", ws_path_pre='/_ws',
              html_pre='/index', html_post='.html', background_msec=2000,
              silent=False):
    """
    start tornado app for dominter
    :param wins: window list. if class is provided, act as multiple-instance.
     if instance is provided, act as single-instance.
    :param port: http/websocket port
    :param template_path: tornado template_path
    :param static_path: tornado static_path
    :param js_path: dominter.js path
    :param ws_path_pre: dominter websocket server path prefix (add index for each window)
    :param html_pre: html path prefix. default='/index'
    :param html_post: html path suffix. default='.html'
    :param background_msec: background worker act period for single-instance
     in milli seconds.
    :param silent: suppress start message
    :return: None
    """
    applst, winlst = make_app(wins, js_path=js_path, ws_path_pre=ws_path_pre,
                              html_pre=html_pre, html_post=html_post,
                              silent=silent)
    if template_path is None:
        app = tornado.web.Application(applst)
    else:
        app = tornado.web.Application(applst,
                                      template_path=template_path,
                                      static_path=static_path)

    def periodic():
        # print('periodic!')
        for win in winlst:
            if not isclass(win):
                # create cache if single instance
                win._dumps()

    app.listen(port)
    if not silent:
        print('start tornado server. port: {}'.format(port))
    ioloop = tornado.ioloop.IOLoop.current()
    if background_msec > 0:
        # background worker to create cache
        tornado.ioloop.PeriodicCallback(periodic, background_msec,
                                        io_loop=ioloop).start()
    ioloop.start()


# if __name__ == "__main__":
#     pass
