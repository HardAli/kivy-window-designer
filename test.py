from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

def show_confirm_popup(on_corfirm):
    anch = AnchorLayout(anchor_x='center', anchor_y='center')
    content = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 0.5))
    anch.add_widget(content)
    content.add_widget(Label(text='Да ты просто урод)'))

    buttons = BoxLayout(orientation='horizontal', height='40dp', spacing=5)
    yes_btn = Button(text='Да я урод')
    no_btn = Button(text='нет я урод')
    buttons.add_widget(yes_btn)
    buttons.add_widget(no_btn)

    content.add_widget(buttons)

    popup = Popup(
        title='Подтверждение Урода',
        content=anch,
        size_hint=(0.5, 0.5),
        auto_dismiss=False
    )
    yes_btn.bind(on_release=lambda *args: (on_corfirm(), popup.dismiss()))
    no_btn.bind(on_release=popup.dismiss)
    popup.open()


class TestApp(App):
    def build(self):
        btn = Button(text='Пройди опрос')

        def on_confirm():
            print('Подтверждено!')

        btn.bind(on_release=lambda *a: show_confirm_popup(on_confirm))

        return btn


if __name__ == '__main__':
    TestApp().run()