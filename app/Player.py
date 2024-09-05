import pygame

class Player():
    def __init__(self, x, width, screen, size, rows_on_screen):
        self.size = size
        self.rows_on_screen = rows_on_screen
        self.x = x
        self.y = size[1] - size[1] // self.rows_on_screen 
        self.width = width
        self.height = size[1] // self.rows_on_screen
        self.direction = 'right'
        self.screen = screen

        self.move_ticker = 0
        

    def draw(self):
        pygame.draw.rect(self.screen, (0, 240, 0), [self.x, self.y, self.width, self.height])

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.move_ticker == 0:
                self.y -= self.height if self.height - self.y <= 0 else 0
                self.move_ticker = 5 if self.height - self.y <= 0 else 0
            else:
                self.move_ticker -= 1
        if keys[pygame.K_s]:
            if self.move_ticker == 0:
                self.y += self.height if self.y + self.height < self.size[1] else 0
                self.move_ticker = 5 if self.y + self.height < self.size[1] else 0
            else:
                self.move_ticker -= 1