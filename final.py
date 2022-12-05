import pygame
import ast

class Game:
    def __init__(self, size=(800, 700)):
        pygame.init()
        self.window = pygame.display.set_mode(size)
        self.background = pygame.image.load('images\\background.png')
        self.background = pygame.transform.smoothscale(self.background.convert_alpha(), (800, 700))
        self.level = 0
        self.screen = "INITIAL"
        self.run = True
    
    def event_treatment(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                if event.key == pygame.K_q:
                    self.run = False

    def loop(self):
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        movimentos = 0
        L = Level(self.level)

        while self.run:
            self.window.blit(self.background, (0, 0))
            self.event_treatment()
            L.draw(self.window)
            L.event()
            pygame.display.flip()
            clock.tick(7)
            
    def time():
        pass

class Level():
    def __init__(self, level) -> None:
        self.level = level
        self.moving_sprites = pygame.sprite.Group()
        with open('levels.txt', 'r') as arq:
            file = arq.readlines()

        self.all_levels_info = [ast.literal_eval(line) for line in file]
        self.create_positions()
        self.top_left_x = (800 - self.dimension[0][0]*30) // 2 - 20
        self.top_left_y = (700 - self.dimension[0][1]*30) // 2
        self.create_level()

    def create_positions(self):
        self.player_position = self.all_levels_info[self.level]['robot_position']
        self.boxes_positions = self.all_levels_info[self.level]['boxes_positions']
        self.goal_positions = self.all_levels_info[self.level]['goal_positions']
        self.walls_positions = self.all_levels_info[self.level]['walls_positions']
        self.walk_positions = self.all_levels_info[self.level]['walk_positions']
        self.dimension = self.all_levels_info[self.level]['dimension']

    def create_level(self):
        #Cria os objetos em suas respectivas categorias
        for tipo in [[self.walk_positions, Floor], [self.walls_positions, Wall], [self.goal_positions, Goal], [self.boxes_positions, Box]]:
            #Retira todos os objetos possivelmente existentes na categoria
            tipo[1].objects.clear()
            #Adiciona os objetos
            for block in tipo[0]:
                object = tipo[1](convert_coordinates(block, self.top_left_x, self.top_left_y))
                self.moving_sprites.add(object)
        self.player = Robot(convert_coordinates(self.player_position[0], self.top_left_x, self.top_left_y))
        self.moving_sprites.add(self.player)
    
    def draw(self, window):
        self.moving_sprites.draw(window)

    def event(self):
        self.player.robot_event_treatment()

class Robot(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.sprites = []
        for image in ['images\\player_up.png', 'images\\player_down.png', 'images\\player_left.png', 'images\\player_right.png']:
            self.sprites.append(pygame.transform.scale(pygame.image.load(image), (30, 30)))
        self.position = position
        self.rotation = 0
        self.image = self.sprites[self.rotation]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position[0], self.position[1]]

    def move(self, x_change, y_change, rot_number):
        self.rotation = rot_number
        self.image = self.sprites[self.rotation]
        new_pos = (self.position[0] + 30*x_change, self.position[1] + 30*y_change) 
        box_moved = 0
        wall_pos = [wall.position for wall in Wall.objects]
        if new_pos in wall_pos:
            return box_moved 
        #Verifica se o movimento é na direção de uma caixa, e se ela pode ser movida
        for box in Box.objects:
            if box.position == new_pos:
                #Caso em que a caixa não pode ser movida
                if box.move(x_change, y_change, wall_pos) == False:
                    return box_moved
                else:
                    box_moved = 1

        #Atualiza a posição
        self.position = new_pos
        self.rect.topleft = [self.position[0], self.position[1]] # type: ignore
        return box_moved

    def robot_event_treatment(self):
        comandos =  pygame.key.get_pressed()
        if comandos[pygame.K_UP] or comandos[pygame.K_w]:
            self.move(0, -1, 0)
        if comandos[pygame.K_DOWN] or comandos[pygame.K_s]:
            self.move(0, 1, 1)
        if comandos[pygame.K_LEFT] or comandos[pygame.K_a]:
            self.move(-1, 0, 2)
        if comandos[pygame.K_RIGHT] or comandos[pygame.K_d]:
            self.move(1, 0, 3)

class Screen:
    pass

class Box(pygame.sprite.Sprite):
    objects = []
    def __init__(self, position) -> None:
        super().__init__()
        self.position = position
        self.sprites = []
        for image in ['images\\box.gif', 'images\\box_port.gif']:
            self.sprites.append(pygame.transform.scale(pygame.image.load(image), (30, 30)))
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position[0], self.position[1]]
        self.__class__.objects.append(self)

    def move(self, x_change, y_change, wall_pos):
        self.rect.topleft = [self.position[0], self.position[1]] 
        object_aux = self.__class__.objects.copy()
        object_aux.remove(self)
        new_pos = (self.position[0] + 30*x_change, self.position[1] + 30*y_change)
        box_pos = [box.position for box in Box.objects]

        #Verifica se o destino da caixa está ocupado
        if new_pos in wall_pos or new_pos in box_pos:
            return False
        
        #Atualiza a posição da caixa
        self.position = new_pos
        self.rect.topleft = [self.position[0], self.position[1]]

        self.in_goal

        return True

    @property
    def in_goal(self):
        goal_pos = [goal.position for goal in Goal.objects]
        if self.position in goal_pos:
            self.image = self.sprites[1]
            return True
        return False
        

class Wall(pygame.sprite.Sprite):
    objects = []
    def __init__(self, position) -> None:
        super().__init__()
        self.position = position
        image = 'images\\brick.gif'
        self.image = pygame.transform.scale(pygame.image.load(image), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position[0], self.position[1]]
        self.__class__.objects.append(self)

class Goal(pygame.sprite.Sprite):
    objects = []
    def __init__(self, position) -> None:
        super().__init__()
        self.position = position
        image = 'images\\port.gif'
        self.image = pygame.transform.scale(pygame.image.load(image), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position[0], self.position[1]]
        self.__class__.objects.append(self)

class Floor(pygame.sprite.Sprite):
    objects = []
    def __init__(self, position) -> None:
        super().__init__()
        self.position = position
        image = 'images\\floor.gif'
        self.image = pygame.transform.scale(pygame.image.load(image), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position[0], self.position[1]]
        self.__class__.objects.append(self)

class Button:
    pass

def convert_coordinates(position, x, y):
    return ((position[0]*30 + x, position[1]*30 + y))

if __name__ == '__main__':
    G = Game()
    G.loop()