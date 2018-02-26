"""This module test each function of find.py."""

import unittest

import constants.find as csfind


class TestFind(unittest.TestCase):
    """The testing class."""

    def test_find_and_get_coords_after(self):
        """Test the function find_sand_get_coords_after."""
        var_list = [
            'coords:0123,1000, thxthxthx',
            'eachtrusndjfcoords:0234,123449221038',
            'this is coords:0001,0098', ]
        good_coords_list = [
            (123, 1000),
            (234, 1234),
            (1, 98), ]

        substring = 'coords:'

        for var, good_coords in zip(var_list, good_coords_list):

            coords = csfind.find_and_get_coords_after(substring, var)

            self.assertEqual(coords, good_coords)

    def test_find_number_after(self):
        """Test the function find_number_after."""
        var_list = [
            'feizgtreio number:1',
            'number:9',
            'fajfeiufgtergzhrnumber:4ofr0',
            'fnumber:888', ]
        good_numbers = [1, 9, 4, 8]

        substring = 'number:'

        for text, good_number in zip(var_list, good_numbers):
            number = csfind.find_number_after(substring, text)

            self.assertIsInstance(number, int)
            self.assertEqual(good_number, number)

    def test_find_text_after(self):
        """Test the function find_text_after."""
        var_list = [
            'erfizrjftext:the_text_here_end roekjcierj',
            'text:fhreauh_end', ]
        good_texts = [
            'the_text_here_end',
            'fhreauh_end', ]

        substring = 'text:'

        for text, good_text in zip(var_list, good_texts):
            current_text = csfind.find_text_after(substring, text)

            self.assertEqual(current_text, good_text)
