from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class LineAndInput(Widget):
    pass


class MySuperTestApp(App):
    def build(self):
        bl = BoxLayout(orientation='horizontal')
        bl.add_widget(LineAndInput())
        return bl


if __name__ == '__main__':
    MySuperTestApp().run()