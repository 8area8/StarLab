"""Game and Game_initiator sprite module."""

import pygame

import constants.game_sizes as csizes

from f_roboc.sprites_classes.game.buttons_menu import BullSprite, TimeSprite
from f_roboc.sprites_classes.game.case_sprite import CaseSprite
from f_roboc.sprites_classes.game.heroes import Hero
from f_roboc.sprites_classes.game.map_sprite import MapSprites
from f_roboc.sprites_classes.game.pathfinder import PathfindingGroup
from f_roboc.sprites_classes.game.Transform_paths import SearchTransformPaths
from f_roboc.sprites_classes.game.others_animations import (NextTurn,
                                                            TransformAnim)


class GameInitSprites:
    """The game initiator sprites class."""

    def __init__(self, images):
        """Initialisation."""

        self.main_surface = pygame.Surface(csizes.SCREEN_SIZE)

        self.background = images[0]


class GameSprites:
    """The game sprites class."""

    def __init__(self, images):
        """Initialization."""
        self.images = images

        self.main_surface = pygame.Surface(csizes.SCREEN_SIZE)

        self.map_surface = pygame.Surface(
            (640 * csizes.UPSCALE, 288 * csizes.UPSCALE),
            pygame.SRCALPHA, 32).convert_alpha()

        self.cases_group = MapSprites()
        self.heroes_grp = pygame.sprite.Group()

        self.menu_blue = self.images["menu"]["super_menu"]
        self.menu_grey = self.images["menu"]["super_menu_grey"]
        self.menu = self.menu_blue

        self.time = TimeSprite(
            self.images["menu"]["time"],
            (274 * csizes.UPSCALE, 284 * csizes.UPSCALE),
            "time")

        self.bull = BullSprite(
            self.images["menu"]["bull"],
            (291 * csizes.UPSCALE, 300 * csizes.UPSCALE),
            "bull")

        self.next_turn = NextTurn(
            self.images["menu"]["next_turn"],
            (13 * csizes.UPSCALE, 20 * csizes.UPSCALE),
            "next_turn")

        self.transform = TransformSprite(
            self.images["menu"]["transform"],
            (189 * csizes.UPSCALE, 306 * csizes.UPSCALE),
            "transform")

        self.transform_anim = TransformAnim(
            self.images["transform"], "transform_anim")

        self.menu_layer_1 = pygame.sprite.Group()
        self.menu_layer_1.add(self.time)

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
                true_coords = x * csizes.CASE_SIZE, y * csizes.CASE_SIZE

                if word == ' ' or word == '.':
                    nature = 'path'
                elif word == 'O':
                    nature = 'wall'
                elif word == 'T':
                    nature = 'teleporter'
                elif word == 'V':
                    nature = 'victory'
                else:
                    raise ValueError("the map contains an invalid caracter."
                                     " valid caracters: '.', 'O', 'T',"
                                     "' ' and 'V'.")

                self.cases_group[x, y] = CaseSprite(self.images["bg"], nature,
                                                    true_coords, number)
                x += 1
                number += 1
            y += 1

        print('map created.')
        print(self.cases_group)

    def init_heroes(self, players):
        """Initialise le héro du joueur."""
        for player in players:
            for case in self.cases_group.sprites():
                if case.number == player[3]:
                    coords = case.coords
                    break

            print("In sprites. Coords = ", coords)
            hero = Hero(
                self.images[player[1]],
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

        img = self.images["paths"][0]
        self.pathfinder = PathfindingGroup(img, good_hero, others)

    def init_transform_paths(self):
        """Init."""
        good_hero = None
        others = []

        for hero in self.heroes_grp.sprites():
            if hero.is_yours:
                good_hero = hero
            else:
                others.append(hero)

        img = self.images["paths"][1]
        self.transform_paths = SearchTransformPaths(img, good_hero, others)
