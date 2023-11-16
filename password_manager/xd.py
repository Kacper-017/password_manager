from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.treeview import TreeViewLabel
import time


## Create classes for all screens in the app. Each class inherits from Screen.
class LoginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class CameraScreen(Screen):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))

    def verify(self):
        pass

class VerifyScreen(Screen):
    pass

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


GUI = Builder.load_string("""

GridLayout:
    cols: 1
    ScreenManager:
        id: screen_manager
        LoginScreen:
            name: "login_screen"
            id: login_screen
        RegisterScreen:
            name: "register_screen"
            id: register_screen
        CameraScreen:
            name: "camera_screen"
            id: camera_screen
        VerifyScreen:
            name: "verify_screen"
            id: verify_screen
        ScanScreen:
            name: "scan_screen"
            id: scan_screen
        PasswordListScreen:
            name: "password_list_screen"
            id: password_list_screen
        PaswordEntryScreen:
            name: "password_entry_screen"
            id: password_entry_screen

<LoginScreen>:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: username
            text: "Username"
            font_size: 20
            halign: 'center'
            valign: 'middle'
            multiline: False
        TextInput:
            id: password
            text: "Password"
            font_size: 20
            halign: 'center'
            valign: 'middle'
            multiline: False
        Button:
            text: "Login"
            font_size: 20
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'camera_screen'
        Button:
            text: "Register"
            font_size: 20
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'register_screen'
        Button:
            text: "Exit"
            font_size: 20
            on_press: app.stop()

<RegisterScreen>:
    orientation: 'vertical'
    BoxLayout:
        TextInput:
            id: username
            text: "Username"
            font_size: 20
            halign: 'center'
            valign: 'middle'
            multiline: False
        TextInput:
            id: password
            text: "Password"
            font_size: 20
            halign: 'center'
            valign: 'middle'
            multiline: False
        TextInput:
            id: password_verify
            text: "Password"
            font_size: 20
            halign: 'center'
            valign: 'middle'
            multiline: False
        Button:
            text: "Scan your face"
            font_size: 20
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'camera_screen'
        Button:
            text: "Back"
            font_size: 20
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'login_screen'
                          
<CameraScreen>:
    orientation: 'vertical'
    GridLayout:
        cols: 1
        Camera:
            id: camera
            resolution: (640, 480)
            play: False
        ToggleButton:
            text: 'Play'
            on_press: camera.play = not camera.play
            size_hint_y: None
            height: '48dp'
        Button:
            text: 'Capture'
            size_hint_y: None
            height: '48dp'
            on_press:
                root.capture()
                # root refers to <CameraScreen>
                # app refers to TestCamera, app.root refers to the GridLayout: at the top
                app.root.ids['screen_manager'].transition.direction = 'left'
                app.root.ids['screen_manager'].current = 'password_list_screen'

<VerifyScreen>:
    orientation: 'vertical'
    GridLayout:
        cols: 1
        Button:
            text: "Verify"
            font_size: 50
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'password_list_screen'
        Button:
            text: "Back"
            font_size: 50
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'login_screen'
                          
<ScanScreen>:
    orientation: 'vertical'
    GridLayout:
        cols: 1
        Button:
            text: "Scan"
            font_size: 50
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'login_screen'
                          
<PasswordListScreen>:
    orientation: 'vertical'
    GridLayout:
        cols: 1
        Button:
            text: "Add Password"
            font_size: 50
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'password_entry_screen'
        ScrollView:
            do_scroll: False, True
            bar_width: dp(10)
            scroll_type: ['bars','content']
            TreeView:
                id: tv
                root_options: {'text': 'The Root of the TreeView'}
                size_hint_y: None
                height: self.minimum_height
                          
<PaswordEntryScreen>:
    orientation: 'vertical'
    GridLayout:
        cols: 1
        TextInput:
            id: password
            text: "Password"
            font_size: 50
        TextInput:
            id: password_verify
            text: "Password"
            font_size: 50
        Button:
            text: "Add"
            font_size: 50
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'password_list_screen'
        Button:
            text: "Back"
            font_size: 50
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'password_list_screen'
        
<PasswordViewScreen>:
    orientation: 'vertical'
    GridLayout:
        cols: 1
        TextBox:
            id: site
            text: "Site"
            font_size: 50
        Textbox:
            id: password
            text: "Password"
            font_size: 50
        Button:
            id: edit
            text: "Edit"
            font_size: 50
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'password_entry_screen'
        Button:
            id: exit
            text: "Exit"
            font_size: 50 
            on_press:
                app.stop()
""")

class TestCamera(App):

    def build(self):
        return GUI


TestCamera().run()