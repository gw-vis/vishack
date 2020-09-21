"""A dtt2hdf wrapper for extracting data from diaggui XML output files
"""

import dtt2hdf
import os

from vishack.logger import logger

class Diaggui:
    """Diaggui class for handling and converting diaggui XML file

    Parameters
    ----------
    path: string
        The path to the diaggui XML output file.x

    Attributes
    ----------
    items: declarative.bunch.bunch.Bunch
        The output from :code:`dtt2hdf.read_diaggui(path)`
    """

    def __init__(self, path):
        """Initial Diaggui class with a diaggui XML file

        Parameters
        ----------
        path: string
            The path to the diaggui XML output file.
        """

        if not os.path.exists(path):
            self.items = None
            raise FileNotFoundError(
                "Path {} doesn't exist.".format(path))
        else:
            self.items = dtt2hdf.read_diaggui(path)
