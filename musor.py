from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.5, 0.7, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Центральный виджет
        self.center_widget = MyWidget(size_hint=(None, None), size=(200, 200), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.add_widget(self.center_widget)

        # Кнопка сверху по центру
        top_button = Button(text="Top", size_hint=(None, None), size=(80, 40))
        self.add_widget(top_button)
        self.bind(size=self.reposition_elements)
        self.top_button = top_button

        # Снизу
        bottom_label = Label(text="Bottom", size_hint=(None, None), size=(80, 40))
        self.add_widget(bottom_label)
        self.bottom_label = bottom_label

        # Слева
        left_button = Button(text="Left", size_hint=(None, None), size=(40, 80))
        self.add_widget(left_button)
        self.left_button = left_button

        # Справа
        right_button = Button(text="Right", size_hint=(None, None), size=(40, 80))
        self.add_widget(right_button)
        self.right_button = right_button

    def reposition_elements(self, *args):
        cx, cy = self.center_widget.center
        w, h = self.center_widget.size

        # Верх
        self.top_button.center_x = cx
        self.top_button.y = cy + h / 2 + 5

        # Низ
        self.bottom_label.center_x = cx
        self.bottom_label.top = cy - h / 2 - 5

        # Лево
        self.left_button.center_y = cy
        self.left_button.right = cx - w / 2 - 5

        # Право
        self.right_button.center_y = cy
        self.right_button.x = cx + w / 2 + 5


class MyApp(App):
    def build(self):
        return MainLayout()


if __name__ == '__main__':
    MyApp().run()
