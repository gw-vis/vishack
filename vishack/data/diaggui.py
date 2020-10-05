"""A dtt2hdf wrapper for extracting data from diaggui XML output files
"""

import dtt2hdf
import os
import vishack.data.diag

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
        pass

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

    def psd(self, channel_a, datatype='results'):
        """Read power spectral density from diaggui file

        Parameters
        ----------
        channel_a: string
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

        if not self._key_exists(datatype, 'PSD', channel_a):
            raise ValueError('channel_a {} not exist'.format(channel_a))
        f = self.items[datatype]['PSD'][channel_a]['FHz']
        psddata = self.items[datatype]['PSD'][channel_a]['PSD'][0]
        return(f, psddata)

    def coh(self, channel_a, channel_b, datatype='results'):
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
        cohdata = self.items[datatype]['COH'][channel_a]['coherence'][channel_b_index]
        return(f, cohdata)

    def get_reference(self, index):
        """Read a reference plot from the diaggui XML file

        Parameters
        ----------
        index: int
            The index of the reference plot in the diaggui XML

        Returns
        -------
        dict
            A dictionary with various useful info about the reference.

        Note
        ----
        The dict is taken from
        dtt2hdf.read_diaggui().references[index].
        Useful keys are 'type_name', 'channelA', 'channelB', 'channelB_inv',
        'df', 'FHz', 'xfer', 'PSD', 'CSD', 'coherence'.

        Example
        -------
        Here, reference #0 is the transfer function from BS_TM_L to BS_TM_L.

        .. code:: python

           In[0]:
            import vishack.data.diaggui
            dg = vishack.data.diaggui.Diaggui(path='data/BS_TML_exc_20200730a.xml')
            dg.reference_dict(0)

        .. code:: python

           Out[0]:
            {'gps_second': 1238215044.0078125,
             'subtype_raw': 0,
             'f0': 0.0,
             'df': 0.0078125,
             'BW': 0.0117187,
             'window_raw': 1,
             'window': 'Hanning',
             'avgtype_raw': 0,
             'avgtype': 'Fixed',
             'averages': 1,
             'channelA': 'K1:VIS-BS_TM_LOCK_L_EXC',
             'channelB': array(['K1:VIS-BS_TM_OPLEV_LEN_DIAG'], dtype='<U27'),
             'channelB_inv': {'K1:VIS-BS_TM_OPLEV_LEN_DIAG': 0},
             'subtype': 'transfer function B/A in format (Y)',
             'type_name': 'TF',
             'xfer': array([[ 2.0319992e-03+0.0000000e+00j,  1.5529208e-03+1.4785477e-03j,
                      9.0984150e-04+1.8886093e-03j, ...,
                      1.1092599e+27-2.3797619e+08j,  5.5111208e-08-2.0454582e-04j,
                     -4.4841594e-35-4.2907759e-42j]], dtype=complex64)}
        """

        return(dict(self.items.references[index]))

    def get_results(self, type_name):
        """Return the results of a particular type from the diaggui XML file.

        Parameters
        ----------
        type_name: string
            The type of results. 'TF', 'COH', 'CSD', or 'PSD'.

        Returns
        -------
        dict
            A dictionary with all the results with key being the channelA
            string.
        """

        # For some reason diaggui doesn't store transfer functions as 'TF' in
        # results, but only in references. So we have to infer from 'CSD'.
        if type_name == 'TF':
            type_name = 'CSD'

        if type_name in self.items.results:
            return(self.items.results[type_name])
        else:
            raise ValueError('The file {} does not contain {} results.'\
                ''.format(self.path, type_name))

    def measure(self):
        """Measure new results using the diaggui XML file.
        """
        vishack.data.diag.run_measurement(
            path=self.path,
            saveas=None,
            remove_tmp=True
        )
        logger.info("Measurement function not ready, skipping.")
        pass
