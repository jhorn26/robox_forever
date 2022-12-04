import pygame
import ast
from game_classes import *
from f_aux import *

pygame.init()
pygame.font.init()

#Definição do tamanho da janela
S_WIDTH = 800
S_HEIGHT = 700

background = pygame.image.load('images\\background.png')
background = pygame.transform.scale(background, (800, 700))

def exec_game(player_position, goal_positions, boxes_positions, walls_positions, walk_positions, dimension):
    global color

    #Imagem de fundo
    window.blit(background, (0, 0))

    #Centralização do mapa na tela
    top_left_x = (S_WIDTH - dimension[0][0]*30) // 2 - 20
    top_left_y = (S_HEIGHT - dimension[0][1]*30) // 2
    moving_sprites = pygame.sprite.Group()
    player = Robo(player_position[0][0]*30 + top_left_x, player_position[0][1]*30 + top_left_y)

    #Criação dos objetos 
    moving_sprites = create_objects(moving_sprites, top_left_x, top_left_y, player, goal_positions, boxes_positions, walls_positions, walk_positions)

    #Inicialização do relógio e contador de movimentos
    clock = pygame.time.Clock()
    movimentos = 0
    start_time = pygame.time.get_ticks()
    movimentos_aux = 0
    list_versions = []
    update_version(list_versions, player, top_left_x, top_left_y)

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
                    boxes_positions = exec_game(player_position, goal_positions, boxes_positions, walls_positions, walk_positions, dimension)
                    run = False
                elif event.key == pygame.K_ESCAPE:
                    color = (0, 0, 160)
                    main()
                    run = False
                elif event.key == pygame.K_z:
                    if len(list_versions) > 1:
                        player = Robo(list_versions[-2]['robot_position'][0][0]*30 + top_left_x, list_versions[-2]['robot_position'][0][1]*30 + top_left_y)
                        boxes_positions = list_versions[-2]['boxes_positions']
                        moving_sprites = pygame.sprite.Group()
                        create_objects(moving_sprites, top_left_x, top_left_y, player, goal_positions, boxes_positions, walls_positions, walk_positions)
                        list_versions.pop()

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

        if movimentos > movimentos_aux:
            update_version(list_versions, player, top_left_x, top_left_y)
            movimentos_aux += 1

        window.fill((0,0,0))
        window.blit(background, (0, 0))
        
        moving_sprites.draw(window)

        #Condição de vitória
        box_pos = [(box.x, box.y) for box in Box.objects]
        goal_pos = [(goal.x, goal.y) for goal in Goal.objects]
        diff = [x for x in box_pos if x not in goal_pos]
        if diff == []:
            run = False

        #Contagem do tempo e movimentos
        time_and_movement_and_title(movimentos, start_time, top_left_y, window, title)

        pygame.display.flip()
        clock.tick(7)

    color = (255, 255, 0)  
    if run == False:
        return boxes_positions

def main_menu():
    global color

    run = True
    color = (0, 0, 160)
    
    while run:
        window.fill(color)
        window.blit(background, (0, 0))
        
        font = pygame.font.SysFont('Times New Roman', 100)
        label = font.render('ROBOX', True, (30, 30, 30))
        window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), S_HEIGHT / 2 - 150))
        label = font.render('FOREVER', True, (30, 30, 30))
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
    global color, title
    with open('levels.txt', 'r') as arq:
        file = arq.readlines()

    lista_dict = [ast.literal_eval(line) for line in file]
    level = None
    menu = []
    run = True

    while run:
        window.fill(color)
        window.blit(background, (0, 0))

        if color == (255, 255, 0):
           font = pygame.font.SysFont('Times New Roman', 60)
           label = font.render('WELL DONE', True, (30, 30, 30))
           window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), S_HEIGHT / 2 - 150)) 
           label = font.render('CONGRATULATIONS', True, (30, 30, 30))
           window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), S_HEIGHT / 2 - 50))
           label = font.render('GENIUS!!!', True, (30, 30, 30))
           window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), S_HEIGHT / 2 + 50))

        elif color == (0, 0, 160):
            font = pygame.font.SysFont('Times New Roman', 60)
            label = font.render('SELECT LEVEL', True, (30, 30, 30))
            window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), 80))

            i = 0
            for j in range(3):
                for k in range(5):
                    menu.append(select_level(i, (k, j), window))
                    i += 1
           
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos() 
                for levels in menu:
                    if levels[0].collidepoint(mouse_position) and color == (0, 0, 160):
                        level = levels[1]
                        player_position = lista_dict[level]['robot_position']
                        boxes_positions = lista_dict[level]['boxes_positions']
                        goal_positions = lista_dict[level]['goal_positions']
                        walls_positions = lista_dict[level]['walls_positions']
                        walk_positions = lista_dict[level]['walk_positions']
                        dimension = lista_dict[level]['dimension']
                        title = levels[2]
                        boxes_positions = exec_game(player_position, goal_positions, boxes_positions, walls_positions, walk_positions, dimension)

            #Eventos associados a cada tecla quando o jogo não está rodando
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    pygame.display.quit()
                    quit()

                elif event.key == pygame.K_r:
                    boxes_positions = exec_game(player_position, goal_positions, boxes_positions, walls_positions, walk_positions, dimension)
                
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
                        title = 'LEVEL ' + str(level + 1)
                        player_position = lista_dict[level]['robot_position']
                        boxes_positions = lista_dict[level]['boxes_positions']
                        goal_positions = lista_dict[level]['goal_positions']
                        walls_positions = lista_dict[level]['walls_positions']
                        walk_positions = lista_dict[level]['walk_positions']
                        dimension = lista_dict[level]['dimension']

                        boxes_positions = exec_game(player_position, goal_positions, boxes_positions, walls_positions, walk_positions, dimension)
                
                elif event.key == pygame.K_ESCAPE:
                    color = (0, 0, 160)
                    main()
                    run = False

        pygame.display.update()

window = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption("Sokoban")

main_menu()