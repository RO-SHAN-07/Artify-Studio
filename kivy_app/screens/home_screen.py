from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.app import MDApp

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical')

        # Top App Bar
        top_app_bar = MDTopAppBar(title="Artify Studio",
                                  left_action_items=[["menu", lambda x: self.open_drawer()]])
        layout.add_widget(top_app_bar)

        # Quick Actions Grid
        quick_actions_grid = MDGridLayout(cols=3, padding=10, spacing=10, adaptive_height=True)

        actions = [("Pencil Sketch", "pencil", "conversion_type"),
                   ("Colored Sketch", "palette", "conversion_type"),
                   ("OpenCV Filters", "camera", "conversion_type")]
        for action, icon, screen_name in actions:
            card = MDCard(orientation='vertical', padding=10, size_hint=(None, None), size=("100dp", "100dp"),
                          ripple_behavior=True, on_release=lambda x, screen=screen_name: self.switch_screen(screen))
            card.add_widget(MDIconButton(icon=icon, pos_hint={'center_x': 0.5}))
            card.add_widget(MDLabel(text=action, halign="center", font_style="Caption"))
            quick_actions_grid.add_widget(card)

        layout.add_widget(quick_actions_grid)

        # Batch Process Button
        layout.add_widget(MDRaisedButton(text="Batch Process", on_release=self.batch_process,
                                       pos_hint={'center_x': 0.5}))

        # Recent Creations
        layout.add_widget(MDLabel(text="Recent Creations", font_style="H6", padding=(10, 10)))

        scroll_view = MDScrollView(scroll_type=['bars'], bar_width='10dp')
        recent_creations_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing=10, padding=10)

        for i in range(5):
            card = MDCard(orientation='vertical', size_hint=(None, None), size=("150dp", "100dp"),
                          on_release=lambda x: self.switch_screen('output_preview'))
            card.add_widget(MDLabel(text=f"Creation {i+1}", halign="center"))
            recent_creations_layout.add_widget(card)

        scroll_view.add_widget(recent_creations_layout)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

    def switch_screen(self, screen_name):
        self.manager.current = screen_name

    def open_drawer(self):
        MDApp.get_running_app().navigation_layout.toggle_nav_drawer()

    def batch_process(self, *args):
        app = MDApp.get_running_app()
        # Simulate selecting multiple images
        image_paths = ["dummy_path1.png", "dummy_path2.png", "dummy_path3.png"]
        results = app.engine.batch_process(image_paths, "pencil_sketch")
        for result in results:
            # In a real app, we would save the images to the gallery
            app.db.save_creation(result["path"], "pencil_sketch")
        self.switch_screen('my_creations')
