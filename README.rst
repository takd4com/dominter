dominter
========
dominter is a simple GUI (Graphical User Interface) Python package for small asynchronous web application.

Features
--------
* JavaScript style API and other types of API that can be written shorter.
* Any tags and attributes can be used.
* Supports onclick(), onchange() and addEventListener().
* Supports multiple window.
* Supports both multiple-instance and single-instance.
* Supports Element.className and Element.style properties.
* Supports Window.addEventListener() for events such as 'hashchange'.
* Supports localStorage and sessionStorage.
* Supports fake Window.onload() to inform localStorage, sessionStorage and location has been set.
* Supports invoke() to operate from other threads.
* Depends only on `Tornado <http://www.tornadoweb.org>`_.

Installation
------------

::

    pip install dominter

Example
-------

* Hello world:

.. code-block:: python

    from dominter import Window, start_app

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

    from dominter import Window, start_app

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

* Three types of tag creation and childList attribute

.. code-block:: python

    from dominter import Window, start_app

    win = Window()
    document = win.document
    # js like
    p1 = document.createElement('p')
    p1.textContent = 'by createElement() '
    # html like : specify all by text excepts event handler
    p2 = document.tag('p _="by tag() "')  # use '_=' for textContent
    # individual tag method
    p3 = document.p('by p() method. ')
    document.body.childList = [p1, p2, p3]
    start_app(win)

Individual tag methods:
title, style, link, script,
br, p, span, div, button,
text, checkbox, radio, color,
date, month, time, week, number,
password, range, select, option,
textarea, table, tr, th, td,
fieldset, legend, img, a, label,
h1, h2, h3, h4, h5, h6, ol, li, ul, section, header, footer

* multiple window

.. code-block:: python

    from dominter import Window, start_app

    class MyWindow1(Window):
        def __init__(self):
            super(MyWindow1, self).__init__()
            document = self.document
            self.txt1 = document.text('windows1')
            self.btn1 = document.button('test1', onclick=self.on_btn1)
            document.body.appendChild(self.txt1)
            document.body.appendChild(self.btn1)

        def on_btn1(self, ev):
            self.txt1.value = 'changed1'

    class MyWindow2(Window):
        def __init__(self):
            super(MyWindow2, self).__init__()
            document = self.document
            self.txt1 = document.text('windows2')
            self.btn1 = document.button('test1', onclick=self.on_btn1)
            document.body.appendChild(self.txt1)
            document.body.appendChild(self.btn1)

        def on_btn1(self, ev):
            self.txt1.value = 'changed2'

    start_app([MyWindow1(),   # localhost:8888/index.html
               MyWindow2()])  # localhost:8888/index1.html

* multiple-instance and single-instance

.. code-block:: python

    from dominter import Window, start_app

    class MyWindow1(Window):
        def __init__(self):
            super(MyWindow1, self).__init__()
            document = self.document
            self.txt1 = document.text('windows1')
            self.btn1 = document.button('test1', onclick=self.on_btn1)
            document.body.appendChild(self.txt1)
            document.body.appendChild(self.btn1)

        def on_btn1(self, ev):
            self.txt1.value = 'changed1'

    class MyWindow2(Window):
        def __init__(self):
            super(MyWindow2, self).__init__()
            document = self.document
            self.txt1 = document.text('windows2')
            self.btn1 = document.button('test1', onclick=self.on_btn1)
            document.body.appendChild(self.txt1)
            document.body.appendChild(self.btn1)

        def on_btn1(self, ev):
            self.txt1.value = 'changed2'


    start_app([MyWindow1(),   # instance for single-instance. localhost:8888/index.html
               MyWindow2])    # class for multiple-instance. localhost:8888/index1.html

Status
------
Alpha


| Copyright (c) 2017-2018 Tamini Bean
| License: MIT
