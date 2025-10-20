from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens.splash_screen import SplashScreen
from screens.home_screen import HomeScreen
from screens.conversion_type_screen import ConversionTypeScreen
from screens.output_preview_screen import OutputPreviewScreen
from screens.settings_screen import SettingsScreen
from screens.my_creations_screen import MyCreationsScreen
from screens.profile_screen import ProfileScreen

class ArtifyStudioApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ConversionTypeScreen(name='conversion_type'))
        sm.add_widget(OutputPreviewScreen(name='output_preview'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(MyCreationsScreen(name='my_creations'))
        sm.add_widget(ProfileScreen(name='profile'))
        return sm

if __name__ == '__main__':
    ArtifyStudioApp().run()
