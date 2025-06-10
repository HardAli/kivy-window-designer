import logging
from functools import partial
from collections import defaultdict
from kivy.metrics import dp
from kivy.app import App
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivymd.uix.behaviors import HoverBehavior

logging.basicConfig(level=logging.INFO)


class DataModel:
    """Модель данных, хранящая информацию о материалах"""

    def __init__(self):
        self.data = defaultdict(lambda: ["", "", "", ""])

    def fill_data(self, data_list):
        """Заполняет модель данными из массива"""
        self.data.clear()
        for i, (num, name, qty) in enumerate(data_list):
            self.data[i] = [str(num), name, str(qty), "Выбрать"]

    def update_value(self, row_index, column_index, value):
        """Обновляет данные в модели"""
        self.data[row_index][column_index] = value

    def get_data(self):
        """Возвращает массив со значениями таблицы"""
        return [row[:3] for row in self.data.values()]  # Возвращаем только ID, материал, количество


class PopupManager:
    """Менеджер всплывающих окон"""

    @staticmethod
    def show_material_popup(callback):
        """Открывает Popup с выбором материала"""
        materials = ["Дерево", "Стекло", "Металл", "Пластик", "Камень"]
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        popup = Popup(title="Выберите материал", content=layout, size_hint=(0.5, 0.5))

        for mat in materials:
            btn = CustomButton(text=mat, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: callback(btn.text, popup))
            layout.add_widget(btn)

        popup.open()

    @staticmethod
    def show_quantity_popup(current_value, callback):
        """Открывает Popup для редактирования количества"""
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        popup = Popup(title="Введите количество", content=layout, size_hint=(0.5, 0.3))

        quantity_input = TextInput(text=current_value, multiline=False, size_hint_y=None, height=40)
        quantity_input.focus = True
        btn_save = CustomButton(text="Сохранить", size_hint_y=None, height=40)
        btn_save.bind(on_release=lambda x: callback(quantity_input.text, popup))

        layout.add_widget(quantity_input)
        layout.add_widget(btn_save)
        popup.open()


class CustomButton(Button, HoverBehavior):
    """Кнопка с изменяющимся цветом при наведении"""
    def on_enter(self):
        self.md_bg_color = (0, 0.7, 1, 1)  # Голубой при наведении

    def on_leave(self):
        self.md_bg_color = (0, 0.5, 1, 1)  # Обычный цвет


class TableManager:
    """Управление таблицей"""

    def __init__(self, screen):
        self.screen = screen
        self.model = DataModel()
        self.create_table()

    def create_table(self):
        """Создаёт таблицу"""
        self.data_table = MDDataTable(
            size_hint=(0.9, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            column_data=[
                ("№", dp(30)),
                ("Материал", dp(40)),
                ("Количество", dp(40)),
                ("Действие", dp(30)),
            ],
            row_data=[],  # Таблица будет заполняться динамически
            rows_num=5,
        )
        self.data_table.bind(on_row_press=self.on_row_press)
        self.screen.add_widget(self.data_table)

    def fill_table(self, data_list):
        """Заполняет таблицу переданными данными"""
        self.model.fill_data(data_list)
        self.update_table()

    def get_table_data(self):
        """Возвращает массив со значениями таблицы"""
        return self.model.get_data()

    def on_row_press(self, instance_table, instance_row):
        """Обрабатывает нажатие на строку"""
        try:
            row_index = int(instance_row.index / len(self.data_table.column_data))
            row_data = self.model.data[row_index]

            if instance_row.text == row_data[1]:
                PopupManager.show_material_popup(partial(self.set_material, row_index))
            elif instance_row.text == row_data[2]:
                PopupManager.show_quantity_popup(row_data[2], partial(self.set_quantity, row_index))

        except IndexError:
            logging.error("Ошибка: Неверный индекс строки!")

    def set_material(self, row_index, material, popup):
        """Устанавливает материал и закрывает popup"""
        self.model.update_value(row_index, 1, material)
        self.update_table()
        popup.dismiss()

    def set_quantity(self, row_index, quantity, popup):
        """Обновляет количество и закрывает popup"""
        if quantity.isdigit() and int(quantity) > 0:
            self.model.update_value(row_index, 2, quantity)
            self.update_table()
            popup.dismiss()
        else:
            logging.warning(f"Ошибка: Некорректное значение '{quantity}' для количества!")

    def update_table(self):
        """Обновляет данные в `MDDataTable`"""
        self.data_table.row_data = [tuple(row) for row in self.model.data.values()]


class TableScreen(MDScreen):
    """Основной экран с таблицей"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = TableManager(self)

        # Пример данных
        example_data = [
            (1, "Дерево", 20),
            (2, "Металл", 15),
            (3, "Стекло", 30),
            (4, "Пластик", 25),
            (5, "Камень", 10),
        ]

        # Заполняем таблицу данными
        self.manager.fill_table(example_data)

        # Вывод данных после загрузки
        self.print_table_data()

    def print_table_data(self):
        """Пример получения данных из таблицы"""
        table_data = self.manager.get_table_data()
        logging.info("Текущие данные таблицы:")
        for row in table_data:
            logging.info(row)


'''class TableApp(MDApp):
    """Главное приложение"""
    def build(self):
        return TableScreen()


if __name__ == "__main__":
    TableApp().run()
'''