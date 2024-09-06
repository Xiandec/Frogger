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

        self.move_ticker = 0

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
        return

    def draw(self) -> None:
        """
        Draw player on screen
        """
        pygame.draw.rect(self.screen, (0, 240, 0), [
                         self.x, self.size[1] - self.current_row * self.height, self.width, self.height])

    def move(self) -> None:
        """
        Move player up and down
        """
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
        return
