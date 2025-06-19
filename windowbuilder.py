from kivy.uix.widget import Widget
from models import Frame
from windowlayout import WindowLayout
from colorlayauts import ColorButtonBoxLayout
from createwinstate import CreateWinState

SPACING = 10


class WindowBuilder(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parent_frame = None
        self.main_widow_layout = WindowLayout()
        CreateWinState.main_window_layout = self.main_widow_layout
        self.main_frame = Frame(0, 900, 400, None, self.main_widow_layout, main_frame=True)
        self.frame_structure = [self.main_frame]
        self.frame_id_to_widget_map: dict[int, Widget] = {0: self.main_widow_layout}

    def update_canvas(self, *args):
        pass  # пока заглушка

    def get_frame_with_id(self, frame_id: int) -> Frame | None:
        for frame in self.frame_structure:
            if frame.frame_id == frame_id:
                return frame
        print(f"⚠ Frame ID {frame_id} not found.")
        return None

    def get_brother(self, frame_id: int = None, frame: Frame = None):
        if frame is None:
            if frame_id is not None:
                frame = self.get_frame_with_id(frame_id)
            else:
                print(f'Error WindowBuilder -> get_brother    frame_id = {frame_id}    frame = {frame}')

        if frame.main_frame:
            print(f'Это main_frame')

        parent_frame = frame.parent
        child = parent_frame.child
        brothers = child[:]
        print(f'Братья вместе со мной: {len(brothers)}')
        brothers.remove(frame)
        if len(brothers) < 1:
            print('У вас нет братьев)')
            return []
        else:
            return brothers

    def get_max_layout_id(self) -> int:
        return max(self.frame_id_to_widget_map.keys(), default=0)

    def add_frame(self, window, frame_id: int = 0, orientation_frame: str = 'horizontal'):
        self.parent_frame = self.get_frame_with_id(frame_id)
        if not self.parent_frame:
            return
        if self.parent_frame.orientation == orientation_frame and self.parent_frame.frame_id != 0:
            self.parent_frame = self.parent_frame.parent

        if self.parent_frame is not None:
            print(f'{orientation_frame},   {self.parent_frame.orientation}')

        def get_calculate_frame_size():
            manual_par = []
            if orientation_frame == 'horizontal':
                for child in self.parent_frame.child:
                    if child.manual_set_parametrs:
                        manual_par.append(child.width)

                    total_len_manual_object = 0
                    for par in manual_par:
                        total_len_manual_object += par

                    print(total_len_manual_object, 'total')

        def create_frame(clear: bool = False):
            new_id = self.get_max_layout_id() + 1
            print(f'{new_id}')
            new_layout = ColorButtonBoxLayout(orientation=orientation_frame,
                                              frame_id=new_id,
                                              window=window,
                                              spacing=SPACING)

            new_frame = Frame(new_id, 100, 100, self.parent_frame, new_layout, orientation=orientation_frame)
            self.frame_structure.append(new_frame)
            self.frame_id_to_widget_map[new_id] = new_layout

            if clear and self.parent_frame.frame_id != 0:
                self.parent_frame.layout.clear_widgets()
                self.parent_frame.layout.canvas.before.clear()

            self.parent_frame.layout.orientation = orientation_frame
            self.parent_frame.layout.add_widget(new_layout)
            self.parent_frame.child.append(new_frame)

            get_calculate_frame_size()

        if len(self.parent_frame.child) <= 1 and orientation_frame != self.parent_frame.orientation:
            create_frame(clear=True)
        create_frame()

        for i in self.frame_structure:
            print(i)




