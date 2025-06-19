from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from createwinstate import CreateWinState

from windowlayout import WindowLayout


class AttachedOverlay(FloatLayout):
    def __init__(self, target_widget: Widget, margin: int = 30, l_el=0, r_el=0, t_el=0, b_el=0, main_frame=None, **kwargs):
        """
        Компонент, размещающий элементы по сторонам от целевого виджета.

        :param target_widget: Виджет, к которому прикрепляются элементы.
        :param margin: Отступ между target и внешними элементами.
        :param r, l, t, b: переменные с ключами 'top', 'bottom', 'left', 'right' и значениями-виджетами.
        """
        super().__init__(**kwargs)
        self.target = target_widget
        self.margin = margin
        self.l_el, self.r_el, self.t_el, self.b_el = l_el, r_el, t_el, b_el

        self.add_widget(self.target)

        if self.l_el:
            self.add_widget(self.l_el)
        if self.r_el:
            self.add_widget(self.r_el)
        if self.t_el:
            self.add_widget(self.t_el)
        if self.b_el:
            self.add_widget(self.b_el)

        self.target.bind(pos=self.update_canvas, size=self.update_canvas)
        Window.bind(on_resize=self.on_window_resize)

        Clock.schedule_interval(self.update_canvas, 0.1)

    def on_window_resize(self, *args):
        Clock.schedule_once(self.update_canvas, 0)

    def update_canvas(self, *args):
        cx, cy = self.target.center
        w, h = self.target.size

        m = self.margin

        # Безопасно обрабатываем только те стороны, которые заданы
        if self.t_el:
            self.t_el.pos = [cx - self.t_el.width/2, cy + h / 2 - self.t_el.height/2 + m]

        if self.b_el:
            self.b_el.pos = [cx - self.b_el.width/2, cy - h/2 - self.b_el.height/2 - m]

        if self.l_el:
            self.l_el.pos = [cx - w / 2 - self.l_el.width/2 - m, cy - self.l_el.height/2]

        if self.r_el:
            self.r_el.pos = [cx + w / 2 - self.r_el.width/2 + m, cy - self.r_el.height/2]


class WindowLinesEvent(AttachedOverlay):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.right_text_input = self.r_el.text_input
        self.bottom_text_input = self.b_el.text_input

        self.right_text_input.bind(on_text_validate=self.r_on_enter)
        self.right_text_input.bind(focus=self.r_on_focus_change)

        self.bottom_text_input.bind(on_text_validate=self.b_on_enter)
        self.bottom_text_input.bind(focus=self.b_on_focus_change)

    def r_on_enter(self, instance):
        self.try_update_target_size()

    def r_on_focus_change(self, instance, focus):
        if not focus:
            self.try_update_target_size()

    def b_on_enter(self, instance):
        self.try_update_target_size()

    def b_on_focus_change(self, instance, focus):
        if not focus:
            self.try_update_target_size()

    def try_update_target_size(self):
        if not isinstance(self.target, WindowLayout):
            print('it is o boje')
            return

        width_text = self.bottom_text_input.text.strip()
        height_text = self.right_text_input.text.strip()
        width = 0
        height = 0

        try:
            if width_text:
                width = int(width_text)
                CreateWinState.main_frame.width = width
            if height_text:
                height = int(height_text)
                CreateWinState.main_frame.height = height

            self.target.update_size(upd_width=width, upd_height=height)
            print(width, height, 'af')

        except ValueError:
            print("⚠ Введены некорректные значения ширины/высоты.")


