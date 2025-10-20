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
from PIL import Image

class ConversionTypeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical')

        # Top App Bar
        top_app_bar = MDTopAppBar(title="Choose Transformation",
                                  left_action_items=[["arrow-left", lambda x: self.go_back()]])
        layout.add_widget(top_app_bar)

        # Image Preview Area
        self.image_preview = MDCard(orientation='vertical', padding=10, size_hint_y=None, height="200dp",
                               ripple_behavior=True)
        self.image_preview.add_widget(MDLabel(text="Image Preview", halign="center"))
        layout.add_widget(self.image_preview)

        # Transformation Options
        transformation_grid = MDGridLayout(cols=3, padding=10, spacing=10, adaptive_height=True)

        transformations = [("Pencil Sketch", "pencil", "pencil_sketch"),
                           ("Colored Sketch", "palette", "colored_sketch"),
                           ("OpenCV Filter", "camera", "opencv_filter"),
                           ("Turtle Graphics", "pen", "turtle_graphics")]
        for transform, icon, transform_name in transformations:
            card = MDCard(orientation='vertical', padding=10, size_hint=(None, None), size=("100dp", "100dp"),
                          ripple_behavior=True, on_release=lambda x, t=transform_name: self.apply_transformation(t))
            card.add_widget(MDIconButton(icon=icon, pos_hint={'center_x': 0.5}))
            card.add_widget(MDLabel(text=transform, halign="center", font_style="Caption"))
            transformation_grid.add_widget(card)

        layout.add_widget(transformation_grid)

        # Action Buttons
        action_buttons = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="50dp", spacing=10, padding=10)
        action_buttons.add_widget(MDRaisedButton(text="Load Image", on_release=self.load_image))
        layout.add_widget(action_buttons)

        self.add_widget(layout)

    def go_back(self):
        MDApp.get_running_app().switch_screen('home', close_drawer=False)

    def load_image(self, *args):
        # Simulate loading an image
        app = MDApp.get_running_app()
        # In a real app, this would be a file path from a file chooser
        app.engine.original_image = Image.new('RGB', (600, 600), color = 'red')
        app.engine.image = app.engine.original_image.copy()
        self.image_preview.clear_widgets()
        from kivy.uix.image import Image as KivyImage
        from io import BytesIO
        img_byte_arr = BytesIO()
        app.engine.image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        self.image_preview.add_widget(KivyImage(source='', coreimage=KivyImage(BytesIO(img_byte_arr.read()), ext='png').coreimage))

    def apply_transformation(self, transform_type):
        app = MDApp.get_running_app()
        result = app.engine.apply_transformation(transform_type)
        if result["success"]:
            self.manager.current = 'output_preview'
        else:
            print(result["message"])
