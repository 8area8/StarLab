"""Module de gestion des sprites de la classe SelectLevel."""

import pygame

import constants.game_sizes as csizes

import f_roboc.select_level.maps_importation as mapimp

from f_roboc.sprites_classes.main_sprite import Button
from f_roboc.sprites_classes.main_sprite import ButtonPlusClick
from f_roboc.sprites_classes.select_level_sprites import NotImplementedSprite
from f_roboc.sprites_classes.select_level_sprites import UnactivatedSprite
from f_roboc.sprites_classes.text_button import TextMapButton


class SpritesController:
    """Main class."""

    def __init__(self, imgs):
        """Init."""
        self.imgs = imgs

        self.main_surface = pygame.Surface(
            csizes.SCREEN_SIZE)

        self.background = self.imgs['background'][0]

        """The back button."""
        self.back = Button(
            self.imgs['buttons'][3],
            self.imgs["buttons"][4],
            (26 * csizes.UPSCALE, 23 * csizes.UPSCALE),
            name='return')

        """Arrow buttons."""
        self.left_arrow = ButtonPlusClick(
            self.imgs["buttons"][0],
            self.imgs["buttons"][1],
            self.imgs["buttons"][2],
            (70 * csizes.UPSCALE, 82 * csizes.UPSCALE),
            name='left_arrow')

        self.right_arrow = ButtonPlusClick(
            self.imgs["buttons"][0],
            self.imgs["buttons"][1],
            self.imgs["buttons"][2],
            (535 * csizes.UPSCALE, 82 * csizes.UPSCALE),
            name='left_arrow')

        """Create a special surface for map buttons."""
        w, h = (122 * csizes.UPSCALE), (165 * csizes.UPSCALE)
        self.text_list_surface = pygame.Surface(
            (w, h), pygame.SRCALPHA, 32).convert_alpha()

        self._get_maps_buttons()
        self._get_warning_sprites()
        self._get_error_sprites()

        self._group_the_buttons()

    def _get_maps_buttons(self):
        """Get the map buttons.

        Create a group who contain all map-button's text.
        These sprites also contain the map list.

        TIP: The bool variables are for warning's buttons.
        """
        self.text_button_list = pygame.sprite.Group()
        self.to_much_files = False
        self.invalide_files = False

        maps_list, map_contents, self.to_much_files,\
            self.invalide_files = mapimp.list_maps()

        y = 15  # the button's height inside the button's surface.
        w_container = self.text_list_surface.get_size()[0]

        for i, name in enumerate(maps_list):
            self.text_button_list.add(
                TextMapButton(name, 15, 'white', 'blue', 0, y,
                              map_contents[i], 259, 160, w_container))
            y += 30

    def _get_warning_sprites(self):
        """Initialize the warning buttons."""
        self.not_implemented = NotImplementedSprite(
            self.imgs["warnings"][0],
            (256 * csizes.UPSCALE, 87 * csizes.UPSCALE))

        self.left_warning = UnactivatedSprite(
            self.imgs["warnings"][1],
            (32 * csizes.UPSCALE, 315 * csizes.UPSCALE),
            name='left_warning')

        self.right_warning = UnactivatedSprite(
            self.imgs["warnings"][2],
            (474 * csizes.UPSCALE, 315 * csizes.UPSCALE),
            name='right_warning')

        if self.to_much_files:
            self.left_warning.activated = True
        if self.invalide_files:
            self.right_warning.activated = True

    def _get_error_sprites(self):
        """Initialize the error sprites."""
        self.launched_game = UnactivatedSprite(
            self.imgs['errors'][0],
            (225 * csizes.UPSCALE, 149 * csizes.UPSCALE),
            name='laucnhed_game')
        self.no_connection = UnactivatedSprite(
            self.imgs['errors'][1],
            (225 * csizes.UPSCALE, 149 * csizes.UPSCALE),
            name='no_connection')

    def _group_the_buttons(self):
        """Make pygame groups to group all buttons."""
        # Group warning buttons.
        self.ponct_sprites = pygame.sprite.Group()
        self.ponct_sprites.add(
            self.not_implemented,
            self.left_warning,
            self.right_warning)

        # Group the others.
        self.button_list = pygame.sprite.Group()
        self.button_list.add(
            self.back,
            self.left_arrow,
            self.right_arrow)
