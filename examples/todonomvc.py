# -*- coding: utf-8 -*-
"""
dominter todo NO MVC example
This is a deterioration copy of http://todomvc.com/examples.
"""

import os
from logging import (getLogger, StreamHandler, basicConfig,
                      DEBUG, INFO, WARN, ERROR)

from dominter.dom import Window, start_app

logger = getLogger(__name__)


class MyWindow(Window):
    def __init__(self):
        super(MyWindow, self).__init__()

        d = self.document
        self.root = d.section(child=(
            d.header(id_='header', child=(
                d.h1('todos'),
                d.text(id_='new_todo', placeholder='What needs to be done?'),
            )),
            #d.section(id_='main', style='display: none;', child=(
            d.section(id_='main', child=(
                d.checkbox(id_='toggle_all'),
                d.label('Mark all as complete', for_='toggle_all'),
                d.ul(id_='todo_list'),
            )),
            #d.footer(id_='footer', style='display: none;', child=(
            d.footer(id_='footer', child=(
                d.span('0', id_='count'),
                d.span(' items left '),
                d.label('All'),
                d.radio(value='All', name='sel', id_='sel_all'),
                d.label('Active'),
                d.radio(value='Active', name='sel', id_='sel_active'),
                d.label('Completed'),
                d.radio(value='Completed', name='sel', id_='sel_completed'),
                d.button('Clear completed', id_='clear_completed'),
            )),
        ))
        self.header = d.getElementById('header')
        self.new_todo = d.getElementById('new_todo')
        self.main = d.getElementById('main')
        self.toggle_all = d.getElementById('toggle_all')
        self.todo_list = d.getElementById('todo_list')
        self.footer = d.getElementById('footer')
        self.count = d.getElementById('count')
        self.sel_all = d.getElementById('sel_all')
        self.sel_active = d.getElementById('sel_active')
        self.sel_completed = d.getElementById('sel_completed')
        self.clear_completed = d.getElementById('clear_completed')
        self.document.body.appendChild(self.root)

        # dmy = d.createElement('dmy')
        self.new_todo.addEventListener('change', self.on_new_todo)
        self.toggle_all.addEventListener('change', self.on_toggle_all)
        self.sel_all.addEventListener('change', self.on_sel_change)
        self.sel_active.addEventListener('change', self.on_sel_change)
        self.sel_completed.addEventListener('change', self.on_sel_change)
        self.clear_completed.addEventListener('click', self.on_clear_completed)

    def add_todo(self, txt):
        info = {'checked': False}
        d = self.document
        elm = d.li(child=(
            d.div(className='view', child=(
                d.checkbox(onchange=self.on_todo_check),
                d.label(txt),
                d.button('x', className='destroy', onclick=self.on_todo_destroy),
            )),
        ))
        self.todo_list.appendChild(elm)
        self.set_left()
        self.new_todo.value = ''

    def get_li_by_chk(self, chk):
        div =chk.parent
        li = div.parent
        return li

    def get_label_by_chk(self, chk):
        div =chk.parent
        label = div.child[1]
        return label

    def get_chk_by_li(self, li):
        return li.child[0].child[0]

    def get_chk_list(self):
        return [li.child[0].child[0] for li in self.todo_list.child]

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

    def left_count(self):
        cnt = 0
        for itm in self.get_chk_list():
            cnt += 0 if itm.checked else 1
        return cnt

    def set_left(self):
        self.count.textContent = self.left_count()

    def on_sel_change(self, ev):
        elm = self.document.getElementById(ev['targetId'])
        if elm is None:
            return
        for li in self.todo_list.child:
            chk = self.get_chk_by_li(li)
            done = chk.checked
            display = (
                (elm.value == 'All') or
                ((elm.value == 'Completed') and done) or
                ((elm.value == 'Active') and (not done)))
            li.style['display'] = 'list-item' if display else 'None'

    def on_clear_completed(self, ev):
        lst = [(self.get_chk_by_li(li), li) for li in self.todo_list.child]
        for chk, li in lst:
            if chk.checked:
                # self.todo_list.removeChild(li)
                self.todo_list.child.remove(li)


def main():
    win = MyWindow()
    start_app(win)


if __name__ == "__main__":
    basicConfig(format='%(asctime)-15s %(module)s %(funcName)s %(levelname)s %(message)s')
    logger = getLogger()  # root logger
    logger.setLevel(DEBUG)
    main()
