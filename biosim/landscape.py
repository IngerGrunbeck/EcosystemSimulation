# -*- coding: utf-8 -*-

"""
__author__ = 'Inger Annett Grünbeck','Yngvild Sauge'
__email__ = 'inger.annett.grunbeck@nmbu.no', 'yngvild.sauge@nmbu.no'
"""


from biosim.animals import Animal, Carnivore, Herbivore
import math

"""
Manages landscape instances, each containing a list which may contain animal instances
"""


class Landscape:
    """
    The class contains different methods that change landscape attributes and parameters.
    It also contains methods iterating through animal-instances, and changing the animal attributes
    """
    param_landscape_limits = {'f_max': (0, math.inf), 'alpha': (0, 1)}

    @classmethod
    def set_parameters(cls, new_params):
        """
        The method redefines landscape parameters, as long as the chosen parameters already exist.

        Source: INF200, example projects: "biolab_project: bacteria"
        Author: Hans E Plesser

        :param new_params: a dict, containing the new parameter values
        """
        for key in new_params:
            if key not in ('f_max', 'alpha'):
                raise KeyError('Invalid parameter name' + key)

        for key, value in new_params.items():
            if cls.param_landscape_limits[key][0] < value < cls.param_landscape_limits[key][1]:
                setattr(cls, key, value)
            else:
                raise ValueError('chosen value for parameter is invalid')

    def __init__(self):
        self.pop_herb = []
        self.pop_carn = []
        self.f_max = 0
        self.food = self.f_max
        self.habitable = True

    def sort_fitness(self):
        """
        Method that sorts the animals by fitness in descending order, one list for herbivores,
        one for carnivores
        """
        for animal in self.pop_herb+self.pop_carn:
            animal.fitness()
        self.pop_herb.sort(key=lambda individual: individual.phi, reverse=True)
        self.pop_carn.sort(key=lambda individual: individual.phi, reverse=True)

    def feeding_herb(self):
        """
        Method that feeds the herbivores
        """
        pass

    def feeding_carn(self):
        """
        Method that feeds the carnivores
        """
        if self.pop_carn and self.pop_herb:
            self.sort_fitness()
            herb_hunted = self.pop_herb.copy()
            herb_survived = []

            for animal in self.pop_carn:
                if animal.not_walked:
                    eat_food = Carnivore.F
                    herb_survived = []
                    while eat_food > 0 and len(herb_hunted) > 0:
                        if animal.kill(herb_hunted[-1].phi):
                            eat_food = animal.carn_eating(herb_hunted[-1].w, eat_food)
                            animal.fitness()
                        else:
                            herb_survived.append(herb_hunted[-1])

                        del herb_hunted[-1]
                    herb_hunted = herb_survived

            self.pop_herb = herb_survived

    def age(self):
        """
        Method that ages the animals
        """
        for animal in self.pop_herb+self.pop_carn:
            animal.aging()

    def weight_loss(self):
        """
        Method that makes the animals loose some weight at the end of each year
        """
        for animal in self.pop_herb+self.pop_carn:
            animal.loose_weight()

    def birth(self):
        """
        Method that checks if animals should give birth and adds the newborn babies to the
        populations
        """

        newborn_herb = []
        newborn_carn = []

        for animal in self.pop_herb+self.pop_carn:
            if animal.not_walked and animal.specie == 'Herbivore':
                baby = animal.give_birth(animal.specie, len(self.pop_herb))
                if baby:
                    newborn_herb.append(baby)

            elif animal.not_walked and animal.specie == 'Carnivore':
                baby = animal.give_birth(animal.specie, len(self.pop_carn))
                if baby:
                    newborn_carn.append(baby)

        self.pop_herb.extend(newborn_herb)
        self.pop_carn.extend(newborn_carn)

    def survive(self):
        """
        Method that updates the populations with the surviving animals at the end of each year
        """
        if self.pop_carn or self.pop_herb:
            alive_herb = []
            alive_carn = []

            for animal in self.pop_herb+self.pop_carn:
                if animal.survival() and animal.specie == 'Herbivore':
                    if animal.fitness() != 0:
                        alive_herb.append(animal)
                elif animal.survival() and animal.specie == 'Carnivore':
                    if animal.fitness() != 0:
                        alive_carn.append(animal)

            self.pop_herb = alive_herb
            self.pop_carn = alive_carn

    def set_not_walked_true(self):
        """
        Method that sets the parameter not.walked to be True
        """
        for animal in self.pop_herb+self.pop_carn:
            animal.not_walked = True


class Jungle(Landscape):
    """
    The class contains methods from Landscape adjusted to Jungle-instances
    """
    f_max = 800

    def __init__(self):
        super().__init__()
        self.food = self.f_max

    def feeding_herb(self):
        """
        Method that feeds the herbivores in jungle instances
        """
        if self.pop_herb:
            self.sort_fitness()
            self.food = self.f_max
            for animal in self.pop_herb:
                if animal.not_walked:
                    self.food = animal.herb_eating(self.food)


class Savannah(Landscape):
    """
    The class contains methods from Landscape adjusted to Savannah-instances
    """
    alpha = 0.3
    f_max = 300

    def __init__(self):
        super().__init__()
        self.food = self.f_max

    def regrow(self):
        """
        Method that regrows some of the vegetation in a savannah instance
        """
        self.food = self.food + self.alpha * (self.f_max - self.food)

    def feeding_herb(self):
        """
        Method that feeds a herbivore in a savannah instance
        """
        self.regrow()
        if self.pop_herb:
            self.sort_fitness()
            for animal in self.pop_herb:
                if animal.not_walked:
                    self.food = animal.herb_eating(self.food)


class Mountain(Landscape):
    """
    The class contains methods from Landscape adjusted to Mountain-instances
    """
    def __init__(self):
        super(Mountain, self).__init__()
        self.habitable = False


class Ocean(Landscape):
    """
    The class contains methods from Landscape adjusted to Ocean-instances
    """
    def __init__(self):
        super().__init__()
        self.habitable = False


class Desert(Landscape):
    """
    The class contains methods from Landscape adjusted to Desert-instances
    """
    def __init__(self):
        super().__init__()



