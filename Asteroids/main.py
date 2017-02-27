from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ObjectProperty, ReferenceListProperty
from kivy.clock import Clock
import random
from kivy.graphics.vertex_instructions import Triangle
from kivy.vector import Vector
from kivy.core.window import Window
import string

ROTATE_STEP = 10
FRICTION_FACTOR = 0.95
ROCK_INTERVAL = 0.5
SCORE_TIME = 1.0

class Rock(Label):

    angle = NumericProperty(0)
    velocity = Vector(0, 0)
    rotation_velocity = 0

    def __init__(self, pos, velocity=(1, 1), **kwargs):
        super(Rock, self).__init__(**kwargs)
        self.velocity = Vector(velocity)
        self.rotation_velocity = ROTATE_STEP * random.random() / 2
        self.pos = pos
        self.text = random.choice(string.letters)
        self.color = (random.random(), random.random(), random.random(), 1)

    def move(self):
        self.pos = self.velocity + self.pos
        self.angle += self.rotation_velocity

class Ship(Widget):
    velocity = Vector(0, 0)
    angle = NumericProperty(0)

    def move(self):
        self.pos = self.velocity + self.pos
        self.velocity *= FRICTION_FACTOR
#        if self.velocity.length() < 0.1:
#            self.velocity = Vector(0, 0)
        if self.pos[0] < self.parent.x:
            self.pos[0] = self.parent.right
        if self.pos[0] > self.parent.right:
            self.pos[0] = self.parent.x
        if self.pos[1] < self.parent.y:
            self.pos[1] = self.parent.top
        if self.pos[1] > self.parent.top:
            self.pos[1] = self.parent.y

    def rotate_left(self):
        self.angle += ROTATE_STEP

    def rotate_right(self):
        self.angle -= ROTATE_STEP

    def fire_engine(self):
        self.velocity += Vector(0, 10).rotate(self.angle)


class GameScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.rock = None

    def add_rock(self):
        y = random.randint(self.y, self.top)
        x = random.randint(self.x, self.right)
        velocity_x = 2 + random.random() - 1
        velocity_y = 2 + random.random() - 1
        side = random.randint(0, 4)
        if side == 0:
            x = self.x - 100
            velocity_x = abs(velocity_x)
        elif side == 1:
            x = self.right + 100
            velocity_x = -abs(velocity_x)
        elif side == 2:
            y = self.y - 100
            velocity_y = abs(velocity_y)
        else:
            y = self.top + 100
            velocity_y = -abs(velocity_y)
        self.rock = Rock(pos=(x, y), velocity=(velocity_x, velocity_y))
        self.add_widget(self.rock)

    def clean_up_rocks(self):
        for entity in self.children:
            if entity.x < self.x - 200 or entity.x > self.right + 200:
                self.remove_widget(entity)
            if entity.y < self.y - 200 or entity.y > self.top + 200:
                self.remove_widget(entity)

    def move_objects(self):
        for entity in self.children:
            entity.move()

    def ship_rock_collision(self):
        for entity in self.children:
            if entity != self.ship:
                if entity.collide_widget(self.ship):
                    return True
        return False


class Game(BoxLayout):

    score = NumericProperty(0)

    def __init__(self):
        super(Game, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'q':
            self.ship.rotate_left()
        elif keycode[1] == 'w':
            self.ship.rotate_right()
        elif keycode[1] == 'e':
            self.ship.fire_engine()
        return True

    def restart(self):
        self.rock_timer = 0.0
        self.score = 0

    def update(self, dt):
        self.game_screen.move_objects()
        self.game_screen.clean_up_rocks()

        if self.game_screen.ship_rock_collision():
            self.restart()

        self.rock_timer += dt
        if self.rock_timer >= ROCK_INTERVAL:
            self.game_screen.add_rock()
            self.rock_timer = 0.0

        self.score += dt

class AsteroidsApp(App):

    def build(self):
        game = Game()
        game.restart()

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    AsteroidsApp().run()
