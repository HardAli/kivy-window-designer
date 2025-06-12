from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class FrameSettingsPopup(Popup):
    """Popup для настройки размеров секции окна."""

    def __init__(self, window_builder, frame_id, **kwargs):
        super().__init__(title="Параметры секции", size_hint=(None, None), size=(600, 400), **kwargs)
        self.window_builder = window_builder
        self.frame_id = frame_id

        self.width_input = TextInput(hint_text="Ширина", multiline=False, input_filter="int",
                                     size_hint=(1, None), height=40)
        self.height_input = TextInput(hint_text="Высота", multiline=False, input_filter="int",
                                      size_hint=(1, None), height=40)

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

        self.add_widget(layout)

    def _on_save(self, *_):
        frame = self.window_builder.get_frame_with_id(self.frame_id)
        if not frame:
            self.dismiss()
            return

        try:
            width = int(self.width_input.text)
            height = int(self.height_input.text)
        except ValueError:
            self.dismiss()
            return

        frame.width = width
        frame.height = height

        layout = frame.layout
        if layout:
            layout.size_hint = (None, None)
            layout.size = (width, height)
            if layout.parent:
                layout.parent.do_layout()

        self.dismiss()