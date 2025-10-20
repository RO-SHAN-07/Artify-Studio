from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.chip import MDChip
from kivymd.app import MDApp

class MyCreationsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical')

        # Top App Bar
        top_app_bar = MDTopAppBar(title="My Creations",
                                  left_action_items=[["arrow-left", lambda x: self.go_back()]],
                                  right_action_items=[["magnify", lambda x: x], ["sort", lambda x: x]])
        layout.add_widget(top_app_bar)

        # Filter & Sort Controls
        filter_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="50dp", spacing=10, padding=10)
        filters = ["All", "Pencil", "Colored", "Turtle", "OpenCV"]
        for f in filters:
            filter_layout.add_widget(MDChip(text=f, type="filter"))
        layout.add_widget(filter_layout)

        # Creations Grid
        creations_grid = MDGridLayout(cols=3, padding=10, spacing=10)

        # Empty State (example)
        if not creations_grid.children:
            empty_state_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10,
                                            pos_hint={'center_x': 0.5, 'center_y': 0.5})
            empty_state_layout.add_widget(MDLabel(text="No creations yet",
                                                 halign="center",
                                                 font_style="H6"))
            empty_state_layout.add_widget(MDRaisedButton(text="Start Creating",
                                                        pos_hint={'center_x': 0.5},
                                                        on_release=lambda x: self.switch_screen('conversion_type')))
            layout.add_widget(empty_state_layout)
        else:
            layout.add_widget(creations_grid)

        self.add_widget(layout)

    def go_back(self):
        MDApp.get_running_app().switch_screen('home', close_drawer=False)

    def switch_screen(self, screen_name):
        self.manager.current = screen_name
