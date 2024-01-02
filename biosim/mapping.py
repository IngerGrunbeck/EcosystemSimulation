# -*- coding: utf-8 -*-

"""
__author__ = 'Inger Annett Grünbeck','Yngvild Sauge'
__email__ = 'inger.annett.grunbeck@nmbu.no', 'yngvild.sauge@nmbu.no'
"""


from biosim.landscape import Landscape, Jungle, Savannah, Desert, Ocean, Mountain
import textwrap

"""
Creates an Island map
"""


class Island:
    """
    The class creates a map containing landscape-instances
    """
    def __init__(self, island_map=None):
        """
        :param island_map: a string containing the letters O, M, D, J and S, representing the
        landscape types
        """

        input_map = island_map if island_map is not None else """\
                                                                    OOOOOOOOOOOOOOOOOOOOO
                                                                    OOOOOOOOSMMMMJJJJJJJO
                                                                    OSSSSSJJJJMMJJJJJJJOO
                                                                    OSSSSSSSSSMMJJJJJJOOO
                                                                    OSSSSSJJJJJJJJJJJJOOO
                                                                    OSSSSSJJJDDJJJSJJJOOO
                                                                    OSSJJJJJDDDJJJSSSSOOO
                                                                    OOSSSSJJJDDJJJSOOOOOO
                                                                    OSSSJJJJJDDJJJJJJJOOO
                                                                    OSSSSJJJJDDJJJJOOOOOO
                                                                    OOSSSSJJJJJJJJOOOOOOO
                                                                    OOOSSSSJJJJJJJOOOOOOO
                                                                    OOOOOOOOOOOOOOOOOOOOO"""
        self.letter_map = textwrap.dedent(input_map)
        self.finished_map = None

    def create_map(self):
        """
        Method that creates a map where each cell is an instance based on the type of
        landscape

        :return: A map containing landscape-instances
        """
        map_split = self.letter_map.split()
        self.finished_map = [list(map_split[j]) for j in range(len(map_split))]

        for element in self.finished_map[0]+self.finished_map[-1]:
            if element is not 'O':
                raise ValueError('The edges of the map must be Ocean')

        for ind in range(len(self.finished_map)):
            for element in self.finished_map[ind]:
                if element == self.finished_map[ind][0] and element is not 'O':
                    raise ValueError('The edges of the map must be Ocean')
                elif element == self.finished_map[ind][-1] and element is not 'O':
                    raise ValueError('The edges of the map must be Ocean')

        comparison_length = len(self.finished_map[0])
        for row in self.finished_map:
            if len(row) != comparison_length:
                raise ValueError('The map has inconsistent line length')

        for i in range(len(self.finished_map)):
            for j in range(len(self.finished_map[i])):
                if self.finished_map[i][j] == 'D':
                    self.finished_map[i][j] = Desert()
                elif self.finished_map[i][j] == 'J':
                    self.finished_map[i][j] = Jungle()
                elif self.finished_map[i][j] == 'S':
                    self.finished_map[i][j] = Savannah()
                elif self.finished_map[i][j] == 'O':
                    self.finished_map[i][j] = Ocean()
                elif self.finished_map[i][j] == 'M':
                    self.finished_map[i][j] = Mountain()
                else:
                    raise ValueError('The map can only consist of the letters D, S, J, M, O')

        return self.finished_map

