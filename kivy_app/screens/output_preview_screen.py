from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.app import MDApp
from kivy.uix.image import Image as KivyImage
from io import BytesIO

class OutputPreviewScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = MDBoxLayout(orientation='vertical')

        # Top App Bar
        top_app_bar = MDTopAppBar(title="Preview Results",
                                  left_action_items=[["arrow-left", lambda x: self.go_back()]],
                                  right_action_items=[["content-save", lambda x: x], ["share-variant", lambda x: x]])
        self.layout.add_widget(top_app_bar)

        # Before/After Comparison
        self.comparison_layout = MDGridLayout(cols=2, padding=10, spacing=10)
        self.layout.add_widget(self.comparison_layout)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        if app.engine.image:
            self.comparison_layout.clear_widgets()

            # Display the transformed image
            img_byte_arr = BytesIO()
            app.engine.image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            after_card = MDCard(orientation='vertical', padding=10, ripple_behavior=True)
            after_card.add_widget(MDLabel(text="After", halign="center"))
            after_card.add_widget(KivyImage(source='', coreimage=KivyImage(BytesIO(img_byte_arr.read()), ext='png').coreimage))
            self.comparison_layout.add_widget(after_card)

    def go_back(self):
        MDApp.get_running_app().switch_screen('conversion_type', close_drawer=False)
