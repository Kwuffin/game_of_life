from unittest import TestCase
from Simulator import *
from random import randint
from copy import deepcopy


class TestSimulator(TestCase):
    """
    Tests for ``Simulator`` implementation.
    """
    def setUp(self):
        self.sim = Simulator()

    def test_update(self):
        """
        Tests that the update functions returns an object of World type.
        """
        self.assertIsInstance(self.sim.update(), World)

    def test_get_generation(self):
        """
        Tests whether get_generation returns the correct value:
            - Generation should be 0 when Simulator just created;
            - Generation should be 2 after 2 updates.
        """
        self.assertIs(self.sim.generation, self.sim.get_generation())
        self.assertEqual(self.sim.get_generation(), 0)
        self.sim.update()
        self.sim.update()
        self.assertEqual(self.sim.get_generation(), 2)

    def test_get_world(self):
        """
        Tests whether the object passed when get_world() is called is of World type, and has the required dimensions.
        When no argument passed to construction of Simulator, world is square shaped with size 20.
        """
        self.assertIs(self.sim.world, self.sim.get_world())
        self.assertEqual(self.sim.get_world().width, 20)
        self.assertEqual(self.sim.get_world().height, 20)

    def test_set_world(self):
        """
        Tests functionality of set_world function.
        """
        world = World(10)
        self.sim.set_world(world)
        self.assertIsInstance(self.sim.get_world(), World)
        self.assertIs(self.sim.get_world(), world)

    def test_rules(self):
        """"
        Tests the basic set of rules on https://canvas.hu.nl/courses/20308/assignments/108690

        Sets a random amount (max. a quarter of the grid) of squares with status 1.

        Loops through every single square in the grid.
            Gets the amount of neighbors.
            Gets the status of the previous generation.

            A cell with three neighbours, should always be alive in the next generation
            despite if it was previously alive or not. (birth)

            A cell with two neighbours, should be alive in the next generation if it was alive
            in the generation prior to that. A dead cell with two neighbours stays dead. (survival)

            A cell with one or less, or four or more neighbours are always dead in the next
            generation (exposure/overcrowding)
        """
        for _ in range(randint(0, (self.sim.world.width * self.sim.world.height) / 4)):
            self.sim.world.set(randint(0, self.sim.world.width), randint(0, self.sim.world.height), 1)

        self.worldOld = deepcopy(self.sim.world)  # Deep copies the old instance of the world, to compare it with later.
        self.sim.update()  # Go to the next generation in the original world.

        #  For every position in the grid.
        for x in range(self.sim.world.width):
            for y in range(self.sim.world.height):
                neighborCount = np.count_nonzero(self.worldOld.get_neighbours(x, y))  # Counts amount of neighbours.

                status = self.worldOld.get(x, y)  # Gets the old status of cell (dead/alive, 0/1)

                if 2 <= neighborCount <= 3:
                    if neighborCount == 3:  # Cells with three neighbours should ALWAYS be alive in generation n+1.
                        self.assertEqual(self.sim.world.get(x, y), 1)

                    elif neighborCount == 2:  # Cells with two neighbors should stay unchanged (survival).
                        if status == 0:  # Dead cells with two neighbors should stay dead.
                            self.assertEqual(self.sim.world.get(x, y), 0)

                        elif status != 0:  # Alive cells with two neighbors should stay alive.
                            self.assertEqual(self.sim.world.get(x, y), 1)

                else:  # If a cell has less than two, or more than three neighbours, they die (exposure/overcrowding).
                    self.assertEqual(self.sim.world.get(x, y), 0)
