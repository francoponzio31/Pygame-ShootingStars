import pygame, random
from constantes import *

# -------------------------- FONDO ----------------------------

class Fondo():

    def __init__(self): 
        self.image = pygame.image.load("data\Background.png").convert()
        self.rect = self.image.get_rect()       
        self.fondo_1_coord_x = 0
        self.fondo_2_coord_x = self.rect.width
        self.fondo_speed_x = 7.7

    def impresion_y_scroll(self, objeto_pantalla):

        # Impresion fondo 1:
        objeto_pantalla.blit(self.image,(self.fondo_1_coord_x, 0))
        if self.fondo_1_coord_x <= 0:
            self.fondo_2_coord_x = self.fondo_1_coord_x + self.rect.width

        # Impresion fondo 2:
        objeto_pantalla.blit(self.image,(self.fondo_2_coord_x, 0))    
        if self.fondo_2_coord_x <= 0:
            self.fondo_1_coord_x = self.fondo_2_coord_x + self.rect.width

        # Desplazamiento:
        self.fondo_1_coord_x -= self.fondo_speed_x    
        self.fondo_2_coord_x -= self.fondo_speed_x  
        

# ------------------------- NAVE JUGADOR -------------------------------

class Jugador(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data\space_ship.png").convert_alpha()
        self.coord_x = -180
        self.coord_y = 300
        self.speed_x = 2
        self.speed_y = 0 
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 100
        self.movimiento_habilitado = False
        self.disparo_normal_habilitado = False
        self.super_disparo_habilitado = False

    def desplazamiento(self):

        # Bloqueo el movimiento del jugador para que no se salga de la pantalla:
        if self.coord_x <= 0 and self.speed_x < 0:
            self.speed_x = 0
        if self.coord_x >= (ANCHO_PANTALLA-self.rect.width) and self.speed_x > 0:
            self.speed_x = 0    
        if self.coord_y <= 0 and self.speed_y < 0:
            self.speed_y = 0   
        if self.coord_y >= (ALTO_PANTALLA-self.rect.height) and self.speed_y > 0:
            self.speed_y = 0  

        # Desplazamiento:
        self.coord_x +=self.speed_x
        self.coord_y +=self.speed_y
        self.rect.x, self.rect.y = self.coord_x, self.coord_y

# ----------------------- CLASES DISPARO  ------------------------

class Disparo_jugador(pygame.sprite.Sprite):

    def __init__(self, nave):
        super().__init__()
        self.image = pygame.image.load("data\Disparo_jugador.png").convert_alpha()
        self.sfx = pygame.mixer.Sound("data\Disparo_jugador.wav")
        self.coord_x = nave.coord_x + nave.rect.width*0.9
        self.coord_y = nave.coord_y + nave.rect.height*0.585
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_x = 6

    def desplazamiento(self):
        self.coord_x += self.speed_x
        self.rect.x, self.rect.y = self.coord_x, self.coord_y

        if self.coord_x > (ANCHO_PANTALLA + 40):
            self.kill()

class Super_disparo_jugador(pygame.sprite.Sprite):

    def __init__(self, nave):
        super().__init__()
        self.image = pygame.image.load("data\Super_disparo_jugador.png").convert_alpha()
        self.sfx = pygame.mixer.Sound("data\Disparo_jugador.wav")
        self.coord_x = nave.coord_x + nave.rect.width*0.88
        self.coord_y = nave.coord_y + nave.rect.height*0.44
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_x = 6

    def desplazamiento(self):
        self.coord_x += self.speed_x
        self.rect.x, self.rect.y = self.coord_x, self.coord_y

        if self.coord_x > (ANCHO_PANTALLA + 40):
            self.kill()

class Disparo_enemigo_1(pygame.sprite.Sprite):

    def __init__(self, nave):
        super().__init__()
        self.image = pygame.image.load("data\Disparo_nave_enemiga_1.png").convert_alpha()
        self.coord_x = nave.coord_x + nave.rect.width*0.2
        self.coord_y = nave.coord_y + nave.rect.height*0.82
        self.speed_x = 9.2
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 10
        self.score_revenue = 5
        self.damage = 10

    def desplazamiento(self):
        self.coord_x -= self.speed_x
        self.rect.x, self.rect.y = self.coord_x, self.coord_y

        if self.coord_x < -40:
            self.kill()


class Disparo_enemigo_2(pygame.sprite.Sprite):

    def __init__(self, nave):
        super().__init__()
        self.image = pygame.image.load("data\Disparo_nave_enemiga_2.png").convert_alpha()
        self.coord_x = nave.coord_x + nave.rect.width*0.3
        self.coord_y = nave.coord_y + nave.rect.height*0.66
        self.speed_x = 8
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 10
        self.score_revenue = 5
        self.damage = 20

    def desplazamiento(self):
        self.coord_x -= self.speed_x
        self.rect.x, self.rect.y = self.coord_x, self.coord_y

        if self.coord_x < -40:
            self.kill()


#------------------------ METEOROS ------------------------------

# Clase meteoro:
class Meteoro(pygame.sprite.Sprite):

    def __init__(self): 
        super().__init__()
        self.image = pygame.image.load("data\meteoro.png").convert_alpha()
        self.coord_x = random.randint(1500,1600)
        self.coord_y = random.randint(20,620)
        self.speed_x = random.uniform(4, 6)   
        self.speed_y = random.uniform(-0.2, 0.3)   
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())    
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 50
        self.score_revenue = 50
        self.damage = 30
        self.random_reward = random.randint(1,12)

    def desplazamiento(self):
        self.coord_x -= self.speed_x
        self.coord_y -= self.speed_y
        self.rect.x, self.rect.y = self.coord_x, self.coord_y

        if self.coord_x < -100:
            self.kill()



#--------------------------- ITEMS ------------------------------

class Item(pygame.sprite.Sprite):

    def __init__(self, coord_x, coord_y): 
        super().__init__()
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.speed_x = 4   

    def desplazamiento(self):
        self.coord_x -= self.speed_x
        self.rect.x, self.rect.y = self.coord_x, self.coord_y

        if self.coord_x < -100:
            self.kill()

class Score_bonus_item(Item):
    def __init__(self, coord_x, coord_y):
        super().__init__(coord_x, coord_y)
        self.image = pygame.image.load("data\Score_bonus_item.png").convert_alpha()
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())    
        self.mask = pygame.mask.from_surface(self.image)

    def item_efect(self, score):
        score += 150
        return score

class Health_item(Item):
    def __init__(self, coord_x, coord_y):
        super().__init__(coord_x, coord_y)
        self.image = pygame.image.load("data\Health_item.png").convert_alpha()
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())    
        self.mask = pygame.mask.from_surface(self.image)

    def item_efect(self, salud):
        if salud <= 200:
            salud += 20
        return salud

class Super_shot_item(Item):
    def __init__(self, coord_x, coord_y):
        super().__init__(coord_x, coord_y)
        self.image = pygame.image.load("data\Super_shot_item.png").convert_alpha()
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())    
        self.mask = pygame.mask.from_surface(self.image)

#------------------------ ENEMIGOS ------------------------------

class Robot_enemigo(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image =  pygame.image.load("data\Robot_enemigo.png").convert_alpha()
        self.coord_x = random.randint(1400,1600)
        self.coord_y = random.randint(40,600)
        self.speed_x = 3
        self.speed_y = 0 
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 90
        self.score_revenue = 80
        self.damage = 40

    def patron_de_movimiento(self, jugador, lista_disparos):
    
        # Patron de movimiento:
        if self.coord_x < ANCHO_PANTALLA-100:
            if self.coord_y < jugador.coord_y - 2:
                self.speed_y = 0.8
            elif self.coord_y > jugador.coord_y + 2:
                self.speed_y = -0.8   
            else:
                self.speed_y = 0  

        # Desplazamiento:
        self.coord_x -= self.speed_x
        self.coord_y += self.speed_y
        self.rect.x, self.rect.y = self.coord_x, self.coord_y

        if self.coord_x < -200:
            self.kill()



class Nave_enemiga_tipo_1(pygame.sprite.Sprite):
 
    def __init__(self):
        super().__init__()
        self.image =  pygame.image.load("data\Enemigo_1.png").convert_alpha()
        self.coord_x = random.randint(1400,1600)
        self.coord_y = random.randint(40,600)
        self.speed_x = 3.5
        self.speed_y = 0 
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 40
        self.score_revenue = 80
        self.damage = 20
        self.indicador_etapa_patron_de_movimiento = 0

    def patron_de_movimiento(self, jugador, lista_disparos):

        # PATRON DE MOVIMIENTO:    
        # Habilito el patron de movimiento una vez que el enemigo entra en pantalla:
        if (self.coord_x < ANCHO_PANTALLA-180):

            # Etapa de movimiento vertical:
            if self.indicador_etapa_patron_de_movimiento == 0:
                self.indicador_etapa_patron_de_movimiento += 1
                self.instante_de_inicio_etapa = pygame.time.get_ticks()

                self.speed_x = 1
                if self.coord_y < jugador.coord_y:
                    self.speed_y = 2
                elif self.coord_y > jugador.coord_y:
                    self.speed_y = -2 
                else:
                    self.speed_y = 0     

            if self.indicador_etapa_patron_de_movimiento == 1:            
                if (round(pygame.time.get_ticks()-self.instante_de_inicio_etapa) >= 1000) or (self.speed_y < 0 and self.coord_y <= 0) or (self.speed_y > 0 and self.coord_y >= ALTO_PANTALLA - self.rect.height):
                    self.speed_x = 0
                    self.speed_y = 0
                    self.indicador_etapa_patron_de_movimiento += 1


            # Si la coordenada x de la nave es menor que ña del jugador se saltea la etapa de disparo:
            if self.indicador_etapa_patron_de_movimiento == 2 and self.coord_x < jugador.coord_x :
                if round(pygame.time.get_ticks()-self.instante_de_inicio_etapa) >= 1500:
                    self.indicador_etapa_patron_de_movimiento = 0
                 
            # Etapa de disparo:
            if self.indicador_etapa_patron_de_movimiento == 2 and self.coord_x >= jugador.coord_x :
                if round(pygame.time.get_ticks()-self.instante_de_inicio_etapa) >= 1200:
                    disparo = Disparo_enemigo_1(self)
                    lista_disparos.add(disparo)
                    self.indicador_etapa_patron_de_movimiento += 1
            if self.indicador_etapa_patron_de_movimiento == 3:
                if round(pygame.time.get_ticks()-self.instante_de_inicio_etapa) >= 1600:
                    disparo = Disparo_enemigo_1(self)
                    lista_disparos.add(disparo)
                    self.indicador_etapa_patron_de_movimiento += 1
            if self.indicador_etapa_patron_de_movimiento == 4:
                if round(pygame.time.get_ticks()-self.instante_de_inicio_etapa) >= 2000:
                    disparo = Disparo_enemigo_1(self)
                    lista_disparos.add(disparo)
                    self.indicador_etapa_patron_de_movimiento += 1        
            if self.indicador_etapa_patron_de_movimiento == 5:
                if round(pygame.time.get_ticks()-self.instante_de_inicio_etapa) >= 2400:
                    self.indicador_etapa_patron_de_movimiento = 0

        # Desplazamiento:
        self.coord_x -= self.speed_x
        self.coord_y += self.speed_y
        self.rect.x, self.rect.y = self.coord_x, self.coord_y


class Nave_enemiga_tipo_2(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image =  pygame.image.load("data\Enemigo_2.png").convert_alpha()
        self.coord_x = random.randint(1400,1600)
        self.coord_y = random.randint(40,600)
        self.speed_x = 1.5
        self.speed_y = 0 
        self.rect = pygame.Rect(self.coord_x, self.coord_y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 70
        self.score_revenue = 100
        self.damage = 40
        self.indicador_etapa_patron_de_movimiento = 0

    def patron_de_movimiento(self, jugador, lista_disparos):

        # PATRON DE MOVIMIENTO:
        # Habilito el patron de movimiento una vez que el enemigo entra en pantalla:
        if (self.coord_x < ANCHO_PANTALLA-180):

            self.speed_x = 0

            # Etapa de movimiento vertical:
            if self.indicador_etapa_patron_de_movimiento == 0:
                self.indicador_etapa_patron_de_movimiento += 1
                self.instante_de_inicio_etapa = pygame.time.get_ticks()

                if self.coord_y < jugador.coord_y:
                    self.speed_y = 0.6
                elif self.coord_y > jugador.coord_y:
                    self.speed_y = -0.6
                else:
                    self.speed_y = 0     

            if self.indicador_etapa_patron_de_movimiento == 1:            
                if (round(pygame.time.get_ticks()-self.instante_de_inicio_etapa) >= 2100) or (self.speed_y < 0 and self.coord_y <= 0) or (self.speed_y > 0 and self.coord_y >= ALTO_PANTALLA - self.rect.height):
                    self.speed_y = 0
                    self.indicador_etapa_patron_de_movimiento += 1

            # Etapa de disparo:
            if self.indicador_etapa_patron_de_movimiento == 2:
                if round(pygame.time.get_ticks()-self.instante_de_inicio_etapa) >= 2600:
                    disparo = Disparo_enemigo_2(self)
                    lista_disparos.add(disparo)
                    self.indicador_etapa_patron_de_movimiento += 1
            if self.indicador_etapa_patron_de_movimiento == 3:
                if round(pygame.time.get_ticks()-self.instante_de_inicio_etapa) >= 3700:
                    disparo = Disparo_enemigo_2(self)
                    lista_disparos.add(disparo)
                    self.indicador_etapa_patron_de_movimiento += 1
            if self.indicador_etapa_patron_de_movimiento == 4:
                if round(pygame.time.get_ticks()-self.instante_de_inicio_etapa) >= 4300:
                    self.indicador_etapa_patron_de_movimiento = 0

        # Desplazamiento:
        self.coord_x -= self.speed_x
        self.coord_y += self.speed_y
        self.rect.x, self.rect.y = self.coord_x, self.coord_y