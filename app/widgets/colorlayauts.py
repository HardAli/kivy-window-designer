from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line, Rectangle

WIDTH = 1
GLASS_COLOR = [122, 200, 251]
GlASS_BOTTOM = 8


class ColoredLayout:
    my_color = {
        'r': 0,
        'g': 0,
        'b': 0,
        'a': 1
    }

    def set_color(self, r=0, g=0, b=0, a=1):
        if r > 1 or g > 1 or b > 1 or a > 1:
            r, g, b, a = self.color_convector(r, g, b, a)
        self.my_color['r'] = r
        self.my_color['g'] = g
        self.my_color['b'] = b
        self.my_color['a'] = a
        self.rect_color.rgba = self.get_color()

    def get_color(self):
        return self.my_color['r'], self.my_color['g'], self.my_color['b'], self.my_color['a']

    def color_convector(self, r, g, b, a):
        if r > 1:
            r = r / 255
        if g > 1:
            g = g / 255
        if b > 1:
            b = b / 255
        if a > 1:
            a = a / 255

        return r, g, b, a


class ColorBoxLayout(BoxLayout, ColoredLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.rect_color = Color(self.get_color())
            self.rect = Rectangle(size=self.size, pos=self.pos)

            self.border_color = Color(0, 0, 0, 1)
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=1.3)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.border.rectangle = (self.x, self.y, self.width, self.height)


class ColorAnchorLayout(AnchorLayout, ColoredLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect_color = Color(self.get_color())
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class ColorFloatLayout(FloatLayout, ColoredLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect_color = Color(self.get_color())
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
