"""Evaluate statistical quantities from frequency series.
"""

import numpy as np

def wrms(data, df=1., whitening=None):
    """Whiten the data and calcuate the expected root-mean-square value.

    Parameters
    ----------
    data: array
        The data to be evaluated.
    df: float, optional
        The frequency spacing between data points. Default to be 1.
    whitening: array, optional
        The whitening/weighting function. If None, default to be ones.


    Returns
    -------
    float
        The whitened expected RMS.

    Note
    ----
    Complex arrays are accepted. Absolute values will be taken after whitening.
    If the data is an amplitude spectral density, then the output will be
    the expected RMS. If the data is a transfer function, then the output
    will be the 2-norm.
    """

    data = np.array(data[1:])

    if whitening is None:
        whitening = np.ones(len(data))
    else:
        whitening = np.array(whitening[1:])

    wdata = np.abs(data*whitening)
    wrms_ = np.sqrt(np.sum(wdata**2*df))

    return(wrms_)

def rms(data, df=1.):
    """ Calculated the expected root-mean-square value from the data

    Parameters
    ----------
    data: array
        The data to be evaluated
    df: float, optional
        The frequency spacing between data points. Default to be 1.

    Returns
    -------
    float
        The expected RMS.

    Note
    ----
    Complex arrays are accepted. Absolute values will be taken after whitening.
    If the data is an amplitude spectral density, then the output will be
    the expected RMS. If the data is a transfer function, then the output
    will be the 2-norm.
    """

    return(wrms(data=data, df=df))

def wmse(data, reference):
    """Mean-square-error between the whitened data and reference data.

    Parameters
    ----------
    data: array
        The data to be evaluted
    reference: array
        The reference data.

    Returns
    -------
    float
        The mean-square-error between the data and the reference whitened
        by the inverse of the reference.
    """

    data = np.array(data[1:])
    reference = np.array(reference[1:])
    werror = np.abs((data-reference)/reference)
    wmse_ = np.mean(werror**2)
    return(wmse_)

def mse(data, reference):
    """Mean-square-error between the data and reference data.

    Parameters
    ----------
    data: array
        The data to be evaluted
    reference: array
        The reference data.

    Returns
    -------
    float
        The mean-square-error between the data and the reference.
    """

    data = np.array(data[1:])
    reference = np.array(reference[1:])
    error = np.abs((data-reference))
    print(error)
    mse_ = np.mean(error**2)
    return(mse_)

def wmae(data, reference):
    """Maximum absolute error between the whitened data and the reference

    Parameters
    ----------
    data: array
        The data to be evaluted
    reference: array
        The reference data.

    Returns
    -------
    float
        The maximum absolute error between the data and the reference whitened
        by the inverse of the reference.
    """

    data = np.array(data[1:])
    reference = np.array(reference[1:])
    werror = np.abs((data-reference)/reference)
    wmae_ = np.max(werror)
    return(wmae_)

def mae(data, reference):
    """Maximum absolute error between the data and the reference

    Parameters
    ----------
    data: array
        The data to be evaluted
    reference: array
        The reference data.

    Returns
    -------
    float
        The maximum absolute error between the data and the reference
    """

    data = np.array(data[1:])
    reference = np.array(reference[1:])
    error = np.abs((data-reference))
    mae_ = np.max(error)
    return(mae_)
