import pygame

class Screen():
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font = 'fonts/Symtext.ttf'

    def front_page(self):
        font = pygame.font.Font(self.font, 100)
        text = font.render('ROBOX', True, (40, 40, 40))
        self.screen.blit(text, (self.width / 2 - (text.get_width() / 2), self.height / 2 - 200))
        text = font.render('FOREVER', True, (15,15,15))
        self.screen.blit(text, (self.width / 2 - (text.get_width() / 2), self.height / 2 - 100))
        
        font = pygame.font.Font(self.font, 20)
        text = font.render('Press SPACE to continue', True, (10,10,10))
        self.screen.blit(text, (self.width / 2 - (text.get_width() / 2), self.height / 2 + 50))

    def select_level(self):
        font = pygame.font.Font(self.font, 60)
        text = font.render('SELECT LEVEL', True, (30, 30, 30))
        self.screen.blit(text, (self.width / 2 - (text.get_width() / 2), 80))

        level = 0
        for y in range(3):
            for x in range(5):
                dim = 80
                pos_x = x*(self.width/5 - 20)-dim/2 + 120
                pos_y = y*((self.height - 300)/3) + dim + 150
                title = 'LEVEL ' + str(level + 1)
                font = pygame.font.Font(self.font, 15)
                text = font.render(title, True, (30, 30, 30))
                self.screen.blit(text, ((pos_x + (dim - text.get_width())/2, pos_y - text.get_height())))
                rect_level = pygame.Rect(pos_x, pos_y, dim, dim)
                image_level = pygame.image.load('images\\level' + str(level + 1) + '.png')
                image_level = pygame.transform.smoothscale(image_level.convert_alpha(), (dim, dim))
                self.screen.blit(image_level, (pos_x, pos_y))
       
                Button.objects.append(rect_level)
                level += 1

    def game(self, movimentos, start_time, top_left_y, level):
        title = title = 'LEVEL ' + str(level + 1)
        font = pygame.font.Font(self.font, 20)
        text = font.render(f'MOVIMENTOS: {movimentos}', True, (30, 30, 30))
        textRect = text.get_rect()
        textRect.center = (100, top_left_y)
        self.screen.blit(text, textRect)
        counting_time = pygame.time.get_ticks() - start_time
        counting_seconds = str( round((counting_time)/1000) ).zfill(1)
        counting_text = font.render(f'TIMER: {counting_seconds}', True, (30, 30, 30))
        counting_rect = counting_text.get_rect()
        counting_rect.center = (650, top_left_y)
        self.screen.blit(counting_text, counting_rect)
        font = pygame.font.Font(self.font, 60)
        text = font.render(title, True, (30, 30, 30))
        self.screen.blit(text, (self.width / 2 - (text.get_width() / 2), 80))

    def victory(self):
        font = pygame.font.Font(self.font, 60)
        label = font.render('CONGRATULATIONS!!!', True, (150, 150, 0))
        self.screen.blit(label, (self.width / 2 - (label.get_width() / 2), self.height / 2 - 50))

        font = pygame.font.Font(self.font, 20)
        label = font.render('Press SPACE to continue', True, (150, 150, 0))
        self.screen.blit(label, (self.width / 2 - (label.get_width() / 2), self.height / 2 + 50))

class Button:
    objects = []
    def event_treatment(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos() 
                for button in self.__class__.objects:
                    if button.collidepoint(mouse_position):
                        return self.__class__.objects.index(button)