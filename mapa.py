import pygame
import constantes as ks
from xml.etree import ElementTree

class MapaTiled:
    def __init__(self, archivo_tmx, archivo_tsx, imagen_tileset):
        self.tile_size = 16
        self.mapa_ancho = 0
        self.mapa_alto = 0
        self.datos_mapa = []
        self.tileset = None
        self.tiles = []
        self.colisiones = []  # Para detectar colisiones
        self.cargar_tileset(imagen_tileset)
        self.cargar_mapa(archivo_tmx)
        self.definir_colisiones()     #####
    
    def cargar_tileset(self, ruta_imagen):
        #Carga la imagen del tileset y divide en tiles individuales
        try:
            self.tileset = pygame.image.load(ruta_imagen).convert_alpha()
            ancho, alto = self.tileset.get_size()
            
            # Dividir en tiles individuales (10 columnas, 10 filas)
            for y in range(0, alto, self.tile_size):
                for x in range(0, ancho, self.tile_size):
                    rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                    tile = self.tileset.subsurface(rect)
                    self.tiles.append(tile)
        except Exception as e:
            print(f"Error cargando tileset: {e}")
    
    def cargar_mapa(self, archivo_tmx):
        #Carga los datos del mapa desde el archivo .tmx
        try:
            tree = ElementTree.parse(archivo_tmx)
            root = tree.getroot()
            
            # Obtener dimensiones del mapa
            self.mapa_ancho = int(root.get('width'))
            self.mapa_alto = int(root.get('height'))
            
            # Buscar la capa de datos
            layer = root.find('layer')
            data = layer.find('data')
            csv_data = data.text.strip()
            
            # Convertir CSV a matriz 2D
            filas = csv_data.split('\n')
            self.datos_mapa = []            
            for fila in filas:
                if fila.strip():
                    tiles_fila = [int(x) for x in fila.split(',') if x]
                    self.datos_mapa.append(tiles_fila)
                    
            print(f"Mapa cargado: {self.mapa_ancho}x{self.mapa_alto} tiles")
            
        except Exception as e:
            print(f"Error cargando mapa: {e}")
    
    def dibujar(self, superficie):
        #Dibuja todo el mapa en la superficie
        for fila in range(self.mapa_alto):
            for columna in range(self.mapa_ancho):
                tile_id = self.datos_mapa[fila][columna]
                if tile_id != 0:  # No dibujar tiles vacíos (valor 0)
                    # Los tile_id en Tiled empiezan en 1, nuestro array en 0
                    tile_index = tile_id - 1
                    if 0 <= tile_index < len(self.tiles):
                        x = columna * self.tile_size
                        y = fila * self.tile_size
                        superficie.blit(self.tiles[tile_index], (x, y))

    def definir_colisiones(self):
        self.colisiones = []
        #Lista de tiles transitables
        tiles_transitables = [37,38,39]
        for fila in range(self.mapa_alto):
            for columna in range(self.mapa_ancho):
                tile_id = self.datos_mapa[fila][columna]
                if tile_id != 0 and tile_id not in tiles_transitables:
                    rect = pygame.Rect(
                        columna * self.tile_size,
                        fila * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
                    self.colisiones.append(rect)

    def verificar_colision(self, rect_jugador):
        for tile_rect in self.colisiones:
            if rect_jugador.colliderect(tile_rect):
                return True
        return False
