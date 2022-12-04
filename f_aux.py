import pygame
from game_classes import *

S_WIDTH = 800
S_HEIGHT = 700
fonte_geral = 'fonts/Symtext.ttf'

def select_level(level, position, window):
    dim = 80
    pos_x = position[0]*(S_WIDTH/5 - 20)-dim/2 + 120
    pos_y = position[1]*((S_HEIGHT - 300)/3) + dim + 150
    text = 'LEVEL ' + str(level + 1)
    font = pygame.font.Font(fonte_geral, 15)
    label = font.render(text, True, (30, 30, 30))
    window.blit(label, ((pos_x + (dim - label.get_width())/2, pos_y - label.get_height())))
    rect_level = pygame.Rect(pos_x, pos_y, dim, dim)
    image_level = pygame.image.load('images\\level' + str(level + 1) + '.png')
    image_level = pygame.transform.smoothscale(image_level.convert_alpha(), (dim, dim))
    window.blit(image_level, (pos_x, pos_y))

    return (rect_level, level, text)

def button_esc(window):
    dim = 50
    pos_x = 10
    pos_y = 10
    rect_level = pygame.Rect(pos_x, pos_y, dim, dim)

    image_level = pygame.image.load('images/Esc.gif')
    image_level = pygame.transform.smoothscale(image_level.convert_alpha(), (dim, dim))
    window.blit(image_level, (pos_x, pos_y))
    return rect_level

def button_restart(window):
    dim = 50
    pos_x = 50
    pos_y = 10
    rect_level = pygame.Rect(pos_x, pos_y, dim, dim)
    image_level = pygame.image.load('images/Restart.gif')
    image_level = pygame.transform.smoothscale(image_level.convert_alpha(), (dim, dim))
    window.blit(image_level, (pos_x, pos_y))
    return rect_level

def time_and_movement_and_title(movimentos, start_time, top_left_y, window, title):
    font = pygame.font.Font(fonte_geral, 20)
    text = font.render(f'MOVIMENTOS: {movimentos}', True, (30, 30, 30))
    textRect = text.get_rect()
    textRect.center = (100, top_left_y)
    window.blit(text, textRect)
    counting_time = pygame.time.get_ticks() - start_time
    counting_seconds = str( round((counting_time)/1000) ).zfill(1)
    counting_text = font.render(f'TIMER: {counting_seconds}', True, (30, 30, 30))
    counting_rect = counting_text.get_rect()
    counting_rect.center = (650, top_left_y)
    window.blit(counting_text, counting_rect)
    font = pygame.font.Font(fonte_geral, 60)
    label = font.render(title, True, (30, 30, 30))
    window.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), 80))

def create_objects(moving_sprites, top_left_x, top_left_y, player, goal_positions, boxes_positions, walls_positions, walk_positions):
    #Cria os objetos em suas respectivas categorias
    for tipo in [[walk_positions, Walk], [walls_positions, Wall], [goal_positions, Goal], [boxes_positions, Box]]:
        #Retira todos os objetos possivelmente existentes na categoria
        if tipo[1] is not Walk:
            tipo[1].objects.clear()
        #Adiciona os objetos
        for block in tipo[0]:
            object = tipo[1](block[0]*30 + top_left_x, block[1]*30 + top_left_y)
            moving_sprites.add(object)
    moving_sprites.add(player)
    return moving_sprites

def update_version(list_versions, player, top_left_x, top_left_y):
    dict = {}
    dict['robot_position'] = [(int((player.x - top_left_x)/30), int((player.y - top_left_y)/30))]
    dict['boxes_positions'] = [(int((box.x - top_left_x)/30), int((box.y - top_left_y)/30)) for box in Box.objects]
    
    list_versions.append(dict)