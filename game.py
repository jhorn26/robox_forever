import pygame

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


def create_grid(locked_positions={}, objects_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(10)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                grid[i][j] = (100, 100, 100)
            if (j,i) in objects_positions:
                grid[i][j] = (160, 82, 45)

    return grid


def valid_space(object, grid):    
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(10)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = (object.x, object.y)

    
    if formatted not in accepted_positions:
        if formatted[1] > -1 or formatted[0] > -1:
            return False

    return True


def push_space(shape, grid):    
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0) or grid[i][j] == (160,82,45)] for i in range(10)]
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
    global grid, r, g, b

    robot = Piece(3, 3, (255, 0, 0))
    boxes_positions = [(1,6), (2,7), (6,8)]
    locked_positions = [(4,5)]
    boxes = [Piece(boxes_positions[i][0], boxes_positions[i][1], (160, 82, 45)) for i in range(len(boxes_positions))]
    objects_positions = [(box.x, box.y) for box in boxes]
    grid = create_grid(locked_positions, objects_positions)
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
                             
                if event.key == pygame.K_LEFT:
                    robot.x -= 1
                    if not push_space(robot, grid):
                        robot.x += 1
                    for box in boxes:
                        if box.x==robot.x and box.y==robot.y:
                            box.x -= 1
                            if not valid_space(box, grid):
                                box.x += 1
                                robot.x += 1

                elif event.key == pygame.K_RIGHT:
                    robot.x += 1
                    if not push_space(robot, grid):
                        robot.x -= 1
                    for box in boxes:
                        if box.x==robot.x and box.y==robot.y:
                            box.x += 1
                            if not valid_space(box, grid):
                                box.x -= 1
                                robot.x -= 1
               
                elif event.key == pygame.K_UP:
                    robot.y -= 1
                    if not push_space(robot, grid):
                        robot.y += 1
                    for box in boxes:
                        if box.x==robot.x and box.y==robot.y:
                            box.y -= 1
                            if not valid_space(box, grid):
                                box.y += 1
                                robot.y += 1
                    
                elif event.key == pygame.K_DOWN:
                    robot.y += 1
                    if not push_space(robot, grid):
                        robot.y -= 1
                    for box in boxes:
                        if box.x==robot.x and box.y==robot.y:
                            box.y += 1
                            if not valid_space(box, grid):
                                box.y -= 1
                                robot.y -= 1

                elif event.key == pygame.K_r:
                    main()
                                  
        
        x, y = robot.x, robot.y
        if y > -1:
            grid[y][x] = robot.color

        for box in boxes:
            x, y = box.x, box.y
            if y > -1:
                grid[y][x] = box.color

        draw_window(win, r, g, b)
               
        pygame.display.update() 
        


win = pygame.display.set_mode((s_width, s_height))

r = 100
g = 100
b = 100

main()      