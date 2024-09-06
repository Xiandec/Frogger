import pygame
from app.Player import Player
from app.Map import Map
from app.Enemy import EnemyController


class Game():
    """
    Game controller class 
    """

    def __init__(self) -> None:
        pygame.init()
        
        self.size = [800, 600]

        self.my_font = pygame.font.SysFont('arial', int(self.size[1] * 0.04))
        self.game_over_font = pygame.font.SysFont('arial', int(self.size[1] * 0.2))
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Frogger')
        self.clock = pygame.time.Clock()

        self.save_coluns = 1
        self.unsave_coluns = 3
        self.rows_on_screen = 10

        self.road_color = (170, 155, 155)
        self.save_color = (214, 204, 203)

    def start(self) -> None:
        """
        Start new game
        """
        self.score = 0
        self.player = Player(self.size[0] // 2 - self.size[1] // 20,
                             self.size[1] // 10, self.screen, self.size, self.rows_on_screen)

        self.map = Map(self.size, self.rows_on_screen,
                       self.save_coluns, self.unsave_coluns)
        self.enemy_controller = EnemyController(
            self.size, self.screen, self.rows_on_screen)
        self.generator()
        return

    def generator(self) -> None:
        """
        Generate new enemys
        """
        for row in self.map.rows_to_generate:
            self.enemy_controller.generate_by_pattern(
                row['row'] - self.score + 1, row['pattern'])
            self.map.rows_to_generate.remove(row)
        return

    def update(self) -> None:
        """
        Draw game on screen
        """
        self.screen.fill(self.save_color)

        # Background
        for i in self.map.get_map(self.score):
            if i['type'] == 'save':
                pygame.draw.rect(self.screen, self.save_color, [0, self.size[1] - self.size[1] // self.rows_on_screen -
                                 (i['row'] - self.score) * self.size[1] // self.rows_on_screen, self.size[0], self.size[1] // self.rows_on_screen])
            else:
                pygame.draw.rect(self.screen, self.road_color, [0, self.size[1] - self.size[1] // self.rows_on_screen -
                                 (i['row'] - self.score) * self.size[1] // self.rows_on_screen, self.size[0], self.size[1] // self.rows_on_screen])

        # player
        self.player.draw()

        # enemies
        self.enemy_controller.update()

        # Score
        text = self.my_font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(text, (self.size[0] * 0.01, self.size[1] * 0.01))

        # Update screen
        pygame.display.flip()
        self.clock.tick(30)
        return

    def check_score(self) -> None:
        """
        Check if reached new line and move everything down
        """
        pos = self.map.get_save_row(
            self.player.get_current_row() - 1 + self.score)
        if pos != None:
            self.animation_down(pos - self.score)
            self.enemy_controller.move_enemies(
                self.player.get_current_row() - 1)
            self.player.set_current_row(1)
            self.score = pos
            self.map.remove_save_row(self.score)
        return
    
    def animation_down(self, down_rows: int) -> None:
        """
        Move down whole screen
        """
        for offset in range(0, self.size[1] // self.rows_on_screen * down_rows, self.size[1] // self.rows_on_screen * down_rows // 10):
            self.screen.fill(self.save_color)

            # Background
            for i in self.map.get_map(self.score + self.save_coluns + self.unsave_coluns):
                if i['type'] == 'save':
                    pygame.draw.rect(self.screen, self.save_color, [0, self.size[1] - self.size[1] // self.rows_on_screen -
                                    (i['row'] - self.score) * self.size[1] // self.rows_on_screen + offset, self.size[0], self.size[1] // self.rows_on_screen])
                else:
                    pygame.draw.rect(self.screen, self.road_color, [0, self.size[1] - self.size[1] // self.rows_on_screen -
                                    (i['row'] - self.score) * self.size[1] // self.rows_on_screen + offset, self.size[0], self.size[1] // self.rows_on_screen])

            # player
            self.player.draw(offset)

            # enemies
            self.enemy_controller.draw_down(offset)

            # Score
            text = self.my_font.render(f'Score: {self.score}', True, (0, 0, 0))
            self.screen.blit(text, (self.size[0] * 0.01, self.size[1] * 0.01))

            # Update screen
            pygame.display.flip()
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        return
    
    def animation_game_over(self, down_rows: int) -> None:
        """
        Move down whole screen
        """
        for offset in range(0, self.size[1] // self.rows_on_screen * (down_rows + 1), self.size[1] // self.rows_on_screen * down_rows // 25):
            self.screen.fill(self.save_color)

            text = self.game_over_font.render(f'Game Over', True, (0, 0, 0))
            self.screen.blit(text, (self.size[0] * 0.01, self.size[1] * 0.01))

            # Score
            text = self.my_font.render(f'Score: {self.score}', True, (0, 0, 0))
            self.screen.blit(text, (self.size[0] * 0.01, self.size[1] * 0.01 + self.size[1] * 0.2))

            # Background
            for i in self.map.get_map(self.score):
                if i['type'] == 'save':
                    pygame.draw.rect(self.screen, self.save_color, [0, self.size[1] - self.size[1] // self.rows_on_screen -
                                    (i['row'] - self.score) * self.size[1] // self.rows_on_screen + offset, self.size[0], self.size[1] // self.rows_on_screen])
                else:
                    pygame.draw.rect(self.screen, self.road_color, [0, self.size[1] - self.size[1] // self.rows_on_screen -
                                    (i['row'] - self.score) * self.size[1] // self.rows_on_screen + offset, self.size[0], self.size[1] // self.rows_on_screen])

            # player
            self.player.draw(offset)

            # enemies
            self.enemy_controller.draw_down(offset)

            # Update screen
            pygame.display.flip()
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        return

    def check_loose(self) -> None:
        """ 
        Check if the player loose and restart if it is
        """
        if self.enemy_controller.check_collisions(self.player.get_current_row(), self.player.x, self.player.width):
            self.animation_game_over(len(self.map.rows))
            self.waiter()
            self.start()
        return
    
    def waiter(self) -> None:
        """
        Wait for player to press any key
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    running = False
        return

    def run(self) -> None:
        """
        Run game loop
        """
        self.start()
        self.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            self.player.move()
            self.generator()
            self.check_score()
            self.check_loose()
            self.update()
        return
