import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

Builder.load_file('my.kv')

class LogInWindow(Screen):
    pass
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     layout = BoxLayout(orientation='vertical')
    #     self.username_input = TextInput(text='Username')
    #     self.password_input = TextInput(text='Password', password=True)
    #     layout.add_widget(self.username_input)
    #     layout.add_widget(self.password_input)
    #     layout.add_widget(Button(text='Login', on_release=self.login))
    #     layout.add_widget(Button(text='Register', on_release=self.go_to_register))
    #     layout.add_widget(Button(text='Exit', on_release=App.get_running_app().stop))
    #     self.add_widget(layout)

    # def login(self, instance):
    #     username = self.username_input.text
    #     password = self.password_input.text

    #     if username == 'admin' and password == 'admin':
    #         self.go_to_camera(instance)

    # def go_to_camera(self, instance):
    #     self.manager.current = 'camerawindow'

    # def go_to_register(self, instance):
    #     self.manager.current = 'register'

class RegisterWindow(Screen):
    pass
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.n
    #     layout = BoxLayout(orientation='vertical')
    #     layout.add_widget(Button(text='Scan your face', on_release=self.go_to_camera))
    #     layout.add_widget(Button(text='Back', on_release=self.go_to_login))
    #     self.add_widget(layout)

    # def go_to_camera(self, instance):
    #     self.manager.current = 'camerawindow'

    # def go_to_login(self, instance):
    #     self.manager.current = 'login'
        

class CameraWindow(Screen):
    pass
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     layout = BoxLayout(orientation='vertical')
    #     self.camera = Camera(play=False)
    #     layout.add_widget(self.camera)
    #     layout.add_widget(ToggleButton(text='Play', on_press=self.play))
    #     layout.add_widget(Button(text='Capture', on_release=self.capture))
    #     layout.add_widget(Button(text='Recognize Face', on_release=self.recognize_face))
    #     self.add_widget(layout)

class PasswordListWindow(Screen):
    pass

class PasswordEntryWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class PasswordApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LogInWindow(name='login'))
        sm.add_widget(RegisterWindow(name='register'))
        sm.add_widget(CameraWindow(name='camerawindow'))
        sm.add_widget(PasswordListWindow(name='list'))
        sm.add_widget(PasswordEntryWindow(name='entry'))
        
        return sm

if __name__ == '__main__':
    PasswordApp().run()