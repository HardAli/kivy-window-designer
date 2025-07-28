from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button


class ContextMenu(Popup):
    """ Всплывающее меню с выбором значения (как выпадающий список) """

    def __init__(self, options, button, title='Выберите значение', **kwargs):
        super().__init__(title=title, size_hint=(0.7, 0.7), **kwargs)
        self.button_height = '20sp'
        self.button = button

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        scroll = ScrollView()
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        button_layout.bind(minimum_height=button_layout.setter('height'))

        for option in options:
            btn = Button(text=option, size_hint_y=None, height=self.button_height)
            btn.bind(on_release=lambda btn, opt=option: self.select_option(opt))
            button_layout.add_widget(btn)

        scroll.add_widget(button_layout)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def select_option(self, option):
        self.button.text = str(option)
        self.dismiss()