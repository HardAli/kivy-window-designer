from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle


class ContextMenu(Popup):
    """ Всплывающее меню с выбором значения (как выпадающий список) """
    def __init__(self, button, options, **kwargs):
        super().__init__(title="Выберите значение", size_hint=(None, None), size=(200, 250), **kwargs)
        self.button = button

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        scroll = ScrollView()
        button_layout = BoxLayout(orientation="vertical", size_hint_y=None)
        button_layout.bind(minimum_height=button_layout.setter("height"))

        for option in options:
            btn = Button(text=option, size_hint_y=None, height=40)
            btn.bind(on_release=self.select_option)
            button_layout.add_widget(btn)

        scroll.add_widget(button_layout)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def select_option(self, button):
        """ Устанавливает выбранное значение в кнопку и закрывает меню """
        self.button.text = button.text
        self.dismiss()


class TableWidget(BoxLayout):
    def __init__(self, columns, data, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.columns = columns
        self.data = data
        self.bg_color = (1, 1, 1, 1)

        # Белый фон
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Заголовки
        header_layout = BoxLayout(size_hint_y=None, height=40)
        with header_layout.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=header_layout.pos, size=header_layout.size)
        header_layout.bind(size=self.update_rect, pos=self.update_rect)

        for col in columns:
            label = Label(text=col[0], size_hint_x=None, width=150, bold=True, color=(0, 0, 0, 1))
            header_layout.add_widget(label)
        self.add_widget(header_layout)

        # Прокручиваемая область
        self.scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True, size_hint=(1, None), height=400)
        self.table_body = GridLayout(cols=len(columns), size_hint_y=None, row_default_height=40)
        self.table_body.bind(minimum_height=self.table_body.setter("height"))

        with self.table_body.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.table_body.pos, size=self.table_body.size)
        self.table_body.bind(size=self.update_rect, pos=self.update_rect)

        self.scroll_view.add_widget(self.table_body)
        self.add_widget(self.scroll_view)

        self.populate_table()

        # Тестируем получение данных
        print(self.get_table_data())

    def update_rect(self, *args):
        """ Обновляет размер фона при изменении окна """
        self.rect.pos = self.pos
        self.rect.size = self.size

    def populate_table(self):
        """ Заполняет таблицу виджетами по типу колонок """
        self.table_body.clear_widgets()
        for row in self.data:
            for i, cell in enumerate(row):
                col_type = self.columns[i][1]

                if col_type == "label":
                    widget = Label(text=str(cell), size_hint_x=None, width=150, color=(0, 0, 0, 1))
                elif col_type == "input":
                    widget = TextInput(text=str(cell), size_hint_x=None, width=150)
                elif col_type == "dropdown":
                    options = self.columns[i][2] if len(self.columns[i]) > 2 else []
                    widget = Spinner(text=str(cell), values=options, size_hint_x=None, width=150)
                elif col_type == "context_menu":
                    options = self.columns[i][2] if len(self.columns[i]) > 2 else []
                    widget = Button(text=str(cell) if cell else "Выбрать", size_hint_x=None, width=150)
                    widget.bind(on_release=lambda btn, opt=options: self.show_context_menu(btn, opt))
                else:
                    widget = Label(text=str(cell), size_hint_x=None, width=150, color=(0, 0, 0, 1))

                self.table_body.add_widget(widget)

    def get_table_data(self):
        """ Возвращает данные таблицы в виде списка словарей """
        data = []
        col_names = [col[0] for col in self.columns]  # Заголовки колонок
        widgets = self.table_body.children[::-1]  # Получаем виджеты в правильном порядке
        row_count = len(self.data)
        col_count = len(self.columns)

        for row_idx in range(row_count):
            row_dict = {}
            for col_idx in range(col_count):
                widget = widgets[row_idx * col_count + col_idx]
                if isinstance(widget, Label) or isinstance(widget, TextInput) or isinstance(widget, Spinner) or isinstance(widget, Button):
                    row_dict[col_names[col_idx]] = widget.text
                else:
                    row_dict[col_names[col_idx]] = None  # Кнопки без текста игнорируются
            data.append(row_dict)
        return data

    def show_context_menu(self, button, options):
        """ Показывает меню выбора для кнопки """
        menu = ContextMenu(button, options)
        menu.open()


'''class TableApp(App):
    def build(self):
        # Определение структуры колонок
        columns = [
            ("ID", "label"),
            ("Имя", "input"),
            ("Возраст", "input"),
            ("Город", "dropdown", ["Москва", "Санкт-Петербург", "Казань", "Екатеринбург"]),
            ("Статус", "context_menu", ["Активен", "Ожидание", "Заблокирован"])
        ]

        # Пример данных
        data = [
            [1, "Иван", 25, "Москва", "Активен"],
            [2, "Анна", 30, "Санкт-Петербург", "Ожидание"],
            [3, "Петр", 28, "Новосибирск", "Заблокирован"],
            [4, "Ольга", 35, "Казань", "Активен"],
            [5, "Дмитрий", 40, "Екатеринбург", "Ожидание"],
        ]
        bl = BoxLayout()
        table = TableWidget(columns, data)

        def get_dt(a):
            for data in table.get_table_data():
                print(data)

        bl.add_widget(table)
        get_data_button = Button(text='get_data', on_press=get_dt)
        bl.add_widget(get_data_button)

        return bl

'''