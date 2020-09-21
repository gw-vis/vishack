"""Library for data comparison
"""

import numpy as np

def tf(tf1, tf2, weight=None):
    """Calculate weighted residue between two transfer function data

    Parameters
    ----------
    tf1: array of complex
        The transfer function data, assumed to have same length and frequency
        axis with the reference trasnfer function data *tf2*.
    tf2: array of complex
        The reference transfer function to be compared with. Same length and
        frequency axis with the reference trasnfer function data *tf1*.
    weight: array-like, optional
        The weighting function. If set to :code:`None`, it will be set ones.

    Returns
    -------
    residue: float
        The weighted residue (see Note)

    Note
    ----
    The residue is defined as :code:`np.sum((np.abs((tf1-tf2)*weight))**2)`

    For health checking, it is recommanded to set tf1 to the data to be
    checked,
    *tf2* to be the reference data, and weight to the inverse of the reference
    data times the coherence of *tf2*.
    """

    residue = np.sum(np.abs((tf1-tf2) * weight)**2)
    return(residue)
