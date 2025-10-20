from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical')

        # Top App Bar Placeholder
        layout.add_widget(MDLabel(text="Artify Studio", halign="center", theme_text_color="Primary", font_style="H6"))

        # Quick Actions Grid
        quick_actions_grid = MDGridLayout(cols=3, padding=10, spacing=10)

        actions = ["Pencil Sketch", "Colored Sketch", "OpenCV Filters"]
        for action in actions:
            card = MDCard(orientation='vertical', padding=10, size_hint=(None, None), size=("100dp", "100dp"))
            card.add_widget(MDLabel(text=action, halign="center"))
            quick_actions_grid.add_widget(card)

        layout.add_widget(quick_actions_grid)

        # Recent Creations
        layout.add_widget(MDLabel(text="Recent Creations", halign="left", theme_text_color="Primary", font_style="H6"))

        self.add_widget(layout)
