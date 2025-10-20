from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Top App Bar Placeholder
        layout.add_widget(MDLabel(text="Profile", halign="center", theme_text_color="Primary", font_style="H6"))

        # User Profile Info
        profile_info = MDCard(orientation='horizontal', padding=10, size_hint_y=None, height="100dp")
        profile_info.add_widget(MDLabel(text="Avatar"))

        details_layout = MDBoxLayout(orientation='vertical')
        details_layout.add_widget(MDLabel(text="Name: John Doe"))
        details_layout.add_widget(MDLabel(text="Email: john@example.com"))
        profile_info.add_widget(details_layout)

        stats_layout = MDBoxLayout(orientation='vertical')
        stats_layout.add_widget(MDLabel(text="Creations: 47"))
        stats_layout.add_widget(MDLabel(text="Favorites: 12"))
        profile_info.add_widget(stats_layout)

        layout.add_widget(profile_info)

        # Account Settings
        layout.add_widget(MDLabel(text="Account Settings", font_style="H6"))

        # App Information
        layout.add_widget(MDLabel(text="App Information", font_style="H6"))

        self.add_widget(layout)
