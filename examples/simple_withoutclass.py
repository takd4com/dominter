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
