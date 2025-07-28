from kivy.uix.spinner import SpinnerOption


class CustomSpinnerOption(SpinnerOption):
    """ Кастомные кнопки выпадающего списка """

    def __init__(self, font_size=20, color=(0.5, 0.5, 0.5, 1), spinner_background_color=(0.2, 0.2, 0.2, 1),
                 **kwargs):
        super().__init__(**kwargs)
        self.font_size = f'{font_size}sp'
        self.color = color
        self.background_normal = ''
        self.background_color = spinner_background_color