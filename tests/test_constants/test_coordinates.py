"""Test of coordinates functions."""

import unittest
import random

from constants.coordinates import RELATIVES_COORDS, transform_coords_to
from constants.game_sizes import CASE_SIZE


class TestCoordinates(unittest.TestCase):
    """The testing class."""

    def setUp(self):
        self.relatives_coords = RELATIVES_COORDS

    """IF YOU WANT TO SEE THE BEAUTIFULL COORDS LISTS.

    for coords_list in self.relatives_coords:
            print(coords_list, '\n')
    """

    def test_relatives_coords(self):
        """Test the relatives coords.

        We just try 2 lists of relatives_coords in this test.

        - We create a fictive hero's coordinates.

        - Then, we adjust the relatives coords to the hero's coords,
          and add the result to the 'true_coords' list.

        - Finally, we try to match the good_list (manually created),
          with true_coords (using relatives_coords).
        """
        moove = self.relatives_coords[:2]

        hero_coords = (12, 45)
        true_coords = []

        for coords_list in moove:
            for coords in coords_list:

                x, y = coords
                h_x, h_y = hero_coords

                h_x += x
                h_y += y

                true_coords.append((h_x, h_y))

        good_list = [
            (13, 45),
            (11, 45),
            (12, 46),
            (12, 44),
            (14, 45),
            (10, 45),
            (12, 47),
            (12, 43),
            (13, 46),
            (11, 44),
            (13, 44),
            (11, 46), ]

        self.assertCountEqual(good_list, true_coords)

    def test_transform_coords(self, number_of_tests=10):
        """Test the transfom_coord_to function.

        We start with a random abstract coordinates,
        made with the random's module.
        max x and y doesn't exceed the sizes of my maps (20 on 9)

        - real_coords must be equal to abstract coords * the size of the cases.

        - return to abstract must be equal to the first abstract variable.

        - size of string coord must be equal to 10.
        - string coords and tuple coords must be str and tuple.

        - the last coords variable must be equal to the first..!

        - finally, we transform real coords to str, and return it to tuple.
        - we test if the tuple didn t change after the transformation.

        After that, call the test again,
        until the parameter 'test number' equals 1.
        """
        coords = (random.randint(0, 19), random.randint(0, 8))
        print("test of 'transform_coords_to'. start coords is ", coords)

        real_coords = transform_coords_to('real', coords)
        x, y = coords
        self.assertEqual((x * CASE_SIZE, y * CASE_SIZE), real_coords)

        abstract_coords = transform_coords_to('abstract', real_coords)
        self.assertEqual(abstract_coords, coords)

        string_coords = transform_coords_to('string', abstract_coords)
        self.assertEqual(10, len(string_coords))
        self.assertIsInstance(string_coords, str)

        tuple_coords = transform_coords_to('tuple', string_coords)
        self.assertIsInstance(tuple_coords, tuple)
        self.assertEqual(tuple_coords, coords)

        string_real_coords = transform_coords_to('string', real_coords)
        tuple_real_coords = transform_coords_to('tuple', string_real_coords)
        self.assertEqual(tuple_real_coords, real_coords)

        if number_of_tests > 1:
            self.test_transform_coords(number_of_tests=number_of_tests - 1)
