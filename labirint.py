# Разработай свою игру в этом файле!
from pygame import*
from random import*
window = display.set_mode((500, 500))

class GameSprite(sprite.Sprite):
# конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
    # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
    # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
 
    # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
# метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_x_speed,player_y_speed):
        GameSprite.__init__(self,player_image,player_x,player_y,size_x,size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        if player.rect.x <= win_width-80 and player.x_speed > 0 or player.rect.x >= 0 and player.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self,barriers,False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if player.rect.y <= win_height-80 and player.y_speed > 0 or player.rect.y >= 0 and player.y_speed < 0:
            self.rect.y += self.y_speed
            platforms_touched = sprite.spritecollide(self,barriers,False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom,p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top,p.rect.bottom)

    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = 'left'
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        GameSprite.__init__(self,player_image,player_x,player_y,size_x,size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'           
        if self.rect.x >= win_width -85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed



class Bullet(GameSprite):
 def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
     GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
     self.speed = player_speed
 def update(self):
     self.rect.x += self.speed
     if self.rect.x > win_width+10:
         self.kill()

win_width = 700
win_height = 500
display.set_caption("Лабиринт")   
window = display.set_mode((win_width, win_height))
back = (100, 100, 100)

barriers = sprite.Group()
bullets = sprite.Group()
enemys = sprite.Group()
 
w1 = GameSprite('platform2.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)

barriers.add(w1)
barriers.add(w2)

player = Player('pacmen.png',5,win_height - 80,80,80,0,0) 
enemy1 = Enemy('enemy.png',450,100,80,80,5)
enemy2 = Enemy('enemy.png',450,200,80,80,5)
enemys.add(enemy1)
enemys.add(enemy2)
finish_sprite = GameSprite('finish.jpg',win_width - 90, win_height -100,80,80)
 
finish = False

run = True
while run:
 
 time.delay(50)
  
 for e in event.get():
      if e.type == QUIT:
          run = False
      elif e.type == KEYDOWN:
          if e.key == K_LEFT:
              player.x_speed = -5
          elif e.key == K_RIGHT:
              player.x_speed = 5
          elif e.key == K_UP:
              player.y_speed = -5
          elif e.key == K_DOWN:
              player.y_speed = 5
          elif e.key == K_SPACE:
             player.fire()
 
      elif e.type == KEYUP:
          if e.key == K_LEFT:
              player.x_speed = 0
          elif e.key == K_RIGHT:
              player.x_speed = 0
          elif e.key == K_UP:
              player.y_speed = 0
          elif e.key == K_DOWN:
              player.y_speed = 0
 

 if not finish:
     
     window.fill(back)
    
     
     player.update()
     bullets.update()
 
      
     player.reset()
     
     w1.reset()
     w2.reset()
     bullets.draw(window)
     barriers.draw(window)
     finish_sprite.reset()
 
     sprite.groupcollide(enemys, bullets, True, True)
     enemys.update()
     enemys.draw(window)
     sprite.groupcollide(bullets, barriers, True, False)
 
     
     if sprite.spritecollide(player, enemys, False):
         finish = True
         
         img = image.load('lose.png')
         d = img.get_width() // img.get_height()
         window.fill((255, 255, 255))
         window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
 
     if sprite.collide_rect(player, finish_sprite):
         finish = True
         img = image.load('win.jpg')
         window.fill((255, 255, 255))
         window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
 display.update()