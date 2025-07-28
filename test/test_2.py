from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton


Builder.load_file('test_2.kv')


class StartScreen(BoxLayout):
    new_text_for_button = StringProperty()



class Program(MDApp):
    def build(self):
        return StartScreen(new_text_for_button='This new text')

Program().run()