import pygame
import ast


pygame.init()
pygame.font.init()


s_width = 800
s_height = 700
play_width = 300 
play_height = 300


top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 200


class Piece(object): 

    def __init__(self, column, row, color):
        self.x = column 
        self.y = row
        self.color = color
        self.rotation = 0


def create_grid(locked_positions=[], objects_positions=[]):
    grid = [[(0,0,0) for x in range(10)] for x in range(10)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                grid[i][j] = (100, 100, 100) # type: ignore
            if (j,i) in objects_positions:
                grid[i][j] = (160, 82, 45) # type: ignore
    return grid

def valid_space(object, grid):    
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0) or grid[i][j] == (255, 192, 203)] for i in range(10)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = (object.x, object.y)

    
    if formatted not in accepted_positions:
        if formatted[1] > -1 or formatted[0] > -1:
            return False

    return True

def push_space(shape, grid):    
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0) or grid[i][j] == (160,82,45) or grid[i][j] == (255, 192, 203)] for i in range(10)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = (shape.x, shape.y)

    if formatted not in accepted_positions:
        if formatted[1] > -1 or formatted[0] > -1:
            return False
                
    return True


def draw_window(surface, r, g, b):
    surface.fill((r,g,b))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)


def main():
    global grid, r, g, b, color, movimentos, robot_position, boxes_positions, goal_positions, locked_positions

    robot = Piece(robot_position[0][0], robot_position[0][1], (255, 0, 0))
    boxes = [Piece(boxes_positions[i][0], boxes_positions[i][1], (160, 82, 45)) for i in range(len(boxes_positions))]
    objects_positions = [(box.x, box.y) for box in boxes]
    grid = create_grid(locked_positions, objects_positions)
    clock = pygame.time.Clock()
    movimentos = 0
    start_time = pygame.time.get_ticks() 

    run = True

    while run:
        
        objects_positions = [(box.x, box.y) for box in boxes]
        grid = create_grid(locked_positions, objects_positions)

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
                    main()
                    run = False
                
                elif event.key == pygame.K_ESCAPE:
                    color = (0, 0, 160)
                    main_opt()
                    run = False

        comandos =  pygame.key.get_pressed()
           
        if comandos[pygame.K_UP] or comandos[pygame.K_w]:
            robot.y -= 1
            if not push_space(robot, grid):
                    robot.y += 1
            for box in boxes:
                if box.x==robot.x and box.y==robot.y:
                    box.y -= 1
                    movimentos += 1
                    if not valid_space(box, grid):
                        box.y += 1
                        robot.y += 1
                        movimentos -= 1

        if comandos[pygame.K_DOWN] or comandos[pygame.K_s]:
            robot.y += 1
            if not push_space(robot, grid):
                    robot.y -= 1
            for box in boxes:
                if box.x==robot.x and box.y==robot.y:
                    box.y += 1
                    movimentos += 1
                    if not valid_space(box, grid):
                        box.y -= 1
                        robot.y -= 1
                        movimentos -= 1

        if comandos[pygame.K_LEFT] or comandos[pygame.K_a]:
            robot.x -= 1
            if not push_space(robot, grid):
                    robot.x += 1
            for box in boxes:
                if box.x==robot.x and box.y==robot.y:
                    box.x -= 1
                    movimentos += 1
                    if not valid_space(box, grid):
                        box.x += 1
                        robot.x += 1
                        movimentos -= 1

        if comandos[pygame.K_RIGHT] or comandos[pygame.K_d]:
            robot.x += 1
            if not push_space(robot, grid):
                    robot.x -= 1
            for box in boxes:
                if box.x==robot.x and box.y==robot.y:
                    box.x += 1
                    movimentos += 1
                    if not valid_space(box, grid):
                        box.x -= 1
                        robot.x -= 1
                        movimentos -= 1

        
        for goal in goal_positions:
            x, y = goal[0], goal[1]
            if y > -1:
                grid[y][x] = (255, 192, 203) # type: ignore
        
        x, y = robot.x, robot.y
        if y > -1:
            grid[y][x] = robot.color # type: ignore
        
        for box in boxes:
            x, y = box.x, box.y
            if y > -1:
                grid[y][x] = box.color # type: ignore
        
        for box in boxes:
            if (box.x, box.y) in goal_positions:
                grid[box.y][box.x] = (139, 0, 0) # type: ignore

                
        draw_window(win, r, g, b)
        

        done = all([grid[pos[1]][pos[0]] == (139, 0, 0) for pos in goal_positions])
        
        font = pygame.font.SysFont('Times New Roman', 20)
        text = font.render(f'MOVIMENTOS: {movimentos}', True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (100,300)
        win.blit(text, textRect)

        counting_time = pygame.time.get_ticks() - start_time
        counting_seconds = str( round((counting_time%60000)/1000) ).zfill(1)

        counting_text = font.render(f'TIMER: {counting_seconds}', True, (255,255,255))
        counting_rect = counting_text.get_rect()
        counting_rect.center = (650,300)
        
        win.blit(counting_text, counting_rect)
        
        pygame.display.flip()
        clock.tick(7)
        
        if done:
            run = False
        
    
    color = (255, 255, 0)
    
        

def main_menu():
    global color

    run = True
    color = (0, 0, 160)
    
    while run:
        win.fill(color)
        
        font = pygame.font.SysFont('Times New Roman', 100)
        label = font.render('ROBLOX', True, (255,255,255))
        win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), s_height / 2 - 150))
        label = font.render('FOREVER', True, (255,255,255))
        win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), s_height / 2 + 30)) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    pygame.display.quit()
                    quit()
            
            
                elif event.key == pygame.K_SPACE:   
                    main_opt()
            
                elif event.key == pygame.K_r:
                    main_opt()
        
        pygame.display.update()

def main_opt():
    global color, robot_position, boxes_positions, goal_positions, locked_positions, level
    with open('arquivo.txt', 'r') as arq:
        file = arq.readlines()

    lista_dict = [ast.literal_eval(line) for line in file]
    level = None
    run = True

    while run:
        win.fill(color)
        if color == (255, 255, 0):
           font = pygame.font.SysFont('Times New Roman', 60)
           label = font.render('WELL', True, (255,255,255))
           win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), s_height / 2 - 150)) 
           label = font.render('CONGRATULATIONS', True, (255,255,255))
           win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), s_height / 2 - 50))
           label = font.render('GENIUS!!!', True, (255,255,255))
           win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), s_height / 2 + 50))  

        elif color == (0, 0, 160):
            font = pygame.font.SysFont('Times New Roman', 60)
            label = font.render('PRESS 1 TO SELECT LEVEL 1', True, (255,255,255))
            win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), s_height / 2 - 150))
            label = font.render('PRESS 2 TO SELECT LEVEL 2', True, (255,255,255))
            win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), s_height / 2 + 50))
           

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    pygame.display.quit()
                    quit()
            
                elif event.key == pygame.K_1:  
                    level = 0 
                    robot_position = lista_dict[level]['robot_position']
                    boxes_positions = lista_dict[level]['boxes_positions']
                    goal_positions = lista_dict[level]['goal_positions']
                    locked_positions = lista_dict[level]['locked_positions']
                    main()

                elif event.key == pygame.K_2:  
                    level = 1
                    robot_position = lista_dict[level]['robot_position']
                    boxes_positions = lista_dict[level]['boxes_positions']
                    goal_positions = lista_dict[level]['goal_positions']
                    locked_positions = lista_dict[level]['locked_positions']
                    main()
                
                elif event.key == pygame.K_r:
                    main()

                elif event.key == pygame.K_SPACE:
                    if level == len(lista_dict)-1:
                        color = (0, 0, 160)
                        main_opt()
                        run = False
                    elif isinstance(level, int):
                        level += 1 
                        robot_position = lista_dict[level]['robot_position']
                        boxes_positions = lista_dict[level]['boxes_positions']
                        goal_positions = lista_dict[level]['goal_positions']
                        locked_positions = lista_dict[level]['locked_positions']
                        main()
                
                elif event.key == pygame.K_ESCAPE:
                    color = (0, 0, 160)
                    main_opt()
                    run = False


        pygame.display.update()

win = pygame.display.set_mode((s_width, s_height))

r = 100
g = 100
b = 100

main_menu()