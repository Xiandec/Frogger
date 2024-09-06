import pygame
from random import randint


class Map():
    """
    Class for game map
    """

    def __init__(self,
                 size: list,
                 rows_on_screen: int,
                 save_colums: int,
                 unsave_colums: int
                 ) -> None:
        self.size = size
        self.rows_on_screen = rows_on_screen
        self.save_colums = save_colums
        self.unsave_colums = unsave_colums

        self.rows_to_generate = []

        self.rows = [{'type': 'save', 'row': 0, 'reached': 0}]
        while rows_on_screen >= len(self.rows):
            self.create_row()

    def create_row(self) -> None:
        """
        Generates a new row for world
        """
        if self.rows[-1]['type'] == 'save':
            rows = [{'type': 'unsave', 'row': len(
                self.rows) + i, 'pattern': randint(1, 3)} for i in range(randint(1, self.unsave_colums))]
            self.rows.extend(rows)
            self.rows_to_generate.extend(rows)
        else:
            self.rows.extend([{'type': 'save', 'row': len(
                self.rows) + i, 'reached': len(self.rows) + i} for i in range(randint(1, self.save_colums))])
        return

    def get_map(self, current_row: int) -> list:
        """
        Get map and generate new if nessesary
        """
        while self.rows_on_screen + current_row >= len(self.rows):
            self.create_row()
        return self.rows

    def get_save_row(self, current_row: int) -> int:
        """
        Return row if its unreached save row
        """
        return self.rows[current_row]['reached'] if self.rows[current_row]['type'] == 'save' and self.rows[current_row]['reached'] != 0 else None

    def remove_save_row(self, current_row: int) -> None:
        """
        Remove unreached save row 
        """
        self.rows[current_row]['reached'] = 0
        return
