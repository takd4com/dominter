# -*- coding: utf-8 -*-
# dominter todo NO MVC example
# This is a poor copy of http://todomvc.com/examples.
import argparse
from logging import (getLogger, StreamHandler, basicConfig,
                      DEBUG, INFO, WARN, ERROR)

from dominter.dom import Window, start_app

logger = getLogger(__name__)


class MyWindow(Window):
    def __init__(self):
        super(MyWindow, self).__init__()
        doc = self.document

        # elements
        self.header = doc.header()
        self.new_todo = doc.text(placeholder='What needs to be done?')
        self.main = doc.section()
        self.toggle_all = doc.checkbox()
        self.todo_list = doc.ul()
        self.footer = doc.footer()
        self.count = doc.span('0')
        self.sel_all = doc.radio(value='All', name='sel', checked=True)
        self.sel_active = doc.radio(value='Active', name='sel')
        self.sel_completed = doc.radio(value='Completed', name='sel')
        self.clear_completed = doc.button('Clear completed')
        self.editbox = None
        self.ws_status = doc.p('init', id_='_ws_status')

        # view
        self.document.head.childList = [
            doc.style('label.editing { color: red; } ')
        ]
        self.document.body.childList = [
            doc.section(childList=[
                self.header,
                self.main,
                self.footer,
                self.ws_status,
            ]),
        ]
        self.header.childList = [
            doc.h1('todos'),
            self.new_todo,
        ]
        self.main.childList = [
            self.toggle_all,
            doc.label('Mark all as complete', for_='toggle_all'),
            self.todo_list,
        ]
        self.footer.childList = [
            self.count,
            doc.span(' items left '),
            doc.label('All'),
            self.sel_all,
            doc.label('Active'),
            self.sel_active,
            doc.label('Completed'),
            self.sel_completed,
            self.clear_completed,
        ]

        # handlers
        self.new_todo.addEventListener('change', self.on_new_todo)
        self.toggle_all.addEventListener('change', self.on_toggle_all)
        self.sel_all.addEventListener('change', self.on_sel_change)
        self.sel_active.addEventListener('change', self.on_sel_change)
        self.sel_completed.addEventListener('change', self.on_sel_change)
        self.clear_completed.addEventListener('click', self.on_clear_completed)

    STORAGE_KEY = 'todos-dominter'
    TODOS_KEY = 'todos'

    def store_init(self):
        dic = self.localStorage.get(self.STORAGE_KEY)
        if dic is None:
            self.localStorage[self.STORAGE_KEY] = {self.TODOS_KEY: []}
        else:
            lst = dic[self.TODOS_KEY]
            for ent in lst:
                txt = ent.get('title')
                checked = ent.get('completed')
                sid = self.add_todo(txt, checked=checked, store=False)
                ent['id'] = sid
            self.localStorage[self.STORAGE_KEY] = dic

    def store_add(self, sid, txt, checked=False):
        dic = self.localStorage[self.STORAGE_KEY]
        dic[self.TODOS_KEY].append({'title': txt, 'completed': False, 'id': sid})
        self.localStorage[self.STORAGE_KEY] = dic

    def store_del(self, sid):
        dic = self.localStorage[self.STORAGE_KEY]
        lst = dic[self.TODOS_KEY]
        for j, x in enumerate(lst):
            if x['id'] == sid:
                del lst[j]
        self.localStorage[self.STORAGE_KEY] = dic

    def store_mod(self, sid, txt=None, checked=None):
        dic = self.localStorage[self.STORAGE_KEY]
        for x in dic[self.TODOS_KEY]:
            if x['id'] == sid:
                if txt is not None:
                    x['title'] = txt
                if checked is not None:
                    x['completed'] = checked
                self.localStorage[self.STORAGE_KEY] = dic
                break

    def onload(self, ev):
        self.todo_list.childList.clear()
        self.store_init()

    def add_todo(self, txt, checked=False, store=False):
        if 0 == len(txt):
            return
        doc = self.document
        itm = doc.label(txt)
        itm.addEventListener('dblclick', self.on_edit_item)
        self.set_todo_label(itm, checked=checked)
        elm = doc.li('', childList=[
            doc.div(className='view', childList=[
                doc.checkbox(onchange=self.on_todo_check, checked=checked),
                itm,
                doc.button('x', className='destroy', onclick=self.on_todo_destroy),
            ]),
        ])
        selval = self.get_sel_value()
        self.set_disp_style(elm, checked, selval)
        self.todo_list.appendChild(elm)
        self.set_left()
        self.new_todo.value = ''
        sid = id(elm)
        if store:
            self.store_add(sid=sid, txt=txt, checked=False)
        return sid

    def get_store_id_by_label(self, label):
        tgt = label.parent.parent
        res = id(tgt)
        return res

    def get_store_id_by_done(self, check):
        return self.get_store_id_by_label(check)

    def get_store_id_by_destroy(self, check):
        return self.get_store_id_by_label(check)

    def on_edit_item(self, ev):
        if 'targetId' not in ev:
            return
        doc = self.document
        target = doc.getElementById(ev['targetId'])
        if target is None:
            return
        title = target.textContent
        target.classList.append('editing')
        self.editbox = doc.text(title)
        self.editbox.className = 'edit'
        self.editbox.addEventListener('blur', self.on_edit_blur)
        self.editbox.addEventListener('change', self.on_edit_change)
        self.editbox.addEventListener('keyup', self.on_edit_keyup)
        target.appendChild(self.editbox)
        self.editbox.focus()

    def on_edit_blur(self, ev):
        if 'targetId' not in ev:
            return
        doc = self.document
        target = doc.getElementById(ev['targetId'])
        self.edit_end(target, True)

    def on_edit_change(self, ev):
        if 'targetId' not in ev:
            return
        #done
        doc = self.document
        target = doc.getElementById(ev['targetId'])
        self.edit_end(target, True)

    def on_edit_keyup(self, ev):
        if 'keyCode' not in ev:
            return
        if 'targetId' not in ev:
            return
        keycode = ev['keyCode']
        doc = self.document
        if keycode == 27:
            # escape
            target = doc.getElementById(ev['targetId'])
            self.edit_end(target, False)
        # blur() test
        # elif keycode == 66:  # 'b'
        #    target = doc.getElementById(ev['targetId'])
        #    target.blur()

    def edit_end(self, target, done=True):
        parent = target.parent
        if parent is None:
            return
        if done:
            txt = target.value
            parent.textContent = txt
            sid = self.get_store_id_by_label(parent)
            self.store_mod(sid=sid, txt=txt)
        parent.classList.remove('editing')
        parent.removeChild(target)

    def get_li_by_chk(self, chk):
        div =chk.parent
        li = div.parent
        return li

    def get_label_by_chk(self, chk):
        div =chk.parent
        label = div.childList[1]
        return label

    def get_chk_by_li(self, li):
        return li.childList[0].childList[0]

    def get_chk_list(self):
        return [li.childList[0].childList[0] for li in self.todo_list.childList]

    def on_todo_destroy(self, ev):
        chk = self.document.getElementById(ev['targetId'])
        li = self.get_li_by_chk(chk)
        self.todo_list.removeChild(li)
        self.set_left()
        sid = self.get_store_id_by_destroy(chk)
        self.store_del(sid)

    def on_todo_check(self, ev):
        chk = self.document.getElementById(ev['targetId'])
        checked = chk.checked
        self.change_check(chk, checked)

    def set_todo_label(self, label, checked):
        key = 'text-decoration'
        value = 'line-through'
        if checked:
            label.style[key] = value
        elif key in label.style:
            label.style.pop(key)

    def change_check(self, chk, checked):
        selval = self.get_sel_value()
        li = self.get_li_by_chk(chk)
        self.set_disp_style(li, checked, selval)
        label = self.get_label_by_chk(chk)
        self.set_todo_label(label, checked)
        self.set_left()
        sid = self.get_store_id_by_done(chk)
        self.store_mod(sid=sid, checked=checked)

    def on_new_todo(self, ev):
        txt = self.new_todo.value
        self.add_todo(txt, checked=False, store=True)

    def on_toggle_all(self, ev):
        chk = self.document.getElementById(ev['targetId'])
        val = chk.checked
        for itm in self.get_chk_list():
            itm.checked = val
            self.change_check(itm, val)

    def set_left(self):
        all, cnt = 0, 0
        for itm in self.get_chk_list():
            all += 1
            cnt += 0 if itm.checked else 1
        self.count.textContent = cnt
        self.toggle_all.checked = 0 < all and 0 == cnt

    def get_sel_value(self):
        lst = self.document.getElementsByName('sel')
        for itm in lst:
            if itm.checked:
                res = itm.value
                return res
        return None

    def set_disp_style(self, li, done, selval):
        display = (
                (selval == 'All') or
                ((selval == 'Completed') and done) or
                ((selval == 'Active') and (not done)))
        li.style['display'] = 'list-item' if display else 'None'

    def on_sel_change(self, ev):
        elm = self.document.getElementById(ev['targetId'])
        if elm is None:
            return
        for li in self.todo_list.childList:
            chk = self.get_chk_by_li(li)
            self.set_disp_style(li, chk.checked, elm.value)

    def on_clear_completed(self, ev):
        lst = [(self.get_chk_by_li(li), li) for li in self.todo_list.childList]
        for chk, li in lst:
            if chk.checked:
                # self.todo_list.removeChild(li)
                self.todo_list.childList.remove(li)
                sid = id(li)
                self.store_del(sid)


def get_arg_port():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', default=8888)
    args = ap.parse_args()
    port = args.port
    return port


def main():
    port = get_arg_port()
    start_app(MyWindow, port=port)


if __name__ == "__main__":
    basicConfig(format='%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s')
    logger = getLogger()  # root logger
    # logger.setLevel(DEBUG)
    logger.setLevel(INFO)
    main()
