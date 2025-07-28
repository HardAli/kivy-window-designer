from kivy.metrics import sp
from kivy.uix.button import Button
from kivy.graphics import Line, Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from enum import Enum

from spineroptions import CustomSpinnerOption
from app.popups.context_menu_popup import ContextMenu


class CellType(str, Enum):
    TEXT = 'text'
    INPUT = 'input'
    DROPDOWN = 'dropdown'
    CONTEXT_MENU = 'context_menu'
    HEADER = 'header'


class TableCell(BoxLayout):
    def __init__(self, cell_type='text', cell_content=None, l_font_size=10, bacgrond_c=(0.9, 0.9, 0.9, 1),
                 cell_text='', context_menu_header='', input_hint_text='', line_width=1, **kwargs):
        super().__init__(**kwargs)
        self.line_width = line_width
        self.cell_type = cell_type
        with self.canvas.before:
            Color(*bacgrond_c)
            self.background_rect = Rectangle(size=self.size, pos=self.pos)

        with self.canvas.after:
            Color(0, 0, 0, 1)
            self.border = Line(rectangle=[self.x, self.y, self.width, self.height], width=self.line_width)

        if self.cell_type == CellType.TEXT:
            self.cell_text = cell_text
            self.widget = Label(text=self.cell_text, font_size=f'{l_font_size}sp', color=(0, 0, 0, 1),
                                halign='center', text_size=self.size, valign='center')
        elif self.cell_type == CellType.INPUT:
            self.input_hint_text = input_hint_text
            self.widget = TextInput(font_size=f'{l_font_size}sp',
                                    hint_text=self.input_hint_text)
        elif self.cell_type == CellType.DROPDOWN:
            self.cell_content = cell_content if cell_content else ['Пусто']
            self.widget = Spinner(text=str(self.cell_content[0]), values=self.cell_content, halign='center',
                                  option_cls=CustomSpinnerOption, font_size=f'{l_font_size}sp', valign='center')
        elif self.cell_type == CellType.CONTEXT_MENU:
            self.cell_content = cell_content if cell_content else ['Пусто']
            self.context_menu_header = context_menu_header if context_menu_header else 'Пусто'
            self.widget = Button(text=self.cell_content[0], font_size=f'{l_font_size}sp',
                                 halign='center', valign='center')
            self.widget.bind(on_release=lambda btn, opt=self.cell_content, title=self.context_menu_header:
            self.show_context_menu(btn, opt, title))
        elif self.cell_type == CellType.HEADER:
            self.widget = Label(text=cell_text, font_size=sp(l_font_size + 5), bold=True, halign='center',
                                valign='middle', color=(0, 0, 0, 1))
        else:
            self.widget = Label(text=f'Error + {self.cell_type}', font_size=f'{l_font_size}sp',
                                halign='center', text_size=self.size)

        self.add_widget(self.widget)

        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.border.rectangle = [self.x, self.y, self.width, self.height]

        self.background_rect.pos = self.pos
        self.background_rect.size = self.size

        self.widget.pos = (self.x, self.y)
        self.widget.size = (self.width, self.height)
        if hasattr(self.widget, 'text_size'):
            self.widget.text_size = self.size

    def show_context_menu(self, button, option, title='Выберите:'):
        """ Показывает меню выбора для кнопки"""
        menu = ContextMenu(button=button, options=option, title=title)
        menu.open()


def convert_data_to_table_rows(data_matrix, cell_type='text'):
    return [
        [{'cell_type': cell_type, 'cell_text': str(cell)} for cell in row]
        for row in data_matrix
    ]


class Table(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.cells = {}
        self.row_layouts = []
        self.row_count = 0
        self.header_height = 40
        self.row_height = 40
        self.column_count = 0

    def add_header(self, header_titles):
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.header_height)

        for col_index, title in enumerate(header_titles):
            cell = TableCell(cell_type=CellType.HEADER, cell_text=title, line_width=1.3)
            cell.widget.bold = True  # Сделать шрифт жирным
            header_layout.add_widget(cell)
            self.cells[(-1, col_index)] = cell  # Сохраняем в ячейках заголовок с индексом строки = -1

        self.row_layouts.insert(0, header_layout)
        self.clear_widgets()
        for layout in self.row_layouts:
            self.add_widget(layout)

        self.column_count = len(header_titles)

    def add_row(self, cell_data_list):
        row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.row_height)
        row_index = self.row_count

        for col_index, cell_data in enumerate(cell_data_list):
            cell = TableCell(**cell_data)
            row_layout.add_widget(cell)
            self.cells[(row_index, col_index)] = cell

        self.column_count = max(self.column_count, len(cell_data_list))
        self.row_layouts.append(row_layout)
        self.add_widget(row_layout)

        self.row_count += 1
        self.update_table_height()

    def delete_row(self, row_index):
        if row_index >= self.row_count:
            return

        row_layout = self.row_layouts.pop(row_index)
        self.remove_widget(row_layout)

        keys_to_delete = [key for key in self.cells if key[0] == row_index]
        for key in keys_to_delete:
            del self.cells[key]

        updated_cells = {}
        for (r, c), cell in self.cells.items():
            if r > row_index:
                updated_cells[(r - 1, c)] = cell
            else:
                updated_cells[(r, c)] = cell

        self.cells = updated_cells
        self.row_count -= 1
        self.update_table_height()

    def insert_row(self, row_index, cell_data_list):
        if row_index > self.row_count:
            row_index = self.row_count

        row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.row_height)

        for col_index, cell_data in enumerate(cell_data_list):
            cell = TableCell(**cell_data)
            row_layout.add_widget(cell)
            self.cells[(row_index, col_index)] = cell

        new_cells = {}
        for (r, c), cell in self.cells.items():
            if r >= row_index:
                new_cells[(r + 1, c)] = cell
            else:
                new_cells[(r, c)] = cell

        self.cells = new_cells
        self.row_layouts.insert(row_index, row_layout)

        self.clear_widgets()
        for layout in self.row_layouts:
            self.add_widget(layout)

        self.row_count += 1
        self.update_table_height()

    def update_table_height(self):
        self.height = self.header_height + self.row_count * self.row_height

    def fill_table(self, rows_data):
        """
        Полностью заполняет таблицу новыми строками.
        :param rows_data: список строк, где каждая строка — список словарей (ячейки)
        """
        # Очистим текущие строки
        for layout in self.row_layouts:
            self.remove_widget(layout)
        self.row_layouts.clear()
        self.cells = {key: val for key, val in self.cells.items() if key[0] == -1}  # Сохраняем только заголовки

        self.row_count = 0

        # Добавим новые строки
        for row in rows_data:
            self.add_row(row)

    def get_table_data(self):
        data = []
        for row in range(self.row_count):
            row_data = []
            for col in range(self.column_count):
                cell = self.cells.get((row, col))
                if cell:
                    if hasattr(cell.widget, 'text'):
                        row_data.append(cell.widget.text)
                    else:
                        row_data.append(None)
                else:
                    row_data.append(None)
            data.append(row_data)
        return data


class TableCellFactory:
    """
      Фабрика конфигураций для ячеек таблицы.
      Используется для генерации словарей, совместимых с TableCell.
    """

    @staticmethod
    def text(value='') -> dict:
        return {'cell_type': CellType.TEXT, 'cell_text': f'{value}'}

    @staticmethod
    def input(hint) -> dict:
        return {'cell_type': CellType.INPUT, 'input_hint_text': f'{hint}'}

    @staticmethod
    def dropdown(options: list[str]) -> dict:
        return {'cell_type': CellType.DROPDOWN, 'cell_content': options}

    @staticmethod
    def context_menu(options: list[str], title: str = 'Выберите:') -> dict:
        return {'cell_type': CellType.CONTEXT_MENU, 'cell_content': options, 'context_menu_header': title}

    @staticmethod
    def header(text: str) -> dict:
        return {'cell_type': CellType.HEADER, 'cell_text': text}


class ScrollableTableContainer(ScrollView, TableCellFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = Table()
        self.add_widget(self.table)

    def add_row(self, cell_data_list):
        self.table.add_row(cell_data_list)

    def fill_table(self, rows_data):
        for row in rows_data:
            self.add_row(row)

    def get_data(self):
        return self.table.get_table_data()





'''class TestApp(App):
    def build(self):

        root = ColorAnchorLayout(anchor_x='center', anchor_y='center')
        root2 = ColorAnchorLayout(anchor_x='center', anchor_y='center')
        root2.set_color(200, 0, 0)
        root2.size_hint = (0.5, 0.5)
        root.add_widget(root2)

        self.scrollable_table = ScrollableTableContainer()

        root2.add_widget(self.scrollable_table)

        self.scrollable_table.table.add_header(['Название', 'Описание', 'Выбор', 'Список'])

        # Добавляем несколько строк

        names = ['нога', 'рука', 'футболка', 'яхта', 'малыш', 'черешня', 'окно', 'бинт', 'болт', 'yes']

        for i in range(25):
            self.scrollable_table.add_row([
                {'cell_type': 'text', 'cell_text': names[randint(0, 9)]},
                {'cell_type': 'input'},
                {'cell_type': 'context_menu', 'cell_content': ['я', 'ты', 'мы']},
                {'cell_type': 'dropdown', 'cell_content': ['я', 'великий', 'король']}
            ])

        return root

if __name__ == '__main__':
    TestApp().run()'''