import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from kivy.uix.button import Button


# Создаём папку для моделей, если её нет
if not os.path.exists("models"):
    os.makedirs("models")


class WindowModel(Widget):
    """Класс для рисования схем открывания окон"""
    def __init__(self, model_type, menu, **kwargs):
        super().__init__(**kwargs)
        self.model_type = model_type
        self.menu = menu  # Ссылка на меню, чтобы обновить `GridLayout`
        self.size_hint = (None, None)
        self.size = (100, 100)

        Clock.schedule_once(self.create_screenshot, 0.5)  # Создаём скриншот после загрузки

    def create_screenshot(self, dt):
        """Создаёт скриншот модели открывания окна"""
        filename = f"models/{self.model_type}.png"
        self.export_to_png(filename)  # Сохраняем картинку с прозрачностью
        Clock.schedule_once(lambda dt: self.menu.reload_images(), 0.2)  # Перезагружаем `GridLayout`

    def on_size(self, *args):
        """Перерисовка схемы при изменении размеров"""
        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 0, 1)
            Line(rectangle=(10, 10, self.width - 20, self.height - 20), width=2)

            if self.model_type == "fixed":
                pass
            elif self.model_type == "turn":
                Line(points=[10, 10, self.width - 10, self.height - 10], width=2)
                Line(points=[self.width - 10, self.height - 10, self.width - 30, self.height - 10], width=2)
            elif self.model_type == "tilt":
                Line(points=[10, 10, self.width - 10, self.height / 2], width=2)
                Line(points=[self.width - 10, self.height / 2, self.width - 20, self.height / 2 + 10], width=2)
            elif self.model_type == "tilt_turn":
                Line(points=[10, 10, self.width - 10, self.height - 10], width=2)
                Line(points=[10, 10, self.width - 10, self.height / 2], width=2)
                Line(points=[self.width - 10, self.height / 2, self.width - 20, self.height / 2 + 10], width=2)
            elif self.model_type == "sliding":
                Line(points=[10, 10, self.width / 2, 10], width=2)
                Line(points=[self.width / 2 + 10, 10, self.width - 10, 10], width=2)
                Line(points=[self.width / 2, 10, self.width / 2 + 10, 10], width=2, dash_offset=5)
            elif self.model_type == "folding":
                Line(points=[10, 10, 30, 10, 30, self.height - 10, 50, self.height - 10, 50, 10, self.width - 10, 10],
                     width=2)
                Line(points=[30, 10, 30, self.height - 10], width=2)
                Line(points=[50, 10, 50, self.height - 10], width=2)
            elif self.model_type == "lift_sliding":
                Line(points=[10, 10, self.width / 2, 10, self.width / 2, self.height - 10, 10, self.height - 10],
                     width=2)
                Line(points=[self.width / 2, 10, self.width - 10, 10, self.width - 10, self.height - 10, self.width / 2,
                             self.height - 10], width=2, dash_offset=5)
                Line(points=[self.width - 20, 10, self.width - 20, self.height - 10], width=2)


class SlideOutMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.width = Window.width * 0.5
        self.height = Window.height
        self.x = Window.width
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        self.label = Label(text="Модель открывания", size_hint=(1, None), height=50, bold=True)
        self.add_widget(self.label)

        self.grid = GridLayout(cols=3, spacing=5, size_hint=(1, 1))

        # Создаём модели открывания окон
        self.models = ["fixed", "turn", "tilt", "tilt_turn", "sliding", "folding", "lift_sliding"]
        self.images = []  # Список `Image`, которые будут обновляться

        for model in self.models:
            WindowModel(model, self)  # Создаём модели и сохраняем их
            img = Image(size_hint=(None, None), size=(120, 120))  # Создаём пустые `Image`
            self.grid.add_widget(img)
            self.images.append(img)  # Сохраняем `Image`, чтобы обновлять

        print(self.images)

        self.add_widget(self.grid)
        Window.bind(on_resize=self.on_window_resize)

    def reload_images(self):
        """Обновляет изображения после создания скриншотов"""
        for i, model in enumerate(self.models):
            with open('test.txt', 'w', encoding='utf-8') as file:
                file.write(i)
            img_path = f"models/{model}.png"
            if os.path.exists(img_path):  # Проверяем, есть ли файл
                self.images[i].source = img_path  # Загружаем изображение

    def update_rect(self, *args):
        """Обновляет фон"""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_window_resize(self, instance, width, height):
        """Обновляет размеры окна"""
        self.width = width * 0.5
        self.height = height
        if self.x != width:
            self.x = width - self.width
        else:
            self.x = width
        self.update_rect()

    def toggle(self):
        """Открывает/закрывает вкладку"""
        target_x = Window.width - self.width if self.x == Window.width else Window.width
        anim = Animation(x=target_x, duration=0.3)
        anim.start(self)


class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = SlideOutMenu()
        self.add_widget(self.menu)

        self.toggle_button = Button(text="Меню", size_hint=(None, None), size=(100, 50), pos_hint={'right': 1, 'y': 0.9})
        self.toggle_button.bind(on_press=lambda x: self.menu.toggle())

        self.add_widget(self.toggle_button)


class MainApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    MainApp().run()
