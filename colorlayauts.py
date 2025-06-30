from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import BooleanProperty

from frame_setting_popup import FrameSettingsPopup
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle, Canvas


WIDTH = 1
GLASS_COLOR = [122, 200, 251]
GlASS_BOTTOM = 8


class schet:
    number = 0

    def add_number(self):
        self.number +=1
        print(self.number)


num = schet()


class ColoredLayout:
    my_color = {
        'r': 0,
        'g': 0,
        'b': 0,
        'a': 1
    }

    def set_color(self, r=0, g=0, b=0, a=1):
        if r > 1 or g > 1 or b > 1 or a > 1:
            r, g, b, a = self.color_convector(r, g, b, a)
        self.my_color['r'] = r
        self.my_color['g'] = g
        self.my_color['b'] = b
        self.my_color['a'] = a
        self.rect_color.rgba = self.get_color()

    def get_color(self):
        return self.my_color['r'], self.my_color['g'], self.my_color['b'], self.my_color['a']

    def color_convector(self, r, g, b, a):
        if r > 1:
            r = r / 255
        if g > 1:
            g = g / 255
        if b > 1:
            b = b / 255
        if a > 1:
            a = a / 255

        return r, g, b, a


class ColorBoxLayout(BoxLayout, ColoredLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.rect_color = Color(self.get_color())
            self.rect = Rectangle(size=self.size, pos=self.pos)

            self.border_color = Color(0, 0, 0, 1)
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=1.3)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.border.rectangle = (self.x, self.y, self.width, self.height)


class ColorButtonBoxLayout(BoxLayout, ColoredLayout):

    show_canvas = BooleanProperty(True)
    def __init__(self, frame_id, window, **kwargs):
        super().__init__(**kwargs)
        self.size_button = [15, 15]
        self.indent_delete_button = 10
        self.frame_id = frame_id
        self.window = window

        with self.canvas.after:
            self.label_id = Label(
                text=str(frame_id),
                pos=[self.center_x, self.center_y],
                size=[25, 25],
                color=(0, 0, 0, 1)
            )

        with self.canvas.before:
            self.rect_color = Color(self.get_color())
            self.rect = Rectangle()

            self.rect_glass_color = Color(GLASS_COLOR[0]/255, GLASS_COLOR[1]/255, GLASS_COLOR[2]/255)
            self.rect_glass = Rectangle()

            self.border_glass_color = Color(0, 0, 0, 1)
            self.glass_border = Line()

            self.border_color = Color(0, 0, 0, 1)
            self.border = Line(width=WIDTH)

        self.bind(size=self.update_rect, pos=self.update_rect, show_canvas=self.update_rect)

        # Контейнер для кнопок
        self.overlay = RelativeLayout()
        self.add_widget(self.overlay)

        # Кнопки добавления и удаления
        self.top_button = Button(text='+', size_hint=(None, None), size=self.size_button)
        self.top_button.id = f'{frame_id}:top'
        self.top_button.bind(on_press=self.on_button_press)
        self.overlay.add_widget(self.top_button)

        self.right_button = Button(text='+', size_hint=(None, None), size=self.size_button)
        self.right_button.id = f'{frame_id}:right'
        self.right_button.bind(on_press=self.on_button_press)
        self.overlay.add_widget(self.right_button)

        self.delet_window_button = Button(text='-', size_hint=(None, None), size=(20, 20))
        self.delet_window_button.font_size = 20
        self.delet_window_button.id = f'{frame_id}:delete'
        self.delet_window_button.background_color = [1, 0, 0, 1]
        self.delet_window_button.bind(on_press=self.on_button_press)
        self.overlay.add_widget(self.delet_window_button)

        self.bind(size=self.update_buttons, pos=self.update_buttons)

    def update_rect(self, *args):
        # рисуем только если число "реальных" детей (не overlay) меньше 2
        non_overlay_children = self.window.get_frame_with_id(self.frame_id).child
        if len(non_overlay_children) < 2 and self.show_canvas:
            self.rect_glass.size = (self.width - GlASS_BOTTOM, self.height - GlASS_BOTTOM)
            self.rect_glass.pos = (self.x + GlASS_BOTTOM/2, self.y + GlASS_BOTTOM/2)
            self.rect.size = self.size
            self.rect.pos = self.pos
            self.border.rectangle = (self.x, self.y, self.width, self.height)
            self.glass_border.rectangle = (
                self.x + GlASS_BOTTOM/2,
                self.y + GlASS_BOTTOM/2,
                self.width - GlASS_BOTTOM,
                self.height - GlASS_BOTTOM
            )
        else:
            # если больше 2 детей — делаем их "невидимыми", но не очищаем canvas полностью
            self.rect.size = (0, 0)
            self.rect_glass.size = (0, 0)
            self.border.rectangle = (0, 0, 0, 0)
            self.glass_border.rectangle = (0, 0, 0, 0)

    def update_buttons(self, *args):
        self.top_button.pos = (self.width/2 - self.top_button.width / 2, self.height - self.top_button.height)
        self.right_button.pos = (self.width - self.right_button.width, self.height / 2 - self.right_button.height / 2)
        self.delet_window_button.pos = (
            self.width - self.delet_window_button.width - 7, 7
        )
        self.label_id.pos = (self.center_x - 12.5, self.center_y - 12.5)

    def on_button_press(self, instance):
        button_id = str(instance.id)
        button_func = button_id.split(':')[1]

        if button_func == 'top':
            self.window.add_frame(window=self.window, frame_id=self.frame_id, orientation_frame='vertical')
            print('top')
        elif button_func == 'right':
            self.window.add_frame(window=self.window, frame_id=self.frame_id, orientation_frame='horizontal')
            print('right')
        elif button_func == 'delete':
            self.window.delete_frame(frame_id=self.frame_id)

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            FrameSettingsPopup(self.window, self.frame_id).open()
            return True
        return False
class ColorAnchorLayout(AnchorLayout, ColoredLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect_color = Color(self.get_color())
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class ColorFloatLayout(FloatLayout, ColoredLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect_color = Color(self.get_color())
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
