# -*- coding: utf-8 -*-
# dominter
# Pure css grid example
from dominter.dom import Window, start_app
from dominter.pure1 import (CSS_URL, GCONTAINER, GROW, GCOL3, GCOL4, GCOL5,
                            GCOL12, GSM12, GMD12, GLG12, GXL12)


class MyWindow(Window):
    def __init__(self):
        super(MyWindow, self).__init__()
        document = self.document

        # header ------------------------------------------------------------
        self.document.head.appendChild(document.link(CSS_URL))

        # body --------------------------------------------------------------
        self.divcont1 = document.div(className=GCONTAINER, childList=[
            document.div(className=GROW, childList=[
                document.div(className=GCOL4[1], childList=[document.button('25%', onclick=self.on_btn)]),
                document.div(className=GCOL4[1], childList=[document.button('25%', onclick=self.on_btn)]),
                document.div(className=GCOL4[2], childList=[document.button('50%', onclick=self.on_btn)]),
            ]),
            document.div(className=GROW, childList=[
                document.div(className=GCOL3[1], childList=[document.button('33%', onclick=self.on_btn)]),
                document.div(className=GCOL3[1], childList=[document.button('33%', onclick=self.on_btn)]),
                document.div(className=GCOL3[1], childList=[document.button('33%', onclick=self.on_btn)]),
            ]),
            document.div(className=GROW, childList=[
                document.div(className=GCOL5[2], childList=[document.button('40%', onclick=self.on_btn)]),
                document.div(className=GCOL5[1], childList=[document.button('20%', onclick=self.on_btn)]),
                document.div(className=GCOL5[1], childList=[document.button('20%', onclick=self.on_btn)]),
                document.div(className=GCOL5[1], childList=[document.button('20%', onclick=self.on_btn)]),
            ]),
            document.div(className=GROW, childList=[
                document.div(className=' '.join((GCOL12[6], GSM12[6], GMD12[6], GLG12[4], GXL12[3])),
                             childList=[document.button('6/12', onclick=self.on_btn)]),
                document.div(className=' '.join((GCOL12[3], GSM12[3], GMD12[3], GLG12[2], GXL12[2])),
                             childList=[document.button('3/12', onclick=self.on_btn)]),
                document.div(className=' '.join((GCOL12[2], GSM12[2], GMD12[2], GLG12[1], GXL12[1])),
                             childList=[document.button('2/12', onclick=self.on_btn)]),
                document.div(className=' '.join((GCOL12[1], GSM12[1], GMD12[1], GLG12[1], GXL12[1])),
                             childList=[document.button('1/12', onclick=self.on_btn)]),
            ]),
        ])
        self.document.body.appendChild(self.divcont1)

    def on_btn(self, ev):
        tid = int(ev['targetId'])
        elm = self.document.getElementById(tid)
        elm.textContent = 'clicked'


if __name__ == "__main__":
    win = MyWindow()
    start_app({'window': win, 'path': '/'}, )
