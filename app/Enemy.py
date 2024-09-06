import pygame

class Enemy():
    def __init__(self, x, row, screen, size_type, size, speed, rows_on_screen):
        self.size = size
        self.rows_on_screen = rows_on_screen
        self.row = row
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
        self.move()
        pygame.draw.rect(self.screen, (255, 0, 0), [self.x, self.y, self.size_car[0], self.size_car[1]])
        return

    def move(self) -> None:
        self.x -= self.speed
        return

    def change_row(self, row) -> None:
        self.row -= row
        self.y = self.size[1] - self.row * self.size[1] // self.rows_on_screen
        return 

    def is_collision(self, player_x, player_width) -> bool:
        if (player_x + player_width >= self.x) and (player_x <= self.x + self.size_car[0]):
            return True
        return False
    
    def is_destroy(self) -> bool:
        if self.x + self.size_car[0] < 0 or self.row <= 0:
            return True
        return False
    
class EnemyController():
    def __init__(self, size, screen, rows_on_screen):
        self.enemies = []
        self.size = size
        self.screen = screen
        self.rows_on_screen = rows_on_screen

    def add_enemy(self, row):
        self.enemies.append({'row': row, 'e': Enemy(self.size[1], row, self.screen, 'medium', self.size, 5, self.rows_on_screen)})

    def update(self):
        for enemy in self.enemies:
            enemy['e'].draw()
            if enemy['e'].is_destroy():
                self.enemies.remove(enemy)

    def move_enemies(self, row):
        for enemy in self.enemies:
            enemy['e'].change_row(row)
            enemy['row'] -= row

    def check_collisions(self, row, player_x, player_width):
        for enemy in self.enemies:
            if enemy['row'] == row and enemy['e'].is_collision(player_x, player_width):
                return True
        return False