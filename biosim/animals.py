# -*- coding: utf-8 -*-

"""
__author__ = 'Inger Annett Grünbeck','Yngvild Sauge'
__email__ = 'inger.annett.grunbeck@nmbu.no', 'yngvild.sauge@nmbu.no'
"""

import math
import random as rand

"""
Implements Herbivores and Carnivores
"""


class Animal:
    """
    The class contains different methods that change animal attributes and parameters
    """
    param_animal_limits = {'phi_age': (0, 1), 'a_half': (0, math.inf), 'phi_weight': (0, math.inf),
                           'w_half': (0, math.inf), 'w_birth': (0, math.inf),
                           'sigma_birth': (0, math.inf), 'omega': (0, 1), 'beta': (0, 1),
                           'gamma': (0, 1), 'eta': (0, 1),
                           'mu': (0, 1), 'zeta': (0, math.inf), 'xi': (0, math.inf),
                           'F': (0, math.inf), 'DeltaPhiMax': (0, math.inf)}

    @classmethod
    def set_parameters(cls, new_params):
        """
        The method redefines animal parameters, as long as the chosen parameters already exist.

        Source: INF200, example projects: "biolab_project: bacteria"
        Author: Hans E Plesser

        :param new_params: a dict, containing the new parameter values
        """
        for key in new_params:
            if key not in ('phi_age', 'a_half', 'phi_weight', 'w_half', 'w_birth', 'sigma_birth',
                           'omega', 'beta', 'gamma', 'eta', 'mu', 'zeta', 'xi', 'F', 'DeltaPhiMax'):
                raise KeyError('Invalid parameter name' + key)

        for key, value in new_params.items():
            if cls.param_animal_limits[key][0] < value < cls.param_animal_limits[key][1]:
                setattr(cls, key, value)
            else:
                raise ValueError('chosen value for parameter is invalid')

    def __init__(self, specie, age, weight):
        """
        :param specie: a str, either Herbivore or Carnivore
        :param age: int, the age of an animal
        :param weight: int, the weight of an animal
        """
        self.a = age
        self.w = weight
        self.specie = specie
        self.phi = None
        self.death_rate = None
        self.not_walked = True

    # noinspection PyUnresolvedReferences
    def fitness(self):
        """
        Method that computes the fitness for an animal

        :return: The fitness, phi (int). If the animals weight is zero, return 0
        """
        if self.w <= 0:
            return 0
        else:
            self.phi = 1 / (1 + math.exp(self.phi_age * (
                    self.a - self.a_half))) * 1 / (
                               1 + math.exp(-self.phi_weight * (self.w - self.w_half)))
            return self.phi

    def move_dir(self):
        """
        Method that decides whether the animal moves or not, and if it moves the direction is
        returned

        :return: The direction the animal is moving, or None
        """
        # noinspection PyUnresolvedReferences
        move_prob = self.mu * self.fitness()

        if rand.random() <= move_prob:
            rand_numb = rand.randint(1, 20)
            if 1 <= rand_numb < 6:
                return 'North'
            elif 6 <= rand_numb < 11:
                return 'East'
            elif 11 <= rand_numb < 16:
                return 'South'
            elif 16 <= rand_numb < 21:
                return 'West'

    def eat_gain_weight(self, available_food):
        """
        Method that increases the animals weight after eating

        :param available_food: The food that is available for the animal to eat
        """
        # noinspection PyUnresolvedReferences
        self.w += self.beta * available_food

    def aging(self):
        """
        Method that ages an animal by a year
        """
        self.a += 1

    def give_birth(self, animal_type, n):
        """
        Method that allows animals to give birth

        :param n: number of animals of the same species
        :param animal_type: str. the type of animal, either herbivore or carnivore

        :return: a new animal instance, or None
        """
        if self.w >= self.zeta * (self.w_birth + self.sigma_birth):
            birth_prob = min(1, self.gamma * self.fitness() * (n - 1))
            if rand.random() <= birth_prob:
                w_baby = rand.gauss(self.w_birth, self.sigma_birth)
                if w_baby > 0:
                    potential_weight_mother = self.w - self.xi * w_baby
                    if potential_weight_mother > 0:
                        self.w -= self.xi * w_baby
                        if animal_type == 'Herbivore':
                            return Herbivore('Herbivore', 0, w_baby)
                        else:
                            return Carnivore('Carnivore', 0, w_baby)

    def loose_weight(self):
        """
        Method that computes the animals new weight after loosing weight
        """
        self.w -= self.eta * self.w

    def survival(self):
        """
        Method that computes an animals probability to survive at the end of a year, based on the
        animals fitness.

        :return: True if the animal survives
        """
        self.death_rate = self.omega * (1 - self.fitness())
        if self.death_rate < rand.random() and self.w > 0:
            return True


class Herbivore(Animal):
    """
    A class containing parameters and methods used to implement Herbivores
    """

    phi_age = 0.2
    a_half = 40.0
    phi_weight = 0.1
    w_half = 10.0
    w_birth = 8.0
    sigma_birth = 1.5
    omega = 0.4
    beta = 0.9
    gamma = 0.2
    eta = 0.05
    mu = 0.25
    zeta = 3.5
    xi = 1.2
    F = 10.0

    def __init__(self, specie, age, weight):
        super().__init__(specie, age, weight)

    def herb_eating(self, food):
        """
        Method that computes how much the animal can eat, depending on the food available

        :param food: The amount of food available to the animal
        """
        if food >= self.F:
            self.eat_gain_weight(self.F)
            food -= self.F
            return food
        elif food < self.F:
            f = self.F - food
            self.eat_gain_weight(f)
            return 0


class Carnivore(Animal):
    """
    A class containing parameters and methods used to implement Carnivores
    """

    phi_age = 0.4
    a_half = 60.0
    phi_weight = 0.4
    w_half = 4.0
    w_birth = 6.0
    sigma_birth = 1.0
    omega = 0.9
    beta = 0.75
    gamma = 0.8
    eta = 0.125
    mu = 0.4
    zeta = 3.5
    xi = 1.1
    F = 50.0
    DeltaPhiMax = 10.0

    def __init__(self, specie, age, weight):
        super().__init__(specie, age, weight)

    def kill(self, phi_herb):
        """
        Function that decides whether a carnivore kills a herbivore or not
        :param phi_herb: fitness of herbivore that's being hunted
        :return: True if herbivore is killed
        """
        if self.phi <= phi_herb:
            kill_prob = 0
        elif 0 < self.phi - phi_herb < self.DeltaPhiMax:
            kill_prob = (self.phi - phi_herb) / self.DeltaPhiMax
        else:
            kill_prob = 1

        if rand.random() < kill_prob:
            return True

    def carn_eating(self, available_food, to_eat):
        """
        Method that computes how much the animal can eat, depending on the food available

        :param available_food: The amount of food available to the animal
        :param to_eat: the amount of food the animal wants to eat

        :return: how much more food the animal wants to eat
        """
        if available_food >= to_eat:
            self.eat_gain_weight(to_eat)
            return 0
        else:
            self.eat_gain_weight(available_food)
            return to_eat - available_food
