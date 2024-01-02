# -*- coding: utf-8 -*-

"""
__author__ = 'Inger Annett Grünbeck','Yngvild Sauge'
__email__ = 'inger.annett.grunbeck@nmbu.no', 'yngvild.sauge@nmbu.no'
"""

import pytest
from biosim.landscape import Landscape, Jungle, Savannah, Desert, Mountain, Ocean
from biosim.cell_control import Cells


class TestLandscape:
    """
    Class for testing the Landscape class
    """
    def test_feeding_walked(self):
        """
        Only animals that haven't moved this cycle are feeding, to prevent double feeding
        """
        celle = Cells()
        celle.generate_animals()

        for row in celle.map:
            for cell in row:
                food_start = cell.food
                for animal in cell.pop_herb+cell.pop_carn:
                    animal.not_walked = False
                cell.feeding_herb()
                cell.feeding_carn()
                assert food_start == cell.food

    def test_appending_newborns(self, mocker):
        """
        The cell_pop list increases if there are any babies born or there are elements in the
        newborn-list
        """
        celle = Cells()
        celle.generate_animals()
        mocker.patch('random.random', return_value=0)

        for row in celle.map:
            for cell in row:
                if not isinstance(cell, Ocean) and not isinstance(cell, Mountain):
                    if cell.pop_herb or cell.pop_carn:
                        for animal in cell.pop_herb+cell.pop_carn:
                            animal.w = 50
                        pre_baby = len(cell.pop_herb+cell.pop_carn)
                        cell.birth()
                        assert len(cell.pop_herb+cell.pop_carn) > pre_baby

    def test_death_list(self, mocker):
        """
        If someone died, the cell_pop list is updated correctly
        """
        celle = Cells()
        celle.generate_animals()
        mocker.patch('random.random', return_value=0)

        for row in celle.map:
            for cell in row:
                if not isinstance(cell, Ocean) and not isinstance(cell, Mountain):
                    if cell.pop_herb or cell.pop_carn:
                        pre_death = len(cell.pop_herb+cell.pop_carn)
                        cell.survive()
                        assert len(cell.pop_herb+cell.pop_carn) < pre_death

    def test_walked_true(self):
        """
        The function set_not_walked_true sets all not_walked-attributes to be true
        """
        celle = Cells()
        celle.generate_animals()

        for row in celle.map:
            for cell in row:
                for animal in cell.pop_herb+cell.pop_carn:
                    animal.not_walked = False
                cell.set_not_walked_true()
                for animal in cell.pop_herb+cell.pop_carn:
                    assert animal.not_walked

    def test_feeding_carn(self):
        pass


class TestJungle:
    """
    Class for testing the Jungle class
    """
    def test_feeding_jungle(self):
        """
        The food is set back to f_max every year in the jungle
        """

        celle = Cells()
        celle.generate_animals()

        for row in celle.map:
            for cell in row:
                if isinstance(cell, Jungle):
                    food_start = cell.food
                    if len(cell.pop_herb) > 0:
                        n_animals = len(cell.pop_herb)
                        cell.feeding_herb()
                        if n_animals*cell.pop_herb[0].F > food_start:
                            assert cell.food == 0
                        else:
                            assert cell.food == (food_start - n_animals*cell.pop_herb[0].F)
                    else:
                        assert cell.food == food_start


class TestSavannah:
    """
    Class for testing the Savannah class
    """

    def test_feeding_savannah(self):
        """
        The food in the cell decreases when animals are eating
        """
        celle = Cells()
        celle.generate_animals()

        for row in celle.map:
            for cell in row:
                if isinstance(cell, Savannah):
                    food_start = cell.food
                    if len(cell.pop_herb) > 0:
                        n_animals = len(cell.pop_herb)
                        cell.feeding_herb()
                        if n_animals*cell.pop_herb[0].F > food_start:
                            assert cell.food == 0
                        else:
                            assert cell.food == (food_start - n_animals*cell.pop_herb[0].F)
                    else:
                        assert cell.food == food_start

    def test_regrow(self):
        """
        The savannah regrows
        """
        map_test = """\
                                            OOOO
                                            OSSO
                                            OOOO"""

        celle = Cells([{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 8, 'weight': 14.2}
                                               for _ in range(10)]}], map_test)

        celle.generate_animals()

        for row in celle.map:
            for cell in row:
                if isinstance(cell, Savannah):
                    init_food = cell.food
                    cell.feeding_herb()
                    cell.regrow()
                    assert init_food >= cell.food


class TestMountainOcean:
    """
    Class for testing the Mountain and Ocean classes
    """
    def test_not_habitable(self):
        """
        It is not possible to generate animals in either mountain or ocean instances
        """
        celle = Cells()
        celle.generate_animals()

        for row in celle.map:
            for cell in row:
                if isinstance(cell, Mountain):
                    n_animals = len(cell.pop_herb+cell.pop_carn)
                    assert n_animals == 0
                elif isinstance(cell, Ocean):
                    n_animals = len(cell.pop_herb+cell.pop_carn)
                    assert n_animals == 0
