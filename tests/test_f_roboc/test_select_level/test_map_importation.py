"""Test the map_importation module."""

import unittest

from f_roboc.select_level import maps_importation as mapimp


class TestMapImportation(unittest.TestCase):
    """Here the testing class."""

    def test_list_maps(self):
        """Test the main function of map_importation.

        We test the lenght and the height of each map content.
        At last, each map content's list must contain characters.
        """
        map_name, contents, err_one, err_two = mapimp.list_maps()

        self.assertIsInstance(err_one, bool)
        self.assertIsInstance(err_two, bool)

        for name, list_content in zip(map_name, contents):
            self.assertIsInstance(name, str)

            self.assertEqual(len(list_content), 9)

            for line in list_content:
                self.assertEqual(len(line), 20)
                for character in line:
                    self.assertIsInstance(character, str)
