import pygame


class Robot(pygame.sprite.Sprite):    
    def __init__(self, position:tuple[int,int]) -> None:  
        """Inicializa sprite do robô.

        Args:
            position (tuple[int,int]): posição inicial do robô.
        """              
        super().__init__()
        self.sprites = []
        for image in ['images\\player_up.png', 'images\\player_down.png', 'images\\player_left.png', 'images\\player_right.png']:
            self.sprites.append(pygame.transform.scale(pygame.image.load(image), (30, 30)))
        self.position = position
        self.rotation = 0
        self.image = self.sprites[self.rotation]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position[0], self.position[1]]

    def move(self, x_change:int, y_change:int, rot_number:int) -> int:       
        """Realiza os movimentos do robô e verifica se ele moveu uma caixa (Box) (caso afirmativo, chama a função de movimento da caixa)

        Args:
            x_change (int): parâmetro que define se o robô vai se mover ao longo do eixo horizontal e em que sentido ele fará isso (0 = não se move, 1 = move uma casa para a direita, -1 = move uma casa para a esquerda)
            y_change (int): parâmetro que define se o robô vai se mover ao longo do eixo vertical e em que sentido ele fará isso (0 = não se move, 1 = move uma casa para baixo, -1 = move uma casa para cima)
            rot_number (int): parâmetro que define a rotação da imagem do robô (0 = voltado para cima, 1 = rotaciona 90º em sentido horário, 2 = rotaciona 180º em sentido horário, 3 = rotaciona 270º em sentido horário). 
        Returns:
            int: inteiro que informa se o robô moveu uma caixa ao se mover (0 = não moveu, 1 = moveu).
        """         
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
        pygame.mixer.Sound("sounds\\robo_move.wav").play()
        return box_moved

    def robot_event_treatment(self) -> int:
        """Trata os eventos do input referentes ao robô.

        Returns:
            int: inteiro que informa se o robô moveu uma caixa (0 = não moveu, 1 = moveu).
        """        
        comandos =  pygame.key.get_pressed()
        moved = 0
        if comandos[pygame.K_UP] or comandos[pygame.K_w]:
            moved = self.move(0, -1, 0)
        if comandos[pygame.K_DOWN] or comandos[pygame.K_s]:
            moved = self.move(0, 1, 1)
        if comandos[pygame.K_LEFT] or comandos[pygame.K_a]:
            moved = self.move(-1, 0, 2)
        if comandos[pygame.K_RIGHT] or comandos[pygame.K_d]:
            moved = self.move(1, 0, 3)
        
        return moved


class Box(pygame.sprite.Sprite):
    objects = []
    def __init__(self, position:tuple[int,int]) -> None:
        """Inicializa sprite da caixa.

        Args:
            position (tuple[int,int]): posição inicial da caixa.
        """        
        super().__init__()
        self.position = position
        self.sprites = []
        for image in ['images\\box.gif', 'images\\box_port.gif']:
            self.sprites.append(pygame.transform.scale(pygame.image.load(image), (30, 30)))
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position[0], self.position[1]]
        self.__class__.objects.append(self)

    def move(self, x_change:int, y_change:int, wall_pos:list[tuple[int,int]]) -> bool:
        """Realiza os movimentos da caixa. É chamado apenas quando o robô se move na direção de uma caixa.

        Args:
            x_change (int): parâmetro que define se a caixa vai se mover ao longo do eixo horizontal e em que sentido ele fará isso (0 = não se move, 1 = move uma casa para a direita, -1 = move uma casa para a esquerda)
            y_change (int): parâmetro que define se a caixa vai se mover ao longo do eixo vertical e em que sentido ele fará isso (0 = não se move, 1 = move uma casa para baixo, -1 = move uma casa para cima)
            wall_pos (list[tuple[int,int]]): lista de posições de sprites de muro na fase.

        Returns:
            bool: booleano que informa se a caixa se moveu. É falso no caso em que a posição de destino da caixa é uma parede ou outra caixa. 
        """        
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
        pygame.mixer.Sound('sounds\\box_move.wav').play()
        return True

    @property
    def in_goal(self) -> bool:
        """Informa se a caixa encontra-se em uma posição-alvo e, caso esteja, troca sua imagem.

        Returns:
            bool: informa se a caixa encontra-se em uma posição-alvo (True caso afirmativo)
        """        
        goal_pos = [goal.position for goal in Goal.objects]
        if self.position in goal_pos:
            self.image = self.sprites[1]
            return True
        else:
            self.image = self.sprites[0]
        return False
        

class Wall(pygame.sprite.Sprite):
    objects = []
    def __init__(self, position:tuple[int,int]) -> None:
        """Inicializa objeto do tipo Wall.

        Args:
            position (tuple[int,int]): posição da parede na fase.
        """        
        super().__init__()
        self.position = position
        image = 'images\\brick.gif'
        self.image = pygame.transform.scale(pygame.image.load(image), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position[0], self.position[1]]
        self.__class__.objects.append(self)


class Goal(pygame.sprite.Sprite):
    objects = []
    def __init__(self, position:tuple[int,int]) -> None:
        """Inicializa objeto do tipo Goal.

        Args:
            position (tuple[int,int]): posição do objetivo na fase.
        """        
        super().__init__()
        self.position = position
        image = 'images\\port.gif'
        self.image = pygame.transform.scale(pygame.image.load(image), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position[0], self.position[1]]
        self.__class__.objects.append(self)


class Floor(pygame.sprite.Sprite):
    objects = []
    def __init__(self, position:tuple[int,int]) -> None:
        """Inicializa objeto do tipo Floor.

        Args:
            position (tuple[int,int]): posição do piso na fase.
        """        
        super().__init__()
        self.position = position
        image = 'images\\floor.gif'
        self.image = pygame.transform.scale(pygame.image.load(image), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position[0], self.position[1]]
        self.__class__.objects.append(self)