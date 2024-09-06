import pygame
from random import randint

class Map():
    def __init__(self, size, rows_on_screen, save_colums, unsave_colums):
        self.size = size
        self.rows_on_screen = rows_on_screen
        self.save_colums = save_colums
        self.unsave_colums = unsave_colums

        self.rows = [{'type': 'save', 'row': 0, 'reached': 0}]
        while rows_on_screen >= len(self.rows):
            self.create_row()

    def create_row(self):
        if self.rows[-1]['type'] == 'save':
            self.rows.extend([{'type': 'unsave', 'row': len(self.rows) + i, 'pattern': '1'} for i in range(randint(1, self.unsave_colums))])
        else:
            self.rows.extend([{'type': 'save', 'row': len(self.rows) + i, 'reached': len(self.rows) + i}  for i in range(randint(1, self.save_colums))])

    def get_map(self, current_row: int) -> list:
        while self.rows_on_screen + current_row >= len(self.rows):
            self.create_row()
        return self.rows
    
    def get_save_row(self, current_row: int) -> int:
        return self.rows[current_row]['reached'] if self.rows[current_row]['type'] == 'save' and self.rows[current_row]['reached'] != 0 else None
    
    def remove_save_row(self, current_row: int) -> None:
        self.rows[current_row]['reached'] = 0
        return