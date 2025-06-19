from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from createwinstate import CreateWinState


class FrameSettingsPopup(Popup):
    """Popup для настройки размеров секции окна."""

    def __init__(self, window_builder, frame_id, **kwargs):
        super().__init__(title="Параметры секции", size_hint=(None, None), size=(600, 400), **kwargs)
        self.window_builder = window_builder
        self.frame_id = frame_id
        self.frame = self.window_builder.get_frame_with_id(self.frame_id)
        self.parent_frame = self.frame.parent

        self.main_window_layout = CreateWinState.main_window_layout

        self.width_input = TextInput(hint_text="Ширина", multiline=False, input_filter="int",
                                     size_hint=(1, None), height=40)
        self.height_input = TextInput(hint_text="Высота", multiline=False, input_filter="int",
                                      size_hint=(1, None), height=40)

        if self.frame.width:
            self.width_input.text = str(self.frame.width)
        if self.frame.height:
            self.height_input.text = str(self.frame.height)

        if len(window_builder.get_brother(frame=self.frame)) <= 1:
            self.set_readonly_input(self.width_input)
            self.set_readonly_input(self.height_input)
        elif self.parent_frame.orientation == 'horizontal':
            self.set_readonly_input(self.width_input)
        elif self.parent_frame.orientation == 'vertical':
            self.set_readonly_input(self.height_input)
        else:
            print(f'error frame_setting_popup __init__ self.parent_frame = {self.parent_frame.orientation}')



        btn_save = Button(text="Сохранить")
        btn_cancel = Button(text="Отмена")

        btn_save.bind(on_release=self._on_save)
        btn_cancel.bind(on_release=lambda *_: self.dismiss())

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        layout.add_widget(self.width_input)
        layout.add_widget(self.height_input)

        btns = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btns.add_widget(btn_save)
        btns.add_widget(btn_cancel)
        layout.add_widget(btns)

        self.window_builder.get_brother(frame_id=self.frame_id)

        self.add_widget(layout)

    def set_readonly_input(self, r_input: TextInput):
        r_input.readonly = True
        r_input.background_color = (0.9, 0.6, 0.6, 1)
        r_input.foreground_color = (0.5, 0.5, 0.5, 1)
        r_input.cursor_color = (0, 0, 0, 0)

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

        self.frame.width = width
        self.frame.height = height
        self.frame.manual_set_parametrs = True

        layout = self.frame.layout
        if layout:
            layout.size_hint = (None, None)
            width = self.main_window_layout.get_update_scale(width)
            height = self.main_window_layout.get_update_scale(height)
            layout.size = (width, height)
            if layout.parent:
                layout.parent.do_layout()

        self.dismiss()
