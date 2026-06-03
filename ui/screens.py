from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.clock import Clock
from ui.components import GameBoard
from core.game_logic import GameLogic
from core.ai_engine import AIEngine
from kivy.properties import StringProperty
import random

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        title = MDLabel(
            text="TIC TAC TOE\nPRO", 
            halign="center", 
            font_style="H3",
            theme_text_color="Primary"
        )
        layout.add_widget(title)

        btns = [
            ("Single Player", "mode_selection"),
            ("Multiplayer", "multiplayer_setup"),
            ("Statistics", "stats"),
            ("Achievements", "achievements"),
            ("Settings", "settings"),
            ("Exit", "exit")
        ]

        for text, action in btns:
            btn = MDFillRoundFlatButton(
                text=text, 
                pos_hint={"center_x": .5},
                size_hint_x=0.8,
                font_size=dp(20)
            )
            btn.bind(on_release=lambda x, a=action: self.handle_action(a))
            layout.add_widget(btn)

        self.add_widget(layout)

    def handle_action(self, action):
        if action == "exit":
            from kivy.app import App
            App.get_running_app().stop()
        elif action == "mode_selection":
            self.manager.current = "mode_selection"
        elif action == "multiplayer_setup":
            app = from_app()
            app.game_mode = "multiplayer"
            app.player1_name = "Player 1"
            app.player2_name = "Player 2"
            self.manager.current = "game"
        elif action == "stats":
            self.manager.current = "stats"
        elif action == "achievements":
            self.manager.current = "achievements"
        elif action == "settings":
            self.manager.current = "settings"

def from_app():
    from kivy.app import App
    return App.get_running_app()

class ModeSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        layout.add_widget(MDLabel(text="Select Difficulty", halign="center", font_style="H4"))

        difficulties = ["Easy", "Medium", "Hard", "Expert", "Impossible"]
        for diff in difficulties:
            btn = MDFillRoundFlatButton(
                text=diff, 
                pos_hint={"center_x": .5},
                size_hint_x=0.8
            )
            btn.bind(on_release=lambda x, d=diff: self.start_single_player(d))
            layout.add_widget(btn)

        back_btn = MDFlatButton(text="Back", pos_hint={"center_x": .5})
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'main_menu'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def start_single_player(self, difficulty):
        app = from_app()
        app.game_mode = "singleplayer"
        app.difficulty = difficulty.lower()
        app.player1_name = "You"
        app.player2_name = f"AI ({difficulty})"
        self.manager.current = "game"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header (Scores, Turn info)
        self.header = MDBoxLayout(size_hint_y=0.2)
        self.info_label = MDLabel(text="Turn: X", halign="center", font_style="H5")
        self.header.add_widget(self.info_label)
        self.layout.add_widget(self.header)

        # Game Board
        self.board_widget = GameBoard(size=3, size_hint_y=0.6)
        self.layout.add_widget(self.board_widget)

        # Controls
        controls = MDBoxLayout(size_hint_y=0.2, spacing=dp(10), padding=dp(10))
        undo_btn = MDFillRoundFlatButton(text="Undo")
        undo_btn.bind(on_release=self.undo_move)
        
        restart_btn = MDFillRoundFlatButton(text="Restart")
        restart_btn.bind(on_release=self.restart_game)

        back_btn = MDFlatButton(text="Menu")
        back_btn.bind(on_release=self.go_to_menu)

        controls.add_widget(undo_btn)
        controls.add_widget(restart_btn)
        controls.add_widget(back_btn)
        
        self.layout.add_widget(controls)
        self.add_widget(self.layout)

        self.game_logic = GameLogic(size=3)
        self.ai_engine = None
        self.dialog = None

    def on_enter(self):
        app = from_app()
        self.game_logic.reset_game()
        self.board_widget.reset_highlights()
        
        if app.game_mode == "singleplayer":
            self.ai_engine = AIEngine(difficulty=app.difficulty)
        else:
            self.ai_engine = None
            
        self.bind_cells()
        self.update_ui()

    def bind_cells(self):
        for i in range(self.game_logic.size):
            for j in range(self.game_logic.size):
                self.board_widget.cells[i][j].bind(on_release=self.on_cell_clicked)

    def on_cell_clicked(self, instance):
        if self.game_logic.winner:
            return

        app = from_app()
        if app.game_mode == "singleplayer" and self.game_logic.current_player == 'O':
            return # AI's turn

        row, col = instance.row, instance.col
        
        if self.game_logic.make_move(row, col):
            self.update_ui()
            self.check_game_over()
            
            if not self.game_logic.winner and app.game_mode == "singleplayer":
                # Schedule AI move
                Clock.schedule_once(self.make_ai_move, 0.5)

    def make_ai_move(self, dt):
        if not self.game_logic.winner:
            move = self.ai_engine.get_best_move(self.game_logic.board, self.game_logic.current_player)
            if move:
                self.game_logic.make_move(move[0], move[1])
                self.update_ui()
                self.check_game_over()

    def update_ui(self):
        app = from_app()
        theme_colors = {'x_color': (1, 0.2, 0.2, 1), 'o_color': (0.2, 0.6, 1, 1)}
        self.board_widget.update_board(self.game_logic.board, theme_colors)
        
        if self.game_logic.winner:
            if self.game_logic.winner == 'Draw':
                self.info_label.text = "It's a Draw!"
            else:
                self.info_label.text = f"{self.game_logic.winner} Wins!"
                self.board_widget.draw_winning_line(self.game_logic.winning_line)
        else:
            current_name = app.player1_name if self.game_logic.current_player == 'X' else app.player2_name
            self.info_label.text = f"Turn: {current_name} ({self.game_logic.current_player})"

    def check_game_over(self):
        if self.game_logic.winner:
            app = from_app()
            
            result_for_stats = 'draw'
            if self.game_logic.winner == 'X':
                result_for_stats = 'win'
            elif self.game_logic.winner == 'O':
                result_for_stats = 'loss' if app.game_mode == 'singleplayer' else 'draw' # Multiplayer stats logic can be adapted
            
            # Update stats
            app.db.update_stats(result_for_stats)
            
            # Show Dialog
            self.dialog = MDDialog(
                title="Game Over",
                text=self.info_label.text,
                buttons=[
                    MDFlatButton(text="Menu", on_release=lambda x: self.go_to_menu()),
                    MDFillRoundFlatButton(text="Play Again", on_release=lambda x: self.restart_game())
                ],
            )
            self.dialog.open()

    def undo_move(self):
        app = from_app()
        if self.game_logic.undo_move():
            if app.game_mode == 'singleplayer':
                self.game_logic.undo_move() # Undo AI move as well
            self.board_widget.reset_highlights()
            self.update_ui()

    def restart_game(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
        self.game_logic.reset_game()
        self.board_widget.reset_highlights()
        self.update_ui()

    def go_to_menu(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
        self.manager.current = "main_menu"


class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        self.layout.add_widget(MDLabel(text="Statistics", font_style="H4", halign="center", size_hint_y=0.2))
        
        self.stats_label = MDLabel(text="", halign="center")
        self.layout.add_widget(self.stats_label)

        back_btn = MDFlatButton(text="Back", pos_hint={"center_x": .5})
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'main_menu'))
        self.layout.add_widget(back_btn)
        
        self.add_widget(self.layout)

    def on_enter(self):
        app = from_app()
        stats = app.db.get_stats()
        text = f"Games Played: {stats.get('games_played', 0)}\n"
        text += f"Wins: {stats.get('wins', 0)}\n"
        text += f"Losses: {stats.get('losses', 0)}\n"
        text += f"Draws: {stats.get('draws', 0)}\n"
        text += f"Current Streak: {stats.get('current_streak', 0)}\n"
        text += f"Best Streak: {stats.get('best_streak', 0)}\n"
        self.stats_label.text = text


class AchievementsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        self.layout.add_widget(MDLabel(text="Achievements", font_style="H4", halign="center", size_hint_y=0.2))
        
        self.ach_label = MDLabel(text="", halign="center")
        self.layout.add_widget(self.ach_label)

        back_btn = MDFlatButton(text="Back", pos_hint={"center_x": .5})
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'main_menu'))
        self.layout.add_widget(back_btn)
        
        self.add_widget(self.layout)

    def on_enter(self):
        app = from_app()
        achievements = app.db.get_achievements()
        text = ""
        for a in achievements:
            status = "🏆 (Unlocked)" if a['unlocked'] else "🔒 (Locked)"
            text += f"{status} {a['name']}\n\n"
        self.ach_label.text = text


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        self.layout.add_widget(MDLabel(text="Settings", font_style="H4", halign="center", size_hint_y=0.2))
        
        # Dark mode toggle
        self.theme_btn = MDFillRoundFlatButton(text="Toggle Dark/Light Mode", pos_hint={"center_x": .5})
        self.theme_btn.bind(on_release=self.toggle_theme)
        self.layout.add_widget(self.theme_btn)

        back_btn = MDFlatButton(text="Back", pos_hint={"center_x": .5})
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'main_menu'))
        self.layout.add_widget(back_btn)
        
        self.add_widget(self.layout)

    def toggle_theme(self, instance):
        app = from_app()
        if app.theme_cls.theme_style == "Dark":
            app.theme_cls.theme_style = "Light"
            app.db.update_settings(dark_mode=False)
        else:
            app.theme_cls.theme_style = "Dark"
            app.db.update_settings(dark_mode=True)
