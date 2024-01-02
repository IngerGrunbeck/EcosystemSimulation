# -*- coding: utf-8 -*-

"""
__author__ = 'Inger Annett Grünbeck','Yngvild Sauge'
__email__ = 'inger.annett.grunbeck@nmbu.no', 'yngvild.sauge@nmbu.no'
"""

import pytest
from biosim.cell_control import Cells


class TestGenAnimal:
    """
    Class for testing the generating of animals
    """
    def test_generate_error(self):
        """
        A ValueError is raised if animals are being generated in ocean
        """
        celle = Cells([{'loc': (1, 1), 'pop': [{'species': 'Herbivore', 'age': 8,
                                        'weight': 14.2} for _ in range(10)]}])

        with pytest.raises(ValueError):
            celle.generate_animals()

    def test_generate_animal(self):
        """
        Animals can be generated
        """
        map_test = """\
                    OOOO
                    OJJO
                    OOOO"""

        celle = Cells([{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 8, 'weight': 14.2}
                                              for _ in range(10)]}, {'loc': (2, 3), 'pop': [{
                                                    'species': 'Carnivore', 'age': 8,
                                                    'weight': 14.2} for _ in range(10)]}], map_test)
        celle.generate_animals()

        assert len(celle.map[1][1].pop_herb) > 0
        assert len(celle.map[1][2].pop_carn) > 0


class TestMove:
    """
    Class for testing the move method
    """
    def test_not_moved(self, mocker):
        """
        The animal doesn't have to move
        :param mocker: mocks a random number
        """
        celle = Cells()
        celle.generate_animals()

        mocker.patch('random.random', return_value=1)

        for x, row in enumerate(celle.map):
            for y, cell in enumerate(row):
                n_animal = len(cell.pop_herb)+len(cell.pop_carn)
                celle.move(x, y)
                assert n_animal == len(cell.pop_herb)+len(cell.pop_carn)


