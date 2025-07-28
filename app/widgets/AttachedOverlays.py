from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from app.state.createwinstate import CreateWinState

from app.widgets.windowlayout import WindowLayout


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

        self._is_updating = False

    def r_on_enter(self, instance):
        self.try_update_target_size('height')
        self.bottom_text_input.focus = True  # обратно на нижний

    def r_on_focus_change(self, instance, focus):
        if not focus:
            self.try_update_target_size('height')

    def b_on_enter(self, instance):
        self.try_update_target_size('width')
        self.right_text_input.focus = True  # направо

    def b_on_focus_change(self, instance, focus):
        if not focus:
            self.try_update_target_size('width')

    def try_update_target_size(self, target: str):
        if self._is_updating:
            return

        self._is_updating = True

        try:
            if not isinstance(self.target, WindowLayout):
                print('it is o boje')
                return

            width_text = self.bottom_text_input.text.strip()
            height_text = self.right_text_input.text.strip()

            width = None
            height = None

            if width_text and target == 'width' or target == 'all':
                #print('width')
                width = int(width_text)
                CreateWinState.main_frame.update_width(width)

                #print('\n\n\n\n  iobanyi urod \n\n\n\n')
            if height_text and target == 'height' or target == 'all':
                height = int(height_text)
                CreateWinState.main_frame.update_height(height)

                #print('\n\n\n\n  iobanyi urod \n\n\n\n')

            self.target.update_size(upd_width=width or 0, upd_height=height or 0)

        except ValueError:
            print("⚠ Введены некорректные значения ширины/высоты.")
        finally:
            Clock.schedule_once(lambda dt: setattr(self, '_is_updating', False), 0.1)  # чуть позже снимаем флаг


