import pygame
import random
import constantes as ks

class Enemy:
    def __init__(
        self,
        x, y,
        patrol_x_range=None,
        patrol_y_range=None,
        mode_interval=4000,
        mode_offset=0,
        speed_x=3,
        speed_y=2,
        anim_speed=0.15,
        sprite_path="assets/sprites/Knight_Walk.png"
    ):
        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
        self.frames = self.cargar_frames(self.sprite_sheet, 100, 64, 7)
        self.frame_index = 0
        self.anim_speed = anim_speed
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=(x, y))
        self.initial_pos = (x, y)

        self.speed_x_val = speed_x
        self.speed_y_val = speed_y
        self.vel_x = random.choice([-1, 1]) * speed_x
        self.vel_y = 0

        margin = 20
        if patrol_x_range is None:
            x_min = max(0, x - 150)
            x_max = min(ks.WIDTH_WINDOW, x + 150)
            patrol_x_range = (x_min, x_max)
        if patrol_y_range is None:
            y_min = max(0, y - 120)
            y_max = min(ks.HIGH_WINDOW, y + 120)
            patrol_y_range = (y_min, y_max)

        self.patrol_x_min, self.patrol_x_max = patrol_x_range
        self.patrol_y_min, self.patrol_y_max = patrol_y_range

        self.mode = "horizontal"
        self.mode_interval = mode_interval
        self.next_mode_switch_time = pygame.time.get_ticks() + mode_offset

        self.direccion_horizontal = "derecha" if self.vel_x >= 0 else "izquierda"

    def cargar_frames(self, sheet, ancho, alto, cantidad):
        frames = []
        for i in range(cantidad):
            frame = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * ancho, 0, ancho, alto))
            frames.append(frame)
        return frames

    def actualizar_animacion(self):
        self.frame_index += self.anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        frame_actual = self.frames[int(self.frame_index)]
        if self.direccion_horizontal == "izquierda":
            self.image = pygame.transform.flip(frame_actual, True, False)
        else:
            self.image = frame_actual

    def actualizar_modo(self):
        ahora = pygame.time.get_ticks()
        if ahora >= self.next_mode_switch_time:
            if self.mode == "horizontal":
                self.mode = "vertical"
                self.vel_x = 0
                self.vel_y = random.choice([-1, 1]) * self.speed_y_val
            else:
                self.mode = "horizontal"
                self.vel_y = 0
                self.vel_x = random.choice([-1, 1]) * self.speed_x_val
            self.next_mode_switch_time = ahora + self.mode_interval

    def mover(self, collision_rects=None):
        if collision_rects is None:
            collision_rects = []

        # mover X
        self.rect.x += self.vel_x
        collided = None
        for muro in collision_rects:
            if self.rect.colliderect(muro):
                collided = muro
                if self.vel_x > 0:
                    self.rect.right = muro.left
                elif self.vel_x < 0:
                    self.rect.left = muro.right
                # rebotar
                self.vel_x *= -1
                break

        # mover Y
        self.rect.y += self.vel_y
        for muro in collision_rects:
            if self.rect.colliderect(muro):
                if self.vel_y > 0:
                    self.rect.bottom = muro.top
                elif self.vel_y < 0:
                    self.rect.top = muro.bottom
                self.vel_y *= -1
                break

        # actualizar dirección de sprite
        if self.vel_x != 0:
            self.direccion_horizontal = "izquierda" if self.vel_x < 0 else "derecha"

        # mantener dentro de rangos de patrulla
        if self.rect.left < self.patrol_x_min:
            self.rect.left = self.patrol_x_min
            self.vel_x *= -1
        if self.rect.right > self.patrol_x_max:
            self.rect.right = self.patrol_x_max
            self.vel_x *= -1
        if self.rect.top < self.patrol_y_min:
            self.rect.top = self.patrol_y_min
            self.vel_y *= -1
        if self.rect.bottom > self.patrol_y_max:
            self.rect.bottom = self.patrol_y_max
            self.vel_y *= -1

    def actualizar(self, collision_rects=None):
        self.actualizar_modo()
        self.mover(collision_rects)
        self.actualizar_animacion()

    def dibujar(self, superficie, collision_rects=None):
        self.actualizar(collision_rects)
        superficie.blit(self.image, self.rect)