import pygame
from random import choice

class Enemy():
    """
    Class for enemys
    """

    def __init__(self,
                 x_move: int,
                 row: int,
                 screen: pygame.display,
                 size_type: str,
                 size: list,
                 speed: int,
                 rows_on_screen: int,
                 direction: int = 1
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
        self.x = self.size[0] + x_move if direction == 1 else x_move - self.size_car[0]
        self.y = size[1] - self.row * size[1] // self.rows_on_screen
        self.screen = screen
        self.speed = speed
        self.direction = direction

    def regenerate(self) -> None:
        """
        Regenerate the enemy in a start position
        """
        self.x = self.size[0] if self.direction == 1 else 0 - self.size_car[0]
        return

    def draw(self, offset: int = 0) -> None:
        """
        Draw the enemy
        """
        pygame.draw.rect(self.screen, (255, 70, 0), [
                         self.x, self.y + offset + self.size_car[1] * 0.05, self.size_car[0], self.size_car[1] * 0.9],
                         border_radius=5)
        return

    def move(self) -> None:
        """
        Move the enemy to the left
        """
        self.x -= self.speed * self.direction
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

    def is_destroy_to_regenerate(self) -> None:
        """
        Check if the enemy is out of bounds and regenerate if necessary
        """
        match self.direction:
            case 1:
                if self.x + self.size_car[0] < 0:
                    self.regenerate()
                    return 
            case -1:
                if self.x > self.size[0] :
                    self.regenerate()
                    return
        return 


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
                  speed: int = 5,
                  direction: int = 1
                  ) -> None:
        """
        Create a new enemy
        """
        self.enemies.append({'row': row, 'e': Enemy(
            x_move, row, self.screen, size, self.size, speed, self.rows_on_screen, direction)})
        return

    def generate_by_pattern(self,
                            row: int,
                            pattern: int
                            ) -> None:
        """
        Generate enemies by pattern
        """
        direction = choice([-1, 1])
        match pattern:
            case 1:
                self.add_enemy(row, direction=direction)
                self.add_enemy(row, 300, direction=direction)
                self.add_enemy(row, 600, direction=direction)
            case 2:
                self.add_enemy(row, 0, 'large', 2, direction=direction)
                self.add_enemy(row, 500, 'large', 2, direction=direction)
                self.add_enemy(row, 1000, 'large', 2, direction=direction)
            case 3:
                self.add_enemy(row, 0, 'small', 10, direction=direction)
                self.add_enemy(row, 350, 'small', 10, direction=direction)
                self.add_enemy(row, 700, 'small', 10, direction=direction)
                self.add_enemy(row, 1050, 'small', 10, direction=direction)
            case 0:
                pass
        return

    def update(self) -> None:
        """
        Update enemies positions and draw them
        """
        for enemy in self.enemies:
            enemy['e'].draw()
            enemy['e'].move()
            enemy['e'].is_destroy_to_regenerate()
        return
    
    def draw_down(self, offset:int = 0) -> None:
        """
        Draw enemies with offset
        """
        for enemy in self.enemies:
            enemy['e'].draw(offset)
        return

    def move_enemies(self, row) -> None:
        """
        Move enemies to the specified row and adjust their row values accordingly
        """
        for enemy in self.enemies.copy():
            if enemy['row'] - row > 0:
                enemy['e'].change_row(row)
                enemy['row'] -= row
            else:
                self.enemies.remove(enemy)
        return

    def check_collisions(self, row, player_x, player_width) -> None:
        """
        Check for collisions with the player at the specified row
        """
        for enemy in self.enemies:
            if enemy['row'] == row and enemy['e'].is_collision(player_x, player_width):
                return True
        return False
