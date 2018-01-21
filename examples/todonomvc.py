# -*- coding: utf-8 -*-
# dominter todo NO MVC example
# This is a poor copy of http://todomvc.com/examples.
import os
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

        # view
        self.document.body.childList = [
            doc.section(childList=[
                self.header,
                self.main,
                self.footer,
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

    def add_todo(self, txt):
        doc = self.document
        itm = doc.label(txt)
        itm.addEventListener('dblclick', self.on_edit_item)
        elm = doc.li('', childList=(
            doc.div(className='view', childList=(
                doc.checkbox(onchange=self.on_todo_check),
                itm,
                doc.button('x', className='destroy', onclick=self.on_todo_destroy),
            )),
        ))
        self.todo_list.appendChild(elm)
        self.set_left()
        self.new_todo.value = ''

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
            parent.textContent = target.value
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

    def on_todo_check(self, ev):
        chk = self.document.getElementById(ev['targetId'])
        checked = chk.checked
        self.change_check(chk, checked)

    def change_check(self, chk, checked):
        label = self.get_label_by_chk(chk)
        if checked:
            label.style['text-decoration'] = 'line-through'
        else:
            label.style.pop('text-decoration')
        self.set_left()

    def on_new_todo(self, ev):
        txt = self.new_todo.value
        self.add_todo(txt)

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

    def on_sel_change(self, ev):
        elm = self.document.getElementById(ev['targetId'])
        if elm is None:
            return
        for li in self.todo_list.childList:
            chk = self.get_chk_by_li(li)
            done = chk.checked
            display = (
                (elm.value == 'All') or
                ((elm.value == 'Completed') and done) or
                ((elm.value == 'Active') and (not done)))
            li.style['display'] = 'list-item' if display else 'None'

    def on_clear_completed(self, ev):
        lst = [(self.get_chk_by_li(li), li) for li in self.todo_list.childList]
        for chk, li in lst:
            if chk.checked:
                # self.todo_list.removeChild(li)
                self.todo_list.childList.remove(li)


def main():
    win = MyWindow()
    start_app(win)


if __name__ == "__main__":
    basicConfig(format='%(asctime)-15s %(module)s %(funcName)s %(levelname)s %(message)s')
    logger = getLogger()  # root logger
    logger.setLevel(DEBUG)
    main()
