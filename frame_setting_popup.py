from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from windowcalculator import WindowCalculator
from collections import Counter
from arrowwidget import ArrowWidget, ArrowButtonWidget

import createwinstate
from createwinstate import CreateWinState, SPACING
from kivy.core.window import Window

ENTER_KEY = 13


class FrameSettingsPopup(Popup):
    """Popup для настройки размеров секции окна."""

    def __init__(self, window_builder, frame_id, **kwargs):
        super().__init__(title="Параметры секции", size_hint=(None, None), size=(500, 600), **kwargs)
        self.window_builder = window_builder
        self.frame_id = frame_id
        self.frame = self.window_builder.get_frame_with_id(self.frame_id)
        self.parent_frame = self.frame.parent

        self.open_window_scheme_layout = GridLayout(rows=4, cols=4, spacing=15, padding=40)
        self.open_window_schemes = [
            ArrowButtonWidget('deaf', self.frame.arrow_widget),
            ArrowButtonWidget('right_folding', self.frame.arrow_widget),
            ArrowButtonWidget('left_folding', self.frame.arrow_widget),
            ArrowButtonWidget('down', self.frame.arrow_widget),
            ArrowButtonWidget('right', self.frame.arrow_widget), ArrowButtonWidget('left', self.frame.arrow_widget),
            ArrowButtonWidget('round', self.frame.arrow_widget), ArrowButtonWidget('up', self.frame.arrow_widget)
        ]
        for open_window_scheme in self.open_window_schemes:
            open_window_scheme.splush = 1
            self.open_window_scheme_layout.add_widget(open_window_scheme)

        wincal = WindowCalculator(CreateWinState.main_frame)
        wincal_resul = wincal.get_all_imposts()
        new_w = []
        for wincal_res in wincal_resul:
            wincal_res['length'] = int(wincal_res['length'])
            new_w.append(wincal_res)
        self.count_duplicate_dicts(new_w)
        print(wincal_resul)

        self.check_change_width = False
        self.check_change_height = False

        self.keep_orig_width = self.frame.width
        self.keep_orig_height = self.frame.height

        self.main_window_layout = CreateWinState.main_window_layout

        self.width_input = TextInput(hint_text="Ширина", multiline=False, input_filter="int",
                                     size_hint=(1, None), height=40)
        self.height_input = TextInput(hint_text="Высота", multiline=False, input_filter="int",
                                      size_hint=(1, None), height=40)

        # Установка фокуса на активный TextInput после открытия popup
        Clock.schedule_once(self._set_initial_focus, 0.1)

        if self.frame.width:
            self.width_input.text = str(int(self.frame.width))
        if self.frame.height:
            self.height_input.text = str(int(self.frame.height))

        brothers = window_builder.get_brother(frame=self.frame)
        if len(brothers) < 1:
            print(len(window_builder.get_brother(frame=self.frame)))
            self.set_readonly_input(self.width_input)
            self.set_readonly_input(self.height_input)
        elif self.parent_frame.orientation == 'horizontal':
            self.set_readonly_input(self.height_input)
            self.check_change_width = True
        elif self.parent_frame.orientation == 'vertical':
            self.set_readonly_input(self.width_input)
            self.check_change_height = True
        else:
            print(f'error frame_setting_popup __init__ self.parent_frame = {self.parent_frame.orientation}')

        btn_save = Button(text="Сохранить")
        btn_cancel = Button(text="Отмена")

        btn_save.bind(on_release=self._on_save)
        btn_cancel.bind(on_release=lambda *_: self.dismiss())

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        layout.add_widget(self.open_window_scheme_layout)
        layout.add_widget(self.width_input)
        layout.add_widget(self.height_input)

        btns = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btns.add_widget(btn_save)
        btns.add_widget(btn_cancel)
        layout.add_widget(btns)

        Window.bind(on_key_down=self._on_key_down)

        self.add_widget(layout)

    def count_duplicate_dicts(self, dict_list):
        hashable_dicts = [frozenset(sorted(d.items())) for d in dict_list]

        # Считаем количество одинаковых
        counter = Counter(hashable_dicts)

        # Выводим результат в виде: оригинальный словарь -> сколько раз встречается
        for hashed, count in counter.items():
            original_dict = dict(hashed)
            print(f"{original_dict} встречается {count} раз(а)")

    def _set_initial_focus(self, *_):
        def set_focus_and_select(input_field, open_frizer: int = 2):
            input_field.focus = True
            Clock.schedule_once(lambda dt: input_field.select_all(), 0.05)
            if open_frizer > 0:
                open_frizer -= 1
                print(open_frizer)
                Clock.schedule_once(lambda dt: set_focus_and_select(input_field, open_frizer), 0.05)

        if not self.width_input.readonly:
            Clock.schedule_once(lambda dt: set_focus_and_select(self.width_input), 0.05)
        elif not self.height_input.readonly:
            Clock.schedule_once(lambda dt: set_focus_and_select(self.height_input), 0.05)

    def set_readonly_input(self, r_input: TextInput):
        r_input.readonly = True
        r_input.background_color = (0.9, 0.6, 0.6, 1)
        r_input.foreground_color = (0, 0, 0, 1)
        r_input.cursor_color = (0, 0, 0, 0)

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == ENTER_KEY:  # Enter
            print("Enter нажата - закрытие Popup")
            self._on_save()
            return True

    def on_dismiss(self):
        # Отвязка клавиш при закрытии
        Window.unbind(on_key_down=self._on_key_down)

    def _on_save(self, *_):
        if not self.frame:
            self.dismiss()
            return

        try:
            width = int(self.width_input.text)
            height = int(self.height_input.text)
        except ValueError:
            self.dismiss()
            return

        if self.check_change_width and self.keep_orig_width == width:
            self.check_change_width = False
        if self.check_change_height and self.keep_orig_height == height:
            self.check_change_height = False

        if self.check_change_width:
            self.frame.update_width(width)
            self.frame.manual_set_parametr_w = True
        if self.check_change_height:
            print('\n\n\n\nUpdate height\n\n\n\n')
            print('\n\n\n\nUpdate height\n\n\n\n')
            print('\n\n\n\nUpdate height\n\n\n\n')
            print('\n\n\n\nUpdate height\n\n\n\n')
            print('\n\n\n\nUpdate height\n\n\n\n')
            self.frame.update_height(height)
            self.frame.manual_set_parametr_h = True

        self.frame.parent.recalculate_dimensions()
        self.frame.update_layouts_size_hint()

        self.dismiss()
