import webbrowser
import itertools
import threading
import os
import time

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivy.properties import (
    NumericProperty, StringProperty, ListProperty, DictProperty, BooleanProperty
)
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.storage.jsonstore import JsonStore

# --- Camera4Kivy Imports ---


store = JsonStore('tournament_data.json')

KV = """
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import Clock kivy.clock.Clock

ScreenManager:
    transition: NoTransition()
    MainTabsScreen:
    MatchDetailsScreen:
    SecondaryCameraScreen:
    PracticeScreen:

<MainTabsScreen>:
    name: 'main_tabs'
    on_enter: Clock.schedule_once(lambda dt: root.load_tournament_data(), 0)
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Cricket Arena"
            md_bg_color: 0.04, 0.25, 0.1, 1
            elevation: 4
            size_hint_y: None
            height: "56dp"
        MDBottomNavigation:
            panel_color: 0.04, 0.25, 0.1, 1
            selected_color_background: 0, 0, 0, .2
            text_color_active: 1, 0.84, 0, 1

            MDBottomNavigationItem:
                name: 'home'
                text: 'Home'
                icon: 'home'
                BoxLayout:
                    orientation: 'vertical'
                    canvas.before:
                        Color:
                            rgba: 0.08, 0.08, 0.08, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    ScrollView:
                        BoxLayout:
                            orientation: 'vertical'
                            padding: "15dp"
                            spacing: "20dp"
                            size_hint_y: None
                            height: self.minimum_height
                            MDCard:
                                size_hint: 1, None
                                height: "140dp"
                                radius: [20]
                                md_bg_color: 0.12, 0.12, 0.12, 1
                                ripple_behavior: True
                                on_release: root.manager.current = 'match_details'
                                MDBoxLayout:
                                    orientation: 'vertical'
                                    padding: "20dp"
                                    MDLabel:
                                        text: "PLAY MATCH"
                                        theme_text_color: "Custom"
                                        text_color: 0.04, 0.7, 0.2, 1
                                        bold: True
                                    MDLabel:
                                        text: "Live Scoring Dashboard"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1
                            MDCard:
                                size_hint: 1, None
                                height: "100dp"
                                radius: [20]
                                md_bg_color: 0.12, 0.12, 0.12, 1
                                on_release: root.manager.current = 'secondary_camera'
                                MDBoxLayout:
                                    padding: "15dp"
                                    spacing: "15dp"
                                    MDIcon:
                                        icon: "video-outline"
                                        theme_text_color: "Custom"
                                        text_color: 1, 0.84, 0, 1
                                        size_hint_x: None
                                        width: "40dp"
                                    MDLabel:
                                        text: "SECONDARY CAMERA"
                            MDCard:
                                size_hint: 1, None
                                height: "100dp"
                                radius: [20]
                                md_bg_color: 0.12, 0.12, 0.12, 1
                                on_release: root.manager.current = 'practice'
                                MDBoxLayout:
                                    padding: "15dp"
                                    spacing: "15dp"
                                    MDIcon:
                                        icon: "run-fast"
                                        theme_text_color: "Custom"
                                        text_color: 0.04, 0.7, 0.2, 1
                                        size_hint_x: None
                                        width: "40dp"
                                    MDLabel:
                                        text: "NET PRACTICE"

            MDBottomNavigationItem:
                name: 'tournament'
                text: 'Tournament'
                icon: 'trophy'
                BoxLayout:
                    orientation: 'vertical'
                    canvas.before:
                        Color:
                            rgba: 0.08, 0.08, 0.08, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    ScrollView:
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            padding: "10dp"
                            spacing: "15dp"
                            MDBoxLayout:
                                adaptive_height: True
                                spacing: "10dp"
                                MDLabel:
                                    text: root.tournament_name if root.tournament_name else "TOURNAMENT SETUP"
                                    halign: "center"
                                    font_style: "H6"
                                    theme_text_color: "Custom"
                                    text_color: 1, 0.84, 0, 1
                                MDIconButton:
                                    icon: "delete-forever"
                                    theme_text_color: "Error"
                                    size_hint_x: None
                                    width: "48dp"
                                    on_release: root.confirm_delete_tournament()
                            MDBoxLayout:
                                id: setup_box
                                orientation: "vertical"
                                adaptive_height: True
                                spacing: "10dp"
                                MDTextField:
                                    id: t_name_in
                                    hint_text: "Tournament Name"
                                    mode: "rectangle"
                                MDTextField:
                                    id: t_count_in
                                    hint_text: "Number of Teams"
                                    mode: "rectangle"
                                    input_filter: "int"
                                MDRaisedButton:
                                    text: "INITIALIZE TEAMS"
                                    size_hint_x: 1
                                    on_release: root.create_team_inputs(t_name_in.text, t_count_in.text)
                                MDBoxLayout:
                                    id: team_inputs_box
                                    orientation: "vertical"
                                    adaptive_height: True
                                MDRaisedButton:
                                    id: start_tourney_btn
                                    text: "START TOURNAMENT"
                                    disabled: True
                                    size_hint_x: 1
                                    on_release: root.start_league()
                            MDLabel:
                                text: root.phase_title
                                theme_text_color: "Custom"
                                text_color: 0.04, 0.7, 0.2, 1
                                halign: "center"
                                size_hint_y: None
                                height: "30dp"
                            MDBoxLayout:
                                id: match_list_box
                                orientation: "vertical"
                                adaptive_height: True
                                spacing: "10dp"
                            MDLabel:
                                text: "STANDINGS"
                                font_style: "Overline"
                                size_hint_y: None
                                height: "24dp"
                            MDBoxLayout:
                                size_hint_y: None
                                height: "220dp"
                                MDCard:
                                    padding: "5dp"
                                    md_bg_color: 0.12, 0.12, 0.12, 1
                                    ScrollView:
                                        MDGridLayout:
                                            id: points_grid
                                            cols: 6
                                            adaptive_height: True
                                            row_default_height: '40dp'
                                            row_force_default: True
                                            size_hint_x: None
                                            width: "480dp"

            MDBottomNavigationItem:
                name: 'no_ball'
                text: 'No Ball'
                icon: 'alert-circle'
                BoxLayout:
                    orientation: 'vertical'
                    canvas.before:
                        Color:
                            rgba: 0.08, 0.08, 0.08, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "10dp"
                        spacing: "8dp"
                        MDLabel:
                            text: "NO BALL REPLAY"
                            font_style: "Overline"
                            theme_text_color: "Custom"
                            text_color: 1, 0.84, 0, 1
                            halign: "center"
                            size_hint_y: None
                            height: "24dp"
                        MDBoxLayout:
                            size_hint_y: None
                            height: "48dp"
                            MDRaisedButton:
                                text: "REPLAY"
                                size_hint_x: 1
                                md_bg_color: 1, 0.84, 0, 1

            MDBottomNavigationItem:
                name: 'contact'
                text: 'Contact Us'
                icon: 'account-box'
                BoxLayout:
                    orientation: 'vertical'
                    canvas.before:
                        Color:
                            rgba: 0.08, 0.08, 0.08, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    ScrollView:
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            padding: "20dp"
                            spacing: "15dp"
                            MDLabel:
                                text: "USER PROFILE"
                                font_style: "Overline"
                                theme_text_color: "Custom"
                                text_color: 0.04, 0.7, 0.2, 1
                                size_hint_y: None
                                height: "24dp"
                            MDCard:
                                adaptive_height: True
                                padding: "15dp"
                                md_bg_color: 0.12, 0.12, 0.12, 1
                                radius: [15]
                                MDBoxLayout:
                                    orientation: "vertical"
                                    adaptive_height: True
                                    MDLabel:
                                        text: "xyz"
                                        font_style: "H6"
                                        size_hint_y: None
                                        height: "36dp"
                                    MDLabel:
                                        text: "Active User"
                                        font_style: "Caption"
                                        theme_text_color: "Hint"
                                        size_hint_y: None
                                        height: "24dp"
                            MDLabel:
                                text: "SUPPORT & SOCIALS"
                                font_style: "Overline"
                                size_hint_y: None
                                height: "24dp"
                            MDRaisedButton:
                                text: "YouTube Channel"
                                size_hint_x: 1
                                md_bg_color: 0.8, 0, 0, 1
                                on_release: root.open_youtube()
                            MDRaisedButton:
                                text: "WhatsApp +91 1234567890"
                                size_hint_x: 1
                                md_bg_color: 0.15, 0.65, 0.15, 1
                                on_release: root.open_whatsapp()

<MatchDetailsScreen>:
    name: 'match_details'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.08, 0.08, 0.08, 1
        MDTopAppBar:
            title: "Live Scorer"
            left_action_items: [["arrow-left", lambda x: setattr(root.manager, 'current', 'main_tabs')]]
            md_bg_color: 0.04, 0.25, 0.1, 1
            size_hint_y: None
            height: "56dp"
        MDBoxLayout:
            orientation: 'vertical'
            padding: "10dp"
            spacing: "8dp"
            MDBoxLayout:
                size_hint_y: None
                height: "80dp"
                orientation: 'vertical'
                MDBoxLayout:
                    size_hint_y: None
                    height: "44dp"
                    spacing: "4dp"
                    MDLabel:
                        text: "Over:"
                        size_hint_x: None
                        width: "45dp"
                        bold: True
                    MDCard:
                        radius: [15]
                        md_bg_color: 0.2, 0.2, 0.2, 1
                        MDLabel:
                            id: b1
                            halign: "center"
                    MDCard:
                        radius: [15]
                        md_bg_color: 0.2, 0.2, 0.2, 1
                        MDLabel:
                            id: b2
                            halign: "center"
                    MDCard:
                        radius: [15]
                        md_bg_color: 0.2, 0.2, 0.2, 1
                        MDLabel:
                            id: b3
                            halign: "center"
                    MDCard:
                        radius: [15]
                        md_bg_color: 0.2, 0.2, 0.2, 1
                        MDLabel:
                            id: b4
                            halign: "center"
                    MDCard:
                        radius: [15]
                        md_bg_color: 0.2, 0.2, 0.2, 1
                        MDLabel:
                            id: b5
                            halign: "center"
                    MDCard:
                        radius: [15]
                        md_bg_color: 0.2, 0.2, 0.2, 1
                        MDLabel:
                            id: b6
                            halign: "center"
                MDBoxLayout:
                    size_hint_y: None
                    height: "36dp"
                    MDLabel:
                        text: str(root.score) + "/" + str(root.wickets)
                        font_style: "H5"
                        bold: True
                    MDLabel:
                        text: "Prev: " + root.previous_score
                        font_style: "Caption"
                        theme_text_color: "Hint"
                    MDLabel:
                        text: "Over: " + root.over_text
                        halign: "right"
                        font_style: "H6"
            MDBoxLayout:
                size_hint_y: None
                height: "64dp"
                spacing: "10dp"
                MDIconButton:
                    icon: "minus-box"
                    on_release: root.prev_ball()
                MDCard:
                    size_hint: None, 1
                    width: "64dp"
                    radius: [32]
                    md_bg_color: 0.04, 0.5, 0.15, 1
                    on_release: root.add_run()
                    MDLabel:
                        text: str(root.ball_number)
                        halign: "center"
                        bold: True
                MDIconButton:
                    icon: "plus-box"
                    on_release: root.next_ball()
            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: "130dp"
                spacing: "8dp"
                MDTextField:
                    hint_text: "Update Striker Name"
                    mode: "rectangle"
                    size_hint_y: None
                    height: "48dp"
                    on_text_validate: root.change_striker_name(self.text); self.text = ""
                MDBoxLayout:
                    spacing: "10dp"
                    MDCard:
                        size_hint_x: 0.65
                        radius: [15]
                        md_bg_color: 0.12, 0.12, 0.12, 1
                        padding: "10dp"
                        MDBoxLayout:
                            orientation: "vertical"
                            MDLabel:
                                text: root.striker
                                bold: True
                            MDLabel:
                                text: root.non_striker
                                theme_text_color: "Hint"
                    MDBoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.35
                        spacing: "5dp"
                        MDCard:
                            size_hint_y: None
                            height: "36dp"
                            radius: [15]
                            md_bg_color: 1, 0.84, 0, 1
                            MDLabel:
                                text: "DRS"
                                halign: "center"
                                bold: True
                                color: 0,0,0,1
                        MDRaisedButton:
                            text: "TRACKING"
                            font_size: "10sp"
                            size_hint_x: 1
                            md_bg_color: 0.04, 0.7, 0.2, 1
            MDGridLayout:
                cols: 3
                size_hint_y: None
                height: "48dp"
                spacing: "8dp"
                MDRaisedButton:
                    text: "WIDE"
                    on_release: root.wide_ball()
                MDRaisedButton:
                    text: "ROTATE"
                    on_release: root.rotate_strike()
                MDRaisedButton:
                    text: "WICKET"
                    md_bg_color: 0.8, 0.1, 0.1, 1
                    on_release: root.wicket()
            MDBoxLayout:
                size_hint_y: None
                height: "48dp"
                spacing: "10dp"
                MDRaisedButton:
                    text: "OVER RESET"
                    md_bg_color: 0.4, 0.4, 0.4, 1
                    on_release: root.reset_game()
                MDRaisedButton:
                    text: "NEXT MATCH"
                    md_bg_color: 0.8, 0.1, 0.1, 1
                    size_hint_x: 1
                    on_release: root.next_match()

<SecondaryCameraScreen>:
    name: 'secondary_camera'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.08, 0.08, 0.08, 1
        MDTopAppBar:
            title: "Secondary Camera"
            left_action_items: [["arrow-left", lambda x: root.back_to_main()]]
            md_bg_color: 0.04, 0.25, 0.1, 1
            size_hint_y: None
            height: "56dp"
        MDBoxLayout:
            id: cam_box
            orientation: 'vertical'
            padding: "8dp"
            spacing: "8dp"
            # Camera4Kivy Preview placeholder
            MDLabel:
                id: rec_status
                text: root.rec_status_text
                halign: "center"
                theme_text_color: "Custom"
                text_color: 1, 0.84, 0, 1
                size_hint_y: None
                height: "36dp"
            MDBoxLayout:
                size_hint_y: None
                height: "52dp"
                spacing: "10dp"
                MDRaisedButton:
                    text: "START REC"
                    size_hint_x: .5
                    md_bg_color: 0.04, 0.7, 0.2, 1
                    on_release: root.start_recording()
                MDRaisedButton:
                    text: "STOP REC"
                    size_hint_x: .5
                    md_bg_color: 0.8, 0.1, 0.1, 1
                    on_release: root.stop_recording()

<PracticeScreen>:
    name: 'practice'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.08, 0.08, 0.08, 1
        MDTopAppBar:
            title: "Net Practice"
            left_action_items: [["arrow-left", lambda x: setattr(root.manager, 'current', 'main_tabs')]]
            md_bg_color: 0.04, 0.25, 0.1, 1
            size_hint_y: None
            height: "56dp"
        MDBoxLayout:
            orientation: 'vertical'
            padding: "10dp"
            spacing: "8dp"
            MDLabel:
                text: "PRACTICE TRACKER"
                font_style: "Overline"
                theme_text_color: "Custom"
                text_color: 0.04, 0.7, 0.2, 1
                halign: "center"
                size_hint_y: None
                height: "24dp"
            MDBoxLayout:
                size_hint_y: None
                height: "48dp"
                spacing: "10dp"
                MDCard:
                    size_hint: None, 1
                    width: "60dp"
                    radius: [15]
                    md_bg_color: 1, 0.84, 0, 1
                    MDLabel:
                        text: "DRS"
                        halign: "center"
                        bold: True
                        color: 0, 0, 0, 1
                MDRaisedButton:
                    text: "START TRACKING"
                    size_hint_x: 1
                    md_bg_color: 0.04, 0.25, 0.1, 1
"""

# ... (MainTabsScreen, MatchDetailsScreen, PracticeScreen classes remain identical to your original code) ...

class MainTabsScreen(Screen):
    tournament_name = StringProperty("")
    phase_title     = StringProperty("LEAGUE STAGE")
    active_matches  = ListProperty([])
    points_data     = DictProperty({})
    current_phase   = StringProperty("league")
    dialog          = None

    def open_youtube(self):  webbrowser.open("https://www.youtube.com/@YourChannelName")
    def open_whatsapp(self): webbrowser.open("https://wa.me/911234567890")

    def load_tournament_data(self):
        try:
            if store.exists('active_tournament'):
                data = store.get('active_tournament')
                self.tournament_name = data['name']
                self.active_matches  = data['matches']
                self.points_data     = data['points']
                self.current_phase   = data['phase']
                self.phase_title     = data['phase_title']
                self.ids.setup_box.opacity  = 0
                self.ids.setup_box.disabled = True
                self.refresh_ui()
        except Exception as e:
            print(f"[load_tournament_data] {e}")

    def save_tournament_data(self):
        store.put('active_tournament',
                  name=self.tournament_name,
                  matches=self.active_matches,
                  points=self.points_data,
                  phase=self.current_phase,
                  phase_title=self.phase_title)

    def confirm_delete_tournament(self):
        self.dialog = MDDialog(
            title="Delete Tournament?",
            text="This will wipe all standings and match history.",
            buttons=[
                MDFlatButton(text="CANCEL",
                             on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="DELETE", md_bg_color=(1,0,0,1),
                               on_release=self.delete_tournament),
            ]
        )
        self.dialog.open()

    def delete_tournament(self, *args):
        if store.exists('active_tournament'):
            store.delete('active_tournament')
        self.tournament_name = ""
        self.active_matches  = []
        self.points_data     = {}
        self.current_phase   = "league"
        self.phase_title     = "LEAGUE STAGE"
        self.ids.setup_box.opacity  = 1
        self.ids.setup_box.disabled = False
        self.ids.match_list_box.clear_widgets()
        self.ids.points_grid.clear_widgets()
        self.dialog.dismiss()

    def create_team_inputs(self, name, count):
        if not name or not count: return
        self.tournament_name = name
        self.ids.team_inputs_box.clear_widgets()
        for i in range(int(count)):
            self.ids.team_inputs_box.add_widget(
                MDTextField(hint_text=f"Team {i+1} Name"))
        self.ids.start_tourney_btn.disabled = False

    def start_league(self):
        teams = [c.text if c.text else f"T{i+1}"
                 for i, c in enumerate(
                     self.ids.team_inputs_box.children[::-1])]
        self.points_data = {t: [0, 0, 0, 0, 0.0] for t in teams}
        self.ids.setup_box.opacity  = 0
        self.ids.setup_box.disabled = True
        pairs = list(itertools.combinations(teams, 2))
        self.active_matches = [[p[0], p[1], "Pending"] for p in pairs]
        self.save_tournament_data()
        self.refresh_ui()

    def refresh_ui(self):
        self.ids.match_list_box.clear_widgets()
        for i, m in enumerate(self.active_matches):
            row = MDBoxLayout(adaptive_height=True, spacing="10dp")
            row.add_widget(
                MDLabel(text=f"{m[0]} vs {m[1]}", font_style="Caption"))
            if m[2] == "Pending":
                row.add_widget(MDRaisedButton(text="SET WIN",
                    on_release=lambda x, idx=i:
                        self.open_result_dialog(idx)))
            else:
                row.add_widget(MDLabel(text=f"Winner: {m[2]}",
                    theme_text_color="Custom",
                    text_color=(1, 0.8, 0, 1)))
            self.ids.match_list_box.add_widget(row)

        self.ids.points_grid.clear_widgets()
        for h in ["Team", "P", "W", "L", "Pts", "NRR"]:
            self.ids.points_grid.add_widget(
                MDLabel(text=h, bold=True, halign="center",
                        font_style="Caption"))
        sorted_table = sorted(self.points_data.items(),
                              key=lambda x: (x[1][3], x[1][4]),
                              reverse=True)
        for team, s in sorted_table:
            self.ids.points_grid.add_widget(
                MDLabel(text=team[:10], halign="center",
                        font_style="Caption"))
            for val in s:
                v_str = f"{val:.2f}" if isinstance(val, float) else str(val)
                self.ids.points_grid.add_widget(
                    MDLabel(text=v_str, halign="center",
                            font_style="Caption"))

    def open_result_dialog(self, idx):
        m = self.active_matches[idx]
        content = MDBoxLayout(orientation="vertical", spacing="10dp",
                              adaptive_height=True)
        self.win_field    = MDTextField(
            hint_text=f"Winner ({m[0]}/{m[1]})")
        self.margin_field = MDTextField(hint_text="Margin Number",
                                        input_filter="int")
        self.type_field   = MDTextField(hint_text="'runs' or 'wickets'")
        for w in [self.win_field, self.margin_field, self.type_field]:
            content.add_widget(w)
        self.dialog = MDDialog(
            title="Enter Match Result", type="custom",
            content_cls=content,
            buttons=[MDFlatButton(text="SUBMIT",
                on_release=lambda x: self.process_result(idx))])
        self.dialog.open()

    def process_result(self, idx):
        winner = self.win_field.text.strip()
        m = self.active_matches[idx]
        if winner not in [m[0], m[1]]: return
        loser = m[0] if winner == m[1] else m[1]
        try:
            margin   = int(self.margin_field.text)
            m_type   = self.type_field.text.lower()
            nrr_gain = (margin / 10.0) if "run" in m_type else float(margin)
            self.active_matches[idx][2] = winner
            if self.current_phase == "league":
                self.points_data[winner][0] += 1
                self.points_data[winner][1] += 1
                self.points_data[winner][3] += 2
                self.points_data[loser][0]  += 1
                self.points_data[loser][2]  += 1
                self.points_data[winner][4] += nrr_gain
                self.points_data[loser][4]  -= nrr_gain
            self.save_tournament_data()
            self.dialog.dismiss()
            self.refresh_ui()
            self.check_progression()
        except Exception as e:
            print(f"[process_result] {e}")

    def check_progression(self):
        if all(m[2] != "Pending" for m in self.active_matches):
            if self.current_phase == "league":
                self.setup_semis()
            elif self.current_phase == "semis":
                self.setup_final()
            self.save_tournament_data()

    def setup_semis(self):
        sorted_teams = sorted(self.points_data.items(),
                              key=lambda x: (x[1][3], x[1][4]),
                              reverse=True)
        t = [x[0] for x in sorted_teams[:4]]
        if len(t) < 4:
            self.setup_final()
            return
        self.active_matches = [
            [t[0], t[3], "Pending"],
            [t[1], t[2], "Pending"]]
        self.current_phase = "semis"
        self.phase_title   = "SEMI-FINALS"
        self.refresh_ui()

    def setup_final(self):
        winners = ([m[2] for m in self.active_matches]
                   if self.current_phase == "semis"
                   else list(self.points_data.keys())[:2])
        self.active_matches = [[winners[0], winners[1], "Pending"]]
        self.current_phase  = "final"
        self.phase_title    = "GRAND FINAL"
        self.refresh_ui()

class MatchDetailsScreen(Screen):
    score             = NumericProperty(0)
    wickets           = NumericProperty(0)
    previous_score    = StringProperty("N/A")
    over              = NumericProperty(0)
    ball_in_over      = NumericProperty(0)
    over_text         = StringProperty("0.0")
    ball_number       = NumericProperty(0)
    striker_name      = StringProperty("Batsman 1")
    non_striker_name  = StringProperty("Batsman 2")
    striker_runs      = NumericProperty(0)
    non_striker_runs  = NumericProperty(0)
    striker_balls     = NumericProperty(0)
    non_striker_balls = NumericProperty(0)
    striker           = StringProperty("Batsman 1 - 0 (0)")
    non_striker       = StringProperty("Batsman 2 - 0 (0)")

    def update_batsman_text(self):
        self.striker = (f"{self.striker_name} - "
                        f"{self.striker_runs} ({self.striker_balls})")
        self.non_striker = (f"{self.non_striker_name} - "
                            f"{self.non_striker_runs} "
                            f"({self.non_striker_balls})")

    def change_striker_name(self, name):
        if name.strip():
            self.striker_name = name
            self.update_batsman_text()

    def add_run(self):
        run = self.ball_number
        self.score        += run
        self.striker_runs += run
        self.striker_balls += 1
        self.update_batsman_text()
        self._increment_ball(str(run))

    def _increment_ball(self, val):
        ball_id = f"b{self.ball_in_over + 1}"
        if ball_id in self.ids:
            self.ids[ball_id].text = val
        if self.ball_in_over < 5:
            self.ball_in_over += 1
        else:
            self.over += 1
            self.ball_in_over = 0
            Clock.schedule_once(self.clear_over_boxes, 1.0)
        self.over_text = f"{self.over}.{self.ball_in_over}"

    def clear_over_boxes(self, dt):
        for i in range(1, 7):
            self.ids[f"b{i}"].text = ""

    def wide_ball(self):
        self.score += 1

    def wicket(self):
        self.wickets      += 1
        self.striker_balls += 1
        self._increment_ball("W")
        self.update_batsman_text()

    def rotate_strike(self):
        self.striker_name,    self.non_striker_name  = \
            self.non_striker_name,  self.striker_name
        self.striker_runs,    self.non_striker_runs  = \
            self.non_striker_runs,  self.striker_runs
        self.striker_balls,   self.non_striker_balls = \
            self.non_striker_balls, self.striker_balls
        self.update_batsman_text()

    def next_ball(self):
        if self.ball_number < 6:
            self.ball_number += 1

    def prev_ball(self):
        if self.ball_number > 0:
            self.ball_number -= 1

    def reset_game(self):
        self.previous_score = (f"{self.score}/{self.wickets} "
                               f"({self.over_text})")
        self.score = self.wickets = self.over = \
            self.ball_in_over = self.ball_number = 0
        self.striker_runs  = self.non_striker_runs  = 0
        self.striker_balls = self.non_striker_balls = 0
        self.over_text = "0.0"
        self.update_batsman_text()
        self.clear_over_boxes(0)

    def next_match(self):
        self.reset_game()
        self.previous_score = "N/A"

class PracticeScreen(Screen):
    pass

# ─────────────────────────────────────────────────────────────────────────────
# SECONDARY CAMERA WITH CAMERA4KIVY
# ─────────────────────────────────────────────────────────────────────────────


class SecondaryCameraScreen(Screen):
    rec_status_text = StringProperty("Waiting...")
    from kivy.utils import platform
    from camera4kivy import Preview
    def on_enter(self):
        # We delay the camera setup to let the ScreenManager transition finish
        Clock.schedule_once(self.request_android_permissions, 0.5)

    def request_android_permissions(self, dt):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA, 
                Permission.RECORD_AUDIO,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ], self.permission_callback)
        else:
            self.setup_camera()

    def permission_callback(self, permissions, grants):
        if all(grants):
            self.setup_camera()
        else:
            self.rec_status_text = "Permission Denied by User"

    def setup_camera(self):
        try:
            # Check if preview already exists to avoid double-adding
            if not hasattr(self, 'preview') or self.preview is None:
                self.preview = Preview(aspect_ratio='16:9')
                self.ids.cam_box.add_widget(self.preview, index=1)
            
            self.preview.connect_camera(enable_video=True, enable_audio=True)
            self.rec_status_text = "Camera Ready"
        except Exception as e:
            self.rec_status_text = f"Startup Error: {e}"

    def start_recording(self):
        if hasattr(self, 'preview') and self.preview:
            # It saves to /DCIM/Camera4Kivy by default
            self.preview.video_record()
            self.rec_status_text = "● RECORDING"

    def stop_recording(self):
        if hasattr(self, 'preview') and self.preview:
            self.preview.video_stop()
            self.rec_status_text = "Saved to Gallery ✓"

    def back_to_main(self):
        self.cleanup_camera()
        self.manager.current = 'main_tabs'

    def cleanup_camera(self):
        if hasattr(self, 'preview') and self.preview:
            self.preview.disconnect_camera()
            self.ids.cam_box.remove_widget(self.preview)
            self.preview = None

    def on_leave(self):
        self.cleanup_camera()


class CricketApp(MDApp):
    def build(self):
        self.theme_cls.theme_style     = "Dark"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

if __name__ == '__main__':
    CricketApp().run()
