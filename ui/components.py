from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line

class CellButton(MDFillRoundFlatButton):
    row = NumericProperty(0)
    col = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = ""
        self.font_size = dp(40)
        self.md_bg_color = (0.2, 0.2, 0.2, 1) # Default dark background
        self.text_color = (1, 1, 1, 1)
        self.radius = [dp(15)]
        
    def set_symbol(self, symbol, theme_colors):
        self.text = symbol
        if symbol == 'X':
            self.text_color = theme_colors.get('x_color', (1, 0.3, 0.3, 1))
        elif symbol == 'O':
            self.text_color = theme_colors.get('o_color', (0.3, 0.8, 1, 1))

class GameBoard(GridLayout):
    def __init__(self, size=3, **kwargs):
        super().__init__(**kwargs)
        self.cols = size
        self.rows = size
        self.padding = dp(10)
        self.spacing = dp(10)
        self.cells = []
        self._build_board()

    def _build_board(self):
        self.clear_widgets()
        self.cells = []
        for i in range(self.rows):
            row_cells = []
            for j in range(self.cols):
                btn = CellButton(row=i, col=j)
                self.add_widget(btn)
                row_cells.append(btn)
            self.cells.append(row_cells)

    def update_board(self, board_state, theme_colors):
        for i in range(self.rows):
            for j in range(self.cols):
                symbol = board_state[i][j]
                self.cells[i][j].set_symbol(symbol, theme_colors)

    def draw_winning_line(self, winning_line):
        # This will add a canvas line over the winning cells. Simple implementation:
        for r, c in winning_line:
            self.cells[r][c].md_bg_color = (0.4, 0.8, 0.4, 1) # Highlight win

    def reset_highlights(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].md_bg_color = (0.2, 0.2, 0.2, 1)
