import pygame


class Player():
    """
    Class for player
    """

    def __init__(self,
                 x: int,
                 width: int,
                 screen: pygame.display,
                 size: list,
                 rows_on_screen: int
                 ) -> None:
        self.size = size
        self.rows_on_screen = rows_on_screen
        self.x = x
        self.current_row = 1
        self.width = width
        self.height = size[1] // self.rows_on_screen
        self.direction = 'right'
        self.screen = screen

        self.move_ticker = 5

    def get_current_row(self) -> int:
        """
        Returns the current row
        """
        return self.current_row

    def set_current_row(self, row: int) -> None:
        """
        Sets the current row to the given row
        """
        self.current_row = row
        self.move_ticker = 5
        return

    def draw(self, offset: int = 0) -> None:
        """
        Draw player on screen
        """
        pygame.draw.rect(self.screen, (0, 175, 100), [
                         self.x, self.size[1] - self.current_row * self.height + offset + self.height * 0.05, self.width, self.height * 0.9],
                         border_radius=5)

    def move(self) -> None:
        """
        Move player up and down
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.move_ticker == 0:
                self.current_row += 1
                self.move_ticker = 5
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.move_ticker == 0:
                self.current_row -= 1 if self.current_row > 1 else 0
                self.move_ticker = 5 if self.current_row > 1 else 0
        self.move_ticker -= 1 if self.move_ticker > 0 else 0
        return
