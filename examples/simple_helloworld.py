# -*- coding: utf-8 -*-
# dominter example
from dominter.dom import Window, start_app


class MyWindow(Window):
    def __init__(self):
        super(MyWindow, self).__init__()
        document = self.document
        self.p1 = document.createElement('p')
        self.p1.textContent = "text content"
        self.btn1 = document.createElement('button')
        self.btn1.textContent = "button1"
        self.btn1.onclick = self.on_btn1
        document.body.appendChild(self.p1)
        document.body.appendChild(self.btn1)

    def on_btn1(self, ev):
        self.p1.textContent = 'Hello world!'


win = MyWindow()
start_app(win)
