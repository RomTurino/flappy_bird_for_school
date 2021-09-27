import random

import arcade

# задаем ширину, высоту и заголовок окна

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
SCREEN_TITLE: str = "flappy bird"


class Bird(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__(1)
        self.textures.append(arcade.load_texture('sprites/bluebird-downflap.png'))
        self.textures.append(arcade.load_texture('sprites/bluebird-midflap.png'))
        self.textures.append(arcade.load_texture('sprites/bluebird-upflap.png'))
        self.center_x = 50
        self.center_y = SCREEN_HEIGHT / 2
        self.angle = 0
        self.hit_sound = arcade.load_sound('audio/hit.wav')
        self.wing_sound = arcade.load_sound('audio/wing.wav')

    def update(self):
        self.center_y += self.change_y
        self.angle += self.change_angle
        self.change_y -= 0.4
        if self.center_y < 0:
            self.center_y = 0
        if self.center_y > SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT
        self.change_angle -= 0.4
        if self.angle >= 40:
            self.angle = 40
        if self.angle <= -30:
            self.angle = -30


# noinspection PyTypeChecker
class PipeTop(arcade.Sprite):
    def update(self):
        self.center_x -= self.change_x
        if self.right < 0:
            self.left = SCREEN_WIDTH
            self.center_y = random.randint(SCREEN_HEIGHT - SCREEN_HEIGHT / 8, SCREEN_HEIGHT)



class PipeBottom(arcade.Sprite):
    def update(self):
        self.center_x -= self.change_x
        if self.right < 0:
            self.left = SCREEN_WIDTH
            self.center_y = random.randint(0, SCREEN_HEIGHT / 8)
            arcade.play_sound(window.point_sound, 0.2)


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bird = Bird()
        self.bg = arcade.load_texture('bg.png')
        self.grass = arcade.load_texture('grass.png')
        self.endgame = arcade.load_texture('sprites/gameover.png')
        self.pipelist = arcade.SpriteList()
        self.game = True
        self.point_sound = arcade.load_sound('audio/point.wav')

    def setup(self):
        for i in range(6):
            pipe_top = PipeTop('pipe2.png', 0.2, flipped_vertically=True)
            pipe_top.center_x = 150 * i+SCREEN_WIDTH
            pipe_top.center_y = random.randint(SCREEN_HEIGHT - SCREEN_HEIGHT / 8, SCREEN_HEIGHT)
            pipe_top.change_x = 4
            self.pipelist.append(pipe_top)
            pipe_bottom = PipeBottom('pipe2.png', 0.2)
            pipe_bottom.center_x = 150 * i+SCREEN_WIDTH
            pipe_bottom.center_y = random.randint(0, SCREEN_HEIGHT / 8)
            pipe_bottom.change_x = 4
            self.pipelist.append(pipe_bottom)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        self.pipelist.draw()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.grass)
        self.bird.draw()
        if not self.game:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, self.endgame.width, self.endgame.height, self.endgame)

    def update(self, delta_time):
        if self.game:
            self.bird.update_animation()
            self.bird.update()
            self.pipelist.update()
            hit_list = arcade.check_for_collision_with_list(self.bird, self.pipelist)
            if len(hit_list) > 0 and self.game:
                self.game = False
                arcade.play_sound(self.bird.hit_sound, 0.2)
                self.bird.change_y=-10
                for pipe in self.pipelist:
                    pipe.stop()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.SPACE and self.game:
            self.bird.change_y = 5
            self.bird.change_angle = 5
            arcade.play_sound(self.bird.wing_sound, 0.2)



window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
import tkinter
tkinter.END