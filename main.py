from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from data.database import Database
from ui.screens import MainMenuScreen, ModeSelectionScreen, GameScreen, StatsScreen, AchievementsScreen, SettingsScreen
from kivy.core.window import Window
from kivy.metrics import dp

# Configure mobile screen size for desktop testing (Optional, but good for preview)
Window.size = (360, 640)

class TicTacToeApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database("tictactoe.db")
        self.game_mode = "singleplayer" # "singleplayer" or "multiplayer"
        self.difficulty = "easy"
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"

    def build(self):
        # Set theme based on settings
        settings = self.db.get_settings()
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark" if settings.get("dark_mode", True) else "Light"

        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(ModeSelectionScreen(name='mode_selection'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(StatsScreen(name='stats'))
        sm.add_widget(AchievementsScreen(name='achievements'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm

if __name__ == '__main__':
    TicTacToeApp().run()
