import sys
from pygame import *
import random


#constants
wind_size = (700, 500)
fps = 60
label_coo = (200, 200)

player_size = [50, 70]
player_x = (200, 500)
player_y = 430
player_speed = 5

enemy_size = [70, 50]
enemy_speed = (1, 3)

bullet_size = [5, 10]
bullet_speed = 5

but_text_color = (0, 0, 0)
but_fill_color = (0, 102, 0)
but_width = 100
but_height = 20


#variables
game = True
score = 0
missed = 0
lifes = 3


#setup
init()

wind = display.set_mode(wind_size)
timer = time.Clock()

back = transform.scale(image.load('galaxy.jpg'), wind_size)

mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

text = font.Font(None, 20)


#classes
class GameSprite(sprite.Sprite):
    def __init__(self, x, y, size, image_name):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (size))
        self.rect = Rect([x, y] + size)
    
    def drow(self):
        wind.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self):
        super().__init__(random.randint(player_x[0], player_x[1]), player_y, player_size, 'rocket.png')
    
    def move(self):
        self.drow()
        keys = key.get_pressed()
        if keys[K_a]:
            if self.rect.x >= 5:
                self.rect.x -= player_speed
        if keys[K_d]:
            if self.rect.x <= 645:
                self.rect.x += player_speed
        if keys[K_SPACE]:
            bullets.add(Bullet(self.rect.x))
            fire.play(0)
    

class Enemy(GameSprite):
    def __init__(self):
        super().__init__(random.randint(0, wind_size[0]), 0, enemy_size, 'ufo.png')
        self.speed = random.randint(enemy_speed[0], enemy_speed[1])
    
    def reset(self):
        self.rect.y = 0
        self.rect.x = random.randint(0, wind_size[0])
        self.speed = random.randint(enemy_speed[0], enemy_speed[1])
    
    def update(self):
        global missed
        global score
        self.drow()
        self.rect.y += self.speed
        if self.rect.y >= 450:
            self.reset()
            missed += 1
        
        for s in sprite.spritecollide(self, bullets, False):
            self.reset()
            score += 1
    

class Bullet(GameSprite):
    def __init__(self, x):
        super().__init__(x + 22, 450, bullet_size, 'bullet.png')
    
    def update(self):
        self.drow()
        self.rect.y -= bullet_speed
        if self.rect.y <= 0:
            self.kill()


class Button(GameSprite):
    def __init__(self, text, x, y, func):
        self.image = main_font.render(text, False, but_text_color, but_fill_color)
        self.rect = Rect(x, y, but_width, but_height)
        self.func = func

    def update(self, eve):
        self.drow()
        if eve.type == MOUSEBUTTONDOWN:
            if eve.button == 1:
                if self.rect.collidepoint(eve.pos):
                    self.func()
    

#obgects
player = Player()
enemies = sprite.Group(Enemy(), Enemy(), Enemy(), Enemy(), Enemy())
bullets = sprite.Group()
main_font = font.Font(None, 50)
win_label = main_font.render('YOU WIN', False, (255, 0, 0))
lose_label = main_font.render('YOU LOSE', False, (0, 0, 0))


#loops
def exit():
    quit()
    sys.exit()

def menu_loop():
    buttons = [Button('exit', 300, 200, exit),
               Button('play', 300, 250, game_loop)]
    while True:
        display.update()

        wind.blit(back, (0, 0))
        for ev in event.get():
            for but in buttons:
                but.update(ev)

        timer.tick(fps)

def game_loop():
    global game
    global lifes
    while game:
        display.update()

        wind.blit(back, (0,0))
        player.move()
        enemies.update()
        bullets.update()
        wind.blit(text.render('score:' + str(score), False, (255, 255, 255)), (0, 0))
        wind.blit(text.render('missed:' + str(missed), False, (255, 255, 255)), (0, 20))
        wind.blit(text.render('lives::' + str(lifes), False, (255, 255, 255)), (0, 40))

        for eve in event.get():
            if eve.type == QUIT:
                game = False
    
        if score >= 10:
            wind.blit(win_label, label_coo)
            display.update()
            timer.tick(2)
            game = False

        if missed >= 3 or lifes <= 0:
            wind.blit(lose_label, label_coo)
            display.update()
            timer.tick(2)
            game = False

        enemies_collide = sprite.spritecollide(player, enemies, False)
        if len(enemies_collide) > 0:
            lifes -= 1
            for enemy in enemies_collide:
                enemy.reset()

        timer.tick(fps)

if __name__ == "__main__":
    menu_loop()