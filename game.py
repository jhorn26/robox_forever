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

    def _init_(self, column, row, color):
        self.x = column 
        self.y = row
        self.color = color


def create_grid():
    grid = [[(0,0,0) for x in range(10)] for x in range(10)]

    return grid


def valid_space(object, grid):    
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(10)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = (object.x, object.y)

    
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
    grid = create_grid()
    run = True

    while run:
        
        grid = create_grid()

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
                    if not valid_space(robot, grid):
                        robot.x += 1

                elif event.key == pygame.K_RIGHT:
                    robot.x += 1
                    if not valid_space(robot, grid):
                        robot.x -= 1
               
                elif event.key == pygame.K_UP:
                    robot.y -= 1
                    if not valid_space(robot, grid):
                        robot.y += 1
                    
                elif event.key == pygame.K_DOWN:
                    robot.y += 1
                    if not valid_space(robot, grid):
                        robot.y -= 1
                                  
        
        x, y = robot.x, robot.y
        if y > -1:
            grid[y][x] = robot.color

        draw_window(win, r, g, b)
               
        pygame.display.update() 
        


win = pygame.display.set_mode((s_width, s_height))

r = 100
g = 100
b = 100

main()
