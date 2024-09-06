import pygame

class Player():
    def __init__(self, x, width, screen, size, rows_on_screen):
        self.size = size
        self.rows_on_screen = rows_on_screen
        self.x = x
        self.current_row = 1
        self.width = width
        self.height = size[1] // self.rows_on_screen
        self.direction = 'right'
        self.screen = screen

        self.move_ticker = 0
        
    def get_current_row(self):
        return self.current_row
    
    def set_current_row(self, row):
        self.current_row = row

    def draw(self):
        pygame.draw.rect(self.screen, (0, 240, 0), [self.x, self.size[1] - self.current_row * self.height, self.width, self.height])

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.move_ticker == 0:
                self.current_row += 1
                self.move_ticker = 5
        if keys[pygame.K_s]:
            if self.move_ticker == 0:
                self.current_row -= 1 if self.current_row > 1 else 0
                self.move_ticker = 5 if self.current_row > 1 else 0
        self.move_ticker -= 1 if self.move_ticker > 0 else 0