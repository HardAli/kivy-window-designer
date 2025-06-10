from kivy.core.window import Window
from colorlayauts import ColorBoxLayout
from kivy.clock import Clock

SPACING = 10


class WindowLayout(ColorBoxLayout):
    def __init__(self, orientation='horizontal', spacing=10, padding=SPACING,
                 background_color=(0.9, 0.9, 0.9, 1), orig_width=2000, orig_height=1000, scale_factor=0.7, **kwargs):
        super().__init__(**kwargs)
        self.orientation = orientation
        self.spacing = spacing
        self.padding = padding
        self.set_color(*background_color)
        self.scale_factor = scale_factor
        self.orig_width = orig_width
        self.orig_height = orig_height
        self.size_hint = (None, None)
        self.bind(size=self.update_scale)
        Window.bind(on_resize=self.on_window_resize)
        print('afssfdad')

        Clock.schedule_once(self.update_scale, 0)

    def update_scale(self, *args):
        if self.orig_height == 0 or self.orig_width == 0:
            return
        if not self.parent:
            return

        box_w, box_h = self.parent.width, self.parent.height

        scale_w = box_w / self.orig_width
        scale_h = box_h / self.orig_height
        scale = min(scale_w, scale_h)

        new_w = self.orig_width * scale * self.scale_factor
        new_h = self.orig_height * scale * self.scale_factor

        if abs(self.width - new_w) > 10 or abs(self.height - new_h) > 10:
            self.size = (new_w, new_h)

    def on_window_resize(self, *args):
        Clock.schedule_once(self.update_scale, 0)

    def set_size(self, width: float, height: float):
        self.orig_width = width
        self.orig_height = height
        Clock.schedule_once(self.update_scale, 0)

    def update_size(
            self,
            upd_size: list[float] | tuple[float, float] | None = None,
            upd_width: float = 0,
            upd_height: float = 0
    ) -> None:
        """
        Обновляет размеры объекта (логические orig_width / orig_height).

        :param upd_size: список или кортеж [ширина, высота]
        :param upd_width: новая ширина (перезаписывает upd_size[0])
        :param upd_height: новая высота (перезаписывает upd_size[1])
        """

        if upd_size and len(upd_size) == 2:
            if upd_size[0]:
                self.orig_width = abs(upd_size[0])
            if upd_size[1]:
                self.orig_height = abs(upd_size[1])

        if upd_width:
            self.orig_width = abs(upd_width)

        if upd_height:
            self.orig_height = abs(upd_height)

        Clock.schedule_once(self.update_scale, 0)


