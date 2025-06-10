from kivy.uix.screenmanager import Screen
from colorlayauts import ColorBoxLayout, ColorAnchorLayout
from slideouts import SlideOutsLayoutWindowModels
from AttachedOverlays import WindowLinesEvent as lineEvent
from Lines import LineIntInput
from tables import ScrollableTableContainer
from windowbuilder import WindowBuilder


class GlassCut(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.over_tablo = None
        self.tablo_anchor_layout = None
        self.main_layout = None
        self.my_window = None
        self._initialized = False

    def on_pre_enter(self, *args):
        if self._initialized:
            return

        self.my_window = WindowBuilder()

        self.main_layout = ColorBoxLayout(orientation='vertical')
        self.main_layout.set_color(0.8, 0.8, 0.8)

        self.tablo_anchor_layout = ColorAnchorLayout(anchor_x='center', anchor_y='center')
        self.tablo_anchor_layout.set_color(0.7, 0.7, 0.7)

        self.add_widget(self.main_layout)
        self.add_widget(SlideOutsLayoutWindowModels(self.main_layout))

        self.my_window.main_box_layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.over_tablo = lineEvent(
            target_widget=self.my_window.main_box_layout,
            b_el=LineIntInput(is_vertical=False),
            r_el=LineIntInput(is_vertical=True)
        )
        self.tablo_anchor_layout.add_widget(self.over_tablo)
        self.main_layout.add_widget(self.tablo_anchor_layout)

        self._add_table()

        self.my_window.add_frame(window=self.my_window)

        self._initialized = True

    def _add_table(self):
        self.my_table = ScrollableTableContainer()
        headers = ["ID", "Имя", "Возраст", "Город", "Статус", "ячейка 1", "ячейка 2"]
        self.my_table.table.add_header(headers)

        city_options = ['Almata', 'Astana', 'Karaganda', 'Taldykorgan', 'Jarkent']
        status_options = ['Готов', 'Не готов']

        data = []
        tb = self.my_table
        for i in range(10):
            row = [
                tb.text(i),
                tb.input('name'),
                tb.input('age'),
                tb.context_menu(city_options),
                tb.dropdown(status_options),
                tb.text(),
                tb.text()
            ]
            data.append(row)

        self.my_table.fill_table(data)
        self.main_layout.add_widget(self.my_table)
