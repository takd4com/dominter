from dominter.dom import Window, start_app


class MyWindow1(Window):
    def __init__(self):
        super(MyWindow1, self).__init__()
        document = self.document
        self.txt1 = document.text('windows1')
        document.body.appendChild(self.txt1)
        self.btn1 = document.button('test1', onclick=self.on_btn1)
        document.body.appendChild(self.btn1)

    def on_btn1(self, ev):
        self.txt1.value = 'changed1'


class MyWindow2(Window):
    def __init__(self):
        super(MyWindow2, self).__init__()
        document = self.document
        self.txt1 = document.text('windows2')
        document.body.appendChild(self.txt1)
        self.btn1 = document.button('test1', onclick=self.on_btn1)
        document.body.appendChild(self.btn1)

    def on_btn1(self, ev):
        self.txt1.value = 'changed2'


start_app([MyWindow1(),  # instance for single-instance. localhost:8888/index.html
           MyWindow2])  # class for multiple-instance. localhost:8888/index1.html
