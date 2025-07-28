from kivymd.uix.screen import MDScreen
from app.widgets.table_manager import TableManager
import logging

class TableScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = TableManager(self)
        self.manager.fill_table([
            (1, "Дерево", 20),
            (2, "Металл", 15),
            (3, "Стекло", 30),
            (4, "Пластик", 25),
            (5, "Камень", 10),
        ])
        self.print_table_data()

    def print_table_data(self):
        table_data = self.manager.get_table_data()
        logging.info("Текущие данные таблицы:")
        for row in table_data:
            logging.info(row)
