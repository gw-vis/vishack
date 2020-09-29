"""Library for handling file outputting.
"""

import os
import time


def rename(path, method='utc'):
    """Rename a file by appending something unique before extension.

    Parameters
    ----------
    path: string
        The path of the file to be outputted. With or without extension.
        If it exists, the new file will be renamed before writing so not
        to replace the old one.
    method: string
        The method to rename. Available methods are 'utc' and '123'.

    Returns
    -------
    new_path: string
        The modified path name.
    """

    name, ext = get_name_and_ext(path)
    if method == 'utc':
        new_path = rename_method_utc(name, ext)
    elif method == '123':
        new_path = rename_method_123(name, ext)
    return(new_path)

def get_name_and_ext(path):
    """Get name and extension from a path

    Parameters
    ----------
    path: string
        The path of the file

    Returns
    -------
    name: string
        The name of the file, i.e. everything before the extension
    ext: string
        The extension of the file.
    """

    if len(path.split('.')) >= 2:
        ext = path.split('.')[-1]
        name = path.rstrip('.'+ext)
    else:
        ext = ''
        name = path
    return(name, ext)

def append_to_name(name, ext, appendix=''):
    """Rename the name of the file if it exists

    Parameters
    ----------
    name: string
        The name of the file, i.e. everything before the extension
    ext: string
        The extension of the file.
    appendix: string
        The appendix to append onto the name

    Returns
    -------
    new_path: string
        The modified path name.
    """

    new_path = name+appendix+'.'+ext
    return(new_path)

def rename_method_utc(name, ext):
    """Rename the name of the file by appending the current utc time.

    Parameters
    ----------
    name: string
        The name of the file, i.e. everything before the extension
    ext: string
        The extension of the file.

    Returns
    -------
    new_path: string
        The modified path name.
    """

    new_path = name+'.'+ext
    while os.path.exists(new_path):
        appendix = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        new_path = append_to_name(name, ext, appendix)
    return(new_path)

def rename_method_123(name, ext):
    """Rename the name of the file by appending bracket enclosed number.

    Parameters
    ----------
    name: string
        The name of the file, i.e. everything before the extension
    ext: string
        The extension of the file.

    Returns
    -------
    new_path: string
        The modified path name.
    """

    new_path = name+'.'+ext
    i = 1
    while os.path.exists(new_path):
        appendix = '({})'.format(i)
        i += 1
        new_path = append_to_name(name, ext, appendix)
    return(new_path)
