from kivy.core.window import Window
from colorlayauts import ColorBoxLayout
from kivy.clock import Clock
from createwinstate import SPACING


class WindowLayout(ColorBoxLayout):
    def __init__(self, orientation='horizontal', spacing=SPACING, padding=SPACING,
                 background_color=(0.9, 0.9, 0.9, 1), orig_width=2000, orig_height=1000, scale_factor=0.7, **kwargs):
        super().__init__(**kwargs)
        self.orientation = orientation
        self.spacing = spacing
        self.padding = padding
        self.set_color(*background_color)
        self.background_color = background_color
        self.scale_factor = scale_factor
        self.orig_width = orig_width
        self.orig_height = orig_height
        self.size_hint = (None, None)
        self._updating = False

        self.bind(pos=self.update_scale)
        self.bind(size=self.update_scale)
        Window.bind(on_resize=self.on_window_resize)
        Clock.schedule_once(self.update_scale, 0)

    def get_update_scale(self, orig_parametr):
        if not self.parent or self.orig_width == 0 or self.orig_height == 0:
            return None

        box_w, box_h = self.parent.width, self.parent.height
        scale = min(box_w / self.orig_width, box_h / self.orig_height)
        return orig_parametr * scale * self.scale_factor

    def update_scale(self, *args):
        if self._updating:
            return
        self._updating = True

        new_w = self.get_update_scale(self.orig_width)
        new_h = self.get_update_scale(self.orig_height)

        if new_w is not None and new_h is not None:
            if abs(self.width - new_w) > 3 or abs(self.height - new_h) > 3:
                self.size = (new_w, new_h)

        self._updating = False

    def on_window_resize(self, *args):
        Clock.schedule_once(self.update_scale, 0)

    def set_size(self, width: float, height: float):
        self.orig_width = width
        self.orig_height = height
        Clock.schedule_once(self.update_scale, 0)

    def update_size(self, upd_size=None, upd_width=0, upd_height=0) -> None:
        if upd_size and len(upd_size) == 2:
            if upd_size[0] is not None:
                self.orig_width = abs(upd_size[0])
            if upd_size[1] is not None:
                self.orig_height = abs(upd_size[1])

        if upd_width:
            self.orig_width = abs(upd_width)

        if upd_height:
            self.orig_height = abs(upd_height)

        Clock.schedule_once(self.update_scale, 0)
