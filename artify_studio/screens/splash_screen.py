from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivy.clock import Clock
from kivymd.app import MDApp

class SplashScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        # Logo and App Name
        logo_layout = MDBoxLayout(orientation='vertical', adaptive_height=True,
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5})
        logo_layout.add_widget(MDLabel(text="Artify Studio",
                                     halign="center",
                                     font_style="H2",
                                     theme_text_color="Custom",
                                     text_color=MDApp.get_running_app().theme_cls.primary_dark if MDApp.get_running_app() else (0,0,0,1) ))
        logo_layout.add_widget(MDLabel(text="Version 1.0.0",
                                     halign="center",
                                     font_style="Caption",
                                     theme_text_color="Secondary"))
        self.layout.add_widget(logo_layout)

        # Progress Bar and Status Label
        progress_layout = MDBoxLayout(orientation='vertical', adaptive_height=True,
                                    pos_hint={'center_x': 0.5})
        self.progress_bar = MDProgressBar(value=0)
        self.status_label = MDLabel(text="Initializing...",
                                    halign="center",
                                    font_style="Body2",
                                    theme_text_color="Secondary")
        progress_layout.add_widget(self.progress_bar)
        progress_layout.add_widget(self.status_label)
        self.layout.add_widget(progress_layout)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.layout.md_bg_color = MDApp.get_running_app().theme_cls.primary_light
        Clock.schedule_interval(self.update_progress, 0.5)

    def update_progress(self, dt):
        if self.progress_bar.value < 100:
            self.progress_bar.value += 25
            if self.progress_bar.value == 25:
                self.status_label.text = "Loading resources..."
            elif self.progress_bar.value == 50:
                self.status_label.text = "Validating cache..."
            elif self.progress_bar.value == 75:
                self.status_label.text = "Finalizing..."
        else:
            Clock.unschedule(self.update_progress)
            self.manager.current = 'home'
