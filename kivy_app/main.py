from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer, MDNavigationDrawerMenu, MDNavigationDrawerHeader, MDNavigationDrawerItem
from screens.splash_screen import SplashScreen
from screens.home_screen import HomeScreen
from screens.conversion_type_screen import ConversionTypeScreen
from screens.output_preview_screen import OutputPreviewScreen
from screens.settings_screen import SettingsScreen
from screens.my_creations_screen import MyCreationsScreen
from screens.profile_screen import ProfileScreen
from engine import ImageTransformationEngine, TransformationConfig

class ArtifyStudioApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        self.engine = ImageTransformationEngine()

        self.navigation_layout = MDNavigationLayout()
        self.screen_manager = ScreenManager()

        screens = {
            'splash': SplashScreen,
            'home': HomeScreen,
            'conversion_type': ConversionTypeScreen,
            'output_preview': OutputPreviewScreen,
            'settings': SettingsScreen,
            'my_creations': MyCreationsScreen,
            'profile': ProfileScreen
        }

        for name, screen_class in screens.items():
            self.screen_manager.add_widget(screen_class(name=name))

        self.navigation_layout.add_widget(self.screen_manager)

        navigation_drawer_menu = MDNavigationDrawerMenu()

        menu_items = [
            ("Home", "home", "home"),
            ("My Creations", "creation", "my_creations"),
            ("Settings", "cog", "settings"),
            ("Profile", "account", "profile"),
        ]

        for text, icon, screen_name in menu_items:
            navigation_drawer_menu.add_widget(
                MDNavigationDrawerItem(
                    MDNavigationDrawerHeader(text=text, icon=icon),
                    on_release=lambda x, screen=screen_name: self.switch_screen(screen)
                )
            )

        navigation_drawer = MDNavigationDrawer(
            MDNavigationDrawerHeader(
                title="Artify Studio",
                text="Version 1.0.0",
                spacing="4dp",
                padding=("12dp", 0, 0, "12dp"),
            ),
            navigation_drawer_menu
        )
        self.navigation_layout.add_widget(navigation_drawer)

        return self.navigation_layout

    def switch_screen(self, screen_name, close_drawer=True):
        self.screen_manager.current = screen_name
        if close_drawer:
            self.navigation_layout.toggle_nav_drawer()

if __name__ == '__main__':
    ArtifyStudioApp().run()
