from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.treeview import TreeViewLabel
from kivy.clock import Clock
from kivy.uix.button import Button
import time
import os
from kivy.properties import StringProperty, BooleanProperty

import mysql.connector
# from database import SessionLocal, engine
# import models
# models.Base.metadata.create_all(bind=engine)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Benzowrak01%",
    database="passwordManager"
)

coursor = db.cursor()

coursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            image TEXT NOT NULL,
            masterkey_hash TEXT NOT NULL,
            device_secret TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );""")

coursor.execute("""CREATE TABLE AUTO_INCREMENT IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );""")

logged_in = False
logged_in_user_id = None

## Create classes for all screens in the app. Each class inherits from Screen.
class LoginScreen(Screen):
    def login(self):
        global logged_in
        global logged_in_user_id
        sql = "SELECT * FROM users WHERE username = %s AND masterkey_hash = %s"
        val = (self.ids.username.text, self.ids.password.text)
        coursor.execute(sql, val)
        result = coursor.fetchone()

        if result is not None:
            logged_in_user_id = result[0]
            self.manager.current = 'camera_screen'
            logged_in = True



class RegisterScreen(Screen):
    def verify(self):
        for input_field in [self.ids.username, self.ids.password, self.ids.password_verify]:
            if input_field.text == '':
                # flash button red
                input_field.background_color = (1, 0, 0, 1)
                # schedule color change back to white after 10 seconds
                Clock.schedule_once(lambda dt: setattr(input_field, 'background_color', (1, 1, 1, 1)), 1)
                return False
        
        if self.ids.password.text == self.ids.password_verify.text:
            # save face, go to login screen
            return True
        else:
            # flash button red 
            self.ids.password_verify.background_color = (1, 0, 0, 1)
            # schedule color change back to white after 10 seconds
            Clock.schedule_once(lambda dt: setattr(self.ids.password_verify, 'background_color', (1, 1, 1, 1)), 1)

    def register(self):
        if self.verify():
            # save credentials to database
            sql = "INSERT INTO users (username, image, masterkey_hash, device_secret) VALUES (%s, %s, %s, %s)"
            val = (self.ids.username.text, "1", self.ids.password.text, "1")
            coursor.execute(sql, val)
            db.commit()
            # save face, go to login screen
            self.manager.current = 'login_screen'
            

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
        global logged_in
        if logged_in:
            sql = "SELECT url FROM passwords  WHERE user_id = %s"
            coursor.execute(sql, (logged_in_user_id,))
            result = coursor.fetchall()
            
            for row in result:
                button = Button(text=row[0], on_release=lambda url=row[0]: self.view_password(url))
                self.ids.button_container.add_widget(button)
                
    def view_password(self, url):
        self.manager.get_screen('password_view_screen').url = url
        self.manager.current = 'password_view_screen'
                
    def add_password(self):
        self.manager.get_screen('password_entry_screen').edit = False
        self.manager.current = 'password_entry_screen'

class PaswordEntryScreen(Screen):
    edit = BooleanProperty()
    def on_enter(self):
        if self.edit:
            self.ids.url.text = self.manager.get_screen('password_view_screen').url
            self.ids.username.text = self.manager.get_screen('password_view_screen').ids.username_label.text
            self.ids.password.text = self.manager.get_screen('password_view_screen').ids.password_label.text
            self.ids.password_verify.text = self.manager.get_screen('password_view_screen').ids.password_label.text
            self.edit = False
        else :
            self.ids.url.text = ''
            self.ids.username.text = ''
            self.ids.password.text = ''
            self.ids.password_verify.text = ''
            self.ids.url.hint_text = "Site"
            self.ids.username.hint_text = "Username"
            self.ids.password.hint_text = "Password"
            self.ids.password_verify.hint_text = "Verify Password"

    def verify(self):
        for input_field in [self.ids.url, self.ids.username, self.ids.password, self.ids.password_verify]:
            if input_field.text == '':
                # flash button red
                input_field.background_color = (1, 0, 0, 1)
                # schedule color change back to white after 10 seconds
                Clock.schedule_once(lambda dt: setattr(input_field, 'background_color', (1, 1, 1, 1)), 1)
                return False
        
        if self.ids.password.text == self.ids.password_verify.text:
            # save face, go to login screen
            return True
        else:
            # flash button red 
            self.ids.password_verify.background_color = (1, 0, 0, 1)
            # schedule color change back to white after 10 seconds
            Clock.schedule_once(lambda dt: setattr(self.ids.password_verify, 'background_color', (1, 1, 1, 1)), 1) 

    def add(self):
        global logged_in
        global logged_in_user_id

        if logged_in and self.verify():
            sql = "INSERT INTO passwords (user_id, username, password, url)  VALUES (%s, %s, %s, %s)"
            val = (logged_in_user_id, self.ids.username.text, self.ids.password.text, self.ids.url.text)
            coursor.execute(sql, val)
            db.commit()
            self.manager.get_screen('password_view_screen').url = self.ids.url.text
            self.manager.current = 'password_view_screen'


class PasswordViewScreen(Screen):
    url = StringProperty()
    def on_enter(self):
        self.ids.site.text = self.url
        self.view_password()

    def view_password(self):
        global logged_in_user_id
        if logged_in_user_id:
            sql = "SELECT username, password FROM passwords WHERE user_id = %s AND url = %s"
            coursor.execute(sql, (logged_in_user_id, self.url))
            result = coursor.fetchone()
            
            if result:
                username, password = result
                self.ids.username_label.text = f"Username: {username}"
                self.ids.password_label.text = f"Password: {password}"
            else:
                self.ids.username_label.text = "Username: N/A"
                self.ids.password_label.text = "Password: N/A"
        else:
            self.ids.username_label.text = "Username: N/A"
            self.ids.password_label.text = "Password: N/A"

    def edit(self):
        self.manager.get_screen('password_entry_screen').edit = True
        self.manager.current = 'password_entry_screen'

#with open("/home/kacper/Documents/password_manager/password_manager/gui.txt", "r") as f:
#    GUI = Builder.load_string(f.read())

gui = """

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
        PasswordViewScreen:
            name: "password_view_screen"
            id: password_view_screen

<LoginScreen>:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: username
            hint_text: "Username"
            font_size: 20
            halign: 'center'
            valign: 'middle'
            multiline: False
        TextInput:
            id: password
            hint_text: "Password"
            font_size: 20
            halign: 'center'
            valign: 'middle'
            multiline: False
            password: True
        Button:
            text: "Login"
            font_size: 20
            on_press:
                root.login()
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
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: username
            hint_text: "Username"
            font_size: 20
            halign: 'center'
            valign: 'middle'
            multiline: False
        TextInput:
            id: password
            hint_text: "Password"
            font_size: 20
            halign: 'center'
            valign: 'middle'
            multiline: False
        TextInput:
            id: password_verify
            hint_text: "Verify Password"
            font_size: 20
            halign: 'center'
            valign: 'middle'
            multiline: False
        Button:
            text: "Scan your face"
            font_size: 20
            on_press:
                root.register()
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
                root.add_password()

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
            id: url
            font_size: 50
            multiline: False
            hint_text: "Site"
            halign: 'center'
            valign: 'middle'
        TextInput:
            id: username
            font_size: 50
            multiline: False
            hint_text: "Username"
            halign: 'center'
            valign: 'middle'
        TextInput:
            id: password
            font_size: 50
            multiline: False
            hint_text: "Password"
            halign: 'center'
            valign: 'middle'
        TextInput:
            id: password_verify
            font_size: 50
            multiline: False
            hint_text: "Verify Password"
            halign: 'center'
            valign: 'middle'
        Button:
            text: "Add"
            font_size: 50
            on_press:
                root.add()
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
        Label:
            id: site_label
            text: "Site"
            font_size: 50
        Label:
            id: url
            text: ""
            font_size: 50
        Label:
            id: username_label
            text: "Password"
            font_size: 50
        Label:
            id: username
            text: ""
            font_size: 50
        Label:
            id: password_label
            text: "Password"
            font_size: 50
        Label:
            id: password
            text: ""
            font_size: 50
        Button:
            id: edit
            text: "Edit"
            font_size: 50
            on_press:
                root.edit()
        Button:
            id: exit
            text: "Exit"
            font_size: 50 
            on_press:
                app.stop()

"""

GUI = Builder.load_string(gui)


class TestCamera(App):

    def build(self):
        return GUI


TestCamera().run()