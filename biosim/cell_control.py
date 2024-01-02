# -*- coding: utf-8 -*-

"""
__author__ = 'Inger Annett Grünbeck','Yngvild Sauge'
__email__ = 'inger.annett.grunbeck@nmbu.no', 'yngvild.sauge@nmbu.no'
"""

from biosim.mapping import Island
from biosim.animals import Animal, Herbivore, Carnivore
from biosim.landscape import Landscape, Jungle, Desert, Savannah, Mountain, Ocean

"""
Controls instances in a map, and generates animals in the map
"""


class Cells:
    """
    The class generates animals onto a map and controls the annual cycle of events
    """

    def __init__(self, population_cell=None, island_map=None):
        """

        :param population_cell: list of dicts containing animals in locations
        :param island_map: a string containing the letters O, M, D, J and S, representing the
        landscape types. If None, the default in the Island class is used
        """
        self.population_cell = population_cell if population_cell \
                                                  is not None else [{'loc': (2, 18),
                                                                     'pop': [{'species':
                                                                                  'Herbivore',
                                                                              'age': 8,
                                                                              'weight': 16} for
                                                                             _ in range(100)]},
                                                                    {'loc': (5, 17),
                                                                     'pop': [
                                                                         {'species': 'Carnivore',
                                                                          'age': 10,
                                                                          'weight': 14.2} for
                                                                         _ in range(50)]}]

        isle = Island(island_map)
        self.map = isle.create_map()
        self.food_source = 0

    def generate_animals(self):
        """
        Method that generates an animal and places it in a cell
        """
        for lo in self.population_cell:
            x, y = lo['loc']
            x -= 1
            y -= 1
            if not self.map[x][y].habitable:
                raise ValueError('The location of animal is not habitable')

            for ind in lo['pop']:
                if ind['species'] == 'Herbivore':
                    herb = Herbivore(ind['species'], ind['age'], ind['weight'])
                    self.map[x][y].pop_herb.append(herb)
                elif ind['species'] == 'Carnivore':
                    carn = Carnivore(ind['species'], ind['age'], ind['weight'])
                    self.map[x][y].pop_carn.append(carn)

    def move(self, x, y):
        """
        Method that may move an animal to a neighbouring cell

        :param x: row coordinate of the animals current position
        :param y: column coordinate of animals current position
        """
        not_move_herb = []
        not_move_carn = []

        for animal in self.map[x][y].pop_herb + self.map[x][y].pop_carn:
            if animal.not_walked:
                direction = animal.move_dir()
                if not direction:
                    if animal.specie == 'Herbivore':
                        not_move_herb.append(animal)
                    else:
                        not_move_carn.append(animal)

                elif direction == 'North':
                    if self.map[x - 1][y].habitable:
                        animal.not_walked = False
                        if animal.specie == 'Herbivore':
                            self.map[x - 1][y].pop_herb.append(animal)
                        else:
                            self.map[x - 1][y].pop_carn.append(animal)
                    else:
                        if animal.specie == 'Herbivore':
                            not_move_herb.append(animal)
                        else:
                            not_move_carn.append(animal)

                elif direction == 'East':
                    if self.map[x][y + 1].habitable:
                        animal.not_walked = False
                        if animal.specie == 'Herbivore':
                            self.map[x][y + 1].pop_herb.append(animal)
                        else:
                            self.map[x][y + 1].pop_carn.append(animal)
                    else:
                        if animal.specie == 'Herbivore':
                            not_move_herb.append(animal)
                        else:
                            not_move_carn.append(animal)

                elif direction == 'South':
                    if self.map[x + 1][y].habitable:
                        animal.not_walked = False
                        if animal.specie == 'Herbivore':
                            self.map[x + 1][y].pop_herb.append(animal)
                        else:
                            self.map[x + 1][y].pop_carn.append(animal)
                    else:
                        if animal.specie == 'Herbivore':
                            not_move_herb.append(animal)
                        else:
                            not_move_carn.append(animal)

                elif direction == 'West':
                    if self.map[x][y - 1].habitable:
                        animal.not_walked = False
                        if animal.specie == 'herbivore':
                            self.map[x][y - 1].pop_herb.append(animal)
                        else:
                            self.map[x][y - 1].pop_carn.append(animal)
                    else:
                        if animal.specie == 'Herbivore':
                            not_move_herb.append(animal)
                        else:
                            not_move_carn.append(animal)

            else:
                if animal.specie == 'Herbivore':
                    not_move_herb.append(animal)
                else:
                    not_move_carn.append(animal)

        self.map[x][y].pop_herb = not_move_herb
        self.map[x][y].pop_carn = not_move_carn

    def cell_cycle(self):
        """
        Method that completes a full cycle of events through a year for all animals in all cells
        """
        for x, row in enumerate(self.map):
            for y, cell in enumerate(row):
                cell.feeding_herb()
                cell.feeding_carn()
                cell.birth()
                self.move(x, y)

        for row in self.map:
            for cell in row:
                cell.set_not_walked_true()
                cell.age()
                cell.weight_loss()
                cell.survive()
