"""Handling health check config files
"""

import configparser
import os

from vishack.logger import logger

def generate_sample_config(name='sample_config.ini', overwrite=False):
    """Generate a sample health check config

    Parameters
    ----------
    name: string, optional
        Name of the output file.
    overwrite: boolean, optional
        Overwrite the sample_config.ini in the current directory.
        If False, a sample config will still be generated. But a number will
        be appended before the :code:`.ini` extension.
    """

    config = configparser.ConfigParser()

    config['General'] = {
        'Output log':'false',
        'Log directory':'path/to/log/directory'
    }

    config['Directory settings'] = {
        'Include subfolders':'false',
    }

    config['Directories'] = {
        'BS':'path/to/bs/xml/directory',
        'ITMY':'path/to/itmy/xml/dirctory',
    }

    config['Paths'] = {
        'BS_TM_L':'path/to/BS/BS_TM_L.xml',
        'this can be anything':'path/to/any/abc.xml',
    }

    config['Coherence'] = {
        'check':'false',
        'methods':'MSE,WMSE, MAE, WMAE, RMS, WRMS'
    }

    config['Power spectral density'] = {
        'check':'false',
        'methods':'MSE, WMSE, MAE, WMAE, RMS, WRMS'
    }

    config['Transfer function'] = {
        'check':'false',
        'methods':'MSE, WMSE, MAE, WMAE, RMS, WRMS'
    }

    i = 1
    if len(name.split('.')) == 2:
        ext = '.'+name.split('.')[1]
        name = name.split('.')[0]
    else:
        ext = ''

    path = name + ext
    if os.path.exists(path):
        logger.info('{} exists in the current directory'.format(path))
        if not overwrite:
            logger.info('overwrite is False. Renaming the sample config.')
            while os.path.exists(path):
                new_name = name + '({})'.format(i)
                path = new_name+ext
                i += 1
        else:
            logger.info('overwrite is True.')

    logger.info('Writing the sample config file to {}.'.format(path))
    with open(path, 'w') as configfile:
        config.write(configfile)
