from pygame import *
import sys
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.flag = True
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class MovementHero(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if (keys_pressed[K_a] or keys_pressed[K_LEFT]) and self.rect.x>0:
            self.rect.x -= self.speed
        if (keys_pressed[K_d] or keys_pressed[K_RIGHT]) and self.rect.x< 640:
            self.rect.x += self.speed
        if (keys_pressed[K_w] or keys_pressed[K_UP]) and self.rect.y > 0:
            self.rect.y -= self.speed
        if (keys_pressed[K_s] or keys_pressed[K_DOWN]) and self.rect.y < 440:
            self.rect.y += self.speed

class MovementCyborg(GameSprite):
    def move(self):
        if self.rect.x <= 500:
            self.flag = True
        if self.rect.x >= 640:
            self.flag = False
        if self.flag:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height

        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))

        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20, 10, 380)
w4 = Wall(154, 205, 50, 200, 130, 10, 350)
w5 = Wall(154, 205, 50, 450, 130, 10, 360)
w6 = Wall(154, 205, 50, 300, 20, 10, 350)
w7 = Wall(154, 205, 50, 390, 120, 130, 10)

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render("YOU LOSE!", True, (180, 0, 0))
restart = font.render('Нажми R для перезапуска', True, (180, 0, 0))
quit_button = font.render('Нажми Q для выхода', True, (0,180,0))

packman = MovementHero('hero.png', 5, win_height - 80, 4)
monster = MovementCyborg('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)
lose = font.render('YOU LOSE!', True, (255, 0, 0))
game = True
finish = False
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('jungles.ogg')
kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')
mixer.music.play()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
    if finish != True:
        window.blit(background,(0,0))
        packman.move()
        monster.move()

        packman.reset()
        monster.reset()
        final.reset()
    
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()

        if sprite.collide_rect(packman, monster) or sprite.collide_rect(packman, w1) or sprite.collide_rect(packman, w2) or sprite.collide_rect(packman, w3) or sprite.collide_rect(packman, w4) or sprite.collide_rect(packman, w5) or sprite.collide_rect(packman, w6) or sprite.collide_rect(packman, w7):
            finish = True
            window.blit(lose, (200,200))
            window.blit(restart, (25,300))
            window.blit(quit_button,(75, 400))
            kick.play()

        if sprite.collide_rect(packman, final):
            finish = True
            window.blit(win ,(200,200))
            window.blit(restart, (25,300))
            window.blit(quit_button,(75, 400))
            money.play()
        
    keys_pressed = key.get_pressed()
    if keys_pressed[K_r]:
        finish = False
        packman = MovementHero('hero.png', 5, win_height - 80, 4)
        monster = MovementCyborg('cyborg.png', win_width - 80, 280, 2)
        display.update()

    if keys_pressed[K_q]:
        game = False

    display.update()
    clock.tick(FPS)