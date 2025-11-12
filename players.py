import pygame
import constantes as ks


class Player:
    def __init__(self, x, y):
        self.sprite_sheet = pygame.image.load("assets/sprites/Walking_KG_1.png").convert_alpha()
        self.frames = self.cargar_frames(self.sprite_sheet, 100, 64, 7)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 5
        self.direccion = "derecha"


    # Cargar frames
    def cargar_frames(self, sheet, ancho, alto, cantidad):
        frames = []
        for i in range(cantidad):
            frame = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * ancho, 0, ancho, alto))
            frames.append(frame)
        return frames
 


    def movimiento(self, delta_x, delta_y): 
        self.rect.x += delta_x              
        self.rect.y += delta_y        

        # Limitar dentro de la ventana
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ks.WIDTH_WINDOW:
            self.rect.right = ks.WIDTH_WINDOW
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ks.HIGH_WINDOW:
            self.rect.bottom = ks.HIGH_WINDOW



    def movimiento_con_colisiones(self, delta_x, delta_y, mapa):
        #Guardar la posicion del player
        original_x = self.rect.x
        original_y = self.rect.y

        #Mover en x
        self.rect.x += delta_x
        if (mapa.verificar_colision(self.rect) or
            self.rect.left < 0 or
            self.rect.right > ks.WIDTH_WINDOW):
            self.rect.x = original_x

        #Mover en y
        self.rect.y += delta_y
        if (mapa.verificar_colision(self.rect) or
            self.rect.top < 0 or
            self.rect.bottom > ks.HIGH_WINDOW):
            self.rect.y = original_y

        # Solo animar si se mueve
        if delta_x != 0 or delta_y != 0:  
            self.frame_index += 0.2
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            frame_actual = self.frames[int(self.frame_index)]


            # Determinar dirección
            if delta_x < 0:
                self.direccion = "izquierda"
            elif delta_x > 0:
                self.direccion = "derecha"

            # Aplicar flip si va hacia la izquierda
            if self.direccion == "izquierda":
                self.image = pygame.transform.flip(frame_actual, True, False)
            else:
                self.image = frame_actual

    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.rect)


