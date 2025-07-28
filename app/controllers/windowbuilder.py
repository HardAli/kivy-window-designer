from kivy.uix.widget import Widget
from kivy.core.window import Window
from models_open_window import Frame
from app.widgets.windowlayout import WindowLayout
from app.widgets.windowsection import WindowSection
from app.state.createwinstate import CreateWinState, SPACING
from app.widgets.arrowwidget import ArrowWidget
from app.popups.popup_resize import FrameResizePopup


class WindowBuilder(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.izm_orient = None
        self.parent_frame = None
        self.main_widow_layout = WindowLayout()
        self.new_frame = None
        CreateWinState.main_window_layout = self.main_widow_layout
        self.main_frame = Frame(
            frame_id=0,
            width=2000,
            height=1000,
            parent=None,
            layout=self.main_widow_layout,
            main_frame=True
        )
        self.frame_structure = [self.main_frame]
        self.frame_id_to_widget_map: dict[int, Widget] = {0: self.main_widow_layout}

        self.selected_frames = []
        self.ctrl_down = False
        Window.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        if 'ctrl' in modifiers:
            self.ctrl_down = True
        if key == 13:  # Enter
            if self.ctrl_down and self.selected_frames:
                popup = FrameResizePopup(self.selected_frames)
                popup.open()
            else:
                self._clear_selection()

    def _on_key_up(self, *args):
        self.ctrl_down = False

    def toggle_select_frame(self, frame):
        if not self.ctrl_down:
            return

        if not self.selected_frames:
            self.selected_frames.append(frame)
            frame.highlight()
        else:
            # Проверка: общий родитель
            common_parent = self.selected_frames[0].parent
            if frame.parent != common_parent:
                return

            if frame in self.selected_frames:
                self.selected_frames.remove(frame)
                frame.un_highlight()
            else:
                self.selected_frames.append(frame)
                frame.highlight()

    def _clear_selection(self):
        for f in self.selected_frames:
            f.un_highlight()
        self.selected_frames.clear()

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
        brothers.remove(frame)
        if len(brothers) < 1:
            return []
        else:
            return brothers

    def get_max_layout_id(self) -> int:
        return max(self.frame_id_to_widget_map.keys(), default=0)

    def delete_frame(self, frame_id: int):
        frame = self.get_frame_with_id(frame_id)
        if not frame:
            print(f"⚠ Невозможно удалить: фрейм с ID {frame_id} не найден.")
            return

        if frame.main_frame:
            print("❌ Нельзя удалить главный фрейм (main_frame).")
            return

        # 🔁 Рекурсивно удаляем всех детей
        for child in frame.child[:]:  # создаём копию, чтобы не портить список во время итерации
            self.delete_frame(child.frame_id)

        # Удаляем себя из родителя
        parent = frame.parent
        if parent and frame in parent.child:
            parent.child.remove(frame)

        # Удаляем виджет layout
        if frame.layout and parent and frame.layout in parent.layout.children:
            parent.layout.remove_widget(frame.layout)

        # Удаляем из мапы
        if frame_id in self.frame_id_to_widget_map:
            del self.frame_id_to_widget_map[frame_id]

        # Удаляем из структуры
        if frame in self.frame_structure:
            self.frame_structure.remove(frame)

        print(f"✅ Удалён фрейм {frame_id}")

        # Логика объединения при одном оставшемся ребёнке
        if parent and len(parent.child) == 1 and not parent.main_frame:
            print('что-то странное')
            parent_orientation = parent.orientation
            parent_frame_id = parent.frame_id

            self.add_frame(self, orientation_frame=parent_orientation, frame_id=parent_frame_id, izm_orient=False)
            self.delete_frame(parent.frame_id)

        # Вывод актуальной структуры
        for f in self.frame_structure:
            print(f, 'frame_structure')

        # Пересчёт только для main_frame
        if self.main_frame:
            self.main_frame.recalculate_window()


    def add_frame(self, window, frame_id: int = 0, orientation_frame: str = 'horizontal', izm_orient=True):
        check_window_changing = False
        self.parent_frame = self.get_frame_with_id(frame_id)
        if not self.parent_frame:
            return
        if self.parent_frame.orientation == orientation_frame and self.parent_frame.frame_id != 0:
            check_window_changing = True

        if check_window_changing:
            self.parent_frame = self.parent_frame.parent

        if self.parent_frame is not None:
            print(f'{orientation_frame},   {self.parent_frame.orientation}')

        def recalculate_frame_size():
            if self.parent_frame.frame_id == 0 and len(self.parent_frame.child) == 0:
                return None

            manual_brothers = []
            not_manual_brothers = self.parent_frame.child[:]
            total_len_manual_object = 0

            if orientation_frame == 'horizontal':
                for child in self.parent_frame.child:
                    if child.manual_set_parametr_w:
                        total_len_manual_object += child.width
                        manual_brothers.append(child)

                for manual_brother in manual_brothers:
                    if manual_brother in not_manual_brothers:
                        not_manual_brothers.remove(manual_brother)

                num_brothers = len(not_manual_brothers) or 1
                width = (self.parent_frame.width - total_len_manual_object) / num_brothers
                height = self.parent_frame.height

            elif orientation_frame == 'vertical':
                for child in self.parent_frame.child:
                    if child.manual_set_parametr_h:
                        total_len_manual_object += child.height
                        manual_brothers.append(child)

                for manual_brother in manual_brothers:
                    if manual_brother in not_manual_brothers:
                        not_manual_brothers.remove(manual_brother)

                num_brothers = len(not_manual_brothers) or 1
                width = self.parent_frame.width
                height = (self.parent_frame.height - total_len_manual_object) / num_brothers

            for not_manual_brother in not_manual_brothers:
                not_manual_brother.update_height(height)
                not_manual_brother.update_width(width)

        def create_frame(clear: bool = False, izm_orient=True):
            new_id = self.get_max_layout_id() + 1
            #print(f'{new_id}')
            new_layout = WindowSection(orientation=orientation_frame,
                                              frame_id=new_id,
                                              window=window,
                                              spacing=SPACING)
            self.new_frame = Frame(frame_id=new_id,
                                   width=100,
                                   height=100,
                                   parent=self.parent_frame,
                                   layout=new_layout,
                                   orientation=orientation_frame)
            new_arrow_widget = ArrowWidget()
            new_layout.overlay.add_widget(new_arrow_widget, index=len(new_layout.children) + 1)
            self.new_frame.arrow_widget = new_arrow_widget


            self.frame_structure.append(self.new_frame)
            self.frame_id_to_widget_map[new_id] = new_layout

            if clear and self.parent_frame.frame_id != 0:
                self.parent_frame.layout.clear_widgets()
                self.parent_frame.layout.show_canvas = False

            # Устанавливаем ориентацию layout у родительского фрейма
            self.parent_frame.layout.orientation = orientation_frame

            # Получаем layout нужного фрейма
            target_layout = self.get_frame_with_id(frame_id=frame_id).layout

            # Вставляем новый layout в нужную позицию или в конец
            if check_window_changing and target_layout in self.parent_frame.layout.children:
                index = self.parent_frame.layout.children.index(target_layout)
                self.parent_frame.layout.add_widget(new_layout, index=index)
            else:
                self.parent_frame.layout.add_widget(new_layout)

            # Добавляем новый фрейм в список детей родителя
            self.parent_frame.child.append(self.new_frame)

        if len(self.parent_frame.child) <= 1 and orientation_frame != self.parent_frame.orientation:
            create_frame(clear=True, izm_orient=False)
        create_frame(izm_orient=False)

        recalculate_frame_size()
        self.new_frame.update_layouts_size_hint()

        for i in self.frame_structure:
            print(i)
