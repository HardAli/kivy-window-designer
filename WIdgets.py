from kivy.graphics import Color, Rectangle


class WidgetWindow(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            x, y, h, w = self.get_parametrs()
            Color(0, 0, 0, 1)
            self.rect_wall = Rectangle(size=self.size, pos=self.pos)
            Color(0.8, 0.8, 0.8, 1)
            self.rect_fill = Rectangle(size=(h, w), pos=(x, y))

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        x, y, h, w = self.get_parametrs()
        self.rect_fill.size = (h, w)
        self.rect_fill.pos = (x, y)
        self.rect_wall.size = self.size
        self.rect_wall.pos = self.pos

    def get_parametrs(self, tick_wall = 3):
        x, y = self.pos
        h, w = self.size
        x, y, h, w = x + tick_wall, y + tick_wall, h - tick_wall * 2, w - tick_wall * 2
        return [x, y, h, w]