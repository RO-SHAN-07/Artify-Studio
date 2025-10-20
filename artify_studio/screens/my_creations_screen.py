from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton

class MyCreationsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Top App Bar Placeholder
        layout.add_widget(MDLabel(text="My Creations", halign="center", theme_text_color="Primary", font_style="H6"))

        # Filter & Sort Controls
        filter_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="30dp", spacing=10)
        filters = ["All", "Pencil", "Colored", "Turtle", "OpenCV"]
        for f in filters:
            filter_layout.add_widget(MDFlatButton(text=f))
        layout.add_widget(filter_layout)

        # Creations Grid
        creations_grid = MDGridLayout(cols=3, padding=10, spacing=10)

        for i in range(9):
            card = MDCard(orientation='vertical', padding=10, size_hint=(None, None), size=("100dp", "120dp"))
            card.add_widget(MDLabel(text=f"Creation {i+1}", halign="center"))
            card.add_widget(MDLabel(text="2 days ago", halign="center", theme_text_color="Secondary"))
            creations_grid.add_widget(card)

        layout.add_widget(creations_grid)

        self.add_widget(layout)
