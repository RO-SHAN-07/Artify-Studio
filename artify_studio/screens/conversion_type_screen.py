from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

class ConversionTypeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Top App Bar Placeholder
        layout.add_widget(MDLabel(text="Choose Transformation", halign="center", theme_text_color="Primary", font_style="H6"))

        # Image Preview Area
        image_preview = MDCard(orientation='vertical', padding=10, size_hint_y=None, height="200dp")
        image_preview.add_widget(MDLabel(text="Image Preview", halign="center"))
        layout.add_widget(image_preview)

        # Transformation Options
        transformation_grid = MDGridLayout(cols=3, padding=10, spacing=10)

        transformations = ["Pencil Sketch", "Colored Sketch", "Turtle Graphics"]
        for transform in transformations:
            card = MDCard(orientation='vertical', padding=10, size_hint=(None, None), size=("100dp", "100dp"))
            card.add_widget(MDLabel(text=transform, halign="center"))
            transformation_grid.add_widget(card)

        layout.add_widget(transformation_grid)

        # Action Buttons
        action_buttons = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="50dp", spacing=10)
        action_buttons.add_widget(MDRaisedButton(text="Process Image"))
        action_buttons.add_widget(MDRaisedButton(text="Save Draft"))
        layout.add_widget(action_buttons)

        self.add_widget(layout)
