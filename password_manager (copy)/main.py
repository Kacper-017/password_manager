from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.treeview import TreeViewLabel
import time
import os

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)
logged_in = False


## Create classes for all screens in the app. Each class inherits from Screen.
class LoginScreen(Screen):
    def login(self):
        global logged_in
        if self.ids.username.text == 'admin' and self.ids.password.text == 'admin':
            self.manager.current = 'camera_screen'
            logged_in = True

class RegisterScreen(Screen):
    pass

class CameraScreen(Screen):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))

    def next(self):
        global logged_in
        if logged_in:
            self.manager.current = 'verify_screen'
        else:
            # save face, go to login screen
            self.manager.current = 'login_screen'

class VerifyScreen(Screen):
    def verify(self):
        global logged_in
        if logged_in:
            # verify face with model
            self.manager.current = 'password_list_screen'
        else:
            # save face, go to login screen
            self.manager.current = 'login_screen'

class ScanScreen(Screen):
    pass

class PasswordListScreen(Screen):
    def on_enter(self):
        for i in range(100):
            self.ids.tv.add_node(TreeViewLabel(text=f'Label Number {i}'))

class PaswordEntryScreen(Screen):
    pass

class PasswordViewScreen(Screen):
    pass


with open("/home/kacper/Documents/password_manager/password_manager/gui.txt", "r") as f:
    GUI = Builder.load_string(f.read())


class TestCamera(App):

    def build(self):
        return GUI


TestCamera().run()