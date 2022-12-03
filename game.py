import pygame
import ast
from game_classes import *

pygame.init()
pygame.font.init()

#Definição do tamanho da janela
S_WIDTH = 800
S_HEIGHT = 700

def draw_levels(lista_dict, level):
    global player_position, boxes_positions, goal_positions, walls_positions, walk_positions, dimension

    player_position = lista_dict[level]['robot_position']
    boxes_positions = lista_dict[level]['boxes_positions']
    goal_positions = lista_dict[level]['goal_positions']
    walls_positions = lista_dict[level]['walls_positions']
    walk_positions = lista_dict[level]['walk_positions']
    dimension = lista_dict[level]['dimension']

def time_and_moviment(movimentos, start_time, top_left_y):
    font = pygame.font.SysFont('Times New Roman', 20)
    text = font.render(f'MOVIMENTOS: {movimentos}', True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (100, top_left_y)
    window.blit(text, textRect)
    counting_time = pygame.time.get_ticks() - start_time
    counting_seconds = str( round((counting_time)/1000) ).zfill(1)
    counting_text = font.render(f'TIMER: {counting_seconds}', True, (255,255,255))
    counting_rect = counting_text.get_rect()
    counting_rect.center = (650, top_left_y)
    window.blit(counting_text, counting_rect)

def create_objects(moving_sprites, top_left_x, top_left_y, player):
    #Cria os objetos em suas respectivas categorias
    for cat in [[walk_positions, Walk], [walls_positions, Wall], [goal_positions, Goal], [boxes_positions, Box]]:
        #Retira todos os objetos possivelmente existentes na categoria
        if cat[1] is not Walk:
            cat[1].objects.clear()
        #Adiciona os objetos
        for block in cat[0]:
            object = cat[1](block[0]*30 + top_left_x, block[1]*30 + top_left_y)
            moving_sprites.add(object)
    moving_sprites.add(player)
    return moving_sprites

def exec_game():
    global grid, r, g, b, color, movimentos

    #Centralização do mapa na tela
    top_left_x = (S_WIDTH - dimension[0][0]*30) // 2
    top_left_y = (S_HEIGHT - dimension[0][1]*30) // 2
    moving_sprites = pygame.sprite.Group()
    player = Robo(player_position[0][0]*30 + top_left_x, player_position[0][1]*30 + top_left_y)

    #Criação dos objetos 
    moving_sprites = create_objects(moving_sprites, top_left_x, top_left_y, player)

    #Inicialização do relógio e contador de movimentos
    clock = pygame.time.Clock()
    movimentos = 0
    start_time = pygame.time.get_ticks()

    #Execução do jogo
    run = True
    while run:
        #Tratamento de eventos (teclas para sair do jogo)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    pygame.display.quit()
                    quit()
                elif event.key == pygame.K_r:
                    exec_game()
                    run = False
                elif event.key == pygame.K_ESCAPE:
                    color = (0, 0, 160)
                    main()
                    run = False

        comandos =  pygame.key.get_pressed()
    
        #Movimento do jogador
        if comandos[pygame.K_UP] or comandos[pygame.K_w]:
            movimentos += player.move(0, -1, 0)
        if comandos[pygame.K_DOWN] or comandos[pygame.K_s]:
            movimentos += player.move(0, 1, 1)
        if comandos[pygame.K_LEFT] or comandos[pygame.K_a]:
            movimentos += player.move(-1, 0, 2)
        if comandos[pygame.K_RIGHT] or comandos[pygame.K_d]:
            movimentos += player.move(1, 0, 3)

        window.fill((0,0,0))
        
        moving_sprites.draw(window)

        #Condição de vitória
        box_pos = [(box.x, box.y) for box in Box.objects]
        goal_pos = [(goal.x, goal.y) for goal in Goal.objects]
        diff = [x for x in box_pos if x not in goal_pos]
        if diff == []:
            run = False

        #Contagem do tempo e movimentos
        time_and_moviment(movimentos, start_time, top_left_y)

        pygame.display.flip()
        clock.tick(7)

    color = (255, 255, 0)        

def main_menu():
    global color

    run = True
    color = (0, 0, 160)
    
    while run:
        window.fill(color)
        
        font = pygame.font.SysFont('Times New Roman', 100)
        label = font.render('ROBLOX', True, (255,255,255))
        window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), S_HEIGHT / 2 - 150))
        label = font.render('FOREVER', True, (255,255,255))
        window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), S_HEIGHT / 2 + 30)) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    pygame.display.quit()
                    quit()
            
                elif event.key == pygame.K_SPACE:   
                    main()
            
                elif event.key == pygame.K_r:
                    main()
        
        pygame.display.update()

def main():
    global color, robot_position, boxes_positions, goal_positions, locked_positions, level, rect_level1, rect_level2, rect_level3, dimension
    with open('levels.txt', 'r') as arq:
        file = arq.readlines()

    lista_dict = [ast.literal_eval(line) for line in file]
    level = None
    run = True

    while run:
        window.fill(color)
        if color == (255, 255, 0):
           font = pygame.font.SysFont('Times New Roman', 60)
           label = font.render('WELL', True, (255,255,255))
           window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), S_HEIGHT / 2 - 150)) 
           label = font.render('CONGRATULATIONS', True, (255,255,255))
           window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), S_HEIGHT / 2 - 50))
           label = font.render('GENIUS!!!', True, (255,255,255))
           window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), S_HEIGHT / 2 + 50))

        elif color == (0, 0, 160):
            font = pygame.font.SysFont('Times New Roman', 60)
            label = font.render('SELECT LEVEL', True, (255,255,255))
            window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), S_HEIGHT / 6 - 60))
            font = pygame.font.SysFont('Times New Roman', 40)
            label = font.render('LEVEL 1', True, (255,255,255))
            window.blit(label, (S_WIDTH / 4 - (label.get_width() / 2), (3*S_HEIGHT) / 8 - 100))
            label = font.render('LEVEL 2', True, (255,255,255))
            window.blit(label, ((3*S_WIDTH) / 4 - (label.get_width() / 2), (3*S_HEIGHT) / 8 - 100))
            label = font.render('LEVEL 3', True, (255,255,255))
            window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), (17*S_HEIGHT) / 24 - 100))
            
            rect_level1 = pygame.Rect(S_WIDTH / 4 - 50, (5*S_HEIGHT) / 12 - 60, 100, 100)
            pygame.draw.rect( window, (0,0,0), rect_level1)
            level1 = pygame.image.load('images\\level1.png')
            level1 = pygame.transform.scale(level1, (100, 100))
            window.blit(level1, (S_WIDTH / 4 - 50, (5*S_HEIGHT) / 12 - 60))

            rect_level2 = pygame.Rect((3*S_WIDTH) / 4 - 50, (5*S_HEIGHT) / 12 - 60, 100, 100)
            pygame.draw.rect( window, (0,0,0), rect_level2)
            level2 = pygame.image.load('images\\level2.png')
            level2 = pygame.transform.scale(level2, (100, 100))
            window.blit(level2, ((3*S_WIDTH) / 4 - 50, (5*S_HEIGHT) / 12 - 60))

            rect_level3 = pygame.Rect(S_WIDTH / 2 - 50, (3*S_HEIGHT) / 4 - 60, 100, 100)
            pygame.draw.rect( window, (0,0,0), rect_level3)
            level3 = pygame.image.load('images\\level3.png')
            level3 = pygame.transform.scale(level3, (100, 100))
            window.blit(level3, (S_WIDTH / 2 - 50, (3*S_HEIGHT) / 4 - 60))
           
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos() 
                if rect_level1.collidepoint(mouse_position) and color == (0, 0, 160):
                    draw_levels(lista_dict, 0)
                    exec_game()
                
                if rect_level2.collidepoint(mouse_position) and color == (0, 0, 160):
                    draw_levels(lista_dict, 1)
                    exec_game()

                if rect_level3.collidepoint(mouse_position) and color == (0, 0, 160):
                    draw_levels(lista_dict, 2)
                    exec_game()

            #Eventos associados a cada tecla quando o jogo não está rodando
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    pygame.display.quit()
                    quit()
            
                elif event.key == pygame.K_1:  
                    level = 0
                    draw_levels(lista_dict, level)
                    exec_game()

                elif event.key == pygame.K_2:  
                    level = 1
                    draw_levels(lista_dict, level)
                    exec_game()

                elif event.key == pygame.K_3: 
                    level = 2 
                    draw_levels(lista_dict, level)
                    exec_game()

                elif event.key == pygame.K_4:  
                    level = 3
                    draw_levels(lista_dict, level)
                    exec_game()

                elif event.key == pygame.K_5:  
                    level = 4
                    draw_levels(lista_dict, level)
                    exec_game()

                elif event.key == pygame.K_6:  
                    level = 5
                    draw_levels(lista_dict, level)
                    exec_game()

                elif event.key == pygame.K_7:  
                    level = 6
                    draw_levels(lista_dict, level)
                    exec_game()

                elif event.key == pygame.K_8:  
                    level = 8
                    draw_levels(lista_dict, level)
                    exec_game()

                elif event.key == pygame.K_r:
                    exec_game()
                
                #Tecla para passagem de fase
                elif event.key == pygame.K_SPACE:
                    #Caso em que não restam fases
                    if level == len(lista_dict) - 1:
                        color = (0, 0, 160)
                        main()
                        return
                    #Caso em que há uma fase seguinte -> passa de fase
                    elif isinstance(level, int):
                        level += 1 
                        draw_levels(lista_dict, level)
                        exec_game()
                
                elif event.key == pygame.K_ESCAPE:
                    color = (0, 0, 160)
                    main()
                    run = False

        pygame.display.update()

window = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption("Sokoban")

main_menu()