from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.slider import MDSlider

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Top App Bar Placeholder
        layout.add_widget(MDLabel(text="Settings", halign="center", theme_text_color="Primary", font_style="H6"))

        # General Settings
        layout.add_widget(MDLabel(text="General Settings", font_style="H6"))

        theme_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="30dp")
        theme_layout.add_widget(MDLabel(text="Dark Mode"))
        theme_layout.add_widget(MDSwitch())
        layout.add_widget(theme_layout)

        # Processing Settings
        layout.add_widget(MDLabel(text="Processing Settings", font_style="H6"))

        quality_layout = MDBoxLayout(orientation='vertical', size_hint_y=None, height="50dp")
        quality_layout.add_widget(MDLabel(text="Default Quality"))
        quality_layout.add_widget(MDSlider())
        layout.add_widget(quality_layout)

        self.add_widget(layout)
