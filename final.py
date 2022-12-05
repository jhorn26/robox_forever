import pygame
import ast
from sprites import *


class Game:
    """Roda o jogo e manipula as demais classes.
    """    
    def __init__(self, size:tuple[int,int]) -> None:  
        """Inicializa a classe Game.

        Args:
            size (tuple[int,int]): dimensões da janela do jogo.
        """        
        pygame.init()
        self.window = pygame.display.set_mode(size)
        self.background = pygame.image.load('images\\background.png')
        self.background = pygame.transform.smoothscale(self.background.convert_alpha(), (800, 700))
        self.level = 0
        self.screen = "INITIAL"
        self.run = True
        self.page = "INITIAL"
        self.background_music = pygame.mixer.Sound("sounds\\som_de_fundo.wav")
        self.background_music.play(-1)

    def event_treatment(self) -> None:  
        """Trata os eventos do input.
        """        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.page == "INITIAL":
                    self.page = "SELECT"
                if event.key == pygame.K_SPACE and self.page == "VICTORY":
                    self.page = "PLAYING"
                    if self.level < 14:
                        self.level += 1
                    else:
                        self.page = "SELECT"

                if event.key == pygame.K_q:
                    self.run = False

    def loop(self) -> None:
        """Responsável por efetivamente rodar o jogo dentro de seu loop interno.
        """        
        self.screen = Screen(self.window)
        self.button = Button()
        while self.run:
            self.window.blit(self.background, (0, 0))
            self.event_treatment()
            if self.page == "INITIAL":
                self.screen.front_page()
            if self.page == "SELECT":
                self.screen.select_level()
                self.level = self.button.event_treatment()
                self.run = self.button.run
                if isinstance(self.level, int):
                    L = Level(self.level)
                    self.page = L.run_level(self.window, self.background, self.screen)

            if self.page == "PLAYING":
                L = Level(self.level)
                self.page = L.run_level(self.window, self.background, self.screen)

            if self.page == "VICTORY":
                self.screen.victory()
            pygame.display.flip()
            

class Level():
    """Cria, manipula e renderiza as fases (levels) do jogo.
    """    
    def __init__(self, level:int) -> None:
        """Inicializa a classe Level.

        Args:
            level (int): número da fase selecionada
        """        
        self.level = level
        self.moving_sprites = pygame.sprite.Group()
        with open('levels.txt', 'r') as arq:
            file = arq.readlines()

        self.all_levels_info = [ast.literal_eval(line) for line in file]
        self.create_positions()
        self.top_left_x = (800 - self.dimension[0][0]*30) // 2 - 20
        self.top_left_y = (700 - self.dimension[0][1]*30) // 2
        self.create_level()
        self.level_running = True

    def create_positions(self) -> None:
        """Define as posições dos objetos (sprites) da fase selecionada.
        """        
        self.player_position = self.all_levels_info[self.level]['robot_position']
        self.boxes_positions = self.all_levels_info[self.level]['boxes_positions']
        self.goal_positions = self.all_levels_info[self.level]['goal_positions']
        self.walls_positions = self.all_levels_info[self.level]['walls_positions']
        self.walk_positions = self.all_levels_info[self.level]['walk_positions']
        self.dimension = self.all_levels_info[self.level]['dimension']

    def create_level(self) -> None:
        """Cria os sprite da fase selecionada
        """        
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
    
    def run_level(self, window:pygame.Surface, background:pygame.Surface, screen) -> str:
        """

        Args:
            window (pygame.Surface): janela de execução do jogo
            background (pygame.Surface): imagem de fundo
            screen (Screen): objeto do tipo screen, cria o layout da tela

        Returns:
            str: informação de qual screen está sendo executada (tela inicial, jogo, tela de vitória etc)
        """        
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        movimentos = 0
        while self.level_running:
            window.blit(background, (0, 0))
            screen.game(movimentos, start_time, self.top_left_y, self.level)
            movimentos += self.player.robot_event_treatment()
            self.moving_sprites.draw(window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.level_running = False
                    pygame.display.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.level_running = False
                        pygame.display.quit()
                        quit()
                    if event.key == pygame.K_ESCAPE:
                        self.level_running = False
                        return "SELECT"
                    if event.key == pygame.K_r:
                        self.create_positions()
                        self.create_level()
                        self.run_level(window, background, screen)
                        self.level_running = False

                if all([box.in_goal for box in Box.objects]):
                    self.level_running = False
                    pygame.mixer.Sound("sounds\\som_de_vitoria.wav").play()
                    return "VICTORY"

            pygame.display.flip()
            clock.tick(7)


class Screen():
    def __init__(self, window:pygame.Surface) -> None:
        """Inicializa objeto da classe Screen.

        Args:
            window (pygame.Surface): _description_
        """        
        self.window = window
        self.width = window.get_width()
        self.height = window.get_height()
        self.font = 'fonts/Symtext.ttf'

    def front_page(self) -> None:
        """Renderiza a tela inicial do jogo.
        """        
        font = pygame.font.Font(self.font, 100)
        text = font.render('ROBOX', True, (40, 40, 40))
        self.window.blit(text, (self.width / 2 - (text.get_width() / 2), self.height / 2 - 200))
        text = font.render('FOREVER', True, (15,15,15))
        self.window.blit(text, (self.width / 2 - (text.get_width() / 2), self.height / 2 - 100))
        
        font = pygame.font.Font(self.font, 20)
        text = font.render('Press SPACE to continue', True, (10,10,10))
        self.window.blit(text, (self.width / 2 - (text.get_width() / 2), self.height / 2 + 50))

    def select_level(self) -> None:
        """Renderiza a tela de seleção de fase.
        """        
        font = pygame.font.Font(self.font, 60)
        text = font.render('SELECT LEVEL', True, (30, 30, 30))
        self.window.blit(text, (self.width / 2 - (text.get_width() / 2), 80))

        level = 0
        for y in range(3):
            for x in range(5):
                dim = 80
                pos_x = x*(self.width/5 - 20)-dim/2 + 120
                pos_y = y*((self.height - 300)/3) + dim + 150
                title = 'LEVEL ' + str(level + 1)
                font = pygame.font.Font(self.font, 15)
                text = font.render(title, True, (30, 30, 30))
                self.window.blit(text, ((pos_x + (dim - text.get_width())/2, pos_y - text.get_height())))
                rect_level = pygame.Rect(pos_x, pos_y, dim, dim)
                image_level = pygame.image.load('images\\level' + str(level + 1) + '.png')
                image_level = pygame.transform.smoothscale(image_level.convert_alpha(), (dim, dim))
                self.window.blit(image_level, (pos_x, pos_y))
       
                Button.objects.append(rect_level)
                level += 1

    def game(self, movimentos:int, start_time:int, top_left_y:int, level:int) -> None:
        """Renderiza os textos da tela da fase sendo jogada.

        Args:
            movimentos (int): quantidade de vezes de o jogador moveu uma caixa
            start_time (int): tempo inicial da fase
            top_left_y (int): ordenada do canto superior do mapa da fase
            level (int): número da fase selecionada
        """        
        title = title = 'LEVEL ' + str(level + 1)
        font = pygame.font.Font(self.font, 20)
        text = font.render(f'MOVIMENTOS: {movimentos}', True, (30, 30, 30))
        textRect = text.get_rect()
        textRect.center = (100, top_left_y)
        self.window.blit(text, textRect)
        counting_time = pygame.time.get_ticks() - start_time
        counting_seconds = str( round((counting_time)/1000) ).zfill(1)
        counting_text = font.render(f'TIMER: {counting_seconds}', True, (30, 30, 30))
        counting_rect = counting_text.get_rect()
        counting_rect.center = (650, top_left_y)
        self.window.blit(counting_text, counting_rect)
        font = pygame.font.Font(self.font, 60)
        text = font.render(title, True, (30, 30, 30))
        self.window.blit(text, (self.width / 2 - (text.get_width() / 2), 80))

    def victory(self) -> None:
        """Renderiza a tela de vitória.
        """        
        font = pygame.font.Font(self.font, 60)
        label = font.render('CONGRATULATIONS!!!', True, (150, 150, 0))
        self.window.blit(label, (self.width / 2 - (label.get_width() / 2), self.height / 2 - 50))

        font = pygame.font.Font(self.font, 20)
        label = font.render('Press SPACE to continue', True, (150, 150, 0))
        self.window.blit(label, (self.width / 2 - (label.get_width() / 2), self.height / 2 + 50))


class Button:
    objects = []
    def __init__(self) -> None:
        """Inicializa objeto da classe Button
        """        
        self.run = True
    def event_treatment(self) -> int:
        """Trata os eventos do input referentes ao Button.

        Returns:
            int: retorna o número da fase escolhida
        """        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos() 
                for button in self.__class__.objects:
                    if button.collidepoint(mouse_position):
                        return self.__class__.objects.index(button)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.run = False
    

def convert_coordinates(position:tuple[int,int], x:int, y:int) -> tuple[int,int]:
    """Converte as coordenadas do formato recebido no arquivo levels.txt para o utilizado no jogo

    Args:
        position (tuple[int,int]): coordenadas de posição no formato do arquivo levels.txt
        x (int): constante para shiftar a posição no eixo horizontal
        y (int): constante para shiftar a posição no eixo vertical

    Returns:
        tuple[int,int]: coordenadas de posição no formato do jogo
    """    
    return ((position[0]*30 + x, position[1]*30 + y))

if __name__ == '__main__':
    G = Game((800, 700))
    G.loop()