# -*- coding: utf-8 -*-
"""
dominter todo no MVC example
This example is python3 only
"""

import os
from logging import (getLogger, StreamHandler, basicConfig,
                      DEBUG, INFO, WARN, ERROR)

from dominter.dom import Window, start_app

logger = getLogger(__name__)


class MyWindow(Window):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.todos = []

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
            d.footer(id_='footer', style='display: none;', child=(
                d.span('0', id_='count'),
                d.span(' items left'),
                d.ul(child=(
                    d.li(child=(
                        d.a(href='#/', textContent='All', id_='sel_all', className='selected'),
                   )),
                    d.li(child=(
                        d.a(href='#/active', textContent='Active', id_='sel_active'),
                   )),
                    d.li(child=(
                        d.a(href='#/completed', textContent='Completed', id_='sel_completed'),
                   )),
                )),
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
        self.document.body.appendChild(self.root)

        dmy = d.createElement('dmy')

        self.new_todo.addEventListener('change', self.on_new_todo)

    def on_new_todo(self, ev):
        txt = self.new_todo.value
        self.add_todo(txt)

    def on_individual_destroy(self, ev):
        chk = self.document.getElementById(ev['targetId'])
        div =chk.parent
        li = div.parent
        self.todo_list.removeChild(li)

    def add_todo(self, txt):
        info = {'checked': False}
        d = self.document
        elm = d.li(txt, child=(
            d.div(className='view', child=(
                d.checkbox(),
                d.label(txt),
                d.button(className='destroy', onclick=self.on_individual_destroy),
            )),
        ))
        self.todo_list.appendChild(elm)

def main():
    win = MyWindow()
    start_app(win)


if __name__ == "__main__":
    basicConfig(format='%(asctime)-15s %(module)s %(funcName)s %(levelname)s %(message)s')
    logger = getLogger()  # root logger
    logger.setLevel(DEBUG)
    main()
