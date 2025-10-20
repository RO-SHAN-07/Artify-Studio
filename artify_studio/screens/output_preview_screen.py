from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

class OutputPreviewScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Top App Bar Placeholder
        layout.add_widget(MDLabel(text="Preview Results", halign="center", theme_text_color="Primary", font_style="H6"))

        # Before/After Comparison
        comparison_layout = MDGridLayout(cols=2, padding=10, spacing=10)

        before_card = MDCard(orientation='vertical', padding=10)
        before_card.add_widget(MDLabel(text="Before", halign="center"))
        comparison_layout.add_widget(before_card)

        after_card = MDCard(orientation='vertical', padding=10)
        after_card.add_widget(MDLabel(text="After", halign="center"))
        comparison_layout.add_widget(after_card)

        layout.add_widget(comparison_layout)

        # Export Options
        export_options = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="50dp", spacing=10)
        export_options.add_widget(MDLabel(text="Format: PNG"))
        export_options.add_widget(MDLabel(text="Quality: 95%"))
        layout.add_widget(export_options)

        # Action Buttons
        action_buttons = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="50dp", spacing=10)
        action_buttons.add_widget(MDRaisedButton(text="Export Image"))
        action_buttons.add_widget(MDRaisedButton(text="Save to Creations"))
        action_buttons.add_widget(MDRaisedButton(text="Share"))
        layout.add_widget(action_buttons)

        self.add_widget(layout)
