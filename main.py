import pygame
import constantes as ks
from players import Player
from enemy import Enemy
from weapons import Weapon, Bullet
from mapa import MapaTiled             #######
import random

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((ks.WIDTH_WINDOW, ks.HIGH_WINDOW))

# Crear el mapa #######
mapa = MapaTiled(
    "assets/tiles/escenario2.tmx",         #archivo_tmx
    "assets/tiles/Dungeon_Tileset.tsx",   #archivo_tsx
    "assets/tiles/Dungeon_Tileset.png"    #imagen_tileset
)


pygame.display.set_caption("Primer videojuego")

font = pygame.font.SysFont(None, 36)

sound_shoot = pygame.mixer.Sound("assets/sounds/shoot.mp3")
sound_explosion = pygame.mixer.Sound("assets/sounds/explosion.mp3")
sound_victory = pygame.mixer.Sound("assets/sounds/victory.mp3")


Player_1 = Player(x=400, y=300)
Gun = Weapon()

pad = 20
half_w = ks.WIDTH_WINDOW // 2
half_h = ks.HIGH_WINDOW // 2

enemies = []

# enemigos iniciales (igual que antes)
e1 = Enemy(x=pad, y=pad, patrol_x_range=(pad, half_w - pad), patrol_y_range=(pad, half_h - pad), mode_interval=4000, mode_offset=0)
enemies.append(e1)

e2 = Enemy(x=ks.WIDTH_WINDOW - pad, y=pad, patrol_x_range=(half_w + pad, ks.WIDTH_WINDOW - pad), patrol_y_range=(pad, half_h - pad), mode_interval=4000, mode_offset=600)
enemies.append(e2)

e3 = Enemy(x=pad, y=ks.HIGH_WINDOW - pad, patrol_x_range=(pad, half_w - pad), patrol_y_range=(half_h + pad, ks.HIGH_WINDOW - pad), mode_interval=4000, mode_offset=1200)
enemies.append(e3)

e4 = Enemy(x=ks.WIDTH_WINDOW - pad, y=ks.HIGH_WINDOW - pad, patrol_x_range=(half_w + pad, ks.WIDTH_WINDOW - pad), patrol_y_range=(half_h + pad, ks.HIGH_WINDOW - pad), mode_interval=4000, mode_offset=1800)
enemies.append(e4)

balas = []

mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

reloj = pygame.time.Clock()

score = 0
total_eliminados = 0
max_en_pantalla = 4
total_para_victoria = 10
victoria = False

# Función para crear enemigo (igual)
def crear_enemigo():
    cuadrante = random.choice(["TL", "TR", "BL", "BR"])
    pad = 40
    half_w = ks.WIDTH_WINDOW // 2
    half_h = ks.HIGH_WINDOW // 2

    if cuadrante == "TL":
        return Enemy(x=random.randint(pad, half_w - pad), y=random.randint(pad, half_h - pad), patrol_x_range=(pad, half_w - pad), patrol_y_range=(pad, half_h - pad), mode_offset=random.randint(0, 2000))
    elif cuadrante == "TR":
        return Enemy(x=random.randint(half_w + pad, ks.WIDTH_WINDOW - pad), y=random.randint(pad, half_h - pad), patrol_x_range=(half_w + pad, ks.WIDTH_WINDOW - pad), patrol_y_range=(pad, half_h - pad), mode_offset=random.randint(0, 2000))
    elif cuadrante == "BL":
        return Enemy(x=random.randint(pad, half_w - pad), y=random.randint(half_h + pad, ks.HIGH_WINDOW - pad), patrol_x_range=(pad, half_w - pad), patrol_y_range=(half_h + pad, ks.HIGH_WINDOW - pad), mode_offset=random.randint(0, 2000))
    else:
        return Enemy(x=random.randint(half_w + pad, ks.WIDTH_WINDOW - pad), y=random.randint(half_h + pad, ks.HIGH_WINDOW - pad), patrol_x_range=(half_w + pad, ks.WIDTH_WINDOW - pad), patrol_y_range=(half_h + pad, ks.HIGH_WINDOW - pad), mode_offset=random.randint(0, 2000))

for _ in range(max_en_pantalla):
    enemies.append(crear_enemigo())

run = True

while run:
    reloj.tick(ks.FPS)

    delta_x = 0
    delta_y = 0

    if mover_arriba:
        delta_y = -ks.VELOCIDAD
    if mover_abajo:
        delta_y = ks.VELOCIDAD
    if mover_derecha:
        delta_x = ks.VELOCIDAD
    if mover_izquierda:
        delta_x = -ks.VELOCIDAD

   
    Player_1.movimiento_con_colisiones(delta_x, delta_y, mapa)
    
    window.fill(ks.COLOR_FONDO)  ######
    mapa.dibujar(window)         ###### 

    Player_1.dibujar(interfaz=window)

    Gun.update(Player_1)
    Gun.dibujar(window)

    #Mover al Enemigo
    for e in enemies:
        e.dibujar(superficie=window)

    
    #### Dibujar balas  ####
    for bullet in balas[:]:        
        bullet.update()            
        bullet.dibujar(window)
        for e in enemies[:]:
            if bullet.rect.colliderect(e.rect):
                try:     ###      
                    sound_explosion.play()     #aaa         
                    balas.remove(bullet)
                    enemies.remove(e)
                    score += 100    ###
                    total_eliminados += 1      #aaa
                except ValueError:  ###
                    pass            ###
                break

    # Mantener 4 enemigos activos hasta que se hayan eliminado 5
    if len(enemies) < max_en_pantalla and total_eliminados < 5:
        enemies.append(crear_enemigo())

    # Después de 5 eliminaciones, reducir generación (máximo 4 activos)
    if 5 <= total_eliminados < total_para_victoria and len(enemies) < max_en_pantalla:
        # Se puede permitir regenerar hasta alcanzar 10 enemigos totales
        if total_eliminados + len(enemies) < total_para_victoria:
            enemies.append(crear_enemigo())

    # Verificar victoria
    if total_eliminados >= total_para_victoria and not victoria:
        victoria = True
        enemies.clear()
        sound_victory.play()


    #### HUD: puntuación y enemigos restantes ####
    texto_score = font.render(f"Puntuación: {score}", True, (255, 255, 0))
    texto_enemigos = font.render(f"Enemigos restantes: {len(enemies)}", True, (255, 0, 255))
    texto_kills = font.render(f"Eliminados: {total_eliminados}/{total_para_victoria}", True, (255, 255, 255))  #aaa
    window.blit(texto_score, (10, 10))      #
    window.blit(texto_enemigos, (10, 40))   #
    window.blit(texto_kills, (10, 70))              #aaa

    # Comprobación de victoria
    if victoria:
        texto_victoria = font.render("¡VICTORIA! Todos los enemigos eliminados.", True, (255, 255, 0))
        window.blit(texto_victoria, (ks.WIDTH_WINDOW // 2 - 250, ks.HIGH_WINDOW // 2))
    #############

       
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:     
            if event.key == pygame.K_a:      
                mover_izquierda = True       

            if event.key == pygame.K_d:      
                mover_derecha = True         

            if event.key == pygame.K_w:     
                mover_arriba = True          

            if event.key == pygame.K_s:      
                mover_abajo = True  

        if event.type == pygame.KEYUP:     
            if event.key == pygame.K_a:      
                mover_izquierda = False       

            if event.key == pygame.K_d:      
                mover_derecha = False         

            if event.key == pygame.K_w:     
                mover_arriba = False          

            if event.key == pygame.K_s:      
                mover_abajo = False
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bullet = Bullet(
                Gun.forma.centerx,
                Gun.forma.centery,
                Gun.angle,
                flip= Gun.giro_izquierda
            )
            sound_shoot.play()
            balas.append(bullet)

    pygame.display.update()                   


pygame.quit()