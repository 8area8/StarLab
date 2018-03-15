"""HUB Module of the game part."""

import pygame

import constants.find as csfind
from f_roboc.interface import Interface
from f_roboc.game.event import EventsController
from f_roboc.game.sprites import GameSprites


class Game(Interface):
    """The game client class.

    Manages the game part.
    """

    def __init__(self, images, connection, players, _map, turn_digit):
        """Initialization of the class."""
        super().__init__()

        # GAME'S MAP
        self._map = _map

        # CONNECTION INFORMATIONS
        self.connection = connection
        self.msg = ""

        # GAME INFORMATIONS
        self.turn_digit = turn_digit
        self.in_action = False

        # SPRITES INITIALIZATION.
        self.sprt = GameSprites(images)
        self.sprt.create_map(self._map)
        self.sprt.init_heroes(players)
        self.sprt.init_pathfinder()
        self.sprt.init_transform_paths()

        # EVENT OBJECTS
        self._events = EventsController(self)

        self.active_player.activate_skills()

    @property
    def active_player(self):
        """Return the active player."""
        for hero in self.sprt.heroes_grp:
            if hero.digit == self.turn_digit:
                return hero
        raise ValueError("The turn's digit doesn't correspond to any hero!")

    @property
    def my_hero(self):
        """Return your hero."""
        for hero in self.sprt.heroes_grp:
            if hero.is_yours:
                return hero

    @property
    def active_turn(self):
        """Return the active turn."""
        if self.my_hero.digit == self.turn_digit:
            return True
        else:
            return False

    def transfer_datas(self):
        """Unused."""
        return

    @Interface._secured_connection
    def start_events(self, event, mouse):
        """Events call."""
        self._events.start(event, mouse)

        # We now send the message.
        self.connection.send(self.msg)
        self.msg = ''

    @Interface._secured_connection
    def update(self):
        """Recept and process the datas."""
        msg = self.connection.receive()

        self._show_moove_or_transform()
        self.sprt.moove_digit.define_text(text=str(self.my_hero.actual_moove))

        if self.active_turn:
            self.sprt.menu = self.sprt.menu_blue
        else:
            self.sprt.menu = self.sprt.menu_grey

        if "time:" in msg:
            self._update_time(msg)
        if "transform:" in msg:
            self._update_transform(msg)
        if "moove" in msg:
            self._update_moove(msg)

        self.sprt.cases_group.update()
        self.sprt.menu_layer_2.update(self.active_turn)
        self.sprt.heroes_grp.update()

    def _update_time(self, msg):
        """Update time and turns."""
        number = csfind.find_number_after("time:", msg)
        self.sprt.time.choose_index(number, self.active_turn)

        if "next_turn" in msg:
            self.turn_digit = csfind.find_number_after("next_turn:", msg)
            self.sprt.next_turn.activate()
            self.active_player.activate_skills()

    def _update_transform(self, msg):
        """Update the transform action."""
        if "transform: activated" in msg:
            self.in_action = True
            self.active_player.define_key_images("transform")
            coords = csfind.find_and_get_coords_after("coords:", msg)
            self.sprt.transform_anim.define_coords(coords)

        elif "index:" in msg:
            index = csfind.find_number_after("index:", msg)
            self.sprt.transform_anim.play_animation(index=index)

        if "transfNow:" in msg:
            coords = csfind.find_and_get_coords_after('transfNow:', msg)
            self.sprt.cases_group[coords].transform()

        if "end" in msg:
            self.in_action = False
            self.sprt.transform_anim.play_animation(end=True)
            self.active_player.define_key_images("breath")

    def _update_moove(self, msg):
        """Update the moove action."""
        if "end" in msg:
            self.in_action = False
            self.active_player.define_key_images("breath")
        else:
            self.in_action = True
            coords = csfind.find_and_get_coords_after("moove:", msg)
            self.active_player.moove(coords)

    def _show_moove_or_transform(self):
        """Show the moove cases or transform cases."""
        if self.active_turn and not self.in_action:
            if self._events.transform_vision:
                self.sprt.transform_paths.show_possibles_cases(
                    self.sprt.cases_group)
            else:
                self.sprt.transform_paths.empty()
                self.sprt.pathfinder.active_the_pathfinding(
                    pygame.mouse.get_pos(), self.sprt.cases_group)
        else:
            self.sprt.pathfinder.empty()
            self.sprt.transform_paths.empty()

    def draw(self):
        """Sprites drawing."""
        self.sprt.cases_group.draw(self.sprt.map_surface)
        self.sprt.heroes_grp.draw(self.sprt.map_surface)
        self.sprt.pathfinder.draw(self.active_turn, self.sprt.map_surface)
        self.sprt.transform_paths.draw(self.active_turn, self.sprt.map_surface)
        self.sprt.main_surface.blit(self.sprt.map_surface, (0, 0))

        self.sprt.main_surface.blit(self.sprt.menu, (0, 0))
        self.sprt.menu_layer_1.draw(self.sprt.main_surface)
        self.sprt.menu_layer_2.draw(self.sprt.main_surface)
