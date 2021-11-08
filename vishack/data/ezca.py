"""Easy channel access (EZCA) utilities."""
import datetime
import time

import numpy as np


def parallel_time_average(ezca, channels, duration=1., fs=None):
    """Read process variables channels and returns a dict of time averages
    
    Parameters
    ----------
    ezca : ezca.ezca.Ezca
        Ezca instance.
    channels : list of str
        The channels to be read.
    duration : float, optional
        The duration (s).
        Defaults to 1 second.
    fs : float, optional
        Sampling frequency (s).
        Note, the sampling frequency of EPICS slow channels
        is maximum at 8 Hz.
        If None, will read as fast as it can.
        Defaults None.

    Returns
    -------
    dict
        A dictionary with channel names as the keys and the time average as
        the value.
    """
    d_time_series = parallel_time_series(
        ezca=ezca, channels=channels, duration=duration, fs=fs)
    d_time_average = {}
    for key in d_time_series.keys():
        if key == "t":
            continue
        d_time_average[key] = np.mean(d_time_series[key])
    return d_time_average


def parallel_read(ezca, channels):
    """Read channels values and returns a dict of values in the EPICS record.

    Parameters
    ----------
    ezca : ezca.ezca.Ezca
        Ezca instance.
    channels : list of str
        The channels to the read

    Returns
    -------
    dict
        A dictionary with channel names as the key and time-series as
        the value.
    """
    d = {}
    for channel in channels:
        d[channel] = ezca.read(channel)
    return d

def parallel_time_series(ezca, channels, duration=1., fs=None):
    """Read channels time-series and returns of dict of time-series.

    Parameters
    ----------
    ezca : ezca.ezca.Ezca
        Ezca instance.
    channels : list of str
        The channels to be read.
    duration : float, optional
        The duration (s).
        Defaults to 1 second.
    fs : float, optional
        Sampling frequency (s).
        Note, the sampling frequency of EPICS slow channels
        is maximum at 8 Hz.
        If None, will read as fast as it can.
        Defaults None.

    Returns
    -------
    dict
        A dictionary with channel names as the keys and time-series as the
        values.
    """
    if fs is None:
        fs = np.inf
    d_values = {}
    d_time_series = {}
    t = np.arange(0, duration, 1/fs)
    d_time_series["t"] = t
    for i in range(len(t)):
        d_values = parallel_read(ezca=ezca, channels=channels)
        time_next = datetime.datetime.now()+ datetime.timedelta(seconds=1/fs)
        for key in d_values.keys():
            if key not in d_time_series.keys():
                d_time_series[key] = np.zeros_like(t)
            d_time_series[key][i] = d_values[key]
        while datetime.datetime.now() < time_next:
            time.sleep(1/fs/100)
    return d_time_series

