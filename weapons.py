import pygame
import constantes as ks
import math               

class Weapon():
    def __init__(self, escala=(40, 20)):  
        self.imagen_png = pygame.image.load(ks.GUN_PATH).convert_alpha()
        self.imagen_png = pygame.transform.scale(self.imagen_png, escala)  
        self.imagen = self.imagen_png
        self.forma = self.imagen.get_rect()
        self.offset_x = 20  
        self.offset_y = 10
        self.angle = 0       
        self.giro_izquierda = False
    

    def update(self, player):
        # Posición del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Determinar ancla (pivote) del arma según la dirección del jugador
        if player.direccion == "izquierda":
            anchor_x = player.rect.centerx - self.offset_x
            self.giro_izquierda = True
            base_image = pygame.transform.flip(self.imagen_png, True, False)
        else:
            anchor_x = player.rect.centerx + self.offset_x
            self.giro_izquierda = False
            base_image = self.imagen_png

        anchor_y = player.rect.centery + self.offset_y

        # Vector entre el pivote del arma y el mouse (usar el pivote real)
        dx = mouse_x - anchor_x
        dy = mouse_y - anchor_y

        # Ángulo en radianes y en grados (ángulo global)
        angle_rad = math.atan2(dy, dx)           
        angle_deg = math.degrees(angle_rad)

        # Guardar ángulo (en grados) para usar al crear la bala
        self.angle = angle_deg

        # Rotar la imagen base (ya flipada si corresponde).
        # pygame.transform.rotate rota en sentido contrario a las agujas del reloj para ángulos positivos,
        # se aplica -angle_deg para que la imagen "apunte" hacia el mouse.
        arma_rotada = pygame.transform.rotate(base_image, -angle_deg)

        # Posicionar el arma de modo que su centro coincida con el pivote (anchor)
        self.imagen = arma_rotada
        self.forma = arma_rotada.get_rect(center=(anchor_x, anchor_y))

    def dibujar(self, interfaz):
        interfaz.blit(self.imagen, self.forma)

# Clase Bullet
class Bullet(pygame.sprite.Sprite):      # Herencia de la clase Sprite
    def __init__(self, x, y, angle, flip= False, escala=(20,10), velocidad=ks.VELOCIDAD_BULLET):
        pygame.sprite.Sprite.__init__(self)         # Inicializa atributos heredados
        imagen = pygame.image.load(ks.BULLET_PATH).convert_alpha()
        imagen = pygame.transform.scale(imagen, escala)
        imagen = pygame.transform.rotate(imagen, -angle)
        self.image = imagen
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = velocidad

        # Usar el mismo ángulo global (en grados) que calculó Weapon
        rad = math.radians(angle)

        # Vector velocidad 
        self.vel_x = velocidad * math.cos(rad)   
        self.vel_y = velocidad * math.sin(rad)    

    def update(self):
        # Mover la bala
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if (self.rect.right < 0 or self.rect.left > ks.WIDTH_WINDOW or
            self.rect.bottom < 0 or self.rect.top > ks.HIGH_WINDOW):
            self.kill()

    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.rect)
