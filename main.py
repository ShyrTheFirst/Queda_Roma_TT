import pygame, sys, random, math

#Iniciar o pygame
pygame.init()
#Iniciar a fonte
pygame.font.init()

#fontes para o jogo
font = pygame.font.SysFont('Arial', 30)


#Inicializar tela do jogo
Tela_H = 1280
Tela_V = 720
tela = pygame.display.set_mode((Tela_H,Tela_V))
pygame.display.set_caption('Concept')
frames = pygame.time.Clock()

#Game Loop
running = True

#variaveis do jogo
villa_col = False
shoot_speed = 1 #### DEFINE A VELOCIDADE DO TIRO
enemy_speed = 1 #### DEFINE A VELOCIDADE DOS INIMIGOS
score = 0 #### DEFINE O SCORE DO JOGO
money = 0 #### DEFINE O DINHEIRO QUE POSSUI

#Grupos de Sprites
shoot_g = pygame.sprite.Group()
villa_g = pygame.sprite.Group()
enemy_g = pygame.sprite.Group()
upgrades_g = pygame.sprite.Group()

#####################################################################################################Classes#####################################################################################################


class Enemy(pygame.sprite.Sprite):
    def __init__(self,posx,posy,speed):
        super().__init__()
        self.image = pygame.image.load(r'enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.rect.x = posx
        self.rect.y = posy
        self.speed = speed #### MUDAR VELOCIDADE DOS INIMIGOS
        self.alvo = (Tela_H//2,Tela_V//2)
        self.value = 1
        self.damage = 1
        

    def update(self):
        global score
        if score > 1:
            self.value = (score//2 * 3)//score
            self.damage = self.value

            min_speed = 1
            new_speed = score/100
            max_speed = 3
            if new_speed < min_speed :
                self.speed = min_speed
            elif new_speed > max_speed:
                self.speed = max_speed
            else:
                self.speed = new_speed
            
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
        self.rect.x = (Tela_H//2) - 40
        self.rect.y = (Tela_V//2) - 40
        self.circle_color = (150,0,0)
        self.radius = 150 #### MUDAR RADIUS DA VILLA PARA DETECTAR INIMIGOS
        self.max_enemy = 1 #### MUDAR A QUANTIDADE DE INIMIGOS AO MESMO TEMPO NA TELA
        self.health = 10
        self.max_health = 10

    def update(self):
        global score
        circle = pygame.draw.circle(tela, self.circle_color, (Tela_H//2, Tela_V//2), self.radius, 1)
        if score > 2:
            if score % 2 == 0:
                self.max_health = score * 2 // self.max_enemy
                self.health = self.max_health
        
        if self.max_health > 200:
            self.max_health = 200
        if self.health > self.max_health:
            self.health = self.max_health
        frac_health = int((80*self.health)/self.max_health)
        pygame.draw.rect(tela,(255,0,0), (self.rect.x,self.rect.y - 10,frac_health,1))

    def Shoot_start(self,enemy):
        global score, money
        if score > 4:
            self.max_enemy = score//4
            if self.max_enemy > 20:
                self.max_enemy = 20
        
        if math.sqrt(pow(Tela_H//2 - enemy.rect.x, 2) + pow(Tela_V//2 - enemy.rect.y, 2)) < self.radius:
            if len(shoot_g) < 1:
                for enemy in enemy_g:
                    self.shoot = Shoot(enemy)
                    shoot_g.add(self.shoot)
                    break
            shooting_collide = pygame.sprite.spritecollide(self.shoot,enemy_g,False)
            if shooting_collide:
                for sprites in shooting_collide:
                    money += sprites.value
                    sprites.kill()
                    self.shoot.kill()
                score += 1
                
        else:
            if len(enemy_g) < 1:
                for shoots in shoot_g:
                    shoots.kill()
            
            
            


class Shoot(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        self.image = pygame.image.load(r'shoot.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.rect.x = Tela_H//2
        self.rect.y = Tela_V//2
        self.speed = 1 #### MUDAR VELOCIDADE DO TIRO
        self.enemy = enemy

    def update(self,speed):
            if villa_col == True:
                if self.speed < 10:
                    self.speed = 10
            else:
                self.speed = speed 
                
            enemy_pos = [self.enemy.rect.x, self.enemy.rect.y]
            self_pos = self.rect
            dxdef,dydef = enemy_pos[0] - self_pos[0] , enemy_pos[1] - self_pos[1]
            distdef = (dxdef**2 + dydef**2) ** 0.5
            if distdef != 0:
                dxdef,dydef = dxdef/distdef, dydef/distdef
            dxdef_final, dydef_final = dxdef*self.speed, dydef*self.speed
            self.rect.x += dxdef_final
            self.rect.y += dydef_final
            
            tela.blit(self.image, (self.rect.x,self.rect.y))


class Upgrades(pygame.sprite.Sprite):
    def __init__(self,villa,x,y,typeup):
        super().__init__()
        self.image = pygame.image.load(r'botao.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.villa = villa
        self.typeup = typeup
        self.nivel = 1
        self.custo = 5
        

    def update(self):
        global money, score, shoot_speed
        if self.typeup == 'Speed':
            self.image = pygame.image.load(r'botao_speed.png')
            custo_text = font.render('Custo: ' + str(self.custo), True, (100,100,100))
            tela.blit(custo_text, (self.rect.x + 70, self.rect.y))
            '''score_text = font.render('Score: ' + str(score), True, (100,100,100))
    tela.blit(score_text, (Tela_V - score_text.get_width()-50, 10))
    '''
            if self.custo > money:
                pass ####Mudar imagem dos botoes
        if self.typeup == 'Radius':
            self.image = pygame.image.load(r'botao_radius.png')
            custo_text = font.render('Custo: ' + str(self.custo), True, (100,100,100))
            tela.blit(custo_text, (self.rect.x + 70, self.rect.y))
            if self.custo > money:
                pass ####Mudar imagem dos botoes

        

        ####CRIAR CUSTO PARA BLITAR AO LADO DE CADA BOTAO#### rect.x + 70 deve ser suficiente, rect.y pode ser o mesmo ou + metade do tamanho do botao para ficar ao meio da imagem
            
        if pygame.mouse.get_pressed() == (1,0,0):
            mousepos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mousepos):
                if self.typeup == 'Speed' :
                    if money >= self.custo :
                        money -= self.custo
                        self.custo += self.nivel * (2 + score)//self.nivel
                        self.nivel += 1
                        shoot_speed += 1
                        ####RETORNO VISUAL DA COMPRA
                        print("Comprou speed")
                    elif money < self.custo:
                        pass
                elif self.typeup == 'Radius':
                    if money >= self.custo :
                        money -= self.custo
                        self.custo += self.nivel * (10 + score)//self.nivel
                        self.nivel += 1
                        self.villa.radius += 10
                        ####RETORNO VISUAL DA COMPRA
                        print("Comprou radius")
                    elif money < self.custo:
                        pass
            


#####################################################################################################Classes#####################################################################################################



#Inicializar classes
enemy_a = Enemy(random.randint(-100,-1),random.randint(0,719),enemy_speed)
enemy_g.add(enemy_a)

villa_a = Villa()
villa_g.add(villa_a)

upgrades_a1 = Upgrades(villa_a,10,10, 'Speed')
upgrades_a2 = Upgrades(villa_a,10,80, 'Radius')
upgrades_g.add(upgrades_a1)
upgrades_g.add(upgrades_a2)

#Rodar loop do jogo
while running:    
    #Preencher tela do jogo
    tela.fill((100,0,0)) 

    #Detectar eventos do pygame
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

    #Gerar novos inimigos, conforme variavel de limite de inimigos
    if len(enemy_g) < villa_a.max_enemy:
            enemy_new = Enemy(random.randint(-100,-1),random.randint(0,719),enemy_speed) ####### PRECISO GERAR INIMIGOS FORA DA TELA, EM QUALQUER POSIÇÃO FORA DA TELA
            enemy_g.add(enemy_new)

    #Detectar colisão dos inimigos com a Villa
    sprites = pygame.sprite.spritecollide(villa_a,enemy_g,False)
    if sprites:
        for enemy in sprites:
            villa_a.health -= enemy.damage
            enemy.kill()

    #Detecta se o tiro está dentro da Villa
    if len(enemy_g) > 0:
        villa_colisao = pygame.sprite.spritecollide(villa_a,shoot_g,False)
        if villa_colisao:
            villa_col = True
        else:
            villa_col = False

    #Impede que os tiros saiam do raio
    for shoots in shoot_g:
        if math.sqrt(pow(Tela_H//2 - shoots.rect.x, 2) + pow(Tela_V//2 - shoots.rect.y, 2)) > villa_a.radius:
            shoots.kill()

    #Desenhar sprites na tela
    shoot_g.draw(tela)
    villa_g.draw(tela)
    upgrades_g.draw(tela)
    if len(enemy_g) > 0:
        enemy_g.draw(tela)
    

    

    #atualizar posição dos inimigos para irem em direção ao centro e tiro para ir em direção aos inimigos
    shoot_g.update(shoot_speed)
    if len(enemy_g) > 0:
        enemy_g.update()
    villa_g.update()
    upgrades_g.update()

    #Atualizar informações de defesa contra os inimigos
    if len(enemy_g) > 0:
        for enemy in enemy_g:
            villa_a.Shoot_start(enemy)

    #Mostrar texto do Score na tela
    score_text = font.render('Score: ' + str(score), True, (100,100,100))
    tela.blit(score_text, (Tela_V - score_text.get_width()-50, 10))
    money_text = font.render('Money: ' + str(money), True, (100,100,100))
    tela.blit(money_text,(Tela_V - money_text.get_width()-50,50))
    
        

    #Definir FPS
    frames.tick(60)

    #Atualizar tela
    pygame.display.update()

