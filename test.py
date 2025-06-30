from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle
from kivy.properties import StringProperty, ColorProperty, NumericProperty
from kivy.uix.button import Button
from kivy.lang import Builder


class ArrowWidget(Widget):
    """
    Кастомный виджет для отображения стрелки в указанном направлении.
    direction: 'up', 'down', 'left', 'right'
    """
    direction = StringProperty("up")  # default direction
    arrcolor = ColorProperty([1, 1, 1, 1])
    splush = NumericProperty(0.7)

    def __init__(self, direction='', **kwargs):
        super().__init__(**kwargs)
        if direction:
            self.direction = direction
        self.size_hint = (None, None)
        self.bind(pos=self._update_arrow, size=self._update_arrow, direction=self._update_arrow,
                  arrcolor=self._update_color, splush=self._update_arrow)
        with self.canvas:
            Color(0.4, 0.4, 0.4, 1)
            self.back_rec = Rectangle(size=self.size, pos=self.size)

            self.arrow_color = Color(*self.arrcolor)
            self.line = Line(points=[], width=1.2)

    def _update_arrow(self, *args):
        cx, cy = self.pos  # Центр виджета
        w, h = self.size
        half = min(w, h) / 2 * 0.8  # Размер стрелки
        self.back_rec.pos = self.pos
        self.back_rec.size = self.size
        padding_ = min(h / 12, w / 12)

        if self.direction == "deaf":
            padding_ = min(h/4, w/4)
            points = [
                self.center_x - padding_, self.center_y,
                self.center_x + padding_, self.center_y,
                self.center_x, self.center_y,
                self.center_x, self.center_y - padding_,
                self.center_x, self.center_y + padding_
            ]
        elif self.direction == "up":
            points = [
                cx + padding_, cy,
                cx + w - padding_, cy,
                self.center_x, cy + h * self.splush,
                cx + padding_, cy
            ]
        elif self.direction == "down":
            points = [
                cx + padding_, cy + h,
                cx + w - padding_, cy + h,
                self.center_x, cy + (h - h * self.splush),
                cx + padding_, cy + h
            ]
        elif self.direction == "left":
            points = [
                cx + w, cy + padding_,
                cx + w, cy + h - padding_,
                cx + (w - w * self.splush), self.center_y,
                cx + w, cy + padding_
            ]
        elif self.direction == "right":
            points = [
                cx, cy + padding_,
                cx, cy + h - padding_,
                cx + w * self.splush, self.center_y,
                cx, cy + padding_
            ]
        elif self.direction == "left_folding":
            points = [
                cx, cy,
                self.center_x, cy + h,
                cx + w, cy,
                cx, self.center_y,
                cx + w, cy + h
            ]
        elif self.direction == "right_folding":
            points = [
                cx + w, cy,
                self.center_x, cy + h,
                cx, cy,
                cx + w, self.center_y,
                cx, cy + h
            ]
        else:
            points = []

        self.line.points = points

    def _update_color(self, *args):
        self.arrow_color.rgba = self.arrcolor


class TestApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_box_layout = None
        self.btns = None
        self.main_anchor = None
        self.center_box = None
        self.revers_color = 1

    def build(self):
        self.main_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        self.main_box_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(700, 300))

        btns = [
            Button(text='1', size=(50, 50)),
            Button(text='2', size=(50, 50)),
            Button(text='3', size=(50, 50)),
            Button(text='4', size=(50, 50)),
            Button(text='color', size=(50, 50))
        ]
        btn_box = BoxLayout(orientation='vertical', size=(100, 300), size_hint=(None, None))
        for i in btns:
            btn_box.add_widget(i)

        self.arr_w = ArrowWidget()
        self.arr_w2 = ArrowWidget()
        self.arr_w2.direction = 'right'
        self.arr_w3 = ArrowWidget()
        self.arr_w3.direction = 'right'

        btns[0].bind(on_press=self.on_press_buttons)
        btns[1].bind(on_press=self.on_press_buttons)
        btns[2].bind(on_press=self.on_press_buttons)
        btns[3].bind(on_press=self.on_press_buttons)
        btns[4].bind(on_press=self.on_press_buttons)

        self.main_anchor.add_widget(self.main_box_layout)
        self.main_box_layout.add_widget(self.arr_w)
        self.main_box_layout.add_widget(self.arr_w2)
        self.main_box_layout.add_widget(self.arr_w3)
        self.main_box_layout.add_widget(ArrowWidget('deaf'))
        self.main_box_layout.add_widget(ArrowWidget('right_folding'))
        self.main_box_layout.add_widget(ArrowWidget('left_folding'))
        self.main_box_layout.add_widget(btn_box)

        return self.main_anchor

    def on_press_buttons(self, instance):
        if instance.text == '1':
            self.arr_w3.direction = 'up'
            self.arr_w.direction = 'up'
        elif instance.text == '2':
            self.arr_w3.direction = 'down'
            self.arr_w.direction = 'down'
        elif instance.text == '3':
            self.arr_w3.direction = 'left'
            self.arr_w.direction = 'left'
        elif instance.text == '4':
            self.arr_w3.direction = 'right'
            self.arr_w.direction = 'right'
        elif instance.text == 'color':
            if self.revers_color == 1:
                self.arr_w3.arrcolor = [1, 1, 0, 1]
                self.arr_w.arrcolor = [1, 1, 0, 1]
                self.revers_color = 2
            elif self.revers_color == 2:
                self.arr_w3.arrcolor = [1, 1, 1, 1]
                self.arr_w.arrcolor = [1, 1, 1, 1]
                self.revers_color = 1


if __name__ == '__main__':
    TestApp().run()
