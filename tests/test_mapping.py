# -*- coding: utf-8 -*-

"""
__author__ = 'Inger Annett Grünbeck','Yngvild Sauge'
__email__ = 'inger.annett.grunbeck@nmbu.no', 'yngvild.sauge@nmbu.no'
"""

import pytest
from biosim.mapping import Island
from biosim.landscape import Landscape


class TestIsland:
    """
    Class for testing the Island class
    """
    def test_map(self):
        """
        An island is created, in which every object is an instance
        """
        isl = Island("""\
                    OOOO
                    ODMO
                    OSSO
                    OOOO""")

        map_test = isl.create_map()
        for x, row in enumerate(map_test):
            for y, cell in enumerate(row):
                assert isinstance(map_test[x][y], Landscape)

