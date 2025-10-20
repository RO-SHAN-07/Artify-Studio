from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.slider import MDSlider
from kivy.uix.accordion import Accordion, AccordionItem
from kivymd.app import MDApp

class ConversionTypeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical')

        # Top App Bar
        top_app_bar = MDTopAppBar(title="Choose Transformation",
                                  left_action_items=[["arrow-left", lambda x: self.go_back()]])
        layout.add_widget(top_app_bar)

        # Image Preview Area
        image_preview = MDCard(orientation='vertical', padding=10, size_hint_y=None, height="200dp",
                               ripple_behavior=True)
        image_preview.add_widget(MDLabel(text="Image Preview", halign="center"))
        layout.add_widget(image_preview)

        # Transformation Options
        transformation_grid = MDGridLayout(cols=3, padding=10, spacing=10, adaptive_height=True)

        transformations = [("Pencil Sketch", "pencil"), ("Colored Sketch", "palette"), ("Turtle Graphics", "pen")]
        for transform, icon in transformations:
            card = MDCard(orientation='vertical', padding=10, size_hint=(None, None), size=("100dp", "100dp"),
                          ripple_behavior=True, on_release=lambda x: self.switch_screen('output_preview'))
            card.add_widget(MDIconButton(icon=icon, pos_hint={'center_x': 0.5}))
            card.add_widget(MDLabel(text=transform, halign="center", font_style="Caption"))
            transformation_grid.add_widget(card)

        layout.add_widget(transformation_grid)

        # Parameter Controls
        accordion = Accordion(orientation='vertical')

        pencil_sketch_options = AccordionItem(title='Pencil Sketch Options')
        pencil_sketch_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        pencil_sketch_layout.add_widget(MDLabel(text="Edge Detection:"))
        pencil_sketch_layout.add_widget(MDSlider())
        pencil_sketch_options.add_widget(pencil_sketch_layout)
        accordion.add_widget(pencil_sketch_options)

        layout.add_widget(accordion)

        # Action Buttons
        action_buttons = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="50dp", spacing=10, padding=10)
        action_buttons.add_widget(MDRaisedButton(text="Process Image"))
        action_buttons.add_widget(MDRaisedButton(text="Save Draft"))
        layout.add_widget(action_buttons)

        self.add_widget(layout)

    def go_back(self):
        MDApp.get_running_app().switch_screen('home', close_drawer=False)

    def switch_screen(self, screen_name):
        self.manager.current = screen_name
