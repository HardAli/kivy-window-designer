from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.boxlayout import BoxLayout


class LineIntInput(Widget):
    def __init__(self, line_ratio=0.8, is_vertical=False, hint_text='1000', **kwargs):
        super().__init__(**kwargs)
        self.line_ratio = line_ratio  # % от размера
        self.is_vertical = is_vertical
        self.font_size = 12

        # Установка size_hint для адаптивности
        self.size_hint = (None, None) if is_vertical else (None, None)
        self.height = 200 if is_vertical else self.height
        self.width = 200 if not is_vertical else self.width

        self.text_input = TextInput(
            hint_text=hint_text,
            multiline=False,
            input_filter='int',
            halign='center',
            font_size=self.font_size,
            size_hint=(None, None),
            size=(55, 30),
        )
        self.add_widget(self.text_input)

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.line = Line(points=[], width=1.2)
            Color(0.3, 0.3, 0.3, 1)
            self.elips = Ellipse()
            self.elips2 = Ellipse()

        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        w, h = self.size
        cx, cy = self.center

        # Длина линии зависит от ratio
        if self.is_vertical:
            line_len = h * self.line_ratio
            radius = 6
            start = (cx, cy + line_len / 2)
            end = (cx, cy - line_len / 2)
            s_el = (cx - radius, cy + line_len / 2 - radius)
            e_el = (cx - radius, cy - line_len / 2 - radius)
        else:
            line_len = w * self.line_ratio
            radius = 6
            start = (cx - line_len / 2, cy)
            end = (cx + line_len / 2, cy)
            s_el = (cx - line_len / 2 - radius, cy - radius)
            e_el = (cx + line_len / 2 - radius, cy - radius)

        self.line.points = [*start, *end]
        self.elips.pos = s_el
        self.elips.size = (2 * radius, 2 * radius)
        self.elips2.pos = e_el
        self.elips2.size = (2 * radius, 2 * radius)
        w

        # Центрируем текст
        ti_w, ti_h = self.text_input.size
        self.text_input.pos = (cx - ti_w / 2, cy - ti_h / 2)

    def get_input_text(self):
        return self.text_input.text

