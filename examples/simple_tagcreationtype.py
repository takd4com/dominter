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
