import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
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
        self.size_hint = (0.3, 0.3)
        self.size = (100, 100)


        Clock.schedule_once(self.create_screenshot, 0.1)  # Создаём скриншот после загрузки

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
                Line(points=[10, 10, self.width - 10, self.height - self.height/2, 10, self.height - 13], width=2)
            elif self.model_type == "tilt":
                Line(points=[self.width - 10, self.height - 10, 10, self.height/2, self.width - 10, 10], width=2)
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


class DraggingImage(Image):
    """Копия изображения, которая двигается за курсором и исчезает при отпускании"""
    def __init__(self, source, **kwargs):
        super().__init__(source=source, **kwargs)
        self.size_hint = (None, None)
        self.size = (80, 80)  # Уменьшенный размер копии
        self.opacity = 1  # Полностью видимый

    def start_drag(self, touch):
        """Запоминаем начальную позицию"""
        self.touch_offset_x = self.center_x - touch.x
        self.touch_offset_y = self.center_y - touch.y
        self.dragging = True

    def on_touch_move(self, touch):
        """Двигаем копию за курсором"""
        if self.dragging:
            self.center_x = touch.x + self.touch_offset_x
            self.center_y = touch.y + self.touch_offset_y
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        """Исчезновение при отпускании"""
        if self.dragging:
            anim = Animation(opacity=0, duration=0.2)
            anim.bind(on_complete=lambda *args: self.parent.remove_widget(self))
            anim.start(self)
            return True
        return super().on_touch_up(touch)


class ClickableImage(Image):
    """Изображение в `GridLayout`, которое создаёт свою копию при нажатии"""
    def __init__(self, model_type, menu, layout, **kwargs):
        super().__init__(**kwargs)
        self.model_type = model_type
        self.layout = layout
        self.menu = menu  # Ссылка на меню, чтобы закрыть её при клике

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            root_layout = self.layout  # Главный `FloatLayout`
            copy = DraggingImage(source=self.source, pos=self.to_window(*self.pos))
            root_layout.add_widget(copy)
            copy.start_drag(touch)

            # Закрываем вкладку при клике
            self.menu.close_menu()
            return True
        return super().on_touch_down(touch)


class SlideOutMenu(BoxLayout):
    def __init__(self, layout, **kwargs):
        super().__init__(**kwargs)
        self.is_open = False
        self.size_hint_x = None
        self.width = Window.width * 0.5
        self.height = Window.height
        self.x = Window.width
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        with self.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        self.label = Label(text="Модель открывания", size_hint=(1, None), height=50, bold=True, color=(0, 0, 0, 1))
        self.add_widget(self.label)

        self.grid = GridLayout(cols=3, spacing=0, padding=0, size_hint=(1, 1))

        # Создаём модели открывания окон
        self.models = ["fixed", "turn", "tilt", "tilt_turn", "sliding", "folding", "lift_sliding"]
        self.images = []  # Список `Image`, которые будут обновляться

        for model in self.models:
            WindowModel(model, self)  # Создаём модели и сохраняем их
            img = ClickableImage(model_type=model, menu=self, size_hint=(0.13, 0.13), layout=layout)
            self.grid.add_widget(img)
            self.images.append(img)  # Сохраняем `Image`, чтобы обновлять

        self.add_widget(self.grid)
        Window.bind(on_resize=self.on_window_resize)

    def reload_images(self):
        """Обновляет изображения после создания скриншотов"""
        for i, model in enumerate(self.models):
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

        if self.is_open:
            self.x = width - self.width
        else:
            self.x = width

        self.update_rect()

    def toggle(self):
        """Открывает/закрывает вкладку"""
        self.is_open = not self.is_open
        target_x = Window.width - self.width if self.is_open else Window.width
        Animation(x=target_x, duration=0.3).start(self)

    def close_menu(self):
        """Закрывает вкладку"""
        self.is_open = False
        Animation(x=Window.width, duration=0.3).start(self)


class SlideOutsLayoutWindowModels(FloatLayout):
    def __init__(self, layout, **kwargs):
        super().__init__(**kwargs)
        self.menu = SlideOutMenu(layout)
        self.add_widget(self.menu)

        self.toggle_button = Button(text="Меню", size_hint=(None, None), size=(100, 50), pos_hint={'right': 1, 'y': 0.9})
        self.toggle_button.bind(on_press=lambda x: self.menu.toggle())

        self.add_widget(self.toggle_button)
