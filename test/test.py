from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget


class MyProject(Widget):
    bl = ObjectProperty(None)
    first_name_inp = ObjectProperty(None)
    last_name_inp = ObjectProperty(None)
    password_inp = ObjectProperty(None)

    def submit(self):
        self.bl.remove_widget(self.first_name_inp)

        self.bl.add_widget(Label(text=f'its ok {self.first_name_inp.text}', font_size=30))



class TestApp(App):
    def build(self):
        game = MyProject()
        return game


if __name__ == '__main__':
    TestApp().run()