
BioSim
======

This is a project that simulates the ecosystem of an island as part of the final student project in INF200 - _Object oriented programming for python (NMBU)_. The island has five different landscape
types, mountain, ocean, desert, savannah, and jungle. The different landscape types have different feeding properties. While the mountain and oceans do not provide any food, the jungles has a high food max.

The Island is populated by herbivores and carnivores. The herbivores eat the food provided on the island, while the carnivores exclusively eat herbivores. All instances of the animals grow, age, feed, migrate and breed. The rates of feeding, migrating, and breeding are determined by various variables. 

When running, a GUI is available for adjusting the various variables, following the migration patterns, and observing the population growth over "years".

Contents
--------

- biosim: Python package for simulation of an island. Simulation is the main class for initializing the simulation
- examples: Script illustrating the use of the package. The script serves as an example, as well as evaluating whether the project fulfills the teacher's requirement.
- exam presentation: A recording of a simulation as well as a short presentation of the project's code.
- tests: Contains tests to facilitate test-driven development, partially based on the teacher's requirements.
