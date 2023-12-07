from kivy.app import App
from kivy.lang import Builder
from kivy.uix.treeview import TreeViewLabel

kv = """
BoxLayout:
    orientation: 'vertical'
    Label:
        text: 'Demonstrate a Scrolling TreeView'
        size_hint_y: None
        height: 24
    ScrollView:
        do_scroll: False, True
        bar_width: dp(10)
        scroll_type: ['bars','content']
        TreeView:
            id: tv
            root_options: {'text': 'The Root of the TreeView'}
            size_hint_y: None
            height: self.minimum_height

"""


class ScrollTreeView(App):
    def build(self):
        return Builder.load_string(kv)

    def on_start(self):
        for i in range(100):
            self.root.ids.tv.add_node(TreeViewLabel(text=f'Label Number {i}'))


ScrollTreeView().run()