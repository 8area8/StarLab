"""Module de gestion des sprites de la classe SelectLevel."""

import pygame

import constants.game_sizes as cst

import f_roboc.select_level.maps_importation as mapimp

from f_roboc.sprites_classes.animated_sprites import PonctualSprite
from f_roboc.sprites_classes.sprites_buttons import SpriteButton
from f_roboc.sprites_classes.text_button import TextMapButton


class SpritesController:
    """Main class."""

    def __init__(self, imgs):
        """Init."""
        self.imgs = imgs

        self.main_surface = pygame.Surface(
            cst.SCREEN_SIZE)

        self.background = self.imgs['bg']

        """Bouton retour arrière."""
        self.back = SpriteButton(
            self.imgs['buttons']['return_act'],
            self.imgs["buttons"]['return_neutr'],
            (26 * cst.UPSCALE, 23 * cst.UPSCALE),
            name='return')

        """Je crée les boutons fléchés."""
        self.left_arrow = SpriteButton(
            self.imgs["buttons"]['sellevel_arrow_act'],
            self.imgs["buttons"]['sellevel_arrow_neutr'],
            (70 * cst.UPSCALE, 82 * cst.UPSCALE),
            name='left_arrow',
            anim_imgs=[self.imgs["buttons"]["arrow_glitch"]],
            time_per_img=[100])

        self.right_arrow = SpriteButton(
            self.imgs["buttons"]['sellevel_arrow_act'],
            self.imgs["buttons"]['sellevel_arrow_neutr'],
            (535 * cst.UPSCALE, 82 * cst.UPSCALE),
            name='left_arrow',
            anim_imgs=[self.imgs["buttons"]["arrow_glitch"]],
            time_per_img=[100])

        """Je récupère les maps et les transormes en bouton texte,
        avec le tableau de chaque map de côté."""
        w, h = (122 * cst.UPSCALE), (165 * cst.UPSCALE)
        self.text_list_surface = pygame.Surface(
            (w, h), pygame.SRCALPHA, 32).convert_alpha()

        self.text_button_list = pygame.sprite.Group()
        self.to_much_files = False
        self.invalide_files = False

        self.get_maps_buttons()

        """Je crée les sprites qui s'affichent sous certaines conditions."""
        self.not_implemented = PonctualSprite(
            self.imgs["warnings"]['not_implemented'],
            (256 * cst.UPSCALE, 87 * cst.UPSCALE),
            name='not_implemented',
            max_time=600)

        self.left_warning = PonctualSprite(
            self.imgs["warnings"]['warning1'],
            (32 * cst.UPSCALE, 315 * cst.UPSCALE),
            name='left_warning',
            infinite=True)
        self.right_warning = PonctualSprite(
            self.imgs["warnings"]['warning2'],
            (474 * cst.UPSCALE, 315 * cst.UPSCALE),
            name='right_warning',
            infinite=True)

        """On active ou non certains sprites."""
        if self.to_much_files:
            self.left_warning.activated = True
        if self.invalide_files:
            self.right_warning.activated = True

        """Liste des boutons de type warning."""
        self.ponct_sprites = pygame.sprite.Group()
        self.ponct_sprites.add(
            self.not_implemented,
            self.left_warning,
            self.right_warning)

        """Liste des boutons simples."""
        self.button_list = pygame.sprite.Group()
        self.button_list.add(
            self.back,
            self.left_arrow,
            self.right_arrow)

    def get_maps_buttons(self):
        """Prend les boutons de maps."""
        maps_list, map_contents, self.to_much_files,\
            self.invalide_files = mapimp.list_maps()
        y = 15
        temp = self.text_list_surface.get_size()
        w_container = temp[0]

        for i, name in enumerate(maps_list):
            self.text_button_list.add(
                TextMapButton(name, 15, 'white', 'blue', 0, y,
                              map_contents[i], 259, 160, w_container))
            y += 30
