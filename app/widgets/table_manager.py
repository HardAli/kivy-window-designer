import logging

from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from functools import partial
from app.models.data_model import DataModel
from app.widgets.popup_manager import PopupManager

class TableManager:
    def __init__(self, screen):
        self.screen = screen
        self.model = DataModel()
        self.create_table()

    def create_table(self):
        self.data_table = MDDataTable(
            size_hint=(0.9, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            column_data=[
                ("№", dp(30)),
                ("Материал", dp(40)),
                ("Количество", dp(40)),
                ("Действие", dp(30)),
            ],
            row_data=[],
            rows_num=5,
        )
        self.data_table.bind(on_row_press=self.on_row_press)
        self.screen.add_widget(self.data_table)

    def fill_table(self, data_list):
        self.model.fill_data(data_list)
        self.update_table()

    def get_table_data(self):
        return self.model.get_data()

    def on_row_press(self, instance_table, instance_row):
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
        self.model.update_value(row_index, 1, material)
        self.update_table()
        popup.dismiss()

    def set_quantity(self, row_index, quantity, popup):
        if quantity.isdigit() and int(quantity) > 0:
            self.model.update_value(row_index, 2, quantity)
            self.update_table()
            popup.dismiss()
        else:
            logging.warning(f"Ошибка: Некорректное значение '{quantity}' для количества!")

    def update_table(self):
        self.data_table.row_data = [tuple(row) for row in self.model.data.values()]
