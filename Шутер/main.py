from pygame import *
from random import randint

mixer.init()
mixer.music.load('Music.mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1)

fire_sound_1 = mixer.Sound('el_primo_atk_05.ogg')
fire_sound_2 = mixer.Sound('el_primo_atk_04.ogg')
fire_sound_3 = mixer.Sound('el_primo_atk_03.ogg')
fire_sound_4 = mixer.Sound('el_primo_atk_02.ogg')
fire_sound_5 = mixer.Sound('el_primo_atk_01.ogg')

fire_sound_5.set_volume(0.04)
fire_sound_4.set_volume(0.04)
fire_sound_3.set_volume(0.04)
fire_sound_2.set_volume(0.04)
fire_sound_1.set_volume(0.04)

fire_sounds = [fire_sound_1, fire_sound_2, fire_sound_3, fire_sound_4,fire_sound_5]

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)

win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True,(180,0,0))

IMG_BACK = "background.jpg"
IMG_HERO = "El_Primo.png"
IMG_ENEMY = "Shelly.png"
IMG_BULLET = "bullet.png"

score = 0
lost = 0
goal  = 10
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if (keys_pressed[K_a] or keys_pressed[K_LEFT]) and self.rect.x>5:
            self.rect.x -= self.speed
        if (keys_pressed[K_d] or keys_pressed[K_RIGHT]) and self.rect.x< win_width-80:
            self.rect.x += self.speed

    def fire(self):
        bullet  = Bullet(IMG_BULLET, self.rect.centerx, self.rect.top, 15,  20,  -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost +=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()

win_width = 1000
win_height  = 800
window = display.set_mode((win_width, win_height))
display.set_caption("Brawl Stars Shooter")
background = transform.scale(image.load(IMG_BACK), (win_width, win_height))

ship = Player(IMG_HERO, 5, win_height  - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(IMG_ENEMY, randint(80, win_width - 80), -40, 50, 75, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

finish  = False
run = True

while run:
    for e  in event.get():
        if e.type == QUIT:
            run = False
        elif e.type  == KEYDOWN:
            if e.key == K_SPACE:
                fire_sounds[randint(0,4)].play()
                ship.fire()

    if not finish:
        window.blit(background,(0,0))

        text = font2.render("Счёт: " + str(score), True, (0, 0, 0))
        window.blit(text, (10,100))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (0, 0, 0))
        window.blit(text_lose, (10,130))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters,  bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(IMG_ENEMY, randint(80, win_width-80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters,  False) or lost >= max_lost:
            finish  = True
            window.blit(lose, (200,200))

        if score >= goal:
            finish =  True
            window.blit(win, (200,200))

        display.update()
    time.delay(50)
