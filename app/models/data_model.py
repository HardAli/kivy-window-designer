from collections import defaultdict

class DataModel:
    def __init__(self):
        self.data = defaultdict(lambda: ["", "", "", ""])

    def fill_data(self, data_list):
        self.data.clear()
        for i, (num, name, qty) in enumerate(data_list):
            self.data[i] = [str(num), name, str(qty), "Выбрать"]

    def update_value(self, row_index, column_index, value):
        self.data[row_index][column_index] = value

    def get_data(self):
        return [row[:3] for row in self.data.values()]
