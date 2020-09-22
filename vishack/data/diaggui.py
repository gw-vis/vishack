"""A dtt2hdf wrapper for extracting data from diaggui XML output files
"""

import dtt2hdf
import os

from vishack.logger import logger

class Diaggui:
    """Diaggui class for handling and converting diaggui XML file.

    Parameters
    ----------
    path: string
        The path to the diaggui XML output file.

    Attributes
    ----------
    items: declarative.bunch.bunch.Bunch
        The output from :code:`dtt2hdf.read_diaggui(path)`.
    path: string
        The path to the diaggui XML output file.
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
            self.path = path
    def __str__(self):
        """ Return some useful info.
        """

    def _key_exists(self, *keys):
        base = self.items
        for key in keys:
            if not (key in base.keys()):
                return False
            else:
                base = base[key]
        return True

    def tf(self, channel_a, channel_b, datatype='results'):
        """ Derive transfer function from CSD and PSD from diaggui file.

        Parameters
        ----------
        channel_a: string
            The input channel string.
        channel_b: string
            The output channel string.

        Returns
        -------
        f: array
            The frequency axis of the transfer function.
        tfdata: array
            The transfer function, defined by B/A, in complex numbers.
        """

        f, csddata = self.csd(channel_a=channel_a, channel_b=channel_b)
        _, psda = self.psd(channel_a)
        tfdata = csddata/psda**2

        return(f, tfdata)

    def csd(self, channel_a, channel_b, datatype='results'):
        """ Read cross-PSD from diaggui file.

        Parameters
        ----------
        channel_a: string
            The input channel string.
        channel_b: string
            The output channel string.

        Returns
        -------
        f: array
            The frequency axis of the cross-power sepctral density.
        csddata: array
            The cross-power spectral density, in complex
            numbers.
        """

        if not self._key_exists(datatype, 'CSD', channel_a):
            raise ValueError('channel_a {} not exist'.format(channel_a))
        elif not self._key_exists(
                datatype, 'CSD', channel_a, 'channelB_inv', channel_b):
            raise ValueError('channel_b {} not exist'.format(channel_b))
        channel_b_index = self.items[datatype]['CSD'][channel_a]['channelB_inv'][channel_b]
        f = self.items[datatype]['CSD'][channel_a]['FHz']
        csddata = self.items[datatype]['CSD'][channel_a]['CSD'][channel_b_index]
        return(f, csddata)

    def psd(self, channel, datatype='results'):
        """Read power spectral density from diaggui file

        Parameters
        ----------
        channel: string
            The channel name of the PSD to be read.

        Returns
        -------
        f: array
            The frequency axis of the PSD.
        psddata: array
            The power spectral density.

        Notes
        -----
        The PSD in diaggui is actually amplitude spectral density (ASD), not
        PSD.
        """
        if not self._key_exists(datatype, 'PSD', channel):
            raise ValueError('channel {} not exist'.format(channel))
        f = self.items[datatype]['PSD'][channel]['FHz']
        psddata = self.items[datatype]['PSD'][channel]['PSD'][0]
        return(f, psddata)

    def coh(self, ):
        """ Read coherence from diaggui file.

        Parameters
        ----------
        channel_a: string
            The input channel string.
        channel_b: string
            The output channel string.

        Returns
        -------
        f: array
            The frequency axis of the coherence.
        cohdata: array
            The coherence between `channel_a` and `channel_b`.
        """
        if not self._key_exists(datatype, 'COH', channel_a):
            raise ValueError('channel_a {} not exist'.format(channel_a))
        elif not self._key_exists(
                datatype, 'COH', channel_a, 'channelB_inv', channel_b):
            raise ValueError('channel_b {} not exist'.format(channel_b))
        channel_b_index = self.items[datatype]['COH'][channel_a]['channelB_inv'][channel_b]
        f = self.items[datatype]['COH'][channel_a]['FHz']
        cohdata = self.items[datatype]['COH'][channel_a]['COH'][channel_b_index]
        return(f, cohdata)
