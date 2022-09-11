import pygame, sys
from clases import *
from funciones import *

pygame.init()

# ----------------------- CONFIGURACION -------------------------
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("__SHOOTING STARS__")

# Clock:
clock = pygame.time.Clock()

# Icono: 
icono = pygame.image.load("data\space_ship.png")
pygame.display.set_icon(icono)

#-------------------------- MENU PRINCIPAL --------------------------
menu_principal(pantalla)


# -------------------------- MUSICA ----------------------------
pygame.mixer.music.load("data\Shooting Stars.wav")
pygame.mixer.music.play(-1)


# ------------------ VARIABLES DEL JUEGO -------------------------
game_over = False
score = 0
high_score = 0
acumulador_tiempo_pasado_partidas_pasadas = 0


#------------------------- LISTAS DE SPRITES ------------------------
lista_meteoros = pygame.sprite.Group()
lista_items = pygame.sprite.Group()
lista_disparos_jugador = pygame.sprite.Group()
lista_disparos_enemigos = pygame.sprite.Group()
lista_enemigos = pygame.sprite.Group()
lista_de_obstaculos = pygame.sprite.Group()

#-------------------------- CREACION DE LOS OBJETOS --------------------------

# Creacion del objeto fondo:
fondo = Fondo()        

# Creacion del objeto jugador:
jugador = Jugador() 

# ------------------------ EVENTOS --------------------------------

# Van a pasar unos instantes desde el inicio de la partida hasta que se habilite el movimiento del jugador:
habilitar_movimiento_jugador =  pygame.USEREVENT + 1
pygame.time.set_timer(habilitar_movimiento_jugador, 2200, 1)

generacion_meteoritos = pygame.USEREVENT + 2
tiempo_generacion_meteoritos_original = 2600
pygame.time.set_timer(generacion_meteoritos, tiempo_generacion_meteoritos_original, 1)

generacion_robot_enemigo = pygame.USEREVENT + 3
tiempo_generacion_robot_enemigo_original = 16000
pygame.time.set_timer(generacion_robot_enemigo, tiempo_generacion_robot_enemigo_original, 1)

generacion_nave_enemiga_tipo_1 = pygame.USEREVENT + 4
tiempo_generacion_nave_enemiga_tipo_1_original = 19000
pygame.time.set_timer(generacion_nave_enemiga_tipo_1, tiempo_generacion_nave_enemiga_tipo_1_original, 1)

generacion_nave_enemiga_tipo_2 = pygame.USEREVENT + 5
tiempo_generacion_nave_enemiga_tipo_2_original = 60000
pygame.time.set_timer(generacion_nave_enemiga_tipo_2, tiempo_generacion_nave_enemiga_tipo_2_original, 1)

# Creo estos eventos que me van a ayudar a limitar la cadencia de disparo: 
habilitar_disparo_normal =  pygame.USEREVENT + 6
habilitar_super_disparo =  pygame.USEREVENT + 7

evento_game_over = pygame.USEREVENT + 8

# ------------------------ BUCLE PRINCIPAL -------------------------------- 

while True:

    # CRONOMETRO:
    tiempo_pasado_partida_actual = round(pygame.time.get_ticks()/1000) - acumulador_tiempo_pasado_partidas_pasadas


    # ---------- REDUCCION PROGRESIVA DE LA FRECUENCIA DE GENERACION DE ENEMIGOS ---------------

    factor_de_reduccion = 0.007*tiempo_pasado_partida_actual

    if factor_de_reduccion < 0.6:
        
        nuevo_tiempo_generacion_meteoritos = tiempo_generacion_meteoritos_original - round(tiempo_generacion_meteoritos_original*factor_de_reduccion*1.35)
        nuevo_tiempo_generacion_robot_enemigo = tiempo_generacion_robot_enemigo_original - round(tiempo_generacion_robot_enemigo_original*factor_de_reduccion)
        nuevo_tiempo_generacion_nave_enemiga_tipo_1 = tiempo_generacion_nave_enemiga_tipo_1_original - round(tiempo_generacion_nave_enemiga_tipo_1_original*factor_de_reduccion)
        nuevo_tiempo_generacion_nave_enemiga_tipo_2 = tiempo_generacion_nave_enemiga_tipo_2_original - round(tiempo_generacion_nave_enemiga_tipo_2_original*factor_de_reduccion*0.4)

    # ----------------------------- CHEQUEO DE EVENTOS -----------------------------------
    for evento in pygame.event.get(): 

        # Configuracion del cierre de la ventana:    
        if evento.type == pygame.QUIT:
            sys.exit()


        # ----------- EVENTOS ASOCIADOS AL JUGADOR ------------

        # Habilito movimiento de la nave:
        if evento.type == habilitar_movimiento_jugador:
            jugador.movimiento_habilitado = True
            jugador.disparo_normal_habilitado = True
            jugador.speed_x = 0

        if jugador.movimiento_habilitado:
            
            # Asocio el moviomiento de la nave al teclado:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador.speed_x = -4
                if evento.key == pygame.K_RIGHT: 
                    jugador.speed_x = 2
                if evento.key == pygame.K_UP:
                    jugador.speed_y = -4.5
                if evento.key == pygame.K_DOWN: 
                    jugador.speed_y = 4.5

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    jugador.speed_x = 0
                if evento.key == pygame.K_RIGHT: 
                    jugador.speed_x = 0  
                if evento.key == pygame.K_UP:
                    jugador.speed_y = 0
                if evento.key == pygame.K_DOWN: 
                    jugador.speed_y = 0     

        # Disparo del jugador:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and jugador.disparo_normal_habilitado:
                disparo = Disparo_jugador(jugador)
                disparo.sfx.play()
                lista_disparos_jugador.add(disparo)
                jugador.disparo_normal_habilitado = False
                pygame.time.set_timer(habilitar_disparo_normal, 215, 1)

            elif evento.key == pygame.K_SPACE and jugador.super_disparo_habilitado:
                super_disparo = Super_disparo_jugador(jugador)
                disparo.sfx.play()
                lista_disparos_jugador.add(super_disparo)
                jugador.super_disparo_habilitado = False
                pygame.event.set_allowed(habilitar_disparo_normal)
                pygame.time.set_timer(habilitar_disparo_normal, 900, 1)

        if evento.type == habilitar_disparo_normal:
            jugador.disparo_normal_habilitado = True
        if evento.type == habilitar_super_disparo:
            jugador.super_disparo_habilitado = True

        # GENERACION DE ENEMIGOS:

        # Generacion de meteoros:
        if evento.type == generacion_meteoritos:
            generar_enemigo(Meteoro, lista_meteoros)
            pygame.time.set_timer(generacion_meteoritos, nuevo_tiempo_generacion_meteoritos, 1)

        # Generacion de robots enemigos:
        if evento.type == generacion_robot_enemigo:
            generar_enemigo(Robot_enemigo, lista_enemigos)   
            pygame.time.set_timer(generacion_robot_enemigo, nuevo_tiempo_generacion_robot_enemigo, 1)

        # Generacion de naves enemigas tipo 1:
        if evento.type == generacion_nave_enemiga_tipo_1:
            enemigo_1 = generar_enemigo(Nave_enemiga_tipo_1, lista_enemigos)  
            pygame.time.set_timer(generacion_nave_enemiga_tipo_1, nuevo_tiempo_generacion_nave_enemiga_tipo_1, 1) 
            
        # Generacion de naves enemigas tipo 2:
        if evento.type == generacion_nave_enemiga_tipo_2:
            #enemigo_2 = generar_enemigo(Nave_enemiga_tipo_2, lista_enemigos)   
            pygame.time.set_timer(generacion_nave_enemiga_tipo_2, nuevo_tiempo_generacion_nave_enemiga_tipo_2, 1)

        if evento.type == evento_game_over:
            game_over = True


    # ------------ DESPLAZAMIENTO E IMPRESION DE LOS SPRITES ------------

    # FONDO:
    fondo.impresion_y_scroll(pantalla)

    # SPRITES:

    # Jugador:
    jugador.desplazamiento()
    if jugador.health > 0:
        pantalla.blit(jugador.image, (jugador.coord_x,jugador.coord_y))

    # Meteoros, items y disparos:
    for grupo in (lista_disparos_jugador, lista_disparos_enemigos, lista_meteoros, lista_items):
        for sprite in grupo:
            sprite.desplazamiento()
            pantalla.blit(sprite.image, (sprite.coord_x,sprite.coord_y))

    # Enemigos:
    for enemigo in lista_enemigos:
        enemigo.patron_de_movimiento(jugador, lista_disparos_enemigos)  
        pantalla.blit(enemigo.image, (enemigo.coord_x,enemigo.coord_y))

    # TABLERO SCORE Y VIDA:
    impresion_tablero(pantalla, score, high_score, jugador.health)
  
    pygame.display.flip()        

    # ----------------------------- COLISIONES --------------------------------

    lista_de_obstaculos.add(lista_enemigos.sprites(),lista_meteoros.sprites(),lista_disparos_enemigos.sprites())

    # Colisiones entre disparos del jugador y obstaculos:
    for disparo in lista_disparos_jugador:
        grupo_individual_disparo = pygame.sprite.GroupSingle(disparo)
        for obstaculo in lista_de_obstaculos:
            # Chequeo primero si hay colision usando rectangulos:
            if pygame.sprite.spritecollide(obstaculo, grupo_individual_disparo, False):
                # Si hay colision entre rectangulos chequeo la colision usando mascaras: 
                if pygame.sprite.spritecollide(obstaculo, grupo_individual_disparo, False, pygame.sprite.collide_mask):                    
                    if isinstance(disparo, Disparo_jugador):
                        disparo.kill()
                        obstaculo.health -= 10
                    elif isinstance(disparo, Super_disparo_jugador):
                        obstaculo.kill()
                        score += obstaculo.score_revenue  

                    # Parpadeo de daño:
                    pantalla.blit(obstaculo.mask.to_surface(setcolor=(150,150,150),unsetcolor=None), (obstaculo.coord_x,obstaculo.coord_y))
                    pygame.display.update(obstaculo.rect)
                    
                    if obstaculo.health <= 0:
                        obstaculo.kill()
                        score += obstaculo.score_revenue   

                        # Items dentro de meteoros:
                        if isinstance(obstaculo, Meteoro):
                            if obstaculo.random_reward == 1 or obstaculo.random_reward == 2:
                                item_bonus_puntaje = Score_bonus_item(obstaculo.coord_x+7, obstaculo.coord_y+7)
                                lista_items.add(item_bonus_puntaje)    
                            elif obstaculo.random_reward == 3:
                                item_vida = Health_item(obstaculo.coord_x+7, obstaculo.coord_y+7)
                                lista_items.add(item_vida)
                            elif obstaculo.random_reward == 4:
                                item_super_disparo = Super_shot_item(obstaculo.coord_x+7, obstaculo.coord_y+7)
                                lista_items.add(item_super_disparo) 


    # Colisiones entre items y el jugador:
    for item in lista_items:
        grupo_individual_item = pygame.sprite.GroupSingle(item)
        if pygame.sprite.spritecollide(jugador, grupo_individual_item, False):
            if pygame.sprite.spritecollide(jugador, grupo_individual_item, True, pygame.sprite.collide_mask): 
                item.kill()
                if isinstance(item, Score_bonus_item):
                    score = item.item_efect(score)
                elif isinstance(item, Health_item):
                    jugador.health = item.item_efect(jugador.health)
                elif isinstance(item, Super_shot_item):
                    jugador.disparo_normal_habilitado = False
                    pygame.event.set_blocked(habilitar_disparo_normal)
                    pygame.event.clear(habilitar_disparo_normal)
                    pygame.time.set_timer(habilitar_super_disparo, 640, 1)

                # Parpadeo:
                pantalla.blit(item.mask.to_surface(setcolor=(150,150,150),unsetcolor=None), (item.coord_x,item.coord_y))
                pygame.display.update(item.rect)


    # Colisiones entre obstaculos y el jugador:
    if jugador.health > 0:
        for obstaculo in lista_de_obstaculos:
            grupo_individual_obstaculo = pygame.sprite.GroupSingle(obstaculo)
            if pygame.sprite.spritecollide(jugador, grupo_individual_obstaculo, False):
                if pygame.sprite.spritecollide(jugador, grupo_individual_obstaculo, True, pygame.sprite.collide_mask):
                    jugador.health -= obstaculo.damage
                    # Parpadeo de daño:
                    pantalla.blit(jugador.mask.to_surface(setcolor=(180,180,180),unsetcolor=None), (jugador.coord_x,jugador.coord_y))
                    pygame.display.update(jugador.rect)
                    if jugador.health < 0:
                        jugador.health = 0
                    if jugador.health == 0:
                        jugador.movimiento_habilitado, jugador.disparo_normal_habilitado = False, False
                        jugador.speed_x, jugador.speed_y = 0,0
                        pygame.time.set_timer(evento_game_over, 150, 1)           


    # ----------------------------- GAME OVER ---------------------------------

    if game_over == True:
        # Actualizo la barra de vida:
        impresion_tablero(pantalla, score, high_score, jugador.health)
        pygame.display.flip()

        # Paro la musica:
        pygame.mixer.music.fadeout(2500)
        
        # Menu de game over:
        menu_game_over(pantalla, score)

        # Puntaje:
        if score > high_score:
            high_score = score
        score = 0    

        # Reseteo el reloj de partida:
        acumulador_tiempo_pasado_partidas_pasadas += tiempo_pasado_partida_actual       

        # Reseteo los eventos:
        pygame.event.clear()
        pygame.time.set_timer(habilitar_movimiento_jugador, 2200, 1)
        pygame.time.set_timer(generacion_meteoritos, tiempo_generacion_meteoritos_original, 1)
        pygame.time.set_timer(generacion_robot_enemigo, tiempo_generacion_robot_enemigo_original, 1)
        pygame.time.set_timer(generacion_nave_enemiga_tipo_1, tiempo_generacion_nave_enemiga_tipo_1_original, 1)
        pygame.time.set_timer(generacion_nave_enemiga_tipo_2, tiempo_generacion_nave_enemiga_tipo_2_original, 1)

        # Vacio las listas de sprites:
        lista_meteoros.empty()
        lista_disparos_jugador.empty()
        lista_disparos_enemigos.empty()
        lista_enemigos.empty()
        lista_de_obstaculos.empty()

        # Vuelvo a crear al objeto jugador:
        jugador = Jugador()

        # Reseteo la musica:
        pygame.mixer.music.play(-1, 0, 1500)
        
        # Devuelvo la variable game_over a False:
        game_over = False

    # -------------------------- CONTROL DE FRAMES ----------------------------
    clock.tick(FPS)
           