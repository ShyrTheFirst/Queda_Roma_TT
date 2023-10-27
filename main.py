import pygame, sys, random

pygame.init()
Tela_H = 1280
Tela_V = 720
tela = pygame.display.set_mode((Tela_H,Tela_V))
pygame.display.set_caption('Concept')

frames = pygame.time.Clock()

#test_rect = pygame.Rect(100,0,50,50) #(posx,posy,alt,larg)
#pygame.draw.rect(tela,(255,0,0),test_rect)

#pygame.display.update()

running = True


class Enemy(pygame.sprite.Sprite):
    def __init__(self,posx,posy,speed):
        super().__init__()
        self.image = pygame.image.load(r'enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.rect.x = posx
        self.rect.y = posy
        self.speed = speed
        self.alvo = (Tela_H//2,Tela_V//2)

    def update(self):
        player_pos = self.alvo
        enemy_pos = self.rect.center
        dx, dy = player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.dx, self.dy = dx * self.speed, dy * self.speed
        self.rect.x += self.dx
        self.rect.y += self.dy

class Villa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'villa.png').convert_alpha()
        self.rect = self.image.get_rect()
        #self.pos = pygame.math.Vector2(self.rect.topleft)
        self.rect.x = (Tela_H//2) - 40
        self.rect.y = (Tela_V//2) - 40
        self.circle_color = (150,0,0)
        self.radius = 200

    def update(self):
        pygame.draw.circle(tela, self.circle_color, (Tela_H//2, Tela_V//2), self.radius, 1)        


enemy_a = Enemy(random.randrange(0,Tela_H),random.randrange(0,Tela_V),1)
enemy_g = pygame.sprite.Group()
enemy_g.add(enemy_a)

villa_a = Villa()
villa_g = pygame.sprite.Group()
villa_g.add(villa_a)


while running:
    tela.fill((100,0,0))
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()
    if len(enemy_g) < 3:
        for i in range(0,len(enemy_g)):
            enemy_new = Enemy(random.randrange(Tela_H,Tela_H+100),random.randrange(Tela_V,Tela_V+100),1)
            enemy_g.add(enemy_new)

    sprites = pygame.sprite.spritecollide(villa_a,enemy_g,False)
    if sprites:
        for enemy in sprites:
            enemy.kill()

    villa_g.draw(tela)
    enemy_g.draw(tela)
    villa_g.update()
    enemy_g.update()
    frames.tick(60)
    pygame.display.update()

