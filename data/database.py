import sqlite3
import os

class Database:
    def __init__(self, db_name="tictactoe.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Statistics Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                games_played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0
            )
        ''')
        
        # Achievements Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                name TEXT PRIMARY KEY,
                unlocked INTEGER DEFAULT 0
            )
        ''')

        # Settings Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                theme TEXT DEFAULT 'classic',
                sound_enabled INTEGER DEFAULT 1,
                music_enabled INTEGER DEFAULT 1,
                dark_mode INTEGER DEFAULT 0
            )
        ''')

        # Initialize default rows if they don't exist
        cursor.execute('SELECT COUNT(*) FROM statistics')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO statistics (games_played) VALUES (0)')

        cursor.execute('SELECT COUNT(*) FROM settings')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO settings (theme) VALUES ("classic")')

        # Default achievements
        achievements_list = [
            'First Win', '10 Wins', '50 Wins', '100 Wins', 
            'Unbeatable Champion', 'Winning Streak', 'Perfect Victory'
        ]
        for ach in achievements_list:
            cursor.execute('INSERT OR IGNORE INTO achievements (name, unlocked) VALUES (?, 0)', (ach,))

        conn.commit()
        conn.close()

    def get_stats(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT games_played, wins, losses, draws, best_streak, current_streak FROM statistics WHERE id = 1')
        row = cursor.fetchone()
        conn.close()
        return {
            "games_played": row[0],
            "wins": row[1],
            "losses": row[2],
            "draws": row[3],
            "best_streak": row[4],
            "current_streak": row[5]
        } if row else {}

    def update_stats(self, result):
        stats = self.get_stats()
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        games_played = stats['games_played'] + 1
        wins = stats['wins']
        losses = stats['losses']
        draws = stats['draws']
        current_streak = stats['current_streak']
        best_streak = stats['best_streak']

        if result == 'win':
            wins += 1
            current_streak += 1
            if current_streak > best_streak:
                best_streak = current_streak
        elif result == 'loss':
            losses += 1
            current_streak = 0
        elif result == 'draw':
            draws += 1
            current_streak = 0

        cursor.execute('''
            UPDATE statistics 
            SET games_played=?, wins=?, losses=?, draws=?, current_streak=?, best_streak=?
            WHERE id = 1
        ''', (games_played, wins, losses, draws, current_streak, best_streak))
        conn.commit()
        conn.close()
        self.check_achievements(wins, current_streak)

    def check_achievements(self, wins, current_streak):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        if wins >= 1:
            cursor.execute('UPDATE achievements SET unlocked = 1 WHERE name = "First Win"')
        if wins >= 10:
            cursor.execute('UPDATE achievements SET unlocked = 1 WHERE name = "10 Wins"')
        if wins >= 50:
            cursor.execute('UPDATE achievements SET unlocked = 1 WHERE name = "50 Wins"')
        if wins >= 100:
            cursor.execute('UPDATE achievements SET unlocked = 1 WHERE name = "100 Wins"')
        if current_streak >= 5:
            cursor.execute('UPDATE achievements SET unlocked = 1 WHERE name = "Winning Streak"')
            
        conn.commit()
        conn.close()

    def get_achievements(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT name, unlocked FROM achievements')
        rows = cursor.fetchall()
        conn.close()
        return [{"name": r[0], "unlocked": bool(r[1])} for r in rows]

    def get_settings(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT theme, sound_enabled, music_enabled, dark_mode FROM settings WHERE id = 1')
        row = cursor.fetchone()
        conn.close()
        return {
            "theme": row[0],
            "sound_enabled": bool(row[1]),
            "music_enabled": bool(row[2]),
            "dark_mode": bool(row[3])
        } if row else {}

    def update_settings(self, theme=None, sound_enabled=None, music_enabled=None, dark_mode=None):
        settings = self.get_settings()
        theme = theme if theme is not None else settings.get('theme', 'classic')
        sound = sound_enabled if sound_enabled is not None else settings.get('sound_enabled', True)
        music = music_enabled if music_enabled is not None else settings.get('music_enabled', True)
        dark = dark_mode if dark_mode is not None else settings.get('dark_mode', False)

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE settings
            SET theme=?, sound_enabled=?, music_enabled=?, dark_mode=?
            WHERE id = 1
        ''', (theme, int(sound), int(music), int(dark)))
        conn.commit()
        conn.close()
