"""This module contains the main class of all sprites classes."""

import pygame


class MainSprite(pygame.sprite.Sprite):
    """The first main class of all others sprite's classes.

    Contains a lot of preconfigured methods.
    """

    def __init__(self, no_images=False):
        """Initialize the class."""
        super().__init__()

        # NAME
        self.name = NotImplemented

        # IMAGES
        self.image = NotImplemented
        if not no_images:
            self.images = None
        self._no_image = pygame\
            .Surface([1, 1], pygame.SRCALPHA, 32)\
            .convert_alpha()

        # BUTTON'S IMAGES
        self._active_image = None
        self._passive_image = None
        self._broken_image = None

        self._image_copy = None
        self._second_image = None

        # POSITION
        self.coords = (0, 0)
        # CALL _INIT_RECT_POSITION NOW

        # INDEX
        self._index = 0
        self._current_time = 0.0
        self._ping_pong = 'ping'
        self._images_max_time = None

        # ACTIVATION
        self._activated_animation = False
        self.activated = False

    @property
    def overflew(self):
        """Return True if the mouse is over the sprite."""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    @property
    def timer(self):
        """Return _current_time, but it's more elegant."""
        return self._current_time

    def _init_rect_position(self):
        """Initialize the rect position of the sprite.

        !! You have to call it in the __init__ method !!
        """
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coords

    def _refresh_timer(self, set_zero=False):
        """Refresh the timer."""
        if set_zero:
            self._current_time = 0.0
        else:
            self._current_time += 33.4

    def _call_method_after_timer(self, method, max_timer=100,
                                 *args, **kwargs):
        """Call a method if timer is greater (or equal) than max_timer.

        If it is, we set the timer to 0.

        TIP: '*arg' and '**kwargs' are method's arguments.
        """
        self._refresh_timer()
        if self.timer >= max_timer:
            self._refresh_timer(set_zero=True)
            method(*args, **kwargs)

    def _set_ascending_index_loop(self):
        """Set an ascending index loop.

        Every call, index increases by 1,
        and return to 0 if it's equal to images lenght.
        """
        self._index = (self._index + 1) % len(self.images)

    def return_len_images(self):
        """Simply return len of self.images."""
        return len(self.images) - 1

    def _set_ping_pong_index(self, len_img=None):
        """Set a 'ping pong' index.

        It's a loop:
        - index increases by 1 if it's lower than images lenght,
        - then index decrease by 1 if it's greater than 0.
        """
        if not len_img:
            len_img = self.return_len_images()

        if self._ping_pong == 'ping':

            if self._index == len_img:
                self._ping_pong = 'pong'
            else:
                self._index += 1

        else:

            if self._index == 0:
                self._ping_pong = 'ping'
            else:
                self._index -= 1

    def activate(self):
        """Active the sprite."""
        self._index = 0
        self._current_time = 0.0
        self._activated_animation = True
        self.activated = True

    def desactivate(self):
        """Desactivates the sprite."""
        self._index = 0
        self.image = self._no_image
        self._activated_animation = False
        self.activated = False

    def _update_image_from_images(self):
        """Update the current image according to the index."""
        self.image = self.images[self._index]

    def _change_image_if_overflew(self):
        """Activate the sprite if the mouse is over it."""
        if self.overflew:
            if self.image is not self._active_image:
                self.image = self._active_image
        else:
            if self.image is not self._passive_image:
                self.image = self._passive_image

    def _add_image_to_the_background(self, coords):
        """Add a new image to the first image."""
        if self._image_copy != self.image:
            self._image_copy = pygame.surface.copy(self.image)

        self._image_copy.blit(self._second_image, coords)


class Button(MainSprite):
    """Simple application for buttons."""

    def __init__(self, active_image, passive_image, coords, name):
        """Initialize the class."""
        super().__init__()

        self.name = name

        self.image = active_image
        self._active_image = active_image
        self._passive_image = passive_image

        self.coords = coords
        self._init_rect_position()

    def adjust_rect_position(self, coords):
        """Use it if the button is a subsprite."""
        x, y = coords
        a, b = self.coords
        a += x
        b += y
        self.rect.x = a
        self.rect.y = b

    def update(self, *arg):
        """Update the sprite."""
        self._change_image_if_overflew()


class ButtonPlusClick(Button):
    """Application for button who has an animation if we click on.

    to use it:
        - set the 'activated' attribut to 'True' in events,
          if a player click on it.
    """

    def __init__(self, pushed_image, active_image, passive_image,
                 coords, name, max_timer=400):
        """Initialize the class."""
        super().__init__(active_image, passive_image, coords, name)

        self._pushed_image = pushed_image
        self._max_timer = max_timer

    def update(self):
        """Update the sprite."""
        if self.activated:
            self.image = self._pushed_image
            self._call_method_after_timer(self.desactivate, self._max_timer)
        else:
            self._change_image_if_overflew()

    def desactivate(self):
        """Desativate the activated variable."""
        self.activated = False


class ButtonGame(ButtonPlusClick):
    """Button plus click, plus animated passive image and broken image.

    To use it:
        - update the sprite (or the sprite group),
          with the 'active_turn' parameter.
        - set the 'activated' attribut to 'True' in events,
          if a player click on it.
    """

    def __init__(self, pushed_image, active_image, passive_images,
                 broken_image, coords, name, max_timer=100):
        """Initialize the class."""
        super().__init__(pushed_image, active_image, None,
                         coords, name, max_timer)

        self.images = passive_images
        self._broken_image = broken_image
        self.image = self.images[self._index]
        self._maxi_timer = max_timer

    def update(self, active_turn):
        """Update the sprite.

        The sprite has 4 forms:
            - the animated passive form, in your active turn.
            - the active form, in your active turn if overflew.
            - the clicked form, quick form if you click on it.
            - the broken form, if it s not your active turn.
        """
        if self.activated:
            self.image = self._pushed_image
            self._call_method_after_timer(self.desactivate)
            return

        if not active_turn:
            self.image = self._broken_image
            return

        self._refresh_timer()
        if self._current_time >= self._maxi_timer:
            self._refresh_timer(set_zero=True)
            self._set_ping_pong_index()

        if self.overflew:
            self.image = self._active_image
        else:
            self.image = self.images[self._index]
