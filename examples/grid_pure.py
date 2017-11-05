"""
dominter
Pure css grid example
"""
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
        self.gridlst1 = [
            [
                (GCOL4[1], document.button('25%', onclick=self.on_btn)),
                (GCOL4[1], document.button('25%', onclick=self.on_btn)),
                (GCOL4[2], document.button('50%', onclick=self.on_btn)),
            ], [
                (GCOL3[1], document.button('33%', onclick=self.on_btn)),
                (GCOL3[1], document.button('33%', onclick=self.on_btn)),
                (GCOL3[1], document.button('33%', onclick=self.on_btn)),
            ], [
                (GCOL5[2], document.button('40%', onclick=self.on_btn)),
                (GCOL5[1], document.button('20%', onclick=self.on_btn)),
                (GCOL5[1], document.button('20%', onclick=self.on_btn)),
                (GCOL5[1], document.button('20%', onclick=self.on_btn)),
            ], [
                ((GCOL12[6], GSM12[6], GMD12[6], GLG12[4], GXL12[3]),
                    document.button('6/12', onclick=self.on_btn)),
                ((GCOL12[3], GSM12[3], GMD12[3], GLG12[2], GXL12[2]),
                    document.button('3/12', onclick=self.on_btn)),
                ((GCOL12[2], GSM12[2], GSM12[2], GLG12[1], GXL12[1]),
                    document.button('2/12', onclick=self.on_btn)),
                ((GCOL12[1], GSM12[1], GSM12[1], GLG12[1], GXL12[1]),
                    document.button('1/12', onclick=self.on_btn)),
            ],
        ]
        divcont = document.div(className=GCONTAINER)
        for j, row in enumerate(self.gridlst1):
            divrow = document.div(className=GROW)
            for GCOL, elm in row:
                if isinstance(GCOL, tuple):
                    cls = ' '.join(GCOL)
                else:
                    cls = GCOL
                divcol = document.div(className=cls)
                divcol.appendChild(elm)
                divrow.appendChild(divcol)
            divcont.appendChild(divrow)
        self.document.body.appendChild(divcont)

    def on_btn(self, ev):
        tid = int(ev['targetId'])
        elm = self.document.getElementById(tid)
        elm.textContent = 'clicked'


if __name__ == "__main__":
    win = MyWindow()
    start_app({'window': win, 'path': '/'}, )
