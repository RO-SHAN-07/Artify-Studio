from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTrailingIcon
from kivymd.app import MDApp

class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical')

        # Top App Bar
        top_app_bar = MDTopAppBar(title="Profile",
                                  left_action_items=[["arrow-left", lambda x: self.go_back()]],
                                  right_action_items=[["pencil", lambda x: x]])
        layout.add_widget(top_app_bar)

        # User Profile Info
        profile_info = MDCard(orientation='horizontal', padding=10, size_hint_y=None, height="120dp",
                              ripple_behavior=True)
        profile_info.add_widget(MDListItemLeadingIcon(icon="account-circle", size=("100dp", "100dp")))

        details_layout = MDBoxLayout(orientation='vertical')
        details_layout.add_widget(MDListItemHeadlineText(text="John Doe"))
        details_layout.add_widget(MDListItemSupportingText(text="john@example.com"))
        profile_info.add_widget(details_layout)

        stats_layout = MDBoxLayout(orientation='vertical')
        stats_layout.add_widget(MDListItemHeadlineText(text="47"))
        stats_layout.add_widget(MDListItemSupportingText(text="Creations"))
        profile_info.add_widget(stats_layout)

        layout.add_widget(profile_info)

        # Account Settings
        account_settings_headline = MDListItemHeadlineText(text="Account Settings")
        account_settings_item = MDListItem()
        account_settings_item.add_widget(account_settings_headline)
        layout.add_widget(account_settings_item)

        export_data_item = MDListItem(
            MDListItemLeadingIcon(icon="export"),
            MDListItemHeadlineText(text="Export Data"),
            MDListItemTrailingIcon(icon="chevron-right")
        )
        layout.add_widget(export_data_item)

        # App Information
        app_info_headline = MDListItemHeadlineText(text="App Information")
        app_info_item = MDListItem()
        app_info_item.add_widget(app_info_headline)
        layout.add_widget(app_info_item)

        version_item = MDListItem(
            MDListItemLeadingIcon(icon="information"),
            MDListItemHeadlineText(text="Version"),
            MDListItemSupportingText(text="1.0.0")
        )
        layout.add_widget(version_item)

        self.add_widget(layout)

    def go_back(self):
        MDApp.get_running_app().switch_screen('home')
