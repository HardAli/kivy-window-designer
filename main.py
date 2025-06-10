from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

from createnewwindow import CreateNewWindow
from glasscut import GlassCut


# задаем размер окна
Window.size = (700, 500)
# set background color
Window.clearcolor = (255/255, 186/255, 186/255, 1)
Window.title = 'ZarWindow'
Window.resizable = True


# фиксируем изменение размера окна
def on_window_resize(window, width, height):
    print('ooo')


# включаем фиксацию размера окна
Window.bind(on_resize=on_window_resize)


# конвертируем цвета rgb и3 255 системы в 0-1
def color_convector(r=0, g=0, b=0, color=None):
    """Преобразуйте значения RGB из диапазона 0-255 в диапазон 0-1."""
    if color is None:
        color = [r, g, b]
    elif len(color) == 3:
        if color[0] > 1:
            color[0] = color[0] / 255
        if color[1] > 1:
            color[1] = color[1] / 255
        if color[2] > 1:
            color[2] = color[2] / 255

    return color


class Menu(Screen):
    pass


class Prices(Screen):
    pass


class Components(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class ZaurWindowApp(MDApp):
    def build(self):
        pass


if __name__ == "__main__":
    ZaurWindowApp().run()
