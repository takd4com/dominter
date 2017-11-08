dominter
========
dominter is a simple GUI (Graphical User Interface) Python package for small asynchronous web application.

Features
--------
* JavaScript style API and other types of API that can be written shorter.
* Any tag and attributes can be used.
* Supports 'click', 'change' and any events.
* Supports multiple window.
* Supports both multiple-instance and single-instance.
* Supports Element.class and Element.style properties.

Example
-------

* Hello world:

.. code-block:: python

    from dominter.dom import Window, start_app

    class MyWindow(Window):
        def __init__(self):
            super().__init__()
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

* Without class:

.. code-block:: python

    from dominter.dom import Window, start_app

    win = Window()
    document = win.document
    tag_p1 = document.createElement('p')
    tag_p1.textContent = "text content"

    def on_btn1(ev):
        tag_p1.textContent = 'Hello world!'

    tag_btn1 = document.createElement('button')
    tag_btn1.textContent = "button1"
    tag_btn1.onclick = on_btn1
    document.body.appendChild(tag_p1)
    document.body.appendChild(tag_btn1)
    start_app(win)

* 3 types of tag creation

.. code-block:: python

    from dominter.dom import Window, start_app

    win = Window()
    document = win.document
    # js like
    p0 = document.createElement('p')
    p0.textContent = 'by createElement() '
    # html like : specify all by text excepts event handler
    p1 = document.tag('p _="by tag() "')  # use '_=' for textContent
    # individual tag method
    p2 = document.p('by p() method. ')
    document.body.appendChild(p0)
    document.body.appendChild(p1)
    document.body.appendChild(p2)
    start_app(win)

Individual tag methods:
title, style, link, script,
br, p, span, div, button,
text, checkbox, radio, color,
date, month, time, week, number,
password, range, select, option,
textarea, table, tr, th, td,
fieldset, legend, img, a


* multiple window

.. code-block:: python

    dominter.dom import Window, start_app

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

    start_app([MyWindow1(),   # localhost:8888/index.html
               MyWindow2()])  # localhost:8888/index1.html

* multiple-instance and single-instance

.. code-block:: python

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


    start_app([MyWindow1(),   # instance for single-instance. localhost:8888/index.html
               MyWindow2])    # class for multiple-instance. localhost:8888/index1.html

Status
------
Pre-alpha


| Copyright (c) 2017 Tamini Bean
| License: MIT
