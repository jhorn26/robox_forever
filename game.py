import pygame

pygame.init()
pygame.font.init()


s_width = 800
s_height = 700
play_width = 300 
play_height = 300


top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 200


def create_grid():
    grid = [[(0,0,0) for x in range(10)] for x in range(10)]

    return grid


def draw_window(surface, r, g, b):
    surface.fill((r,g,b))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)


def main():
    global grid, r, g, b

    grid = create_grid()
    run = True

    while run:

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
      
        
        draw_window(win, r, g, b)
               
        pygame.display.update() 
        

win = pygame.display.set_mode((s_width, s_height))

r = 100
g = 100
b = 100

main()
