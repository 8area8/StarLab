"""Module qui gère le lancement de la vidéo."""

import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import VideoFileClip


class Movie:
    """Classe qui lance la vidéo."""

    def __init__(self):
        """Initialisation."""
        clip = VideoFileClip('f_roboc/movie/movie.mp4')
        clip.preview(fps=25)
