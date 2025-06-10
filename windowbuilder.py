from kivy.uix.widget import Widget
from models import Frame
from windowlayout import WindowLayout
from colorlayauts import ColorButtonBoxLayout
from utils import get_rand_color

SPACING = 10


class WindowBuilder(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_box_layout = WindowLayout()
        self.main_frame = Frame(0, 900, 400, None, self.main_box_layout)
        self.frame_structure = [self.main_frame]
        self.frame_id_to_widget_map: dict[int, Widget] = {0: self.main_box_layout}

    def update_canvas(self, *args):
        pass  # пока заглушка

    def get_frame_with_id(self, frame_id: int) -> Frame | None:
        for frame in self.frame_structure:
            if frame.frame_id == frame_id:
                return frame
        print(f"⚠ Frame ID {frame_id} not found.")
        return None

    def get_max_layout_id(self) -> int:
        return max(self.frame_id_to_widget_map.keys(), default=0)

    def add_frame(self, window, frame_id: int = 0, orientation_frame: str = 'horizontal'):
        parent_frame = self.get_frame_with_id(frame_id)
        if not parent_frame:
            return

        def create_frame(clear: bool = False):
            new_id = self.get_max_layout_id() + 1
            new_layout = ColorButtonBoxLayout(orientation=orientation_frame,
                                              frame_id=new_id,
                                              window=window,
                                              spacing=SPACING)

            new_color = get_rand_color()
            new_layout.set_color(*new_color)

            new_frame = Frame(new_id, 0, 0, parent_frame, new_layout)
            self.frame_structure.append(new_frame)
            self.frame_id_to_widget_map[new_id] = new_layout

            if clear and parent_frame.frame_id != 0:
                parent_frame.layout.clear_widgets()
                parent_frame.layout.canvas.before.clear()

            parent_frame.layout.orientation = orientation_frame
            parent_frame.layout.add_widget(new_layout)
            parent_frame.child.append(new_frame)

        if len(parent_frame.child) <= 1:
            create_frame(clear=True)
        create_frame()
