import pygame

class Robo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.sprites = []
        #Carrega imagens para o robô
        for image in ['images\\player_up.png', 'images\\player_down.png', 'images\\player_left.png', 'images\\player_right.png']:
            self.sprites.append(pygame.transform.scale(pygame.image.load(image), (30, 30)))

        self.rotation = 0
        self.image = self.sprites[self.rotation]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

    def move(self, x_change, y_change, rot_number):
        box_moved = 0
        audio_mover_box = pygame.mixer.Sound('sounds/box_move.wav')
        audio_mover_robo = pygame.mixer.Sound('sounds/robo_move.wav')

        self.rotation = rot_number
        self.image = self.sprites[self.rotation]
        new_pos = (self.x + 30*x_change, self.y + 30*y_change) 
        wall_pos = [(wall.x, wall.y) for wall in Wall.objects]
        #Verifica se o movimento é na direção da parede
        if new_pos in wall_pos:
            return box_moved 

        #Verifica se o movimento é na direção de uma caixa, e se ela pode ser movida
        for box in Box.objects:
            if (box.x, box.y) == new_pos:
                #Caso em que a caixa não pode ser movida
                if box.move(x_change, y_change, wall_pos) == False:
                    return box_moved
                else:
                    audio_mover_box.play()
                    box_moved = 1

        #Atualiza a posição
        self.x = new_pos[0]
        self.y = new_pos[1]
        self.rect.topleft = [self.x, self.y] # type: ignore
        audio_mover_robo.play()
        return box_moved

class Box(pygame.sprite.Sprite):
    objects = []
    def __init__(self, pos_x, pos_y):
        goal_pos = [(goal.x, goal.y) for goal in Goal.objects]
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.image = pygame.transform.scale(pygame.image.load('images\\box.gif'), (30, 30))
        self.sprites = []
        for image in ['images\\box.gif', 'images\\box_port.gif']:
            self.sprites.append(pygame.transform.scale(pygame.image.load(image), (30, 30)))

        if (self.x, self.y) in goal_pos:
            self.image = self.sprites[1]
        else:
            self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.__class__.objects.append(self)

    def move(self, x_change, y_change, wall_pos):
        goal_pos = [(goal.x, goal.y) for goal in Goal.objects]
        self.rect.topleft = [self.x, self.y] 
        object_aux = self.__class__.objects.copy()
        object_aux.remove(self)
        new_pos = (self.x + 30*x_change, self.y + 30*y_change)
        box_pos = [(box.x, box.y) for box in Box.objects]

        #Verifica se o destino da caixa está ocupado
        if new_pos in wall_pos or new_pos in box_pos:
            return False
        
        #Atualiza a posição da caixa
        self.x = new_pos[0]
        self.y = new_pos[1]
        self.rect.topleft = [self.x, self.y]
        if (self.x, self.y) in goal_pos:
            self.image = self.sprites[1]
        else:
            self.image = self.sprites[0]
        return True

class Wall(pygame.sprite.Sprite):
    objects = []
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.image = pygame.transform.scale(pygame.image.load('images\\brick.gif'), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.__class__.objects.append(self)

class Walk(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images\\floor.gif'), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

class Goal(pygame.sprite.Sprite):
    objects = []
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.image = pygame.transform.scale(pygame.image.load('images\\port.gif'), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        self.__class__.objects.append(self)