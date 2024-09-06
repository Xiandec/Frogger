import pygame


class Enemy():
    """
    Class for enemys
    """

    def __init__(self,
                 x: int,
                 row: int,
                 screen: pygame.display,
                 size_type: str,
                 size: list,
                 speed: int,
                 rows_on_screen: int
                 ) -> None:
        self.size = size
        self.rows_on_screen = rows_on_screen
        self.row = row
        self.size_type = size_type
        match size_type:
            case 'small':
                self.size_car = (50, size[1] // self.rows_on_screen)
            case 'medium':
                self.size_car = (100, size[1] // self.rows_on_screen)
            case 'large':
                self.size_car = (200, size[1] // self.rows_on_screen)
        self.x = x
        self.y = size[1] - self.row * size[1] // self.rows_on_screen
        self.screen = screen
        self.speed = speed

    def draw(self) -> None:
        """
        Move and draw the enemy
        """
        self.move()
        pygame.draw.rect(self.screen, (255, 0, 0), [
                         self.x, self.y, self.size_car[0], self.size_car[1]])
        return

    def move(self) -> None:
        """
        Move the enemy to the left
        """
        self.x -= self.speed
        return

    def change_row(self, row: int) -> None:
        """
        Change the enemy row
        """
        self.row -= row
        self.y = self.size[1] - self.row * self.size[1] // self.rows_on_screen
        return

    def is_collision(self, player_x: int, player_width: int) -> bool:
        """
        Check if the enemy collide with the player
        """
        if (player_x + player_width >= self.x) and (player_x <= self.x + self.size_car[0]):
            return True
        return False

    def is_destroy(self) -> bool:
        """
        Check if the enemy is out of bounds
        """
        if self.x + self.size_car[0] < 0 or self.row <= 0:
            return True
        return False


class EnemyController():
    """
    Class for managing enemy movements and collisions
    """

    def __init__(self,
                 size: list,
                 screen,
                 rows_on_screen: int) -> None:
        self.enemies = []
        self.size = size
        self.screen = screen
        self.rows_on_screen = rows_on_screen

    def add_enemy(self,
                  row: int,
                  x_move: int = 0,
                  size: str = 'medium',
                  speed: int = 5
                  ) -> None:
        """
        Create a new enemy
        """
        self.enemies.append({'row': row, 'e': Enemy(
            self.size[1] + x_move, row, self.screen, size, self.size, speed, self.rows_on_screen)})
        return

    def generate_by_pattern(self,
                            row: int,
                            pattern: int
                            ) -> None:
        """
        Generate enemies by pattern
        """
        match pattern:
            case 1:
                self.add_enemy(row)
                self.add_enemy(row, 300)
                self.add_enemy(row, 600)
            case 2:
                self.add_enemy(row, 0, 'large', 2)
                self.add_enemy(row, 500, 'large', 2)
                self.add_enemy(row, 1000, 'large', 2)
            case 3:
                self.add_enemy(row, 0, 'small', 10)
                self.add_enemy(row, 350, 'small', 10)
                self.add_enemy(row, 700, 'small', 10)
                self.add_enemy(row, 1050, 'small', 10)
            case 0:
                pass
        return

    def update(self) -> None:
        """
        Update enemies positions and draw them
        """
        for enemy in self.enemies:
            enemy['e'].draw()
            if enemy['e'].is_destroy():
                if enemy['e'].row >= 0:  # if its reached left bound generate new
                    self.enemies.append({'row': enemy['e'].row, 'e': Enemy(
                        self.size[0], enemy['e'].row, self.screen, enemy['e'].size_type, self.size, enemy['e'].speed, self.rows_on_screen)})
                self.enemies.remove(enemy)
        return

    def move_enemies(self, row) -> None:
        """
        Move enemies to the specified row and adjust their row values accordingly
        """
        for enemy in self.enemies:
            enemy['e'].change_row(row)
            enemy['row'] -= row
        return

    def check_collisions(self, row, player_x, player_width) -> None:
        """
        Check for collisions with the player at the specified row
        """
        for enemy in self.enemies:
            if enemy['row'] == row and enemy['e'].is_collision(player_x, player_width):
                return True
        return False
