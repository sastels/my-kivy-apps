from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock
import itertools
from random import randint


COLS = 50
ROWS = 50
STEP_DELAY_SECONDS = 0.5


class Cell(Label):
    alive = NumericProperty(0)
    alive_nearby = 0

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.alive = 0
        self.alive_nearby = 0

    def update(self):
        if self.alive:
            if self.alive_nearby < 2 or self.alive_nearby > 3:
                self.alive = 0
        else:
            if self.alive_nearby == 3:
                self.alive = 1


class GameBoard(GridLayout):
    cols = COLS
    rows = ROWS

    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)
        self.gameGrid = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        for row, col in itertools.product(range(self.rows), range(self.cols)):
            self.add_widget(self.gameGrid[row][col])

    def restart(self):
        for row, col in itertools.product(range(self.rows), range(self.cols)):
            self.gameGrid[row][col].alive = int(randint(0, int(1 / float(self.parent.density_input.text))) == 0)

    def refresh_counts(self):
        for target_row, target_col in itertools.product(range(self.rows), range(self.cols)):
            target_cell = self.gameGrid[target_row][target_col]
            target_cell.alive_nearby = 0
            for row, col in itertools.product(range(target_row - 1, target_row + 2),
                                              range(target_col - 1, target_col + 2)):
                if row >= 0 and col >= 0 and row < self.rows and col < self.cols:
                    target_cell.alive_nearby += self.gameGrid[row][col].alive
            target_cell.alive_nearby -= target_cell.alive

    def update(self):
        self.refresh_counts()
        for target_row, target_col in itertools.product(range(self.rows), range(self.cols)):
            self.gameGrid[target_row][target_col].update()


class Game(BoxLayout):

    def restart(self):
        self.game_board.restart()

    def update(self, _):
        self.game_board.update()


class LifeApp(App):
    def build(self):
        game = Game()
        Clock.schedule_interval(game.update, STEP_DELAY_SECONDS)
        game.restart()
        return game


if __name__ == "__main__":
    LifeApp().run()
