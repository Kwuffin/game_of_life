from World import *
from copy import deepcopy


class Simulator:
    """
    Game of Life simulator. Handles the evolution of a Game of Life ``World``.
    Read https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life for an introduction to Conway's Game of Life.
    """

    def __init__(self, world=None):
        """
        Constructor for Game of Life simulator.

        :param world: (optional) environment used to simulate Game of Life.
        """
        self.generation = 0
        if world is None:
            self.world = World(20)
        else:
            self.world = world

    def update(self) -> World:
        """
        Updates the state of the world to the next generation. Uses rules for evolution.

        Rules:
        1. Every living cell with less than two neighbours die (exposure).
        2. Every living cell with more than three neighbours die (overcrowding).
        3. Every cell with two, or three neighbours remain unchanged (survival).
        4. Every dead cell with three neighbours, come to life (birth).

        We need to make a copy and a new instance of the world with generation n - 1, so that changes in the new world
        don't affect changes in the same generation. Since we have two for-loops, the top-left cells in the grid will
        be updated earlier than the cells in the bottom-right.

        Then we just need to set the status of every cell according to the unittest that we wrote earlier.

        :return: New state of the world.
        """
        self.generation += 1

        # TODO: Do something to evolve the generation
        self.worldOld = deepcopy(self.world)  # Deepcopy the world with generation n - 1.

        #  For every position in the grid.
        for x in range(self.world.width):
            for y in range(self.world.height):
                neighborCount = np.count_nonzero(self.worldOld.get_neighbours(x, y))  # Gets the amount of neighbours.

                oldStatus = self.worldOld.get(x, y)  # Gets the status of the cell in generation n - 1.

                # Set cell status for generation n.
                self.world.set(x, y) if (neighborCount == 3) or (neighborCount == 2 and oldStatus == 1) else self.world.set(x, y, 0)

                # Before refactor:
                # if 2 <= neighborCount <= 3:
                #     if neighborCount == 3:
                #         self.world.set(x, y)
                #
                #     elif neighborCount == 2:
                #         if oldStatus == 1:
                #             self.world.set(x, y)
                #         elif oldStatus == 0:
                #             self.world.set(x, y, 0)
                #
                # else:
                #     self.world.set(x, y, 0)

        return self.world

    def get_generation(self):
        """
        Returns the value of the current generation of the simulated Game of Life.

        :return: generation of simulated Game of Life.
        """
        return self.generation

    def get_world(self):
        """
        Returns the current version of the ``World``.

        :return: current state of the world.
        """
        return self.world

    def set_world(self, world: World) -> None:
        """
        Changes the current world to the given value.

        :param world: new version of the world.

        """
        self.world = world
