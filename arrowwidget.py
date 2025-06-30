from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle
from kivy.properties import StringProperty, ColorProperty, NumericProperty


class ArrowWidget(Widget):
    """
    Кастомный виджет для отображения стрелки в указанном направлении.
    direction: 'up', 'down', 'left', 'right', 'deaf', 'right_folding', 'left_folding'
    """
    direction = StringProperty("deaf")  # default direction
    arrcolor = ColorProperty([0, 0, 0, 1])
    color_back = ColorProperty([0.4, 0.4, 0.4, 0])

    def __init__(self, direction='', **kwargs):
        super().__init__(**kwargs)
        if direction:
            self.direction = direction
        self.size_hint = (1, 1)
        self.bind(pos=self._update_arrow, size=self._update_arrow, direction=self._update_arrow,
                  arrcolor=self._update_color, color_back=self._update_color_back)
        with self.canvas:
            self.back_ground_color = Color(*self.color_back)
            self.back_rec = Rectangle(size=self.size, pos=self.size)

            self.arrow_color = Color(*self.arrcolor)
            self.line = Line(points=[], width=1.1)

    def _update_color_back(self, *args):
        self.back_ground_color.rgba = self.color_back

    def _update_arrow(self, *args):
        cx, cy = self.pos  # Центр виджета
        w, h = self.size
        self.half_relevant = 0.7
        half = min(w, h) * self.half_relevant  # Размер стрелки
        self.back_rec.pos = cx, cy
        self.back_rec.size = w, h
        self.base_width = 2
        self.min_indent = 5

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
                cx + (w-half) / self.base_width, cy + (h-half) / 2,
                cx + w - (w-half) / self.base_width, cy + (h-half) / 2,
                self.center_x, cy + h - (h-half) / 2,
                cx + (w-half) / self.base_width, cy + (h-half) / 2,
            ]
        elif self.direction == "down":
            points = [
                cx + (w-half) / self.base_width, cy + h - (h-half) / 2,
                cx + w - (w-half) / self.base_width, cy + h - (h-half) / 2,
                self.center_x, cy + (h - half) / 2,
                cx + (w-half) / self.base_width, cy + h - (h-half) / 2,
            ]
        elif self.direction == "left":
            points = [
                cx + w - (w-half) / 2, cy + (h-half) / self.base_width,
                cx + w - (w-half) / 2, cy + h - (h-half) / self.base_width,
                cx + (w-half) / 2, self.center_y,
                cx + w - (w-half) / 2, cy + (h-half) / self.base_width,
            ]
        elif self.direction == "right":
            points = [
                cx + (w-half) / 2, cy + (h-half) / self.base_width,
                cx + (w-half) / 2, cy + h - (h-half) / self.base_width,
                cx + w - (w-half) / 2, self.center_y,
                cx + (w-half) / 2, cy + (h-half) / self.base_width
            ]
        elif self.direction == "left_folding":
            points = [
                cx+self.min_indent, cy+self.min_indent,
                self.center_x, cy + h - self.min_indent,
                cx + w-self.min_indent, cy+self.min_indent,
                cx+self.min_indent, self.center_y,
                cx + w-self.min_indent, cy + h-self.min_indent
            ]
        elif self.direction == "right_folding":
            points = [
                cx + w-self.min_indent, cy+self.min_indent,
                self.center_x, cy + h-self.min_indent,
                cx+self.min_indent, cy+self.min_indent,
                cx + w-self.min_indent, self.center_y,
                cx+self.min_indent, cy + h-self.min_indent
            ]
        elif self.direction == "round":
            points = [
                cx, self.center_y,
                self.center_x, cy + h,
                cx + w, self.center_y,
                self.center_x, cy,
                cx, self.center_y
            ]
        else:
            points = []

        self.line.points = points

    def _update_color(self, *args):
        self.arrow_color.rgba = self.color_back


class ArrowButtonWidget(ArrowWidget):
    max_spacing = 20
    active_buttons = []  # список всех созданных кнопок

    def __init__(self, direction: str = '', arrow_widget: ArrowWidget = None, **kwargs):
        super().__init__(**kwargs)

        self.arrow_widget = arrow_widget
        if direction:
            self.direction = direction

        self.back_ground_color.a = 1
        self.default_color = self.back_ground_color.rgba[:]  # сохраним оригинальный цвет

        if direction:
            if self.direction == arrow_widget.direction:
                self.back_ground_color.rgba = [0.4, 0.7, 0.7, 1]

        # Добавляем себя в общий список
        ArrowButtonWidget.active_buttons.append(self)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not self.arrow_widget:
                print('Нет arrow_widget')
                return False

            # Снимаем подсветку со всех
            for btn in ArrowButtonWidget.active_buttons:
                btn.color_back = btn.default_color

            # Подсвечиваем текущую
            self.color_back = [0.4, 0.7, 0.7, 1]

            # Меняем направление
            self.arrow_widget.direction = self.direction
            print(f'Выбрана стрелка: {self.direction}')
            return True

        return super().on_touch_down(touch)

