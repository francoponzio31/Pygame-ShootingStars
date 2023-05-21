import pygame, sys
from constantes import *
from clases import*

def menu_principal(objeto_pantalla):

    boton_menu_sfx = pygame.mixer.Sound("data\Menu_sfx.wav")
    cursor_en_el_boton = False
    run_menu = True
    
    while run_menu:
     
        # Fondo:
        fondo = pygame.image.load("data\Background.png").convert()
        objeto_pantalla.blit(fondo, (0,0))

        # Ventana:
        ancho_ventana_menu, alto_ventana_menu = 700,400
        ventana = pygame.Rect(((ANCHO_PANTALLA-ancho_ventana_menu)/2, (ALTO_PANTALLA-alto_ventana_menu)/2), (ancho_ventana_menu, alto_ventana_menu))
        pygame.draw.rect(objeto_pantalla, (30,30,30), ventana, border_radius=5)
        pygame.draw.rect(objeto_pantalla, (150,150,150), ventana, width=2, border_radius=5)
        
        # Titulo:
        titulo = pygame.image.load("data\Titulo_menu_principal.png").convert_alpha()
        objeto_pantalla.blit(titulo, (ventana.x + (ancho_ventana_menu - titulo.get_width())/2, ventana.y + 55))

        # Boton play:
        ancho_boton_play, alto_boton_play = 200, 65
        boton_play = pygame.Rect((ventana.x+(ancho_ventana_menu-ancho_boton_play)/2, ventana.y + 175), (ancho_boton_play, alto_boton_play))
        pygame.draw.rect(objeto_pantalla, (15,15,15), boton_play, border_radius=7)
        pygame.draw.rect(objeto_pantalla, (125,125,125), boton_play, width=2, border_radius=7)
        texto_play = pygame.image.load("data\Texto_play_menu.png").convert_alpha()
        objeto_pantalla.blit(texto_play, (boton_play.x + (ancho_boton_play - texto_play.get_width())/2, boton_play.y + (alto_boton_play - texto_play.get_height())/2))
        
        # Boton quit:
        ancho_boton_quit, alto_boton_quit = 200, 65
        boton_quit = pygame.Rect((ventana.x+(ancho_ventana_menu-ancho_boton_quit)/2, ventana.y + 275), (ancho_boton_quit, alto_boton_quit))
        pygame.draw.rect(objeto_pantalla, (15,15,15), boton_quit, border_radius=7)
        pygame.draw.rect(objeto_pantalla, (125,125,125), boton_quit, width=2, border_radius=7)
        texto_quit = pygame.image.load("data\Texto_quit_menu.png").convert_alpha()
        objeto_pantalla.blit(texto_quit, (boton_quit.x + (ancho_boton_quit - texto_quit.get_width())/2, boton_quit.y + (alto_boton_quit - texto_quit.get_height())/2))

        # Hover:
        if boton_play.collidepoint(pygame.mouse.get_pos()):
            if cursor_en_el_boton == False:
                boton_menu_sfx.play()   
                cursor_en_el_boton = True
            pygame.draw.rect(objeto_pantalla, (25,25,25), boton_play, border_radius=7)
            pygame.draw.rect(objeto_pantalla, (125,125,125), boton_play, width=2, border_radius=7)
            objeto_pantalla.blit(texto_play, (boton_play.x + (ancho_boton_play - texto_play.get_width())/2, boton_play.y + (alto_boton_play - texto_play.get_height())/2))
                
        elif boton_quit.collidepoint(pygame.mouse.get_pos()):
            if cursor_en_el_boton == False:
                boton_menu_sfx.play()   
                cursor_en_el_boton = True
            pygame.draw.rect(objeto_pantalla, (25,25,25), boton_quit, border_radius=7)
            pygame.draw.rect(objeto_pantalla, (125,125,125), boton_quit, width=2, border_radius=7)
            objeto_pantalla.blit(texto_quit, (boton_quit.x + (ancho_boton_quit - texto_quit.get_width())/2, boton_quit.y + (alto_boton_quit - texto_quit.get_height())/2))

        else: 
            cursor_en_el_boton = False

        # Eventos:    
        for evento in pygame.event.get(): 
            if evento.type == pygame.QUIT:
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_play.collidepoint(pygame.mouse.get_pos()):
                    pygame.mouse.set_visible(False)
                    run_menu = False  
                if boton_quit.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()

        pygame.display.flip()


def menu_game_over(objeto_pantalla, score):

    pygame.mouse.set_visible(True)
    run_menu = True
    boton_menu_sfx = pygame.mixer.Sound("data\Menu_sfx.wav")
    cursor_en_el_boton = False

    while run_menu:
     
        # Ventana:
        ancho_ventana_menu, alto_ventana_menu = 600,450
        ventana = pygame.Rect(((ANCHO_PANTALLA-ancho_ventana_menu)/2, (ALTO_PANTALLA-alto_ventana_menu)/2), (ancho_ventana_menu, alto_ventana_menu))
        pygame.draw.rect(objeto_pantalla, (30,30,30), ventana, border_radius=5)
        pygame.draw.rect(objeto_pantalla, (150,150,150), ventana, width=2, border_radius=5)
        
        # Texto game over:
        texto_game_over = pygame.image.load("data\Texto_game_over_menu.png").convert_alpha()
        objeto_pantalla.blit(texto_game_over, (ventana.x + (ancho_ventana_menu - texto_game_over.get_width())/2, ventana.y + 55))

        # Score:
        impresion_score = pygame.font.SysFont("Consolas", 55).render( f"Score: {score}", True, (180,180,180))
        objeto_pantalla.blit(impresion_score, (ventana.x+(ancho_ventana_menu-impresion_score.get_width())/2, ventana.y + 145))

        # Boton retry:
        ancho_boton_retry, alto_boton_retry = 200, 65
        boton_retry = pygame.Rect((ventana.x+(ancho_ventana_menu-ancho_boton_retry)/2, ventana.y + 235), (ancho_boton_retry, alto_boton_retry))
        pygame.draw.rect(objeto_pantalla, (15,15,15), boton_retry, border_radius=7)
        pygame.draw.rect(objeto_pantalla, (125,125,125), boton_retry, width=2, border_radius=7)
        texto_retry = pygame.image.load("data\Texto_retry_menu.png").convert_alpha()
        objeto_pantalla.blit(texto_retry, (boton_retry.x + (ancho_boton_retry - texto_retry.get_width())/2, boton_retry.y + (alto_boton_retry - texto_retry.get_height())/2))
        
        # Boton quit:
        ancho_boton_quit, alto_boton_quit = 200, 65
        boton_quit = pygame.Rect((ventana.x+(ancho_ventana_menu-ancho_boton_quit)/2, ventana.y + 335), (ancho_boton_quit, alto_boton_quit))
        pygame.draw.rect(objeto_pantalla, (15,15,15), boton_quit, border_radius=7)
        pygame.draw.rect(objeto_pantalla, (125,125,125), boton_quit, width=2, border_radius=7)
        texto_quit = pygame.image.load("data\Texto_quit_menu.png").convert_alpha()
        objeto_pantalla.blit(texto_quit, (boton_quit.x + (ancho_boton_quit - texto_quit.get_width())/2, boton_quit.y + (alto_boton_quit - texto_quit.get_height())/2))

        # Hover:
        if boton_retry.collidepoint(pygame.mouse.get_pos()):
            if cursor_en_el_boton == False:
                boton_menu_sfx.play()   
                cursor_en_el_boton = True
            pygame.draw.rect(objeto_pantalla, (25,25,25), boton_retry, border_radius=7)
            pygame.draw.rect(objeto_pantalla, (125,125,125), boton_retry, width=2, border_radius=7)
            objeto_pantalla.blit(texto_retry, (boton_retry.x + (ancho_boton_retry - texto_retry.get_width())/2, boton_retry.y + (alto_boton_retry - texto_retry.get_height())/2))
                
        elif boton_quit.collidepoint(pygame.mouse.get_pos()):
            if cursor_en_el_boton == False:
                boton_menu_sfx.play()   
                cursor_en_el_boton = True
            pygame.draw.rect(objeto_pantalla, (25,25,25), boton_quit, border_radius=7)
            pygame.draw.rect(objeto_pantalla, (125,125,125), boton_quit, width=2, border_radius=7)
            objeto_pantalla.blit(texto_quit, (boton_quit.x + (ancho_boton_quit - texto_quit.get_width())/2, boton_quit.y + (alto_boton_quit - texto_quit.get_height())/2))

        else:
            cursor_en_el_boton = False

        # Eventos:    
        for evento in pygame.event.get(): 
            if evento.type == pygame.QUIT:
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_retry.collidepoint(pygame.mouse.get_pos()):
                    pygame.mouse.set_visible(False)
                    run_menu = False  
                if boton_quit.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()

        pygame.display.flip()


def impresion_tablero(objeto_pantalla, score, high_score, health):

    FUENTE = pygame.font.SysFont("Consolas", 20)
    COLOR_PUNTAJE = (210,210,210)

    # score:     
    impresion_score = FUENTE.render( f"Score: {score}", True, COLOR_PUNTAJE)
    objeto_pantalla.blit(impresion_score, (10, 10))

    # High score:
    impresion_highscore = FUENTE.render( f"High Score: {high_score}", True, COLOR_PUNTAJE)
    objeto_pantalla.blit(impresion_highscore, (10, 32))   

    # Barra de vida:
    texto_health = FUENTE.render( f"Health:", True, COLOR_PUNTAJE)
    objeto_pantalla.blit(texto_health, (10, 54))
    fondo = pygame.Rect((texto_health.get_width()+15, 54+(texto_health.get_height()-10)/2), (100, 10))
    pygame.draw.rect(objeto_pantalla, (120,120,120), fondo, border_radius=1)
    vida = pygame.Rect((fondo.x, fondo.y), (fondo.width*health/100, fondo.height))
    pygame.draw.rect(objeto_pantalla, (23,187,104), vida, border_radius=1)


def generar_enemigo(clase_del_enemigo, lista_enemigos):
    enemigo = clase_del_enemigo()
    lista_enemigos.add(enemigo)

    return enemigo
