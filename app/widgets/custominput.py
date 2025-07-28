from kivy.uix.textinput import TextInput


class CustomInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def set_readonly(self):
        self.readonly = True
        self.background_color = (0.9, 0.6, 0.6, 1)
        self.foreground_color = (0, 0, 0, 1)
        self.cursor_color = (0, 0, 0, 0)

    def set_active(self):
        self.readonly = False
        self.background_color = (1, 1, 1, 1)
        self.foreground_color = (0, 0, 0, 1)
        self.cursor_color = (0, 0, 0, 1)

    def set_not_active(self):
        self.readonly = True
        self.background_color = (0.5, 0.5, 0.5, 0.5)
        self.cursor_color = (0, 0, 0, 0.1)
