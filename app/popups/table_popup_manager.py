from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivymd.uix.behaviors.hover_behavior import HoverBehavior

class PopupManager:
    @staticmethod
    def show_material_popup(callback):
        materials = ["Дерево", "Стекло", "Металл", "Пластик", "Камень"]
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        popup = Popup(title="Выберите материал", content=layout, size_hint=(0.5, 0.5))

        for mat in materials:
            btn = CustomButton(text=mat, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: callback(btn.text, popup))
            layout.add_widget(btn)

        popup.open()

    @staticmethod
    def show_quantity_popup(current_value, callback):
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        popup = Popup(title="Введите количество", content=layout, size_hint=(0.5, 0.3))

        quantity_input = TextInput(text=current_value, multiline=False, size_hint_y=None, height=40)
        quantity_input.focus = True
        btn_save = CustomButton(text="Сохранить", size_hint_y=None, height=40)
        btn_save.bind(on_release=lambda x: callback(quantity_input.text, popup))

        layout.add_widget(quantity_input)
        layout.add_widget(btn_save)
        popup.open()

class CustomButton(Button, HoverBehavior):
    def on_enter(self):
        self.md_bg_color = (0, 0.7, 1, 1)

    def on_leave(self):
        self.md_bg_color = (0, 0.5, 1, 1)
