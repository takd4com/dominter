# -*- coding: utf-8 -*-
# dominter
# class and style example
from dominter.dom import Window, start_app


class MyWindow(Window):
    def __init__(self):
        super(MyWindow, self).__init__()

        document = self.document
        button = document.button
        br = document.br

        self.document.head.childList = [
            document.title('class and style example'),
            document.style(
                '.cls1 { background-color: yellow; } ' +
                '.cls2 { color: green; } ' +
                '.cls3 { font-weight:bold; } '),
        ]
        self.btn_target = button('btn1', className="cls1", onclick=self.on_btn_target)
        self.disp = document.span('')
        self.btn_class_set = button('className="cls2 cls3"', onclick=self.on_btn_class_set)
        self.btn_class_toggle = button('classList.toggle("cls2")', onclick=self.on_btn_toggle)
        self.btn_class_remove = button('classList.remove("cls3")', onclick=self.on_btn_remove)
        self.btn_class_append = button('classList.append("cls3")', onclick=self.on_btn_append)
        self.btn_style_set = button('style="color:blue; background-color:orange;"', onclick=self.on_btn_style_set)
        self.btn_style_del = button('del style["color"]', onclick=self.on_btn_style_del)
        self.disp_class_style()

        document.body.childList = [
            self.btn_target, self.disp, br(),
            self.btn_class_set, self.btn_class_append, self.btn_class_remove, br(),
            self.btn_style_set, self.btn_style_del, br(),
        ]

    def on_btn_target(self, ev):
        tid = int(ev['targetId'])
        elm = self.document.getElementById(tid)
        elm.className = 'cls1'
        elm.style.clear()
        self.disp.textContent = 'class:{}, style:{}'.format(elm.className, elm.style.cssText)

    def disp_class_style(self):
        elm = self.btn_target
        self.disp.textContent = 'class:{}, style:{}'.format(elm.className, elm.style.cssText)

    def on_btn_class_set(self, ev):
        self.btn_target.className = 'cls2 cls3'
        self.disp_class_style()

    def on_btn_toggle(self, ev):
        self.btn_target.classList.toggle('cls2')
        self.disp_class_style()

    def on_btn_remove(self, ev):
        if 'cls3' in self.btn_target.classList:
            self.btn_target.classList.remove('cls3')
            self.disp_class_style()

    def on_btn_append(self, ev):
        if 'cls3' not in self.btn_target.classList:
            self.btn_target.classList.append('cls3')
            self.disp_class_style()

    def on_btn_style_set(self, ev):
        self.btn_target.style = "color:blue; background-color:orange;"
        self.disp_class_style()

    def on_btn_style_del(self, ev):
        self.btn_target.style.removeProperty('color')
        #if 'color' in self.btn_target.style:
        #    del self.btn_target.style['color']
        self.disp_class_style()


start_app(MyWindow())  # for http://localhost:8888/index.html