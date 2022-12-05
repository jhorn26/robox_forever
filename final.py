import pygame
import ast

class Game:
    def __init__(self, size=(800, 700)):
        pygame.init()
        self.window = pygame.display.set_mode(size)
        self.background = pygame.image.load('images\\background.png')
        self.background = pygame.transform.smoothscale(self.background.convert_alpha(), (800, 700))
        self.moving_sprites = pygame.sprite.Group()
        self.level = 0
        self.run = True
        
    def create_positions(self, all_levels_info):
        self.player_position = all_levels_info[self.level]['robot_position']
        self.boxes_positions = all_levels_info[self.level]['boxes_positions']
        self.goal_positions = all_levels_info[self.level]['goal_positions']
        self.walls_positions = all_levels_info[self.level]['walls_positions']
        self.walk_positions = all_levels_info[self.level]['walk_positions']
        self.dimension = all_levels_info[self.level]['dimension']

    def event_treatment(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                if event.key == pygame.K_q:
                    self.run = False

    def create_level(self):
        #Adiciona os objetos
        for block in self.player_position:
            object = Robot(block[0]*30 + self.top_left_x, block[1]*30 + self.top_left_y)
            self.moving_sprites.add(object)
        self.moving_sprites.add(self.player)
        return 

    def loop(self):
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        movimentos = 0

        with open('levels.txt', 'r') as arq:
            file = arq.readlines()
        all_levels_info = [ast.literal_eval(line) for line in file]

        self.create_positions(all_levels_info)
        self.top_left_x = (800 - self.dimension[0][0]*30) // 2 - 20
        self.top_left_y = (700 - self.dimension[0][1]*30) // 2

        self.player = Robot(convert_coordinates(self.player_position[0], self.top_left_x, self.top_left_y))

        while self.run:
            self.window.blit(self.background, (0, 0))
            self.event_treatment()
            self.moving_sprites.draw(self.window)
            pygame.display.flip()
            
    def time():
        pass

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

    def move():
        pass

class Screen:
    pass

class Block:
    def __init__(self, position) -> None:
        self.position = position

class Box(Block):
    def __init__(self) -> None:
        super().__init__()

    @property
    def in_goal(self):
        pass

class Wall(Block):
    pass

class Goal(Block):
    pass

class Floor(Block):
    pass

class Button:
    pass

def convert_coordinates(position, x, y):
    return ((position[0]*30 + x, position[1]*30 + y))

if __name__ == '__main__':
    G = Game()
    G.loop()