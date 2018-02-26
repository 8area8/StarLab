"""This modules manages the launch of the movie."""

import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import VideoFileClip


def play_video():
    """Play the cinematic."""
    clip = VideoFileClip('f_roboc/introduction/movie.mp4')
    clip.preview(fps=25)
