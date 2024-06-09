import pygame
import random
import math
from pygame import mixer

# inicializar pygame
pygame.init()

# crear la pantalla
pantalla = pygame.display.set_mode((800, 600))


# titulo del icono
pygame.display.set_caption('Invacion Espacial')
icono = pygame.image.load('ovni (2).png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Fondo.jpg')

# Agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.8)
mixer.music.play(-1)


# loop del juego
se_ejecuta = True

# variables del jugador
img_jugador = pygame.image.load('cohete.png')
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('enemigo.png'))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(1.2)
    enemigo_y_cambio.append(50)

# variables de la bala
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 4
bala_visible = False

# puntaje
puntaje = 0

# fuente
fuente = pygame.font.Font('Good-Game.otf', 32)
texto_x = 10
texto_y = 10

# Texto final del juego
fuente_final = pygame.font.Font('Good-Game.otf', 70)

def texto_final():
    texto_final = fuente_final.render(f'JUEGO TERMINADO', True, (255, 255, 255))
    pantalla.blit(texto_final, (200, 250))

# funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'puntaje: {puntaje}', True, (255,255,255))
    pantalla.blit(texto, (x, y))

# funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador,(x,y))

# funcion enemigo
def enemigo(x,y, ene):
    pantalla.blit(img_enemigo[ene],(x, y))

# funcion disparar
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

# funcion detectar colicion
def hay_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distancia < 27:
        return True
    else:
        return False

while se_ejecuta:

    # imagen de fondo
    pantalla.blit(fondo, (0,0))

    # iterar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # evento presionar teclas
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_LEFT:
                jugador_x_cambio += -2.5

            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio += 2.5

            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, jugador_y)

        # evento soltar teclas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # modificar ubicacion del jugador
    jugador_x += jugador_x_cambio


    # mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    if jugador_x >= 736:
        jugador_x = 736

    # modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        # fin del juego
        if enemigo_y[e] > 470:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    # mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1.7
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1.7
            enemigo_y[e] += enemigo_y_cambio[e]

        # colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            print(puntaje)
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # movimiento bala
    if bala_y <= 64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio



    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    # actualizar
    pygame.display.update()