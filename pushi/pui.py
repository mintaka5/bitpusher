from math import pi, cos, sin

from pyglet.app import run
from pyglet.gl import Config, glBegin, GL_LINES, glEnd, glVertex3f
from pyglet.window import key, mouse, Window


class Pui(Window):
    def __init__(self):
        print("sin(1): %lf" % sin(1))
        print("cos(1): %lf" % cos(1))
        print("pi: %lf" % pi)

        config = Config(sample_buffers=1, samples=8)
        super().__init__(width=640, height=480, config=config)

        run()

    def on_draw(self):

        glBegin(GL_LINES)
        glVertex3f(100.0, 100.0, 0.25)
        glVertex3f(200.0, 300.0, -0.75)
        glEnd()

    def on_resize(self, width, height):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.A:
            print("going left")
        elif symbol == key.W:
            print("going forward")
        elif symbol == key.S:
            print("going backward")
        elif symbol == key.D:
            print("going right")

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            print("pew pew pew: %d, %d" % (x, y))
