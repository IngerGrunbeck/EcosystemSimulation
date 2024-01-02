# -*- coding: utf-8 -*-

"""
__author__ = 'Inger Annett Grünbeck','Yngvild Sauge'
__email__ = 'inger.annett.grunbeck@nmbu.no', 'yngvild.sauge@nmbu.no'
"""

import pytest
from biosim.animals import Animal, Carnivore, Herbivore


class TestAnimal:
    """
    Class for testing the Animal Class
    """

    def test_aging(self):
        """
        The animal ages
        """
        start_age = 5
        herb = Herbivore('Herbivore', start_age, 10)
        herb.aging()
        assert herb.a > start_age

    def test_weight_gain(self):
        """
        The animal gains weight after eating
        """
        start_weight = 20
        carn = Carnivore('Carnivore', 5, start_weight)
        carn.eat_gain_weight(800)
        assert carn.w > start_weight

    def test_loose(self):
        """
        The animal looses weight
        """
        start_weight = 20
        herb = Herbivore('Herbivore', 5, start_weight)
        herb.loose_weight()
        assert herb.w < start_weight

    def test_dies(self, mocker):
        """
        The animal dies
        :param mocker: mocks a random number
        """
        mocker.patch('random.random', return_value=0)
        carn = Carnivore('Carnivore', 5, 10)
        assert not carn.survival()

    def test_alive(self, mocker):
        """
        The animal survives
        :param mocker: mocks a random number
        """
        mocker.patch('random.random', return_value=0.999999)
        herb = Herbivore('Herbivore', 6, 2)
        assert herb.survival()

    def test_food_loss(self):
        """
        The amount of food in cell decreases after the animal eats
        """
        carn = Carnivore('Carnivore', 5, 10)
        food = 20
        new_food = carn.carn_eating(food, 10)
        assert new_food < food

    def test_fitness(self):
        """
        The fitness parameter is between 0 and 1
        """
        herb = Herbivore('Herbivore', 5, 10)
        assert 0 <= herb.fitness() <= 1

    def test_direction_not_move(self, mocker):
        """
        The animal does not move
        :param mocker: mocks a random number
        """
        herb = Herbivore('Herbivore', 5, 10)
        mocker.patch('random.random', return_value=1)
        assert herb.move_dir() is None

    def test_direction_north(self, mocker):
        """
        The animal moves north
        :param mocker: mocks a random number
        """
        herb = Herbivore('Herbivore', 5, 10)
        mocker.patch('random.random', return_value=0.0001)
        mocker.patch('random.randint', return_value=3)
        assert herb.move_dir() == 'North'

    def test_direction_east(self, mocker):
        """
        The animal moves east
        :param mocker: mocks a random number
        """
        herb = Herbivore('Herbivore', 5, 10)
        mocker.patch('random.random', return_value=0.0001)
        mocker.patch('random.randint', return_value=7)
        assert herb.move_dir() == 'East'

    def test_direction_south(self, mocker):
        """
        The animal moves south
        :param mocker: mocks a random number
        """
        herb = Herbivore('Herbivore', 5, 10)
        mocker.patch('random.random', return_value=0.0001)
        mocker.patch('random.randint', return_value=12)
        assert herb.move_dir() == 'South'

    def test_direction_west(self, mocker):
        """
        The animal moves west
        :param mocker: mocks a random number
        """
        herb = Herbivore('Herbivore', 5, 10)
        mocker.patch('random.random', return_value=0.0001)
        mocker.patch('random.randint', return_value=17)
        assert herb.move_dir() == 'West'

    def test_birth_weight(self, mocker):
        """
        The animal gives birth to a baby and the mother looses the correct weight
        :param mocker: mocks a random number
        :return:
        """
        carn = Carnivore('Carnivore', 5, 10000)
        mocker.patch('random.random', return_value=0)
        baby = carn.give_birth('Carnivore', 2)
        assert carn.w == 10000-carn.xi*baby.w

    def test_birth_weight_zero(self, mocker):
        """
        The mothers weight can't be negative after giving birth
        :param mocker: mocks a random number
        """
        herb = Herbivore('Herbivore', 5, 34)
        mocker.patch('random.random', return_value=0)
        mocker.patch('random.gauss', return_value=50)
        herb.give_birth('Herbivore', 2)
        assert herb.w == 34


class TestHerbivore:
    """
    Class for testing the Herbivore class
    """

    def test_herb_eating(self):
        """
        The herbivore can eat
        """
        herb = Herbivore('Herbivore', 5, 10)
        food = 100
        assert herb.herb_eating(food) == 100-herb.F

    def test_herb_eating_weight_increases(self):
        """
        The herbivore gains weight after eating
        """
        herb = Herbivore('Herbivore', 5, 10)
        food = 5
        herb.herb_eating(food)
        assert herb.w == 10 + herb.beta*food


class TestCarnivore:
    """
    Class for testing the Carnivore class
    """
    def test_kill(self, mocker):
        """
        The carnivore can kill a herbivore
        :param mocker: mocks a random number
        """
        mocker.patch('random.random', return_value=0.0001)
        carn = Carnivore('Carnivore', 5, 10)
        carn.fitness()
        assert carn.kill(0.000001)

    def test_carn_eating(self):
        """
        The carnivore can eat
        """
        carn = Carnivore('Carnivore', 5, 10)
        assert carn.carn_eating(100, 10) == 0
        assert carn.carn_eating(5, 10) == 5
