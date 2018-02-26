"""Test the module 'images' of f_roboc folder's.

_________________________________________________________
Warning: launch this module by using 'python -m unittest'
in the root of the project (StarLab),
or you will get some importations errors.
"""
import pygame
import f_roboc.images as images
import tests.parent_class as parent


pygame.init()


class TestImgs(parent.PygameTest):
    """Tests."""

    def setUp(self):
        """Called before."""
        super().setUp()
        self.images_folder = images.get_content_of('f_roboc/assets/images/')

        images.find_characters_and_create_their_moove_r_folder(
            self.images_folder)

    def test_interlocking(self):
        """Tests interlocking of dicts."""
        img = self.images_folder

        try:
            img["game"]["characters"]["superstar"]["breath"][2]
            img["main_menu"]["buttons"][1]
        except ValueError:
            raise ValueError

    def test_if_each_value_is_a_surface(self, surface_list=None):
        """Test if each value of a list is a pygame's surface."""
        if not surface_list:
            return

        for value in surface_list:
            self.assertIsInstance(value, pygame.surface.Surface)

    def test_if_a_folder_contain_a_list(self, folder=None):
        """Test if the folder contain a list.

        If it contain a dict, we this method again with this dict.
        Otherwise we test the list to check if all the values ​​are surfaces.
        """
        if not folder:
            folder = self.images_folder

        for key, value in folder.items():
            if isinstance(value, dict):
                self.test_if_a_folder_contain_a_list(value)
            elif isinstance(value, list):
                self.test_if_each_value_is_a_surface(value)
            elif not value:
                print("{}'s folder is empty.".format(key))
            else:
                raise TypeError("The type must be a list or a dict.\n",
                                "type is: {}.\n".format(value),
                                "key is: {}.".format(key))

    def test_if_the_moove_r_folder_works(self):
        """Test if the moove_r folders are correctly created."""
        characters = self.images_folder['game']['characters']

        for folder in characters.values():

            for image in folder['moove_r']:
                self.assertIsInstance(image, pygame.surface.Surface)
