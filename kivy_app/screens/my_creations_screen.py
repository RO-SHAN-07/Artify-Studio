from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.chip import MDChip
from kivymd.app import MDApp
from kivy.uix.image import Image as KivyImage
from PIL import Image

class MyCreationsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = MDBoxLayout(orientation='vertical')

        # Top App Bar
        top_app_bar = MDTopAppBar(title="My Creations",
                                  left_action_items=[["arrow-left", lambda x: self.go_back()]],
                                  right_action_items=[["magnify", lambda x: x], ["sort", lambda x: x]])
        self.layout.add_widget(top_app_bar)

        # Filter & Sort Controls
        filter_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="50dp", spacing=10, padding=10)
        filters = ["All", "Pencil", "Colored", "Turtle", "OpenCV"]
        for f in filters:
            filter_layout.add_widget(MDChip(text=f, type="filter"))
        self.layout.add_widget(filter_layout)

        # Creations Grid
        self.creations_grid = MDGridLayout(cols=3, padding=10, spacing=10)
        self.layout.add_widget(self.creations_grid)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.load_creations()

    def load_creations(self):
        self.creations_grid.clear_widgets()
        app = MDApp.get_running_app()
        creations = app.db.get_creations()

        if not creations:
            empty_state_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10,
                                            pos_hint={'center_x': 0.5, 'center_y': 0.5})
            empty_state_layout.add_widget(MDLabel(text="No creations yet",
                                                 halign="center",
                                                 font_style="H6"))
            empty_state_layout.add_widget(MDRaisedButton(text="Start Creating",
                                                        pos_hint={'center_x': 0.5},
                                                        on_release=lambda x: self.switch_screen('conversion_type')))
            self.creations_grid.add_widget(empty_state_layout)
        else:
            for creation in creations:
                card = MDCard(orientation='vertical', padding=10, size_hint=(None, None), size=("100dp", "120dp"))
                card.add_widget(KivyImage(source=creation[1]))
                card.add_widget(MDLabel(text=creation[2], halign="center", theme_text_color="Secondary"))
                self.creations_grid.add_widget(card)

    def go_back(self):
        MDApp.get_running_app().switch_screen('home', close_drawer=False)

    def switch_screen(self, screen_name):
        self.manager.current = screen_name
