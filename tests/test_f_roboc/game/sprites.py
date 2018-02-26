"""Module de gestion des sprites de la classe Game."""

import pygame

import f_roboc.constants as cst

from f_roboc.sprites_classes.case_sprite import CaseSprite as CaseSprite
from f_roboc.sprites_classes.map_sprite import MapSprites as MapSprites

from f_roboc.sprites_classes.animated_sprites import TimeSprite as TimeSprite
from f_roboc.sprites_classes.animated_sprites import BullSprite as BullSprite
from f_roboc.sprites_classes.animated_sprites import AnimatedPonctualSprite
from f_roboc.sprites_classes.animated_sprites import TransformSprite
from f_roboc.sprites_classes.animated_sprites import TransformAnimSprite
from f_roboc.sprites_classes.Transform_paths import TransformPaths
from f_roboc.sprites_classes.heroes import Hero
import f_roboc.sprites_classes.pathfinder as pth


class SpritesController:
    """Main class."""

    def __init__(self, imgs, map_name=None):
        """Init."""
        self.imgs = imgs

        self.main_surface = pygame.Surface(
            cst.SCREEN_SIZE)

        self.wait_players = self.imgs["informations"]["wait_players"]

        self.map_surface = pygame.Surface(
            (640 * cst.UPSCALE, 288 * cst.UPSCALE),
            pygame.SRCALPHA, 32).convert_alpha()

        self.cases_group = MapSprites()
        self.heroes_grp = pygame.sprite.Group()

        self.menu_blue = self.imgs["menu"]["super_menu"]
        self.menu_grey = self.imgs["menu"]["super_menu_grey"]
        self.menu = self.menu_blue

        self.time = TimeSprite(
            self.imgs["menu"]["time"],
            (274 * cst.UPSCALE, 284 * cst.UPSCALE),
            "time")

        self.bull = BullSprite(
            self.imgs["menu"]["bull"],
            (291 * cst.UPSCALE, 300 * cst.UPSCALE),
            "bull")

        self.next_turn = AnimatedPonctualSprite(
            self.imgs["menu"]["next_turn"],
            (13 * cst.UPSCALE, 20 * cst.UPSCALE),
            "next_turn")

        self.transform = TransformSprite(
            self.imgs["menu"]["transform"],
            (189 * cst.UPSCALE, 306 * cst.UPSCALE),
            "transform")

        self.transform_anim = TransformAnimSprite(
            self.imgs["transform"], "transform_anim")

        self.menu_layer_1 = pygame.sprite.Group()
        self.menu_layer_1.add(
            self.time)

        self.menu_layer_2 = pygame.sprite.Group()
        self.menu_layer_2.add(
            self.bull,
            self.next_turn,
            self.transform,
            self.transform_anim)

        self.pathfinder = None
        self.transform_paths = None

    def create_map(self, map_contents):
        """Incorpore chaque case dans un groupe de sprite."""
        x = 0
        y = 0
        nature = ''
        true_coords = ()
        number = 1

        for line in map_contents:

            x = 0
            for word in line:
                true_coords = x * cst.CASE_SIZE, y * cst.CASE_SIZE

                if word == ' ' or word == '.':
                    nature = 'path'
                elif word == 'O':
                    nature = 'wall'
                elif word == 'T':
                    nature = 'teleporter'
                elif word == 'V':
                    nature = 'victory'
                else:
                    raise ValueError("la map contient un caractere invalide."
                                     " Caracteres valides: '.', 'O', 'T',"
                                     "' ' et 'V'.")

                self.cases_group[x, y] = CaseSprite(self.imgs["bg"], nature,
                                                    true_coords, number)
                x += 1
                number += 1
            y += 1

        print('map crée.')
        print(self.cases_group)

    def init_heroes(self, players):
        """Initialise le héro du joueur."""
        for player in players:
            for case in self.cases_group.sprites():
                if case.number == player[3]:
                    coords = case.coords
                    break

            print("dans sprites. coords = ", coords)
            hero = Hero(
                self.imgs[player[1]],
                coords,
                player[1],
                player[0],
                player[2])
            self.heroes_grp.add(hero)

    def init_pathfinder(self):
        """Init the pathfinder."""
        good_hero = None
        others = []

        for hero in self.heroes_grp.sprites():
            if hero.is_yours:
                good_hero = hero
            else:
                others.append(hero)

        img = self.imgs["paths"][0]
        self.pathfinder = pth.PathfindingGroup(img, good_hero, others)

    def init_transform_paths(self):
        """Init."""
        good_hero = None
        others = []

        for hero in self.heroes_grp.sprites():
            if hero.is_yours:
                good_hero = hero
            else:
                others.append(hero)

        img = self.imgs["paths"][1]
        self.transform_paths = TransformPaths(img, good_hero, others)
