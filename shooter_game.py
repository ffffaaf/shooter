from pygame import *
from random import *
from time import time as timer
font.init()

window_wight = 700
window_height = 500
font = font.SysFont('Arial' , 40)
health = 3
text_lose = font.render('ВЫ ПРОИГРАЛИ!', 1 , (255 , 0 , 0))
text_win = font.render('ВЫ ПОБЕДИЛИ!' , 1 , (0 , 255 , 0))
text_health = font.render(str(health) , 1 , (255 , 255 , 255))
score = 0
lost = 0
color_1 = (0 , 255 , 0)
color_2 = (255 , 255 , 0)
color_3 = (255 , 0  , 0)
num_fire = 0
real_time = False

window = display.set_mode((window_wight , window_height))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg') , (window_wight , window_height))

mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
fire = mixer.Sound('fire.ogg')

game = True
clock = time.Clock()
FPS = 40

class GameSprite(sprite.Sprite):
    def __init__(self , player_x , player_y , player_image , player_speed , size_x , size_y):
        super().__init__()
        self.speed = player_speed
        self.image = transform.scale(image.load(player_image) , (size_x , size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image , (self.rect.x , self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 395:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(self.rect.centerx , self.rect.top ,'bullet.png' , -15  , 15 , 20 )
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y  > window_height:
            self.rect.x = randint(80 , window_wight - 80)
            self.rect.y = - 50
            lost = lost + 1

class Bullet(GameSprite):
   def update(self):
       self.rect.y += self.speed
       if self.rect.y < 0:
           self.kill()

ship = Player(200 , 420 , 'rocket.png' , 6 , 50 , 80)
monsters = sprite.Group()
monsters_speed = 0
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(6):
    monster = Enemy(randint(80 , window_height - 80) , -50 , 'ufo.png' , randint(0 , 15)/10 + 2 , 60 , 40 )
    monsters.add(monster)
for i in range(3):
    asteroid = Enemy(randint(80 , window_height - 80) , -50 , 'asteroid.png' , randint(0 , 15)/10 + 2 , 60 , 40)
    asteroids.add(asteroid)


finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_time == False:
                    ship.fire()
                    num_fire += 1
                if num_fire >= 5 and real_time == False:
                    real_time = True
                    last_time = timer()

                #fire.play()
    if finish != True:
        window.blit(background , (0 , 0))
        text_lost = font.render('Пропущено: ' +str(lost) , 1 , (255 , 255 , 255))
        text_score = font.render('Счёт: ' +str(score) , 1 , (255 , 255 , 255))
        
        window.blit(text_lost , (10 , 50))
        window.blit(text_score , (10 , 20))
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        ship.update()
        ship.reset()

        if real_time == True:
            now_time = timer()
            if now_time - last_time < 2:
                text_reload = font.render('Подождите, перезарядка!' , 1 , (255 , 0 , 0))
                window.blit(text_reload , (150 , 460))
            else:
                num_fire = 0
                real_time = False
        sprites_list = sprite.groupcollide(monsters , bullets , True , True)
        sprite.groupcollide(asteroids , bullets , False , True)

        for s in sprites_list:
            score += 1
            monster = Enemy(randint(80 , window_height - 80) , -50 , 'ufo.png' , randint(0 , 15)/10 + 2 + score//10 , 60 , 40 )
            monsters.add(monster)
            #fire.play()
        if sprite.spritecollide(ship , monsters , True) or sprite.spritecollide(ship , asteroids , True):
            health -= 1
        if health == 0 or lost >= 3:
            finish = True
            window.blit(text_lose , (200 , 250))
        if health == 3:
            text_health = font.render(str(health) , 1 , (color_1))
        if health == 2:
            text_health = font.render(str(health) , 1 , (color_2))
        if health == 1:
            text_health = font.render(str(health) , 1 , (color_3))
        window.blit(text_health , (650 , 10))

        display.update()

    clock.tick(FPS)

