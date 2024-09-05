import pygame
from app.Player import Player


class Game():
    def __init__(self) -> None:
        pygame.init()
        self.my_font = pygame.font.SysFont('arial', 20)
        self.size = [800, 600]
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Frogger')
        self.clock = pygame.time.Clock()

        self.save_coluns = 1
        self.unsave_coluns = 3
        self.score = 0

        self.rows_on_screen = 10

        self.player = Player(self.size[0] // 2 - self.size[1] // 20,
                             self.size[1] // 10, self.screen, self.size, self.rows_on_screen)

    def update(self) -> None:
        self.screen.fill((240, 240, 240))

        # Background
        for i in range(self.rows_on_screen):
            if i % (self.save_coluns + self.unsave_coluns) + 1 <= self.save_coluns:
                pygame.draw.rect(self.screen, (230, 230, 230), [0, self.size[1] - self.size[1] // self.rows_on_screen -
                                 i * self.size[1] // self.rows_on_screen, self.size[0], self.size[1] // self.rows_on_screen])
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), [0, self.size[1] - self.size[1] // self.rows_on_screen -
                                 i * self.size[1] // self.rows_on_screen, self.size[0], self.size[1] // self.rows_on_screen])

        self.player.draw()

        text = self.my_font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        pygame.display.flip()
        self.clock.tick(30)


    def run(self) -> None:
        self.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.player.move()
            self.update()
        return
