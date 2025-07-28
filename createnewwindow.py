from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle, Canvas
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from colorlayauts import *


# Coздаем обьект окна
class WindowObject():
    window = [
        {
            'id': 0,
            'width': 0,
            'height': 0,
            'pos_x': 0,
            'pos_y': 0
        },
        [],
        []
    ]
    # расстояние между окнами(ширина стенок)
    wall_tick = 7
    check = 0

    # добавляет элемент в список с конкретным id
    def add_to_list_with_id(self, target_id, new_element, data=None):
        if not data:
            data = self.get_windows()
        for i, item in enumerate(data):
            if isinstance(item, list):
                if target_id in item:
                    item.append(new_element)
                    return True
                elif self.add_to_list_with_id(target_id, new_element, item):
                    return True
        return False

    def add_win_parametrs(self, win_id, size, section=False):
        self.window[2].append({
            'id': win_id,
            'width': size[0],
            'height': size[1],
            'section': section
        })

    def find_subarray_with_id(self, target_id, data=[]):
        if target_id == 0:
            return [1, 2, 3]
        if not data:
            data = self.get_windows()

        for item in data:
            if isinstance(item, list):
                result = self.find_subarray_with_id(target_id, item)
                if result is not None:
                    return result
            elif item == target_id:
                return data
        return None

    def find_parent_id(self, target_id=0, data=[], parent=None):
        if not data:
            data = self.get_windows()
        for item in data:
            if isinstance(item, list):
                # если вложенный элемент это - список, продолжаем искать рекурсивно
                result = self.find_parent_id(target_id, item, parent=data[0])
                if result is not None:
                    return result
            elif item == target_id:
                if isinstance(parent, list):
                    parent = parent[0]
                return parent
        return None

    def sorted_parametrs_with_id(self):
        parametrs = self.window[2]
        sorted_parametrs = sorted(parametrs, key=lambda x: x['id'])
        self.window[2] = sorted_parametrs[:]

    def add_section(self, win_id=0, orientation='horizontal'):
        # получаем все id
        ids = self.collect_ids()

        tick_section = 0
        # проверяем если нет id значит это новое окно
        if not ids:
            win_parametrs = self.calculate_win_parametrs(orient=orientation)
            size = win_parametrs[0]
            pos1 = win_parametrs[1][0]
            pos2 = win_parametrs[1][1]
            if orientation == 'horizontal':
                self.window[1].append([1])
                self.window[1].append([2])
                self.add_win_parametrs(1, size, pos1)
                self.add_win_parametrs(2, size, pos2)
            elif orientation == 'vertical':
                self.window[1].append([1])
                self.add_to_list_with_id(1, [2])
                self.add_to_list_with_id(1, [3])
                self.add_win_parametrs(2, size, pos1)
                self.add_win_parametrs(3, size, pos2)

                pos = self.get_pos()
                pos = [pos[0] + tick_section, pos[1] + tick_section]
                size = self.get_size()
                size = [size[0] - tick_section * 2, size[1] - tick_section * 2]
                self.add_win_parametrs(1, size, pos, True)

            else:
                print(f'непонятная ориентация: {orientation}')
        else:
            if win_id == 0:
                print('id is 0')
                return None
            else:
                win_parametrs = self.calculate_win_parametrs(parent_id=win_id, orient=orientation)
                size = win_parametrs[0]
                pos1 = win_parametrs[1][0]
                pos2 = win_parametrs[1][1]
                new_win_id = max(self.collect_ids()) + 1
                if orientation == 'horizontal':
                    self.add_to_list_with_id(win_id, [new_win_id])
                    self.add_to_list_with_id(win_id, [new_win_id + 1])
                    self.add_win_parametrs(new_win_id, size, pos1)
                    self.add_win_parametrs(new_win_id + 1, size, pos2)
                elif orientation == 'vertical':
                    self.add_to_list_with_id(win_id, [new_win_id])
                    self.add_to_list_with_id(new_win_id, [new_win_id + 1])
                    self.add_to_list_with_id(new_win_id, [new_win_id + 2])

                    self.add_win_parametrs(new_win_id + 1, size, pos1)
                    self.add_win_parametrs(new_win_id + 2, size, pos2)

                    parent_id = self.find_parent_id(win_id)
                    parent_parametrs = self.get_win_parametrs(parent_id)
                    pos = [parent_parametrs['pos_x'], parent_parametrs['pos_y']]
                    pos = [pos[0] + tick_section, pos[1] + tick_section]
                    size = [parent_parametrs['width'], parent_parametrs['height']]
                    size = [size[0] - tick_section * 2, size[1] - tick_section * 2]
                    self.add_win_parametrs(new_win_id, size, pos, True)

    def calculate_win_parametrs(self, parent_id=0, orient='horizontal'):
        def get_parametrs(parent_size, parent_pos, tick, orientation):
            if orientation == 'horizontal':
                size = [(parent_size[0] - (tick * 3)) / 2, parent_size[1] - tick * 2]
                pos = [
                    [(parent_pos[0] + (size[0] * 0)) + (tick * 1), parent_pos[1] + tick],
                    [(parent_pos[0] + (size[0] * 1)) + (tick * 2), parent_pos[1] + tick]
                ]
            elif orientation == 'vertical':
                size = [parent_size[0] - tick * 2, (parent_size[1] - (tick * 3)) / 2]
                pos = [
                    [parent_pos[0] + tick, (parent_pos[1] + (size[1] * 0)) + (tick * 1)],
                    [parent_pos[0] + tick, (parent_pos[1] + (size[1] * 1)) + (tick * 2)]
                ]
            return [size, pos]

        if parent_id == 0:
            par_size = self.get_size()
            par_pos = self.get_pos()
            win_tick = self.get_tick()

        else:
            parent_parametrs = self.get_win_parametrs(parent_id)
            par_size = [parent_parametrs['width'], parent_parametrs['height']]
            par_pos = [parent_parametrs['pos_x'], parent_parametrs['pos_y']]
            win_tick = self.get_tick()
        return get_parametrs(par_size, par_pos, win_tick, orient)


    def set_width(self, width):
        self.window[0]['width'] = width

    def set_height(self, height):
        self.window[0]['height'] = height

    def set_wall_tick(self, tick):
        self.wall_tick = tick

    def set_size(self, size=[]):
        self.set_width(size[0])
        self.set_height(size[1])

    def set_position(self, pos=[0, 0]):
        pos = pos[:]
        self.window[0]['pos_x'] = pos[0]
        self.window[0]['pos_y'] = pos[1]

    def collect_ids(self, data=0):
        if not data:
            data = self.get_windows()
        ids = []
        for item in data:
            if isinstance(item, list):
                ids.extend(self.collect_ids(item))
            else:
                ids.append(item)
        return ids

    def get_win_parametrs(self, win_id):
        parametrs = self.window[2]
        for i in parametrs:
            if i['id'] == win_id:
                return i
        else:
            print('not found parametrs id')
            return None

    def get_tick(self):
        return self.wall_tick

    def get_width(self):
        return self.window[0]['width']

    def get_height(self):
        return self.window[0]['height']

    def get_size(self):
        return [self.window[0]['width'], self.window[0]['height']]

    def get_pos(self):
        return [self.window[0]['pos_x'], self.window[0]['pos_y']]

    def get_windows(self):
        return self.window[1]


class WidgetWindow(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            x, y, h, w = self.get_parametrs()
            Color(0, 0, 0, 1)
            self.rect_wall = Rectangle(size=self.size, pos=self.pos)
            Color(0.8, 0.8, 0.8, 1)
            self.rect_fill = Rectangle(size=(h, w), pos=(x, y))

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        x, y, h, w = self.get_parametrs()
        self.rect_fill.size = (h, w)
        self.rect_fill.pos = (x, y)
        self.rect_wall.size = self.size
        self.rect_wall.pos = self.pos

    def get_parametrs(self, tick_wall = 3):
        x, y = self.pos
        h, w = self.size
        x, y, h, w = x + tick_wall, y + tick_wall, h - tick_wall * 2, w - tick_wall * 2
        return [x, y, h, w]


# Создаем обьект табло
class TabloObject:
    # запрашиваем размер рабочего окна
    screen_width, screen_height = Window.width, Window.height

    tablo = {
        'pos_x': 50,
        'pos_y': screen_height / 3,
        'width': screen_width - 100,
        'height': screen_height - ((screen_height / 4) * 2),
        'color': [1, 1, 1],
        'alpha': 1
    }
    tablo_layout = AnchorLayout()

    def automatic_size(self):
        self.set_width(Window.width - 100)
        self.set_height(Window.height - ((Window.height / 4) * 2))

    def set_pos_x(self, pos_x):
        self.tablo['pos_x'] = pos_x

    def set_pos_y(self, pos_y):
        self.tablo['pos_y'] = pos_y

    def set_width(self, width):
        self.tablo['width'] = width

    def set_height(self, height):
        self.tablo['height'] = height

    def set_alpha(self, alpha):
        self.tablo['alpha'] = alpha

    def get_tablo_coordinate(self):
        return [self.tablo['pos_x'], self.tablo['pos_y']]

    def get_tablo_size(self):
        return [self.tablo['width'], self.tablo['height']]

    def set_tablo_canvas(self):
        can = Canvas()

        with can:
            Color(
                self.tablo['color'][0],
                self.tablo['color'][1],
                self.tablo['color'][2],
                self.tablo['alpha']
            )

            Rectangle(
                pos=(self.tablo['pos_x'], self.tablo['pos_y']),
                size=(self.tablo['width'], self.tablo['height'])
            )
        self.tablo_layout.canvas.add(can)

    def get_tablo_layout(self):
        self.set_tablo_canvas()
        return self.tablo_layout

    def get_center_point(self):
        return [(self.tablo['width'] / 2) + self.tablo['pos_x'], (self.tablo['height'] / 2) + self.tablo['pos_y']]


# экран создания нового окна
class CreateNewWindow(Screen):
    # создаем обьекты табло и окна
    tablo = TabloObject()
    window = WindowObject()

    create_window_layout = ColorBoxLayout(orientation='vertical')
    tablo_layout = ColorAnchorLayout()
    window_layout = FloatLayout()
    parametrs_layout = FloatLayout()
    button_layout = FloatLayout()


    # событие при первом открытии
    def on_enter(self, *args):
        # проверяем создается окно в первый раз или уже было создано
        if self.window.check == 0:
            self.window.check = 1

            self.add_all_layout()

            # задаем изначальные размеры окна тестовый вариант
            self.window.set_width(600 / 2)
            self.window.set_height(400 / 2)
            # устанавливаем цвет у табло
            self.tablo.set_color([165, 165, 165])
        # установка правильной позиции окна относительно табло
        self.set_position_window()
        # заполнение начальной модели окна
        self.fill_empty_window()
        self.window.sorted_parametrs_with_id()
        self.draw_window(self.window)
        #print(self.window.get_windows())




    def add_all_layout(self):
        self.create_window_layout.clear_widgets()
        self.create_window_layout.add_widget(self.tablo_layout)
        self.create_window_layout.add_widget(self.window_layout)
        self.create_window_layout.add_widget(self.parametrs_layout)
        self.create_window_layout.add_widget(self.button_layout)

        self.add_widget(self.create_window_layout)

    def fill_empty_window(self):
        if not self.window.window[1]:
            self.window.window[2].append(self.window.window[0])
            self.window.add_section()
            #self.window.add_section(2, orientation='vertical')
            #self.window.add_section(1, orientation='horizontal')
            self.window.set_position_parametrs_zero_cords()

    def set_position_window(self):
        tablo_center_point = self.tablo.get_center_point()
        window_size = self.window.get_size()

        window_position = [
            tablo_center_point[0] - (window_size[0] / 2),
            tablo_center_point[1] - (window_size[1] / 2)
        ]

        self.window.set_position(window_position)

    def draw_window(self, window_object):
        def draw_tablo():
            self.tablo_layout.clear_widgets()
            self.tablo_layout.add_widget(self.tablo.get_tablo_layout())

        def draw_rec(p=[], s=[], c=[175, 175, 175], linebold=1, tick=0, alpha=1, after=False):
            self.window_layer = FloatLayout()
            self.window_layout.add_widget(self.window_layer)
            p = p[:]
            s = s[:]
            p[0], p[1] = p[0] + tick, p[1] + tick
            s[0], s[1] = s[0] - (tick * 2), s[1] - (tick * 2)
            #c = color_convector(color=c)
            if after:
                with self.window_layer.canvas.after:
                    #Color(c[0], c[1], c[2], alpha)
                    Rectangle(
                        pos=(p[0], p[1]),
                        size=(s[0], s[1])
                    )
                    Color(0, 0, 0, 1)
                    Line(
                        rectangle=(
                            p[0],
                            p[1],
                            s[0],
                            s[1]
                        ),
                        width=linebold
                    )
            else:
                with self.window_layer.canvas:
                    Color(c[0], c[1], c[2], alpha)
                    Rectangle(
                        pos=(p[0], p[1]),
                        size=(s[0], s[1])
                    )
                    Color(0, 0, 0, 1)
                    Line(
                        rectangle=(
                            p[0],
                            p[1],
                            s[0],
                            s[1]
                        ),
                        width=linebold
                    )

        def draw_windows(window_parametrs=[]):
            if not window_parametrs:
                window_parametrs = self.window.window[2]
            glaw_win_pos = self.window.get_pos()
            #print(f'glaw win pos: {glaw_win_pos}')
            for i, window in enumerate(window_parametrs):
                #Проверка на то что id != 0, потому что координаты рамки не обнуляются
                if window['id'] != 0:
                    #Добавление коррдинат рамки к кординациооной системе окон
                    pos = [window['pos_x'] + glaw_win_pos[0], window['pos_y'] + glaw_win_pos[1]]
                    size = [window['width'], window['height']]
                else:
                    pos = [window['pos_x'], window['pos_y']]
                    size = [window['width'], window['height']]
                # проверка есть сколько обьектов находится внутри рамки, если < 2 то значит это стекло
                if len(self.window.find_subarray_with_id(window['id'])) < 2:
                    draw_rec(pos, size, linebold=1, c=[122, 200, 251], tick=0, after=True)
                else:
                    draw_rec(pos, size, linebold=1, c=[200, 200, 200])

        def draw_parametrs_and_button(window_parametrs):
            window_glass = []

            def draw_parametrs(pos_x, pos_y, width, height):
                line_width = 2
                line_y = pos_y + height / 3
                with self.parametrs_layout.canvas:
                    Color(1, 0, 0, 1)
                    Line(points=[pos_x, line_y, pos_x + width, line_y], width=line_width)

                    label = Label(text=f'{width}mm ',
                                  pos=(pos_x + width / 2 - 50, line_y - 60),
                                  size_hint=(None, None),
                                  color=[0, 0, 0, 1],
                                  font_size=12,
                                  halign="center", valign="middle",
                                  text_size=(60, 15))
                    self.parametrs_layout.add_widget(label)

            def draw_button(pos_x, pos_y, width, height, button_parametrs):
                size = [25, 25]
                btn_top = Button(text="+",
                                 pos=(pos_x + width / 2 - 12.5, pos_y + height - 30),
                                 size=size,
                                 size_hint=(None, None))
                btn_top.bind(on_press=lambda btn, p=button_parametrs: draw_add_new_section(p, 'vertical'))
                btn_right = Button(text="+",
                                   pos=(pos_x + width - 30, pos_y + height / 2 - 12.5),
                                   size=size,
                                   size_hint=(None, None))
                btn_right.bind(on_press=lambda btn, p=button_parametrs: draw_add_new_section(p, 'horizontal'))

                self.button_layout.add_widget(btn_top)
                self.button_layout.add_widget(btn_right)

            glaw_win_pos = self.window.get_pos()
            for par in window_parametrs:
                if len(self.window.find_subarray_with_id(par['id'])) < 2:
                    window_glass.append(par)
            i = 0
            for par in window_glass:
                i += 1
                x, y, w, h = par['pos_x'], par['pos_y'], par['width'], par['height']
                if par['id'] != 0:
                    x, y = x + glaw_win_pos[0], y + glaw_win_pos[1]
                draw_parametrs(x, y, w, h)
                draw_button(x, y, w, h, par)



        def draw_add_new_section(paramets, orientation):
            self.window.add_section(paramets["id"], orientation=orientation)
            draw_windows()


        windows = window_object.get_windows()

        window_pos = window_object.get_pos()
        window_size = window_object.get_size()
        line_bold = 1.1
        wall_tick = window_object.wall_tick

        self.tablo.automatic_size()
        draw_tablo()
        draw_rec(window_pos, window_size, [230, 230, 230], line_bold, -30)
        draw_rec(self.window.get_pos(), self.window.get_size())
        if len(windows) <= 1:
            draw_rec(window_pos, window_size, [175, 175, 175], line_bold, wall_tick)
        else:
            draw_windows(window_object.window[2])

        draw_parametrs_and_button(window_object.window[2])