from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
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
        on_press: root.capture()
    Button:
        text: 'Back'
        size_hint_y: None
        height: '48dp'
        on_press: root.manager.current = 'login'
''')


class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()


# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.screenmanager import ScreenManager, Screen
# import time



# class Screen1(Screen):
#     def capture(self):
#         '''
#         Function to capture the images and give them the names
#         according to their captured time and date.
#         '''
#         camera = self.ids['camera']
#         timestr = time.strftime("%Y%m%d_%H%M%S")
#         camera.export_to_png("IMG_{}.png".format(timestr))
#         print("Captured")

# class WindowManager(ScreenManager):
#     pass



# class TestCamera(App):

#     def build(self):
#         sm=ScreenManager()
#         sm.add_widget(Screen1(name='screen1'))
#         return sm
    
# if __name__ == '__main__':
#     TestCamera().run()


# import numpy as np
# import cv2
# #import controle #--custom opncv methods

# from kivy.uix.image import Image
# from kivy.core.camera import Camera as CoreCamera
# from kivy.properties import NumericProperty, ListProperty, BooleanProperty

# # access to camera
# core_camera = CoreCamera(index=0, resolution=(640, 480), stopped=True)

# # Widget to display camera
# class CameraCv(Image):
#     '''Camera class. See module documentation for more information.
#     '''

#     play = BooleanProperty(True)
#     '''Boolean indicating whether the camera is playing or not.
#     You can start/stop the camera by setting this property::
#         # start the camera playing at creation (default)
#         cam = Camera(play=True)
#         # create the camera, and start later
#         cam = Camera(play=False)
#         # and later
#         cam.play = True
#     :attr:`play` is a :class:`~kivy.properties.BooleanProperty` and defaults to
#     True.
#     '''

#     index = NumericProperty(-1)
#     '''Index of the used camera, starting from 0.
#     :attr:`index` is a :class:`~kivy.properties.NumericProperty` and defaults
#     to -1 to allow auto selection.
#     '''

#     resolution = ListProperty([-1, -1])
#     '''Preferred resolution to use when invoking the camera. If you are using
#     [-1, -1], the resolution will be the default one::
#         # create a camera object with the best image available
#         cam = Camera()
#         # create a camera object with an image of 320x240 if possible
#         cam = Camera(resolution=(320, 240))
#     .. warning::
#         Depending on the implementation, the camera may not respect this
#         property.
#     :attr:`resolution` is a :class:`~kivy.properties.ListProperty` and defaults
#     to [-1, -1].
#     '''

#     def __init__(self, **kwargs):
#         self._camera = None
#         super(CameraCv, self).__init__(**kwargs)  # `CameraCv` instead of `Camera`
#         if self.index == -1:
#             self.index = 0
#         on_index = self._on_index
#         fbind = self.fbind
#         fbind('index', on_index)
#         fbind('resolution', on_index)
#         on_index()

#     def on_tex(self, *l):

#         image = np.frombuffer(self.texture.pixels, dtype='uint8')
#         image = image.reshape(self.texture.height, self.texture.width, -1)
#         #image = controle.cropCircle(image,50,210) #custom opencv method
#         numpy_data = image.tostring()

#         self.texture.blit_buffer(numpy_data, bufferfmt="ubyte", colorfmt='rgba')
#         self.canvas.ask_update()

#     def _on_index(self, *largs):
#         self._camera = None
#         if self.index < 0:
#             return
#         if self.resolution[0] < 0 or self.resolution[1] < 0:
#             return

#         self._camera = core_camera # `core_camera` instead of `CoreCamera(index=self.index, resolution=self.resolution, stopped=True)`

#         self._camera.bind(on_load=self._camera_loaded)
#         if self.play:
#             self._camera.start()
#             self._camera.bind(on_texture=self.on_tex)

#     def _camera_loaded(self, *largs):
#         self.texture = self._camera.texture
#         self.texture_size = list(self.texture.size)

#     def on_play(self, instance, value):
#         if self._camera:
#             return
#         if not value:
#             self._camera.start()
#         else:
#             self._camera.stop()