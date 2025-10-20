from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.slider import MDSlider
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTrailingIcon
from kivymd.uix.button import MDRaisedButton
from kivymd.app import MDApp

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical')

        # Top App Bar
        top_app_bar = MDTopAppBar(title="Settings",
                                  left_action_items=[["arrow-left", lambda x: self.go_back()]])
        layout.add_widget(top_app_bar)

        # General Settings
        general_settings_headline = MDListItemHeadlineText(text="General Settings")
        general_settings_item = MDListItem()
        general_settings_item.add_widget(general_settings_headline)
        layout.add_widget(general_settings_item)

        theme_item = MDListItem(
            MDListItemLeadingIcon(icon="theme-light-dark"),
            MDListItemHeadlineText(text="Dark Mode"),
            MDListItemSupportingText(text="Enable or disable dark mode"),
            MDListItemTrailingIcon(icon="toggle-switch")
        )
        layout.add_widget(theme_item)

        # Processing Settings
        processing_settings_headline = MDListItemHeadlineText(text="Processing Settings")
        processing_settings_item = MDListItem()
        processing_settings_item.add_widget(processing_settings_headline)
        layout.add_widget(processing_settings_item)

        quality_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10, adaptive_height=True)
        quality_layout.add_widget(MDLabel(text="Default Quality"))
        quality_layout.add_widget(MDSlider())
        layout.add_widget(quality_layout)

        # Storage & Cache
        storage_settings_headline = MDListItemHeadlineText(text="Storage & Cache")
        storage_settings_item = MDListItem()
        storage_settings_item.add_widget(storage_settings_headline)
        layout.add_widget(storage_settings_item)

        clear_cache_button = MDRaisedButton(text="Clear Cache", pos_hint={'center_x': 0.5})
        layout.add_widget(clear_cache_button)

        self.add_widget(layout)

    def go_back(self):
        MDApp.get_running_app().switch_screen('home')
