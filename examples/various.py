# -*- coding: utf-8 -*-
import os
from logging import (getLogger, StreamHandler, basicConfig,
                      DEBUG, INFO, WARN, ERROR)

from dominter.dom import Window, start_app

logger = getLogger(__name__)


class MyWindow(Window):
    def __init__(self):
        super(MyWindow, self).__init__()

        # test for dynamic button and checkbox
        self.dyn_btn = None
        self.dyn_chk = None

        # shortcuts
        document = self.document
        add_head = self.document.head.appendChild
        add_body = self.document.body.appendChild

        def br():
            br = self.document.br()
            add_body(br)

        # header ------------------------------------------------------------
        self.title = document.title('THE TITLE')
        add_head(self.title)
        self.style = document.style(
            'span { color:red; font-weight:bold; }\n' +
            'textarea { resize: both; }\n' +
            '.cls1 { color:green; font-weight:bold; }\n' +
            'table, th, td { border: 1px solid black; }'
        )
        add_head(self.style)

        # body --------------------------------------------------------------
        self.img1 = document.img('static/icooon-mono-soy1.png', alt='alt1',
                                 width='50', height='50',
                                 onclick=self.on_img1_click)
        add_body(self.img1)
        br()
        self.a1 = document.a(href='http://www.tornadoweb.org',
                             textContent='tornado')
        add_body(self.a1)
        self.p1 = document.p('this is p tag')
        add_body(self.p1)
        self.fieldset1 = document.fieldset()
        self.legend1 = document.legend('this is legend')
        self.spaninfs1 = document.span('this is span in fieldset')
        self.fieldset1.appendChild(self.legend1)
        self.fieldset1.appendChild(self.spaninfs1)
        add_body(self.fieldset1)
        self.span1 = document.span('[this is span tag]')
        add_body(self.span1)
        self.txt1 = document.text()
        add_body(self.txt1)
        br()
        self.btn1 = document.button('test1', onclick=self.on_btn1,
                                    style="background-color: yellow;",
                                    className="cls1")
        add_body(self.btn1)
        br()
        self.spn1 = document.span('red background by individual style')
        add_body(self.spn1)
        br()
        self.txt2 = document.text()
        add_body(self.txt2)
        br()
        self.btn2 = document.button('test2', onclick=self.on_btn2,
                                    className="cls1")
        add_body(self.btn2)
        br()
        self.clear_btn = document.button('clear',
                                         onclick=self.on_clear_btn)
        add_body(self.clear_btn)
        br()
        self.sel1 = document.select(selectedIndex=0, value='red',
                                    onchange=self.on_sel1)
        opts1 = (
            document.option('red', textContent='option red'),
            document.option('green', textContent='option green'),
            document.option('blue', textContent='option blue'),
        )
        list([self.sel1.appendChild(elm) for elm in opts1])
        add_body(self.sel1)
        br()
        self.txt3 = document.text(style="width:300px;")
        add_body(self.txt3)
        br()
        self.btn3 = document.button('test3', onclick=self.on_btn3,
                                    className="cls1")
        add_body(self.btn3)
        br()
        self.texta1 = document.textarea('this is textarea', cols='40', rows='4')
        add_body(self.texta1)
        self.btn4 = document.button('test4', onclick=self.on_btn4,
                                    className="cls1")
        add_body(self.btn4)
        br()
        self.chk_tst1 = document.checkbox()
        add_body(self.chk_tst1)
        self.btn5 = document.button('test5', onclick=self.on_btn5,
                                    className="cls1")
        add_body(self.btn5)
        br()
        self.radio11 = document.radio(value='radio11', name='radio1', checked=False)
        add_body(self.radio11)
        self.radio12 = document.radio(value='radio12', name='radio1', checked=True)
        add_body(self.radio12)
        self.radio13 = document.radio(value='radio13', name='radio1', checked=False)
        add_body(self.radio13)
        self.btn6 = document.button('test6', onclick=self.on_btn6,
                                    className="cls1")
        add_body(self.btn6)
        br()
        self.rmv_btn = document.button('removeChild', onclick=self.on_rmv_btn,
                                    className="cls1")
        add_body(self.rmv_btn)
        self.add_btn = document.button('appendChild', onclick=self.on_add_btn,
                                    className="cls1")
        add_body(self.add_btn)
        br()
        self.table1 = document.table()
        self.tbl1d = [
            [
                document.th('header1'), document.th('header2'),
                document.th('header3'), document.th('header4'),
            ], [
                document.td('data11'), document.td('data12'),
                document.td('data13'), document.td('data14'),
            ], [
                document.td('data21'), document.td('data22'),
                document.td('data23'), document.td('data24'),
            ], [
                document.td('data31'), document.td('data32'),
                document.td('data33'), document.td('data34'),
            ],
        ]
        for j, row in enumerate(self.tbl1d):
            tr = document.tr()
            self.table1.appendChild(tr)
            for thd in row:
                tr.appendChild(thd)
        add_body(self.table1)

        self.dmycnt = 0
        self.tbl_btn = document.button('change table', onclick=self.on_tbl_btn,
                                    className="cls1")
        add_body(self.tbl_btn)
        br()
        self.dtl1 = document.datetime_local('2017-10-14T12:34:56')
        add_body(self.dtl1)
        self.month1 = document.month('2017-10')
        add_body(self.month1)
        br()
        self.week1 = document.week('2017-W12')
        add_body(self.week1)
        self.date1 = document.date('2017-10-14')
        add_body(self.date1)
        self.time1 = document.time('01:23:45')
        add_body(self.time1)
        br()
        self.color1 = document.color('#80ff80')
        add_body(self.color1)
        self.num1 = document.number(12345, min=-1000, max=50000)
        add_body(self.num1)
        self.range1 = document.range(-10, min=-10, max=250, step=2)
        add_body(self.range1)
        self.pw1 = document.password('12345678')
        add_body(self.pw1)
        self.inputs_btn = document.button('inputs', onclick=self.on_inputs_btn)
        add_body(self.inputs_btn)
        br()
        document.clean_diff()

    def on_btn1(self, ev):
        self.txt1.value = 'modified'
        self.btn1.textContent = 'the button'
        self.btn1.setAttribute("style", "background-color: red;")
        self.p1.textContent = 'p tag'
        self.span1.textContent = 'span tag'
        self.spaninfs1.textContent = 'changed span in fieldset'

    def on_btn2(self, ev):
        self.txt2.value = 'copy:' + self.txt1.value
        self.btn1.setAttribute("style", "background-color: grey;")
        self.legend1.textContent = 'changed legend'
        if self.dyn_btn is not None:
            self.dyn_btn.textContent = 'dyn_btn changed'

    def on_clear_btn(self, ev):
        self.txt1.value = ''
        self.txt2.value = ''
        self.btn1.removeAttribute("style")
        self.btn2.removeAttribute("style")

    def on_btn3(self, ev):
        lst = self.document.getElementsByClassName('cls1')
        self.txt3.value = len(lst)

    def on_sel1(self, ev):
        self.txt3.value = str(self.sel1.selectedIndex)

    def on_btn4(self, ev):
        self.txt3.value = self.texta1.value

    def on_btn5(self, ev):
        self.txt3.value = self.chk_tst1.checked

    def on_btn6(self, ev):
        self.txt3.value = self.radio11.checked

    def on_rmv_btn(self, ev):
        self.document.body.removeChild(self.sel1)

    def on_add_btn(self, ev):
        self.dyn_chk = self.document.checkbox(checked=True)
        self.document.body.appendChild(self.dyn_chk)

        def dyn_btn_fnc(ev):
            self.txt3.value = 'yes dynamic' + str(self.dyn_chk.checked)
        self.dyn_btn = self.document.button('dynamic', onclick=dyn_btn_fnc,
                                            className="cls1")
        self.document.body.appendChild(self.dyn_btn)
        br = self.document.br()
        self.document.body.appendChild(br)

    def on_tbl_btn(self, ev):
        self.dmycnt += 1
        if len(self.table1.elements) > 3:
            self.tbl1d[0][0].textContent = 'changed!00_' + str(self.dmycnt)
            self.tbl1d[1][1].textContent = 'changed!11_' + str(self.dmycnt)
            self.tbl1d[2][2].textContent = 'changed!22_' + str(self.dmycnt)
            self.tbl1d[3][3].textContent = 'changed!33_' + str(self.dmycnt)
            self.table1.removeChild(self.table1.elements[2])
            del(self.tbl1d[2])

    def on_inputs_btn(self, ev):
        self.texta1.value = (
            (
             ' datetime-local: {}\n' +
             ' month: {}\n' +
             ' week: {}\n' +
             ' date: {}\n' +
             ' time: {}\n' +
             ' color: {}\n' +
             ' number: {}\n' +
             ' range: {}\n' +
             ' password: {}\n' +
             ''
             )
            .format(
                self.dtl1.value,
                self.month1.value,
                self.week1.value,
                self.date1.value,
                self.time1.value,
                self.color1.value,
                self.num1.value,
                self.range1.value,
                self.pw1.value,
            ))

    def on_img1_click(self, ev):
        self.texta1.value = ('client: {}, {}\nlayer: {}, {}\n' +
                             'offset: {}, {}\n' +
                             'page: {}, {}\nscreen: {}, {}').format(
            ev['clientX'], ev['clientY'],
            ev['layerX'], ev['layerY'],
            ev['offsetX'], ev['offsetY'],
            ev['pageX'], ev['pageY'],
            ev['screenX'], ev['screenY'],
        )

def main():
    win1 = MyWindow()
    start_app({'window': win1, 'path': '/'},
               template_path=os.path.dirname(__file__),
               static_path=os.path.join(os.path.dirname(__file__), 'static'),
              )


if __name__ == "__main__":
    basicConfig(format='%(asctime)-15s %(module)s %(funcName)s %(levelname)s %(message)s')
    logger = getLogger()  # root logger
    logger.setLevel(DEBUG)
    logger.info('start')
    main()
