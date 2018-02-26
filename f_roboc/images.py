"""This module repeats all the game's pictures."""

import os
import pygame

import constants.game_sizes as cst


def _upscale_the(image):
    """Upscale an return an image."""
    upscale = cst.UPSCALE
    w, h = image.get_size()

    upscaled_size = ((w * upscale), (h * upscale))
    upscaled_image = pygame.transform.scale(image, upscaled_size)

    return upscaled_image


def _create_image(path):
    """Create and return a pygame image from a path.

    if the upscale variable of the constant module is greater than 1,
    then we upscale the image.
    """
    image = pygame.image.load(path).convert_alpha()

    if cst.UPSCALE > 1:
        image = _upscale_the(image)

    return image


def _try_only_files_or_folders_in(folder):
    """Test wether the folder contain only files OR only folders.

    return 'folders' if the folder contains only folders.
    return 'files' if the folder contains only files.
    raise an error if the folder contains a mixt of both.
    return 'empty' if the folder is empty.
    """
    must_contain = "empty"
    error_message = ("The current folder contains 1+ folder(s) "
                     "AND 1+ file(s)!\n"
                     "each folder must contain "
                     "only files OR folders.")

    for path in os.listdir(folder):
        path = folder + path

        if os.path.isdir(path):
            if must_contain == "empty":
                must_contain = "folders"
            elif must_contain == "files":
                raise ValueError(error_message)

        else:
            if must_contain == "empty":
                must_contain = "files"
            elif must_contain == "folders":
                raise ValueError(error_message)

    return must_contain


def get_content_of(folder):
    """Return: a dict who contain some folders, or a list of images.

    Note: each folder from this folder must contain only images.
    otherwise, an exception will be thrown by pygame.
    """
    contain = _try_only_files_or_folders_in(folder)
    content = None

    if contain == 'folders':
        content = {}
        for path in os.listdir(folder):
            new_folder = folder + path + '/'
            content[path] = get_content_of(new_folder)

    elif contain == 'files':
        content = []
        for path in os.listdir(folder):
            image_path = folder + path
            image = _create_image(image_path)
            content.append(image)

    elif contain == 'empty':
        pass

    else:
        raise ValueError("'contain' must be 'folders', 'files' or 'empty'.\n"
                         "Actually contain is: {}".format(contain))

    return content


def create_moove_r_images(l_moove_folder):
    """Create the moove_r images from the moove_l folder.

    return  a new list with images of moove_l folder horizontaly splitted.
    """
    r_moove_list = []

    for image in l_moove_folder:
        r_moove_list.append(pygame.transform.flip(image, True, False))

    return r_moove_list


def find_characters_and_create_their_moove_r_folder(base_folder):
    """Find all characters in a folder and create their moove_r folder.

    We works on a mutable object (a dict),
    so we don t have to return anything.
    """
    for name, folder in base_folder.items():

        if name == "characters":
            characters_folder = folder

            for hero in characters_folder.values():
                hero['moove_r'] = create_moove_r_images(hero['moove_l'])

            return

        elif isinstance(folder, dict):
            find_characters_and_create_their_moove_r_folder(folder)
