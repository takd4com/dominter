# -*- coding: utf-8 -*-
# dominter canvas demo
#
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/arc
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/arcTo
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/bezierCurveTo
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/clearHitRegions
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/clearRect
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/clip
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/closePath
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/ellipse
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/fill
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/fillRect
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/fillText
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/lineTo
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/moveTo
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/quadraticCurveTo
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/rect
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/resetTransform
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/restore
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/rotate
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/save
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/scale
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/scrollPathIntoView
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/setLineDash
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/setTransform
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/stroke
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/strokeRect
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/strokeText
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/transform
# https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/translate
# These examples by Mozilla Contributors are licensed under CC-BY-SA 2.5(https://creativecommons.org/licenses/by-sa/2.5/).
#
import math
import argparse
from logging import (getLogger, StreamHandler, basicConfig,
                      DEBUG, INFO, WARN, ERROR)

from dominter import Window, start_app

logger = getLogger(__name__)


class MyWindow(Window):
    def __init__(self):
        super(MyWindow, self).__init__()
        doc = self.document

        # elements
        self.header = doc.header()
        self.canvas1 = doc.tag('canvas width="310" height="210" style="background-color:yellow;"')

        self.arc_btn = doc.button('arc')
        self.arcTo_btn = doc.button('arcTo')
        self.bezierCurveTo_btn = doc.button('bezierCurveTo')
        self.clearHitRegions_btn = doc.button('clearHitRegions')
        self.clearRect_btn = doc.button('clearRect')
        self.clip_btn = doc.button('clip')
        self.closePath_btn = doc.button('closePath')
        self.ellipse_btn = doc.button('ellipse')
        self.fill_btn =doc.button('fill')
        self.fillRect_btn = doc.button('fillRect')
        self.fillText_btn = doc.button('fillText')
        self.lineTo_btn = doc.button('lineTo')
        self.moveTo_btn = doc.button('moveTo')
        self.quadraticCurveTo_btn = doc.button('quadraticCurveTo')
        self.rect_btn = doc.button('rect')
        self.resetTransform_btn = doc.button('resetTransform')
        self.restore_btn = doc.button('restore')
        self.rotate_btn = doc.button('rotate')
        self.save_btn = doc.button('save')
        self.scale_btn = doc.button('scale')
        self.scrollPathIntoView_btn = doc.button('scrollPathIntoView')
        self.setLineDash_btn = doc.button('setLineDash')
        self.setTransform_btn = doc.button('setTransform')
        self.stroke_btn = doc.button('stroke')
        self.strokeRect_btn = doc.button('strokeRect')
        self.strokeText_btn = doc.button('strokeText')
        self.transform_btn = doc.button('transform')
        self.translate_btn = doc.button('translate')

        # view
        doc.body.childList.extend([
            self.canvas1,
            doc.br(),
            self.arc_btn,
            self.arcTo_btn,
            self.bezierCurveTo_btn,
            self.clearHitRegions_btn,
            self.clearRect_btn,
            self.clip_btn,
            self.closePath_btn,
            self.ellipse_btn,
            self.fill_btn,
            self.fillRect_btn,
            self.fillText_btn,
            self.lineTo_btn,
            self.moveTo_btn,
            self.quadraticCurveTo_btn,
            self.rect_btn,
            self.resetTransform_btn,
            self.restore_btn,
            self.rotate_btn,
            self.save_btn,
            self.scale_btn,
            self.scrollPathIntoView_btn,
            self.setLineDash_btn,
            self.setTransform_btn,
            self.stroke_btn,
            self.strokeRect_btn,
            self.strokeText_btn,
            self.transform_btn,
            self.translate_btn,
        ])

        # event listeners
        self.arc_btn.addEventListener('click', self.on_arc_btn)
        self.arcTo_btn.addEventListener('click', self.on_arcTo_btn)
        self.bezierCurveTo_btn.addEventListener('click', self.on_bezierCurveTo_btn)
        self.clearHitRegions_btn.addEventListener('click', self.on_clearHitRegions_btn)
        self.clearRect_btn.addEventListener('click', self.on_clearRect_btn)
        self.clip_btn.addEventListener('click', self.on_clip_btn)
        self.closePath_btn.addEventListener('click', self.on_closePath_btn)
        self.ellipse_btn.addEventListener('click', self.on_ellipse_btn)
        self.fill_btn.addEventListener('click', self.on_fill_btn)
        self.fillRect_btn.addEventListener('click', self.on_fillRect_btn)
        self.fillText_btn.addEventListener('click', self.on_fillText_btn)
        self.lineTo_btn.addEventListener('click', self.on_lineTo_btn)
        self.moveTo_btn.addEventListener('click', self.on_moveTo_btn)
        self.quadraticCurveTo_btn.addEventListener('click', self.on_quadraticCurveTo_btn)
        self.rect_btn.addEventListener('click', self.on_rect_btn)
        self.resetTransform_btn.addEventListener('click', self.on_resetTransform_btn)
        self.restore_btn.addEventListener('click', self.on_restore_btn)
        self.rotate_btn.addEventListener('click', self.on_rotate_btn)
        self.save_btn.addEventListener('click', self.on_save_btn)
        self.scale_btn.addEventListener('click', self.on_scale_btn)
        self.scrollPathIntoView_btn.addEventListener('click', self.on_scrollPathIntoView_btn)
        self.setLineDash_btn.addEventListener('click', self.on_setLineDash_btn)
        self.setTransform_btn.addEventListener('click', self.on_setTransform_btn)
        self.stroke_btn.addEventListener('click', self.on_stroke_btn)
        self.strokeRect_btn.addEventListener('click', self.on_strokeRect_btn)
        self.strokeText_btn.addEventListener('click', self.on_strokeText_btn)
        self.transform_btn.addEventListener('click', self.on_transform_btn)
        self.translate_btn.addEventListener('click', self.on_translate_btn)

        # work
        self.ctx = None

    def get_ctx(self):
        if self.ctx is None:
            self.ctx = self.canvas1.getContext('2d')
        return self.ctx

    def on_arc_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/arc
        ctx = self.get_ctx()
        ctx.beginPath()
        ctx.strokeStyle = 'green'
        ctx.arc(75, 75, 50, 0, 2 * math.pi)
        ctx.stroke()

    def on_arcTo_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/arcTo
        ctx = self.get_ctx()
        ctx.beginPath()
        ctx.moveTo(150, 20)
        ctx.arcTo(150, 100, 50, 20, 30)
        ctx.lineTo(50, 20)
        ctx.stroke()

        ctx.fillStyle = 'blue'
        # starting point
        ctx.fillRect(150, 20, 10, 10)

        ctx.fillStyle = 'red'
        # control point one
        ctx.fillRect(150, 100, 10, 10)
        # control point two
        ctx.fillRect(50, 20, 10, 10)

    def on_bezierCurveTo_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/bezierCurveTo
        ctx = self.get_ctx()
        ctx.beginPath()
        ctx.moveTo(50, 20)
        ctx.bezierCurveTo(230, 30, 150, 60, 50, 100)
        ctx.stroke()

        ctx.fillStyle = 'blue'
        # start point
        ctx.fillRect(50, 20, 10, 10)
        # end point
        ctx.fillRect(50, 100, 10, 10)

        ctx.fillStyle = 'red'
        # control point one
        ctx.fillRect(230, 30, 10, 10)
        # control point two
        ctx.fillRect(150, 60, 10, 10)

    def on_clearHitRegions_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/clearHitRegions
        ctx = self.get_ctx()
        # set some hit regions
        ctx.addHitRegion({'id': 'eyes'})
        ctx.addHitRegion({'id': 'nose'})
        ctx.addHitRegion({'id': 'mouth'})

        # remove them altogether from the canvas
        ctx.clearHitRegions()

    def on_clearRect_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/clearRect
        ctx = self.get_ctx()
        ctx.beginPath()
        ctx.moveTo(20, 20)
        ctx.lineTo(200, 20)
        ctx.lineTo(120, 120)
        ctx.closePath()    # draws last line of the triangle
        ctx.stroke()
        ctx.clearRect(10, 10, 100, 100)

    def on_clip_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/clip
        ctx = self.get_ctx()
        # Create clipping region
        ctx.beginPath()
        ctx.arc(100, 100, 75, 0, math.pi * 2, False)
        ctx.clip()

        ctx.fillRect(0, 0, 100, 100)

    def on_closePath_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/closePath
        ctx = self.get_ctx()
        ctx.beginPath()
        ctx.moveTo(20, 20)
        ctx.lineTo(200, 20)
        ctx.lineTo(120, 120)
        ctx.closePath()    # draws last line of the triangle
        ctx.stroke()

    def on_ellipse_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/ellipse
        ctx = self.get_ctx()
        ctx.setLineDash([])
        ctx.beginPath()
        ctx.ellipse(100, 100, 50, 75, 45 * math.pi / 180, 0, 2 * math.pi)
        ctx.stroke()
        ctx.setLineDash([5, 5])
        ctx.moveTo(0, 200)
        ctx.lineTo(200, 0)
        ctx.stroke()

    def on_fill_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/fill
        ctx = self.get_ctx()
        ctx.beginPath()
        ctx.strokeStyle = 'red'
        ctx.rect(10, 10, 100, 100)
        ctx.fill()

    def on_fillRect_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/fillRect
        ctx = self.get_ctx()
        ctx.fillStyle = "DarkSeaGreen"
        # ctx.fillRect(10, 10, 100, 100)
        ctx.fillRect(0, 0, 300, 200)
        ctx.fillStyle = "black"

    def on_fillText_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/fillText
        ctx = self.get_ctx()
        ctx.font = '48px serif'
        ctx.fillText('Hello world', 50, 100)

    def on_lineTo_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/lineTo
        ctx = self.get_ctx()
        ctx.beginPath()
        ctx.moveTo(50, 50)
        ctx.lineTo(100, 100)
        ctx.stroke()

    def on_moveTo_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/moveTo
        ctx = self.get_ctx()
        ctx.beginPath()
        ctx.moveTo(50, 50)
        ctx.lineTo(200, 50)
        ctx.stroke()

    def on_quadraticCurveTo_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/quadraticCurveTo
        ctx = self.get_ctx()
        ctx.beginPath()
        ctx.moveTo(50, 20)
        ctx.quadraticCurveTo(230, 30, 50, 100)
        ctx.stroke()

        ctx.fillStyle = 'blue'
        # start point
        ctx.fillRect(50, 20, 10, 10)
        # end point
        ctx.fillRect(50, 100, 10, 10)

        ctx.fillStyle = 'red'
        # control point
        ctx.fillRect(230, 30, 10, 10)

    def on_rect_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/rect
        ctx = self.get_ctx()
        ctx.rect(10, 10, 100, 100)
        ctx.fill()

    def on_resetTransform_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/resetTransform
        ctx = self.get_ctx()
        ctx.rotate(45 * math.pi / 180)
        ctx.fillRect(70, 0, 100, 30)
        ctx.resetTransform()

    def on_restore_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/restore
        ctx = self.get_ctx()
        ctx.save()    # save the default state
        ctx.fillStyle = "green"
        ctx.fillRect(10, 10, 100, 100)
        ctx.restore()    # restore to the default state
        ctx.fillRect(150, 75, 100, 100)

    def on_rotate_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/rotate
        ctx = self.get_ctx()
        ctx.rotate(45 * math.pi / 180)
        ctx.fillRect(70, 0, 100, 30)
        ctx.setTransform(1, 0, 0, 1, 0, 0)

    def on_save_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/save
        ctx = self.get_ctx()
        ctx.save()    # save the default state
        ctx.fillStyle = "green"
        ctx.fillRect(10, 10, 100, 100)
        ctx.restore()    # restore to the default state
        ctx.fillRect(150, 75, 100, 100)

    def on_scale_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/scale
        ctx = self.get_ctx()
        ctx.scale(10, 3)
        ctx.fillRect(10, 10, 10, 10)
        ctx.setTransform(1, 0, 0, 1, 0, 0)

    def on_scrollPathIntoView_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/scrollPathIntoView
        ctx = self.get_ctx()
        ctx.beginPath()
        ctx.rect(10, 10, 30, 30)
        ctx.scrollPathIntoView()

    def on_setLineDash_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/setLineDash
        ctx = self.get_ctx()
        ctx.beginPath()
        ctx.setLineDash([5, 15])
        ctx.moveTo(0, 50)
        ctx.lineTo(400, 50)
        ctx.stroke()
        ctx.beginPath()
        ctx.setLineDash([])
        ctx.moveTo(0, 150)
        ctx.lineTo(400, 150)
        ctx.stroke()

    def on_setTransform_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/setTransform
        ctx = self.get_ctx()
        ctx.setTransform(1, 1, 0, 1, 0, 0)
        ctx.fillRect(0, 0, 100, 100)
        ctx.setTransform(1, 0, 0, 1, 0, 0)

    def on_stroke_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/stroke
        ctx = self.get_ctx()
        ctx.rect(10, 10, 100, 100)
        ctx.stroke()

    def on_strokeRect_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/strokeRect
        ctx = self.get_ctx()
        ctx.strokeStyle = "green"
        ctx.strokeRect(10, 10, 100, 100)

    def on_strokeText_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/strokeText
        ctx = self.get_ctx()
        ctx.font = "48px serif"
        ctx.strokeText("Hello world", 50, 100)

    def on_transform_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/transform
        ctx = self.get_ctx()
        ctx.transform(1, 1, 0, 1, 0, 0)
        ctx.fillRect(0, 0, 100, 100)

    def on_translate_btn(self, evnt):
        # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/translate
        ctx = self.get_ctx()
        ctx.translate(50, 50)
        ctx.fillRect(0, 0, 100, 100)

        # reset current transformation matrix to the identity matrix
        ctx.setTransform(1, 0, 0, 1, 0, 0)


def get_arg_port():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', default=8888)
    args = ap.parse_args()
    port = args.port
    return port


def main():
    port = get_arg_port()
    start_app(MyWindow, port=port)


if __name__ == "__main__":
    basicConfig(format='%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s')
    logger = getLogger()  # root logger
    # logger.setLevel(DEBUG)
    logger.setLevel(INFO)
    main()
