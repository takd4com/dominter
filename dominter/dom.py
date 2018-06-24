# -*- coding: utf-8 -*-
# dominter: Simple Python GUI (Graphical User Interface) package for
#  small asynchronous web application.
# Copyright (c) 2017-2018 Tamini Bean
# License: MIT

import sys
import os
import json
import shlex
import re
import collections
import threading
import functools
import collections
from inspect import isclass
from logging import (getLogger, basicConfig, DEBUG, INFO, WARN, ERROR)

import tornado
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
        ik = self.attr2item_key(key)
        if ik in self:
            val = self[ik]
            self.__delitem__(ik)
            return val
        else:
            if 0 < len(args):
                return args[0]
            else:
                raise TypeError

    def popitem(self):
        res = super(Style, self).popitem()
        key, value = res
        self.elm._style_delete(key)
        return res

    def setdefault(self, key, default=None):
        ik = self.attr2item_key(key)
        if ik not in self:
            super(Style, self).__setitem__(ik, default)
            self.elm._style_set(ik, default)
        return super(Style, self).setdefault(ik, default)

    def update(self, other):
        dic = dict(other)
        dic = {self.attr2item_key(k): v for k, v in dic.items()}
        for k, v in dic.items():
            self.elm._style_set(k, v)
        super(Style, self).update(dic)

    def copy(self):
        res = super(Style, self).copy()
        return Style(self.elm, res)

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
            elif 2 < len(kv):
                key = kv[0].strip()
                value = ':'.join(kv[1:]).strip()
                self.__setitem__(key, value)
            else:
                raise ValueError()

    @property
    def cssText(self):
        return self.__str__()

    def setProperty(self, key, value):
        self[key] = value

    def removeProperty(self, key):
        res = None
        if key in self:
            res = self[key]
            self.__delitem__(key)
        return res


class StorageBase(collections.OrderedDict):
    def __init__(self, init_val=None,
                 setitem_hook=None,
                 delitem_hook=None,
                 update_hook=None,
                 clear_hook=None,
                 # pop_hook=None,
                 # popitem_hook=None,
                 # setdefault_hook=None,
                 name=None, ):
        self.name = name
        if init_val is None:
            init_val = {}
        super(StorageBase, self).__init__(init_val)
        self.setitem_hook = setitem_hook
        self.delitem_hook = delitem_hook
        self.update_hook = update_hook
        self.clear_hook = clear_hook
        # self.pop_hook = pop_hook
        # self.popitem_hook = popitem_hook
        # self.setdefault_hook = setdefault_hook

    def _raw_setitem(self, key, value):
        return super(StorageBase, self).__setitem__(key, value)

    def __setitem__(self, key, value):
        if callable(self.setitem_hook):
            if not self.setitem_hook(key, value, name=self.name):
                return
        super(StorageBase, self).__setitem__(key, value)

    def _raw_delitem(self, key):
        super(StorageBase, self).__delitem__(key)

    def __delitem__(self, key):
        if callable(self.delitem_hook):
            if not self.delitem_hook(key, name=self.name):
                return
        super(StorageBase, self).__delitem__(key)

    def _raw_pop(self, key, *args):
        return super(StorageBase, self).pop(key, *args)

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

    def _raw_popitem(self):
        return super(StorageBase, self).popitem()

    def popitem(self):
        res = super(StorageBase, self).popitem()
        key, value = res
        self.__delitem__(key)
        return res

    def _raw_setdefault(self, key, default=None):
        return super(StorageBase, self).setdefault(key, default)

    def setdefault(self, key, default=None):
        if key not in self:
            super(StorageBase, self).__setitem__(key, default)
            self.__setitem__(key, default)
        return super(StorageBase, self).setdefault(key, default)

    def _raw_update(self, other):
        return super(StorageBase, self).update(other)

    def update(self, other):
        dic = dict(other)
        for k, v in dic.items():
            self.setitem_hook(k, v, name=self.name)
        super(StorageBase, self).update(dic)

    def _raw_clear(self):
        return super(StorageBase, self).clear()

    def clear(self):
        if callable(self.clear_hook):
            if not self.clear_hook(name=self.name):
                return
        if 0 < len(self):
            super(StorageBase, self).clear()

    @property
    def length(self):
        return len(self)

    def key(self, index):
        try:
            return list(self.keys())[index]
        except IndexError:
            return None

    def getItem(self, key):
        return self.get(key)

    def setItem(self, key, value):
        self[key] = value

    def removeItem(self, key):
        self.pop(key, None)


class WinStorage(StorageBase):
    def __init__(self, window, init_val=None, name=None):
        super(WinStorage, self).__init__(init_val=init_val,
                                         name=name,
                                         setitem_hook=window._storage_setitem,
                                         delitem_hook=window._storage_delitem,
                                         update_hook=window._storage_update,
                                         clear_hook=window._storage_clear,
                                         )


class ThreadSafe(object):
    _disabled = False
    _tornado_thread_id = None
    ioloop = None

    @classmethod
    def set_tornado_thread_id(cls, ioloop):
        # must call from tornado thread
        cls._tornado_thread_id = threading.current_thread().ident
        cls.ioloop = ioloop

    @classmethod
    def invoke_required(cls):
        if cls._disabled:
            return False
        elif cls._tornado_thread_id is None:
            return False
        elif cls._tornado_thread_id == threading.current_thread().ident:
            return False
        else:
            return True

    @classmethod
    def enable(cls):
        cls._disabled = False

    @classmethod
    def disable(cls):
        cls._disabled = True


# decorator PENDING
def element_thread_safe(fnc):
    @functools.wraps(fnc)
    def wrap(self, *args, **kwargs):
        if (not ThreadSafe.invoke_required() or
                not hasattr(self, '_in_init_') or
                self._in_init_):
            return fnc(self, *args, **kwargs)
        else:
            self.document.window.invoke(fnc, self, *args, **kwargs)
    return wrap


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
        self._childList = ChildList(self)
        self._classList = ClassList(self)
        self._style = Style(self)
        self._onclick = None
        self._onchange = None
        self._sortorder = 0 # to sort childList
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
        self._in_init_ = False

    dif_excepts = ['_in_init_', '_sortorder', 'classList', '_classList', 'style',
                   'childList', '_childList',
                   'parent', 'document',
                   'onclick', '_onclick', 'onchange', '_onchange', ]
    ser_excepts = ['_in_init_', '_sortorder', 'parent', 'document', ]

    def _raw_setattr(self, key, value):
        super(Element, self).__setattr__(key, value)

    def _pre_setattr(self, key, value):
        if 'document' in self.__dict__:
            if (not self._in_init_) and (key not in self.dif_excepts):
                self.document._add_diff({_OBJKEY_: self._id, key: value})

    # @element_thread_safe # PENDING
    def __setattr__(self, key, value):
        # logger.debug('thread:{} key:{} value:{}'.format(threading.current_thread().ident, key, value))
        self._pre_setattr(key, value)
        super(Element, self).__setattr__(key, value)

    def _raw_delattr(self, key):
        super(Element, self).__delattr__(key)

    def _pre_delattr(self, key):
        if (not self._in_init_) and (key not in self.dif_excepts):
            self.document._add_diff({_OBJKEY_: self._id, '_delattr': [key, ]})

    def __delattr__(self, item):
        self._pre_delattr(item)
        super(Element, self).__delattr__(item)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._set_id(value)

    def _set_id(self, txt):
        orgid = self._id
        self.__dict__['_id'] = txt
        objdic = self.document._obj_dic
        if orgid in objdic:
            del(objdic[orgid])
        objdic[txt] = self

    @property
    def childList(self):
        return self._childList

    @childList.setter
    def childList(self, lst):
        self._set_child_list(lst)

    def _set_child_list(self, lst):
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
        self._set_style(value)

    def _set_style(self, value):
        self._style.cssText = value

    def _addhandler(self, fnc):
        name = repr(fnc)
        self.document._handlers[name] = fnc
        return name

    @property
    def onclick(self):
        return self._onclick

    @onclick.setter
    def onclick(self, value):
        self._set_onclick(value)

    def _set_onclick(self, fnc):
        self._onclick = fnc
        name = self._addhandler(fnc)
        self.document._add_diff({_OBJKEY_: self.id, 'onclick': name})

    @property
    def onchange(self):
        return self._onchange

    @onchange.setter
    def onchange(self, value):
        self._set_onchange(value)

    def _set_onchange(self, fnc):
        self._onchange = fnc
        name = self._addhandler(fnc)
        self.document._add_diff({_OBJKEY_: self._id, 'onchange': name})

    def removeChild(self, elm):
        if elm not in self._childList:
            raise ValueError('not child')
        self.document._add_diff({_OBJKEY_: self._id, '_removeChild': elm.id})
        elm.parent = None
        self._childList._raw_remove(elm)

    def appendChild(self, elm):
        if elm.parent is not None:
            elm.parent.removeChild(elm)
        self.childList._raw_append(elm)
        elm.parent = self
        self.document._add_diff({_OBJKEY_: self._id, '_appendChild': elm.id})
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
                self.document._add_diff({_OBJKEY_: parent._id, '_appendChild': chd.id})
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
            self.document._add_diff({_OBJKEY_: self._id, '_insertBefore': [new_elm._id, ref_elm._id]})

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
            self.document._add_diff({_OBJKEY_: self._id, '_replaceChild': [new_elm._id, old_elm._id]})

    def getAttribute(self, name):
        if 'style' == name:
            return str(self._style)
        elif 'class' == name:
            return self.className
        elif name in self.__dict__:
            return self.__dict__[name]

    def setAttribute(self, name, value):
        if 'style' == name:
            # self._style.set_text(value)
            # self.style.cssText = value
            self._set_style(value)
        elif 'class' == name:
            self.className = value
        else:
            self._raw_setattr(name, value)
            self.document._add_diff({_OBJKEY_: self._id, '_setAttributes': {name: value}})

    def removeAttribute(self, name):
        if 'style' == name:
            self._style.clear()
        elif 'class' == name:
            self.className = ''
        elif name in self.__dict__:
            self.document._add_diff({_OBJKEY_: self._id, '_removeAttributes': [name, ]})
            self._raw_delattr(name)

    def addEventListener(self, type_, listener):
        self._eventlisteners.append((type_, listener))
        self.document._add_diff({_OBJKEY_: self._id, '_addEventListener': [type_, repr(listener), ]})
        self._addhandler(listener)

    def removeEventListener(self, type_, listener):
        tpl = (type_, listener)
        if tpl in self._eventlisteners:
            self._eventlisteners.remove(tpl)
            name = repr(listener)
            self.document._add_diff({_OBJKEY_: self._id, '_removeEventListener': [type_, name, ]})
            del(self.document._handlers[name])

    def focus(self):
        self.document._add_diff({_OBJKEY_: self._id, '_method': 'focus'})

    def blur(self):
        self.document._add_diff({_OBJKEY_: self._id, '_method': 'blur'})

    def scrollIntoView(self, alignToTop=None, behavior=None, block=None, inline=None):
        self.document._add_diff({_OBJKEY_: self._id, '_method': 'scrollIntoView',
                                 'alignToTop': alignToTop, 'behavior': behavior,
                                  'block': block, 'inline': inline})

    def getContext(self, contextType, contextAttributes=None):
        res = RenderingContext(self, contextType, contextAttributes)
        return res

    def _dumps(self):
        # self.onload()
        str = json.dumps(self, default=self._serializer, indent=2)
        # print(str)
        return str

    @staticmethod
    def _serializer(obj):
        if isinstance(obj, Element):
            dic = obj.__dict__.copy()
            # delete reference to other elements to avoid circular reference
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
        self.document._add_diff({_OBJKEY_: self._id, '_reverseChild': True})
        return True

    def _childList_sort(self, key=None, reverse=False):
        for j, elm in enumerate(self.childList):
            elm._sortorder = j
        self.childList._raw_sort(key=key, reverse=reverse)
        ordr = list([elm._sortorder for elm in self.childList])
        self.document._add_diff({_OBJKEY_: self._id, '_sortChild': ordr})
        return False

    def _childList_clear(self):
        self.document._add_diff({_OBJKEY_: self._id, '_clearChild': True})
        for elm in self.childList:
            elm.parent = None
        return True

    def _classList_append(self, txt):
        self.document._add_diff({_OBJKEY_: self._id, '_addClass': [txt, ]})
        return True

    def _classList_insert(self, index, txt):
        self.document._add_diff({_OBJKEY_: self._id, '_addClass': [txt, ]})
        return True

    def _classList_extend(self, lst):
        self.document._add_diff({_OBJKEY_: self._id, '_addClass': lst})
        return True

    def _classList_remove(self, txt):
        self.document._add_diff({_OBJKEY_: self._id, '_removeClass': [txt, ]})
        return True

    def _classList_pop(self, idx):
        if 0 <= idx < len(self._classList):
            txt = self._classList[idx]
            self.document._add_diff({_OBJKEY_: self._id, '_removeClass': [txt, ]})
        return True, None

    def _classList_setitem(self, idx, value):
        if isinstance(idx, int):
            elm = self._classList[idx]
            if not isinstance(value, str):
                raise TypeError('can only assign an str')
            self.document._add_diff({_OBJKEY_: self._id, '_addClass': [value, ]})
            if elm:
                self.document._add_diff({_OBJKEY_: self._id, '_removeClass': [elm, ]})
        elif isinstance(idx, slice):
            lst = self._classList[idx]
            if (not isinstance(value, list)) and (not isinstance(value, tuple)):
                raise TypeError('can only assign an iterable')
            if 0 == len(lst):
                for elm in value:
                    self.document._add_diff({_OBJKEY_: self._id, '_addClass': elm})
            else:
                ref = lst[0]
                self.document._add_diff({_OBJKEY_: self._id, '_addClass': value})
                self.document._add_diff({_OBJKEY_: self._id, '_removeClass': lst})
        else:
            raise TypeError('bad value type')
        return True

    def _classList_delitem(self, idx):
        lst = self._classList[idx]
        if lst:
            if isinstance(lst, str):
                lst = [lst,]
            self.document._add_diff({_OBJKEY_: self._id, '_removeClass': lst})
        return True

    def _classList_clear(self):
        self.document._add_diff({_OBJKEY_: self._id, '_clearClass': True})
        return True

    def _style_set(self, key, value):
        self.document._add_diff({_OBJKEY_: self._id, '_setStyle': {key: value}})
        return True

    def _style_delete(self, key):
        self.document._add_diff({_OBJKEY_: self._id, '_deleteStyle': [key, ]})
        return True

    def _style_clear(self):
        self.document._add_diff({_OBJKEY_: self._id, '_clearStyle': True})
        return True


class DomObject(object):
    def __init__(self, document, parent, method, objtyp, *args):
        self._id = str(id(self))
        self.document = document
        self.parent = parent
        self.method = method
        self.objtyp = objtyp
        self._eventlisteners = []
        dic = {_OBJKEY_: parent._id,
               '_win_method': '_create',
               '_method': method,
               '_objType': objtyp,
               '_id': self._id,
               'args': args,
               '_register': True,
               }
        document._add_diff(dic)
        self.document._obj_dic[self._id] = self

    excepts = ('_id', 'document', 'parent', 'method', 'objtyp',
               '_eventlisteners', '_del', 'excepts')

    def __enter__(self):
        return self

    def delme(self):
        self._raw_setattr('_del', True)
        dic = {_OBJKEY_: self._id,
               '_objType': 'RenderingContext',
               '_method': '__del__',
               }
        self.document._add_diff(dic)
        logger.info('{}: {}'.format(_OBJKEY_, self._id)) # tmp

    def __exit__(self, exc_type, exc_value, tb):
        if not hasattr(self, '_del'):
            self.delme()

    def __del__(self):
        if not hasattr(self, '_del'):
            self.delme()

    def _raw_setattr(self, key, value):
        super(DomObject, self).__setattr__(key, value)

    def _raw_getattr(self, name):
        return super(DomObject, self).__getattr__(name)

    def __setattr__(self, key, value):
        # logger.debug('thread:{} key:{} value:{}'.format(threading.current_thread().ident, key, value))
        if key in self.excepts:
            super(DomObject, self).__setattr__(key, value)
            return
        dic = {_OBJKEY_: self._id,
               '_objType': self.objtyp,
               '_method': 'setattr',
               'key': key,
               'value': value,
               '_valueType': '',
               }
        self.document._add_diff(dic)
        super(DomObject, self).__setattr__(key, value)

    def __getattr__(self, name):
        if name in self.excepts:
            return super(DomObject, self).__getattr__(name)
        def fnc(*args):
            dic = {_OBJKEY_: self._id,
                   '_objType': self.objtyp,
                   '_method': name,
                   'args': args,
                   }
            self.document._add_diff(dic)
        self._raw_setattr(name, fnc)
        return fnc

    def _addhandler(self, fnc):
        name = repr(fnc)
        self.document._handlers[name] = fnc
        return name

    def addEventListener(self, type_, listener):
        self._eventlisteners.append((type_, listener))
        dic = {_OBJKEY_: self._id,
               '_method':'addEventListener',
               'args': [type_, repr(listener), ]}
        self.document._add_diff(dic)
        self._addhandler(listener)

    def removeEventListener(self, type_, listener):
        tpl = (type_, listener)
        if tpl in self._eventlisteners:
            self._eventlisteners.remove(tpl)
            name = repr(listener)
            dic = {_OBJKEY_: self._id,
                   '_method': 'removeEventListener',
                   'args': [type_, name, ]}
            self.document._add_diff(dic)
            del(self.document._handlers[name])


class RenderingContext(object):
    def __init__(self, canvas, contextType, contextAttributes=None):
        self._id = str(id(self))
        self.canvas = canvas
        dic = {_OBJKEY_: canvas._id,
               '_method': 'getContext',
               'contentType': contextType,
               'contextAttributes': contextAttributes,
               '_id': self._id,
               }
        canvas.document._add_diff(dic)

    def __enter__(self):
        return self

    def delme(self):
        self._raw_setattr('_del', True)
        dic = {_OBJKEY_: self._id,
               '_objType': 'RenderingContext',
               '_method': '__del__',
               }
        self.canvas.document._add_diff(dic)
        logger.info('{}: {}'.format(_OBJKEY_, self._id)) # tmp

    def __exit__(self, exc_type, exc_value, tb):
        if not hasattr(self, '_del'):
            self.delme()

    def __del__(self):
        if not hasattr(self, '_del'):
            self.delme()

    excepts = ('_id', 'canvas', '_del', 'excepts')
    creates = ('createLinearGradient',
               'createRadialGradient',
               'createPattern',
               )

    def _raw_setattr(self, key, value):
        super(RenderingContext, self).__setattr__(key, value)

    def _raw_getattr(self, name):
        return super(RenderingContext, self).__getattr__(name)

    def __setattr__(self, key, value):
        # logger.debug('thread:{} key:{} value:{}'.format(threading.current_thread().ident, key, value))
        if key in self.excepts:
            super(RenderingContext, self).__setattr__(key, value)
            return
        dic = {_OBJKEY_: self._id,
               '_objType': 'RenderingContext',
               '_method': 'setattr',
               'key': key,
               'value': value,
               '_valueType': '',
               }
        if isinstance(value, DomObject):
            dic['value'] = value._id
            dic['_valueType'] = 'DomObject'
        self.canvas.document._add_diff(dic)
        super(RenderingContext, self).__setattr__(key, value)

    def __getattr__(self, name):
        if name in self.excepts:
            return super(RenderingContext, self).__getattr__(name)
        def modargs(args):
            res = []
            for arg in args:
                if arg in self.canvas.document._obj_dic.values():
                    res.append({'_id': arg._id, })
                else:
                    res.append(arg)
            return res
        if name in self.creates:
            def fnc(*args):
                lst = modargs(args)
                res = DomObject(self.canvas.document, self, name, 'RenderingContext', *lst)
                return res
        else:
            def fnc(*args):
                lst = modargs(args)
                self.canvas.document._add_diff({_OBJKEY_: self._id,
                                                '_objType': 'RenderingContext',
                                                '_method': name,
                                                'args': lst,
                                                '_register': False,
                                                })
        self._raw_setattr(name, fnc)
        return fnc


class Document(object):
    """
    virtual document class
    """
    def __init__(self, window):
        self._dirty_diff = False
        self._dirty_cache = True
        self._obj_dic = {}
        self._diffdat = []
        self._handlers = {}
        self.head = Element(self, 'head')
        self.body = Element(self, 'body')
        self.window = window
        self._window_element = Element(self, '_window_element')
        self._cache = None

    def _clean_diff(self):
        self._diffdat = []
        self._dirty_diff = False

    def _add_diff(self, dat):
        self._dirty_diff = True
        self._dirty_cache = True
        self._diffdat.append(dat)

    def getElementById(self, eid):
        if isinstance(eid, int):
            eid = str(eid)
        return self._obj_dic.get(eid, None)

    def getElementsByName(self, name):
        return [elm for key, elm in self._obj_dic.items()
                if elm.name == name]

    def getElementsByTagName(self, tag):
        return [elm for key, elm in self._obj_dic.items()
                if elm.tagName == tag]

    def getElementsByClassName(self, cls):
        return [elm for key, elm in self._obj_dic.items()
                if cls in elm.classList]

    def createElement(self, tag):
        elm = Element(self, tag)
        dat = elm._dumps()
        self._add_diff({_OBJKEY_: elm._id, '_createElement': dat})
        self._obj_dic[elm._id] = elm
        return elm

    """ not supported. use span
    def createTextNode(self, txt):
        pass
    """

    def tag(self, tagtxt, textContent=None, attrs=None,
            onclick=None, onchange=None, handler=None, childList=None):
        """
        create a tag with a specification method similar to html.

        :param tagtxt:
        :param textContent:
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
                elm.__dict__[d[0]] = True
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
        if attrs is not None:
            for key, val in attrs.items():
                elm.setAttribute(key, val)
        if onclick is not None:
            elm.onclick = onclick
        if onchange is not None:
            elm.onchange = onchange
        if handler is not None:
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
                    min=None, max=None, step=None,
                    minlength=None, maxlength=None, pattern=None,
                    multiple=None, size=None,
                    label=None, selected=None, rows=None, cols=None,
                    alt=None, width=None, height=None, href=None, rel=None,
                    integrity=None, media=None, scoped=None, crossorigin=None,
                    longdesc=None, sizes=None, referrerpolicy=None,
                    srcset=None, download=None, target=None,
                    readonly=None, disabled=None, placeholder=None, for_=None,
                    id_=None, accesskey=None, hidden=None, tabindex=None,
                    title=None, style=None, className=None, childList=None,
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
        if minlength is not None:
            elm.minlength = minlength
        if maxlength is not None:
            elm.maxlength = maxlength
        if pattern is not None:
            elm.pattern = pattern
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
        if title is not None:
            elm.title = title
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

    def title(self, textContent, id_=None):
        return self.create_with('title', textContent=textContent, id_=id_)

    def style(self, textContent, type_='text/css', media=None, scoped=None, id_=None):
        return self.create_with('style', textContent=textContent, type_=type_,
                                media=media, scoped=scoped, id_=id_)

    def link(self, href, rel='stylesheet', integrity=None, media=None, id_=None):
        return self.create_with('link', href=href, rel=rel, integrity=integrity,
                                media=media, id_=id_)

    def script(self, textContent='', type_='text/javascript', src=None,
               crossorigin=None, id_=None):
        return self.create_with('script', textContent=textContent, type_=type_,
                                src=src, crossorigin=crossorigin, id_=id_)

    def br(self, id_=None):
        return self.create_with('br', id_=id_)

    def p(self, textContent, id_=None, tabindex=None, title=None,
          style=None, className=None):
        return self.create_with('p', textContent=textContent,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def span(self, textContent, id_=None, tabindex=None, title=None,
             style=None, className=None):
        return self.create_with('span', textContent=textContent,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def div(self, textContent=None, id_=None,  tabindex=None, title=None,
            style=None, className=None, childList=None):

        return self.create_with('div', textContent=textContent,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className,
                                childList=childList)

    def button(self, textContent='', type_='button', name=None, value=None,
               disabled=None, onclick=None, tabindex=None, title=None,
               id_=None, style=None, className=None):
        return self.create_with('button', textContent=textContent,
                                type_=type_, name=name, value=value,
                                disabled=disabled, onclick=onclick,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def text(self, value='', type_='text', onchange=None,
             readonly=None, disabled=None, placeholder=None,
             pattern=None, minlength=None, maxlength=None, size=None,
             id_=None, tabindex=None, title=None, style=None, className=None):
        return self.create_with('input', type_=type_, value=value,
                                onchange=onchange, readonly=readonly,
                                disabled=disabled, placeholder=placeholder,
                                pattern=pattern, size=size,
                                minlength=minlength, maxlength=maxlength,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def checkbox(self, checked=False, value=None, onchange=None,
                 readonly=None, disabled=None,
                 id_=None, tabindex=None, title=None,
                 style=None, className=None):
        return self.create_with('input', type_='checkbox', value=value,
                                checked=checked, readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def radio(self, name, value, checked=False, onchange=None,
              readonly=None, disabled=None,
              id_=None, tabindex=None, title=None,
              style=None, className=None):
        return self.create_with('input', type_='radio', name=name, value=value,
                                checked=checked, readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def color(self, value='', onchange=None, readonly=None, disabled=None,
              id_=None, tabindex=None, title=None,
              style=None, className=None):
        return self.create_with('input', type_='color', value=value,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def date(self, value='', onchange=None, readonly=None, disabled=None,
             id_=None, tabindex=None, title=None,
             style=None, className=None):
        return self.create_with('input', type_='date', value=value,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def datetime_local(self, value='', onchange=None, step='1',
                       readonly=None, disabled=None,
                       id_=None, tabindex=None, title=None,
                       style=None, className=None):
        return self.create_with('input', type_='datetime-local', value=value,
                                 step=step, readonly=readonly,
                                 onchange=onchange, disabled=disabled,
                                 id_=id_, tabindex=tabindex, title=title,
                                 style=style, className=className)

    def month(self, value='', onchange=None, readonly=None, disabled=None,
              id_=None, tabindex=None, title=None,
              style=None, className=None):
        return self.create_with('input', type_='month', value=value,
                                 readonly=readonly,
                                 onchange=onchange, disabled=disabled,
                                 id_=id_, tabindex=tabindex, title=title,
                                 style=style, className=className)

    def time(self, value='', onchange=None, step='1',
             readonly=None, disabled=None,
             id_=None, tabindex=None, title=None,
             style=None, className=None):
        return self.create_with('input', type_='time', value=value,
                                 step=step, readonly=readonly,
                                 onchange=onchange, disabled=disabled,
                                 id_=id_, tabindex=tabindex, title=title,
                                 style=style, className=className)

    def week(self, value='', onchange=None, readonly=None, disabled=None,
             id_=None, tabindex=None, title=None,
             style=None, className=None):
        return self.create_with('input', type_='week', value=value,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def file(self, value='', onchange=None, readonly=None, disabled=None,
             id_=None, tabindex=None, title=None,
             style=None, className=None):
        return self.create_with('input', type_='file', value=value,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def number(self, value='', min=None, max=None, step=None, onchange=None,
               readonly=None, disabled=None,
               id_=None, tabindex=None, title=None,
               style=None, className=None):
        return self.create_with('input', type_='number', value=value,
                                min=min, max=max, step=step,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def password(self, value='', onchange=None, readonly=None, disabled=None,
                 id_=None, tabindex=None, title=None,
                 style=None, className=None):
        return self.create_with('input', type_='password', value=value,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def range(self, value='', min='0', max='100', step='1', onchange=None,
              readonly=None, disabled=None,
              id_=None, tabindex=None, title=None,
              style=None, className=None):
        return self.create_with('input', type_='range', value=value,
                                min=min, max=max, step=step,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def select(self, value=None, selectedIndex=None, name=None, onchange=None,
               multiple=None, size=None, readonly=None, disabled=None,
               id_=None, tabindex=None, title=None,
               style=None, className=None):
        return self.create_with('select', value=value, name=name,
                                selectedIndex=selectedIndex, multiple=multiple,
                                size=size, readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def option(self, value, textContent, label=None, selected=None,
               onchange=None, readonly=None, disabled=None,
               id_=None, tabindex=None, title=None,
               style=None, className=None):
        return self.create_with('option', value=value, textContent=textContent,
                                label=label, selected=selected,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def textarea(self, value, rows=None, cols=None, onchange=None,
                 readonly=None, disabled=None,
                 id_=None, tabindex=None, title=None,
                 style=None, className=None):
        return self.create_with('textarea', value=value, rows=rows, cols=cols,
                                readonly=readonly,
                                onchange=onchange, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def table(self, readonly=None, disabled=None,
              id_=None, tabindex=None, title=None,
              style=None, className=None, childList=None):
        return self.create_with('table',
                                readonly=readonly, disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className,
                                childList=childList)

    def tr(self, id_=None, tabindex=None, title=None,
           style=None, className=None, childList=None):
        return self.create_with('tr',
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className,
                                childList=childList)

    def th(self, textContent,
           id_=None, tabindex=None, title=None,
           style=None, className=None):
        return self.create_with('th', textContent=textContent,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def td(self, textContent,
           id_=None, tabindex=None, title=None,
           style=None, className=None):
        return self.create_with('td', textContent=textContent,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def fieldset(self, textContent='', disabled=None,
                 id_=None, tabindex=None, title=None,
                 style=None, className=None, childList=None):
        return self.create_with('fieldset', textContent=textContent,
                                disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className,
                                childList=childList)

    def legend(self, textContent, disabled=None,
               id_=None, tabindex=None, title=None,
               style=None, className=None):
        return self.create_with('legend', textContent=textContent,
                                disabled=disabled,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def img(self, src, alt='', width=None, height=None, onclick=None,
            crossorigin=None, longdesc=None, sizes=None, referrerpolicy=None,
            srcset=None,
            id_=None, tabindex=None, title=None,
            style=None, className=None):
        return self.create_with('img', src=src, alt=alt, width=width, height=height,
                                onclick=onclick, crossorigin=crossorigin,
                                longdesc=longdesc, sizes=sizes,
                                referrerpolicy=referrerpolicy, srcset=srcset,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def a(self, href, textContent, download=None, rel=None, target=None,
          referrerpolicy=None,
          id_=None, tabindex=None, title=None,
          style=None, className=None):
        return self.create_with('a', href=href, textContent=textContent,
                                download=download, rel=rel, target=target,
                                referrerpolicy=referrerpolicy,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def label(self, textContent, for_=None,
              id_=None, tabindex=None, title=None,
              style=None, className=None):
        return self.create_with('label', textContent=textContent, for_=for_,
                                id_=id_, tabindex=tabindex, title=title,
                                style=style, className=className)

    def h1(self, textContent, id_=None, accesskey=None, hidden=None,
           tabindex=None, title=None, style=None, className=None):
        return self.create_with('h1', textContent=textContent,
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className)

    def h2(self, textContent, id_=None, accesskey=None, hidden=None,
           tabindex=None, title=None, style=None, className=None):
        return self.create_with('h2', textContent=textContent,
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className)

    def h3(self, textContent, id_=None, accesskey=None, hidden=None,
           tabindex=None, title=None, style=None, className=None):
        return self.create_with('h3', textContent=textContent,
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className)

    def h4(self, textContent, id_=None, accesskey=None, hidden=None,
           tabindex=None, title=None, style=None, className=None):
        return self.create_with('h4', textContent=textContent,
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className)

    def h5(self, textContent, id_=None, accesskey=None, hidden=None,
           tabindex=None, title=None, style=None, className=None):
        return self.create_with('h5', textContent=textContent,
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className)

    def h6(self, textContent, id_=None, accesskey=None, hidden=None,
           tabindex=None, title=None, style=None, className=None):
        return self.create_with('h6', textContent=textContent,
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className)

    def ol(self, id_=None, accesskey=None, hidden=None,
           tabindex=None, title=None, style=None, className=None,
           childList=None):
        return self.create_with('ol',
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className,
                                childList=childList)

    def ul(self, id_=None, accesskey=None, hidden=None,
           tabindex=None, title=None, style=None, className=None,
           childList=None):
        return self.create_with('ul',
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className,
                                childList=childList)

    def li(self, textContent, id_=None, accesskey=None, hidden=None,
           tabindex=None, title=None, style=None, className=None,
           childList=None):
        return self.create_with('li', textContent=textContent,
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className,
                                childList=childList)

    def section(self, id_=None, accesskey=None, hidden=None,
                tabindex=None, title=None, style=None, className=None,
                childList=None):
        return self.create_with('section', id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className,
                                childList=childList)

    def header(self, id_=None, accesskey=None, hidden=None,
               tabindex=None, title=None, style=None, className=None,
               childList=None):
        return self.create_with('header',
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className,
                                childList=childList)

    def footer(self, id_=None, accesskey=None, hidden=None,
               tabindex=None, title=None, style=None, className=None,
               childList=None):
        return self.create_with('footer',
                                id_=id_, accesskey=accesskey,
                                hidden=hidden, tabindex=tabindex, title=title,
                                style=style, className=className,
                                childList=childList)


# decorator PENDING
def window_thread_safe(fnc):
    @functools.wraps(fnc)
    def wrap(self, *args, **kwargs):
        if ThreadSafe.invoke_required():
            self.invoke(fnc, self, *args, **kwargs)
        else:
            return fnc(self, *args, **kwargs)
    return wrap


class Window(object):
    """
    virtual window class
    """
    def __init__(self):
        self._id = str(id(self))
        self.document = Document(self)
        #self.name = ''
        self._socks = []
        self._modalcallback = None
        self._win_dic = {}
        self._win_cnt = 0
        self.location = None
        self.localStorage = WinStorage(window=self, name='localStorage')
        self.sessionStorage = WinStorage(window=self, name='sessionStorage')

    def _add_sock(self, sock):
        self._socks.append(sock)

    def _remove_sock(self, sock):
        if sock in self._socks:
            self._socks.remove(sock)

    def _dumps(self):
        if self.document._dirty_cache:
            logger.debug('create cache')
            s = json.dumps(self.document, default=self._serializer, indent=2)
            self.document._cache = s
            self.document._dirty_cache = False
        else:
            s = self.document._cache
        return s

    @staticmethod
    def _serializer(obj):
        if isinstance(obj, Document):
            return {'head': obj.head, 'body': obj.body,
                    '_window_element': obj._window_element, }
        if isinstance(obj, Element):
            return Element._serializer(obj)
        if callable(obj):
            name = repr(obj)
            return name
        raise TypeError(repr(obj) + " is not serializable!")

    def sync(self):
        if 0 < len(self._socks):
            self._socks[0].sync()

    def invoke(self, fnc, *args, **kwargs):
        # invoke fnc   * thread safe
        logger.debug("thread:{} self:{}".format(threading.current_thread().ident, self))
        #ioloop = tornado.ioloop.IOLoop.current()
        ioloop = ThreadSafe.ioloop
        if ioloop is None:
            return

        def f():
            fnc(*args, **kwargs)
            self.sync()
        ioloop.add_callback(f)
        return True

    def set_timeout(self, fnc, delay, *args, **kwargs):
        logger.debug("thread:{} self:{}".format(threading.current_thread().ident, self))
        #ioloop = tornado.ioloop.IOLoop.current()
        ioloop = ThreadSafe.ioloop
        if ioloop is None:
            return

        def f():
            fnc(*args, **kwargs)
            self.sync()
        # self._timeout_id += 1
        hdl = ioloop.call_later(delay, f)
        # self._timeout_dic[self._timeout_id] = hdl
        # return self._timeout_id
        return hdl

    # @window_thread_safe # PENDING
    def remove_timeout(self, hdl):
        #ioloop = tornado.ioloop.IOLoop.current()
        ioloop = ThreadSafe.ioloop
        if ioloop is None:
            return
        # hdl = self._timeout_dic.get(timeout_id)
        if hdl is None:
            logger.error('unknown timer_id')
            return False
        else:
            ioloop.remove_timeout(hdl)
            return True

    @staticmethod
    def invoke_required():
        return ThreadSafe.invoke_required()

    def addEventListener(self, type_, listener):
        elm = self.document._window_element
        elm._eventlisteners.append((type_, listener))
        name = elm._addhandler(listener)
        self.document._add_diff({_OBJKEY_: '_window_handler', '_addEventListener': [type_, name, ]})

    def removeEventListener(self, type_, listener):
        elm = self.document._window_element
        tpl = (type_, listener)
        if tpl in elm._eventlisteners:
            elm._eventlisteners.remove(tpl)
            name = repr(listener)
            self.document._add_diff({_OBJKEY_: '_window_handler', '_removeEventListener': [type_, name, ]})
            del(self.document._handlers[name])

    # def onload(self, ev): # called when uesr defined
    #    logger.debug('default onload. location:{}'.format(self.location))

    def _modaldialog(self, typ, msg, callback=None, value=None):
        if callable(callback):
            self._modalcallback = callback
            name = repr(callback)
        else:
            name = ''
        self.document._add_diff({'_win_method': typ, _OBJKEY_: '', 'message': msg, 'callback': name, 'value': value})

    def alert(self, msg, callback=None):
        self._modaldialog('_alert', msg=msg, callback=callback)

    def confirm(self, msg, callback=None):
        self._modaldialog('_confirm', msg=msg, callback=callback)

    def prompt(self, msg, value='', callback=None):
        self._modaldialog('_prompt', msg=msg, callback=callback, value=value)

    def open(self, url, name, features=None, callback=None):
        self._win_cnt += 1
        winid = self._win_cnt
        self.document._add_diff({'_win_method': '_open', _OBJKEY_: '', 'url': url, 'name': name,
                                 'features': features, 'callback': callback, 'window': winid})
        return winid

    def _simplefnc(self, typ, window):
        self.document._add_diff({'_win_method': typ, _OBJKEY_: window, })

    def close(self, window=None):
        self._simplefnc('_close', window)

    def blur(self, window=None):
        self._simplefnc('_blur', window)

    def focus(self, window=None):
        self._simplefnc('_focus', window)

    #def minimize(self, window=None):
    #    self._simplefnc('_minimize', window)

    def print_(self, window=None):
        self._simplefnc('_print', window)

    def _xyfnc(self, typ, x, y, window):
        self.document._add_diff({'_win_method': typ, _OBJKEY_: window, 'x': x, 'y': y})

    def moveBy(self, x, y, window=None):
        self._xyfnc('_moveBy', x, y, window)

    def moveTo(self, x, y, window=None):
        self._xyfnc('_moveTo', x, y, window)

    def resizeBy(self, x, y, window=None):
        self._xyfnc('_resizeBy', x, y, window)

    def resizeTo(self, x, y, window=None):
        self._xyfnc('_resizeTo', x, y, window)

    def scroll(self, x, y, window=None):
        self._xyfnc('_scroll', x, y, window)

    def scrollBy(self, x, y, window=None):
        self._xyfnc('_scrollBy', x, y, window)

    def scrollTo(self, x, y, window=None):
        self._xyfnc('_scrollTo', x, y, window)

    def _storage_setitem(self, key, value, name=''):
        self.document._add_diff({_OBJKEY_: '_' + name, 'setitem': [key, value, ]})
        return True

    def _storage_delitem(self, key, name=''):
        self.document._add_diff({_OBJKEY_: '_' + name, 'delitem': key})
        return True

    def _storage_update(self, other, name=''):
        self.document._add_diff({_OBJKEY_: '_' + name, 'update': other})
        return True

    def _storage_clear(self, name=''):
        self.document._add_diff({_OBJKEY_: '_' + name, 'clear': True})
        return True

    def Image(self):
        res = DomObject(self.document, self, 'Image', 'Image')
        return res


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
        # logger.debug("thread:{} self:{}".format(threading.current_thread().ident, self))
        self.ismulti = False
        if isclass(window):
            self.ismulti = True
            self.window = window()
        else:
            self.window = window
        self.window._add_sock(self)

    def open(self):
        # logger.debug('open connection: {}'.format(self))
        logger.debug("thread:{} self:{} open connection.".format(threading.current_thread().ident, self))
        wins = str(self.window)
        if wins not in self.clients:
            self.clients[wins] = []
        if self not in self.clients[wins]:
            self.clients[wins].append(self)
        # self.send_whole_data() # sometimes not sent

    def send_whole_data(self):
        if self.window is not None:
            dat = self.window._dumps()
            logger.debug('thread:{} self:{} send window dat(len={})'.format(
                threading.current_thread().ident, self, len(dat)))
            self.write_message(dat)
            # tornado.ioloop.IOLoop.current().call_later(0.01, self.write_message, dat)
        else:
            logger.warn('thread:{} self:{} no window dat'.format(threading.current_thread().ident, self))

    def on_message(self, msg):
        dic = json.loads(msg)
        type_ = dic['type']
        id_ = dic['id']
        logger.debug('id: {} type:{}'.format(id_, type_))
        win = self.window
        doc = win.document
        # logger.debug("thread:{} self:{} id: {} type:{}".format(threading.current_thread().ident, self, id_, type_))
        # system handler
        if 'open' == type_:
            self.send_whole_data()
            win.location = dic.get('location')
            win.localStorage._raw_update(dic.get('localStorage'))
            win.sessionStorage._raw_update(dic.get('sessionStorage'))
            if hasattr(win, 'onload'):
                win.onload(None)
                self.sync()
            return
        if 'confirm' == type_ or 'prompt' == type_ or 'alert' == type_:
            doc = win.document
            cb = win._modalcallback
            if callable(cb):
                res = dic.get('value')
                doc._clean_diff()
                cb(res)
                self.sync()
            return
        if 'change' == type_:
            objdic = win.document._obj_dic
            if id_ in objdic:
                obj = objdic[id_]
                if 'value' in dic:
                    obj.value = dic['value']
                    # print('set by {} {}.value={}'.format(type_, id_, obj.value))
                if 'selectedIndex' in dic:
                    obj.selectedIndex = dic['selectedIndex']
                if 'checked' in dic:
                    obj.checked = dic['checked']
                    if obj.type == 'radio' and obj.checked:
                        group = self.window.document.getElementsByName(obj.name)
                        if group is not None:
                            for elm in group:
                                elm.checked = elm is obj
            if not self.ismulti:
                # boradcast if single instance
                self.broadcast(msg)
        # user handler
        if win is not None:
            doc = win.document
            if id_ in doc._handlers:
                fnc = doc._handlers[id_]
                if callable(fnc):
                    if ('keypress' == type_ or
                       'keyup' == type_ or 'keydown' == type_):
                        tid = dic['targetId']
                        target = doc.getElementById(tid)
                        target.value = dic['value']
                        # print('set by {} {}.value={}'.format(type_, tid, target.value))
                    doc._clean_diff()
                    fnc(dic)
                    self.sync()

    def sync(self):
        doc = self.window.document
        # del#if 0 < len(doc._diffdat):
        if doc._dirty_diff:
            # self.write_message({'diff': doc._diffdat})
            logger.debug('broadcast diff: {}'.format(len(doc._diffdat)))
            self.broadcast(json.dumps({'diff': doc._diffdat}))
            doc._clean_diff()

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
        # logger.debug("thread:{} self:{} open connection.".format(threading.current_thread().ident, self))
        self.window._remove_sock(self)
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


def start_app(wins, port=8888,
              js_path="/dominter.js", ws_path_pre='/_ws',
              html_pre='/index', html_post='.html', background_msec=2000,
              websocket_ping_interval=20, silent=False,
              ex_apps=None, template_path=None, static_path=None, **settings):
    """
    start tornado app for dominter
    :param wins: window list. if class is provided, act as multiple-instance.
     if instance is provided, act as single-instance.
    :param port: http/websocket port
    :param js_path: dominter.js path
    :param ws_path_pre: dominter websocket server path prefix (add index for each window)
    :param html_pre: html path prefix. default='/index'
    :param html_post: html path suffix. default='.html'
    :param background_msec: background worker act period for single-instance
     in milli seconds.
    :param websocket_ping_interval: websocket ping interval
    :param silent: suppress start message
    :param ex_apps: tornado extra apps
    :param template_path: tornado template_path
    :param static_path: tornado static_path
    :param settings: tornado settings
    :return: None
    """
    applst, winlst = make_app(wins, js_path=js_path, ws_path_pre=ws_path_pre,
                              html_pre=html_pre, html_post=html_post,
                              silent=silent)
    if ex_apps is not None:
        applst.extend(ex_apps)
    if template_path is not None:
        settings['template_path'] = template_path
    if static_path is not None:
        settings['static_path'] = static_path
    app = tornado.web.Application(applst,
                                  websocket_ping_interval=websocket_ping_interval,
                                  **settings)

    def periodic():
        # logger.debug("thread:{}".format(threading.current_thread().ident))
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
        if 4 >= tornado.version_info[0]:
            tornado.ioloop.PeriodicCallback(periodic, background_msec,
                                            io_loop=ioloop).start()
        else:
            tornado.ioloop.PeriodicCallback(periodic, background_msec).start()

    ioloop.add_callback(ThreadSafe.set_tornado_thread_id, ioloop)
    ioloop.start()
