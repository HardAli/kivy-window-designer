# popup_resize.py
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from app.widgets.custominput import CustomInput
from kivy.lang.builder import Builder


Builder.load_file('../../kv/popup_resize.kv')


class AllResizeBlock(BoxLayout):
    height_resize = BooleanProperty(False)
    width_resize = BooleanProperty(False)
    frame_resize_popup = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width_input = self.ids.all_height_input
        self.height_input = self.ids.all_width_input

    def on_height_resize(self, instance, value):
        if value is True:
            self.height_input.set_active()
            print(self.frame_resize_popup)
        else:
            self.height_input.set_not_active()

    def on_width_resize(self, instance, value):
        if value is True:
            self.width_input.set_active()
        else:
            self.width_input.set_not_active()


class FrameResizePopup(Popup):
    def __init__(self, frames, **kwargs):
        super().__init__(**kwargs)
        self.title = "Массовое изменение размеров"
        self.size_hint = (0.8, 0.8)
        AllResizeBlock.frame_resize_popup = self

        self.frames = [frame.window.get_frame_with_id(frame.frame_id) for frame in frames]
        self.inputs = []
        self.same_width_cb = CheckBox()
        self.same_height_cb = CheckBox()

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        for i, frame in enumerate(self.frames):
            row = BoxLayout(size_hint_y=None, height=35)
            row.add_widget(Label(text=f"Окно {frame.frame_id}"))

            width_input = CustomInput(text=str(frame.width), multiline=False)
            height_input = CustomInput(text=str(frame.height), multiline=False)

            if frame.orientation == 'vertical':
                width_input.set_readonly()
            if frame.orientation == 'horizontal':
                height_input.set_readonly()

            row.add_widget(Label(text="Ширина:"))
            row.add_widget(width_input)
            row.add_widget(Label(text="Высота:"))
            row.add_widget(height_input)

            self.inputs.append((frame, width_input, height_input))
            layout.add_widget(row)

        layout.add_widget(AllResizeBlock())

        apply_btn = Button(text="Применить", size_hint_y=None, height=40, on_press=self.apply_changes)
        layout.add_widget(apply_btn)

        self.content = layout

    def apply_changes(self, instance):
        if not self.inputs:
            return

        try:
            if self.same_width_cb.active:
                width_value = float(self.inputs[0][1].text)
                for frame, _, _ in self.inputs:
                    frame.width = round(width_value)
            else:
                for frame, width_input, _ in self.inputs:
                    frame.width = round(float(width_input.text))

            if self.same_height_cb.active:
                height_value = float(self.inputs[0][2].text)
                for frame, _, _ in self.inputs:
                    frame.height = round(height_value)
            else:
                for frame, _, height_input in self.inputs:
                    frame.height = round(float(height_input.text))

            self.dismiss()

        except ValueError as e:
            from kivy.uix.label import Label
            from kivy.uix.popup import Popup

            err = Popup(title="Ошибка",
                        content=Label(text="Некорректное значение\nПожалуйста, введите число"),
                        size_hint=(None, None), size=(400, 200))
            err.open()
