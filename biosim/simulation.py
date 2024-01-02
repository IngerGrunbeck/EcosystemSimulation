# -*- coding: utf-8 -*-

"""
__author__ = 'Inger Annett Grünbeck','Yngvild Sauge'
__email__ = 'inger.annett.grunbeck@nmbu.no', 'yngvild.sauge@nmbu.no'
"""

import matplotlib.pyplot as plt
from biosim.cell_control import *
import pandas as pd
import numpy as np
import random as rand
from matplotlib.widgets import Button, Slider
import subprocess

"""
Simulates an ecosystem
"""

# update the variable to your path
_FFMPEG_BINARY = 'ffmpeg'


class BioSim:
    """
    The class simulates the seasons on an Island, and creates an interface that plots the animal
    distribution

    Source1: INF200, example projects: "randvis: simulation"
    Source2: INF200, J05:"plot_update"
    Source3: INF200, J05:"mapping"
    Source4: INF200, L11:"demo_gui"

    Author: Hans E Plesser
    """

    def __init__(self, seed=None, island_map=None, ini_pop=None, ymax_animals=None,
                 cmax_animals=None, img_base=None, img_fmt='png'):

        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path. If None,
         no figures are written to file
        :param img_fmt: String with file type for figures, e.g. ’png’

        If img_base is None, no figures are written to file.

        Filenames are formed as
            ’{}_{:05d}.{}’.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self._cycle = Cells(ini_pop, island_map)
        self._isl = Island(island_map)

        rand.seed(seed)
        self.ymax_animals = ymax_animals if ymax_animals is not None else self.num_animals + 10
        self.automatic_ymax = False if ymax_animals is not None else True
        self.cmax_animals = cmax_animals if cmax_animals is not None else {'Herbivore': 100,
                                                                           'Carnivore': 50}
        self.img_base = img_base
        self.img_fmt = img_fmt
        self._img_ctr = 0

        self._fig = None
        self._map_ax = None
        self._legend_ax = None
        self._herb_ax = None
        self._carn_ax = None
        self._herb_dist_axis = None
        self._carn_dist_axis = None
        self._pop_ax = None
        self._herb_line = None
        self._carn_line = None

        self._ax_omega_herb_slider = None
        self._omega_herb_slide = None
        self._ax_gamma_herb_slider = None
        self._gamma_herb_slide = None
        self._ax_omega_carn_slider = None
        self._omega_carn_slide = None
        self._ax_gamma_carn_slider = None
        self._gamma_carn_slide = None

        self._ax_reset = None
        self._reset_widget = None
        self._ax_interrupt = None
        self._interrupt_widget = None

        self._year = 0
        self._final_year = None
        self._quit_sim = None

        self._omega_herb = Herbivore.omega
        self._omega_carn = Carnivore.omega
        self._gamma_herb = Herbivore.gamma
        self._gamma_carn = Carnivore.gamma

    def set_animal_parameters(self, species, params):
        """
        The method sets parameters for animal species

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == 'Herbivore':
            Herbivore.set_parameters(params)
        elif species == 'Carnivore':
            Carnivore.set_parameters(params)
        else:
            raise ValueError('Your chosen species is not valid. Choose either Herbivore or '
                             'Carnivore')

    def set_landscape_parameters(self, landscape, params):
        """
        The method sets parameters for landscape type

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == 'J':
            Jungle.set_parameters(params)
        elif landscape == 'S':
            Savannah.set_parameters(params)
        else:
            raise ValueError('Your chosen landscape is not valid. Choose either J or '
                             'S')

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Runs simulation while visualizing the result

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        """
        if img_years is None:
            img_years = vis_years

        self._quit_sim = False
        self._final_year = self.year + num_years
        #self.set_up_graphics()

        self._cycle.generate_animals()

        while self._year < self._final_year:

            self._cycle.cell_cycle()

            #if self._year % vis_years == 0:
                #self._update_graphics()

            #if self._year % img_years == 0:
                #self._save_graphics()

            self._year += 1

            if self._quit_sim:
                break

    def set_up_graphics(self):
        """
        Method sets up graphics, and creates axes containing a island map, distribution maps and
        a line plot. The methods also creates widgets that let us adjust parameters and stop and
        reset the simulation
        """
        if self._fig is None:
            self._fig = plt.figure()
            self._fig.suptitle('BioSimulation Year:{}'.format(self.year), fontsize=16)

        #                   R    G    B
        rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                     'M': (0.5, 0.5, 0.5),  # grey
                     'J': (0.0, 0.6, 0.0),  # dark green
                     'S': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row]
                    for row in self._isl.letter_map.splitlines()]

        if self._legend_ax is None:
            self._legend_ax = self._fig.add_axes([0.7, 0.1, 0.1, 0.8])  # llx, lly, w, h
            self._legend_ax.axis('off')
            for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                       'Savannah', 'Desert')):
                self._legend_ax.add_patch(plt.Rectangle((0., ix * 0.2), 0.1, 0.1,
                                                        edgecolor='none',
                                                        facecolor=rgb_value[name[0]]))
                self._legend_ax.text(0.35, ix * 0.2, name, transform=self._legend_ax.transAxes)

        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(2, 2, 2)
            self._map_ax.imshow(kart_rgb)
            self._map_ax.set_title('Island map')

            self._map_ax.set_xticks(range(len(kart_rgb[0])))
            self._map_ax.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
            self._map_ax.set_yticks(range(len(kart_rgb)))
            self._map_ax.set_yticklabels(range(1, 1 + len(kart_rgb)))

        if self._herb_ax is None:
            self._herb_ax = self._fig.add_subplot(2, 2, 3)
            self._herb_ax.set_title('Herbivore distribution')
            self._herb_dist_axis = None

            self._herb_ax.set_xticks(range(len(kart_rgb[0])))
            self._herb_ax.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
            self._herb_ax.set_yticks(range(len(kart_rgb)))
            self._herb_ax.set_yticklabels(range(1, 1 + len(kart_rgb)))

        if self._carn_ax is None:
            self._carn_ax = self._fig.add_subplot(2, 2, 4)
            self._carn_ax.set_title('Carnivore distribution')
            self._carn_dist_axis = None

            self._carn_ax.set_xticks(range(len(kart_rgb[0])))
            self._carn_ax.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
            self._carn_ax.set_yticks(range(len(kart_rgb)))
            self._carn_ax.set_yticklabels(range(1, 1 + len(kart_rgb)))

        if self._pop_ax is None:
            self._pop_ax = self._fig.add_subplot(2, 2, 1)
            self._pop_ax.set_ylim(0, self.ymax_animals)
        self._pop_ax.set_xlim(0, self._final_year + 10)
        self._pop_ax.set_title('Animal count')

        if self._herb_line is None:
            herb_plot = self._pop_ax.plot(np.arange(0, self._final_year),
                                          np.full(self._final_year, np.nan))
            self._herb_line = herb_plot[0]
            self._herb_line.set_label('Herbivore')
        else:
            xdata, ydata = self._herb_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._herb_line.set_data(np.hstack((xdata, xnew)),
                                         np.hstack((ydata, ynew)))

        if self._carn_line is None:
            carn_plot = self._pop_ax.plot(np.arange(0, self._final_year),
                                          np.full(self._final_year, np.nan))
            self._carn_line = carn_plot[0]
            self._carn_line.set_label('Carnivore')
        else:
            xdata, ydata = self._carn_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._carn_line.set_data(np.hstack((xdata, xnew)),
                                         np.hstack((ydata, ynew)))

        self._pop_ax.legend()
        plt.subplots_adjust(bottom=0.1, right=0.65, top=0.9)

        self._ax_omega_herb_slider = self._fig.add_axes([0.86, 0.75, 0.1, 0.05])
        self._omega_herb_slide = Slider(self._ax_omega_herb_slider,
                                        label='Herbivore: Omega',
                                        valmin=0, valmax=1,
                                        valinit=Herbivore.omega,
                                        valfmt='%.2f')
        self._omega_herb_slide.on_changed(self._set_om_herb)

        self._ax_gamma_herb_slider = self._fig.add_axes([0.86, 0.65, 0.1, 0.05])
        self._gamma_herb_slide = Slider(self._ax_gamma_herb_slider,
                                        label='Herbivore: Gamma',
                                        valmin=0, valmax=1,
                                        valinit=Herbivore.gamma,
                                        valfmt='%.2f')
        self._gamma_herb_slide.on_changed(self._set_ga_herb)

        self._ax_omega_carn_slider = self._fig.add_axes([0.86, 0.55, 0.1, 0.05])
        self._omega_carn_slide = Slider(self._ax_omega_carn_slider,
                                        label='Carnivore: Omega',
                                        valmin=0, valmax=1,
                                        valinit=Carnivore.omega,
                                        valfmt='%.2f')
        self._omega_carn_slide.on_changed(self._set_om_carn)

        self._ax_gamma_carn_slider = self._fig.add_axes([0.86, 0.45, 0.1, 0.05])
        self._gamma_carn_slide = Slider(self._ax_gamma_carn_slider,
                                        label='Carnivore: Gamma',
                                        valmin=0, valmax=1,
                                        valinit=Carnivore.gamma,
                                        valfmt='%.2f')
        self._gamma_carn_slide.on_changed(self._set_ga_carn)

        self._ax_reset = self._fig.add_axes([0.85, 0.3, 0.05, 0.05])
        self._reset_widget = Button(self._ax_reset, 'Reset')
        self._reset_widget.on_clicked(self._reset)

        self._ax_interrupt = self._fig.add_axes([0.85, 0.2, 0.05, 0.05])
        self._interrupt_widget = Button(self._ax_interrupt, 'Quit')
        self._interrupt_widget.on_clicked(self._interrupt)

        plt.show()

    def _set_om_herb(self, value):
        """
        Method sets the value of herbivores omega

        :param value: new value of omega
        """
        Herbivore.omega = value

    def _set_ga_herb(self, value):
        """
        Method sets the value of herbivores gamma

        :param value: new value of gamma
        """
        Herbivore.gamma = value

    def _set_om_carn(self, value):
        """
        Method sets the value of carnivores omega

        :param value: new value of omega
        """
        Carnivore.omega = value

    def _set_ga_carn(self, value):
        """
        Method sets the value of carnivore gamma

        :param value: new value of gamma
        """
        Carnivore.gamma = value

    def _reset(self, event):
        """
        Reset parameters

        :param event: the button click
        """

        Herbivore.omega = self._omega_herb
        Carnivore.omega = self._omega_carn
        Herbivore.gamma = self._gamma_herb
        Carnivore.gamma = self._gamma_carn

        self._omega_herb_slide.reset()
        self._omega_carn_slide.reset()
        self._gamma_herb_slide.reset()
        self._gamma_carn_slide.reset()

    def _interrupt(self, event):
        """
        Closes the figure and changes self._interrupt to True, which will end the simulation

        :param event: the button click
        """
        self._quit_sim = True
        Herbivore.omega = self._omega_herb
        Carnivore.omega = self._omega_carn
        Herbivore.gamma = self._gamma_herb
        Carnivore.gamma = self._gamma_carn

    def _df_to_matrix(self):
        """
        turns a dataframe into a matrix

        :return: matrix containing number of animals in cells
        """
        df = self.animal_distribution
        herb_mat = df['Herbivore'].values
        carn_mat = df['Carnivore'].values

        length_x = len(self._cycle.map)
        length_y = len(self._cycle.map[0])

        return np.reshape(herb_mat, (length_x, length_y)), \
               np.reshape(carn_mat, (length_x, length_y))

    def _update_distribution_map(self):
        """
        Updates the distribution maps

        """
        herb_matrix, carn_matrix = self._df_to_matrix()

        if self._herb_dist_axis is not None:
            self._herb_dist_axis.set_data(herb_matrix)
        else:
            self._herb_dist_axis = self._herb_ax.imshow(herb_matrix,
                                                        interpolation='nearest',
                                                        vmin=0, vmax=self.cmax_animals['Herbivore'])
            plt.colorbar(self._herb_dist_axis, ax=self._herb_ax,
                         orientation='horizontal')

        if self._carn_dist_axis is not None:
            self._carn_dist_axis.set_data(carn_matrix)
        else:
            self._carn_dist_axis = self._carn_ax.imshow(carn_matrix,
                                                        interpolation='nearest',
                                                        vmin=0, vmax=self.cmax_animals['Carnivore'])
            plt.colorbar(self._carn_dist_axis, ax=self._carn_ax,
                         orientation='horizontal')

    def _update_population_graph(self):
        """
        Updates the population graph
        """
        animal_dict = self.num_animals_per_species
        ydata_herb = self._herb_line.get_ydata()
        ydata_carn = self._carn_line.get_ydata()

        ydata_herb[self._year] = animal_dict['Herbivore']
        ydata_carn[self._year] = animal_dict['Carnivore']

        self._herb_line.set_ydata(ydata_herb)
        self._carn_line.set_ydata(ydata_carn)

        if self.automatic_ymax and self.ymax_animals < (self.num_animals + 100):
            self.ymax_animals = self.num_animals + 100
            self._pop_ax.set_ylim(0, self.ymax_animals)

    def _update_graphics(self):
        """
        Updates the interface, and pauses the figure
        """
        self._update_distribution_map()
        self._update_population_graph()
        self._fig.suptitle('BioSimulation Year:{}'.format(self.year), fontsize=16)

        plt.pause(1e-6)

    def add_population(self, population):
        """
        Adds a population to the island

        :param population: List of dictionaries specifying population
        """
        self._cycle.population_cell = population
        self._cycle.generate_animals()

    @property
    def year(self):
        """
        Last year simulated"""
        return self._year

    @property
    def num_animals(self):
        """Returns total number of animals on island"""
        df_pop = self.animal_distribution
        num_herb = df_pop['Herbivore'].sum()
        num_carn = df_pop['Carnivore'].sum()
        return num_carn + num_herb

    @property
    def num_animals_per_species(self):
        """Returns number of animals per species in island, as dictionary."""
        df_pop = self.animal_distribution
        num_herb = df_pop['Herbivore'].sum()
        num_carn = df_pop['Carnivore'].sum()
        return {'Herbivore': num_herb, 'Carnivore': num_carn}

    @property
    def animal_distribution(self):
        """Returns pandas DataFrame with animal count per species for each cell on island."""
        animal_df = pd.DataFrame(columns=['Row', 'Col', 'Herbivore', 'Carnivore'])

        ix = 0
        for x, row in enumerate(self._cycle.map):
            for y, cell in enumerate(row):
                ix += 1
                animal_df.loc[ix] = [x, y, len(cell.pop_herb), len(cell.pop_carn)]
        animal_df = animal_df.astype(int)
        return animal_df

    def _save_graphics(self):
        """
        Saves graphics to file if file name given

        """

        if self.img_base is None:
            return

        self._fig.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                           num=self._img_ctr,
                                                           type=self.img_fmt))
        self._img_ctr += 1

    def make_movie(self, movie_fmt=None):
        """
        Create MPEG4 movie from visualization images saved
        :param movie_fmt: movie format
        """
        movie_fmt = movie_fmt if movie_fmt is not None else 'mp4'

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self.img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self.img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)
