"""Health check for KAGRA vibration isolation system
"""

import configparser
import dtt2hdf
import os
import xml.etree

from vishack.logger import logger

class HealthCheck:
    """[Unreleased] Various healthcheck methods

    Parameters
    ----------
    config: string
        Path to the config file.

    Attributes
    ----------
    config: configparser.ConfigParser
        The config parser
    config_path: string
        The path to the config file
    paths: list of strings
        A list of paths to the diaggui XML files to be checked.
    """
    def __init__(self, config=None):
        """
        Parameters
        ----------
        config: string
            Path to the config file.
        """

        if not os.path.exists(config):
            raise FileNotFoundError('{} not found.'.format(config))

        self.config = configparser.ConfigParser()
        self.config.read(config)
        self.config_path = config

        if 'General' in self.config.sections():
            general = self.config['General']
            self._output_log = general.getboolean('Output log', fallback=False)
            self._log_dir = general['Log directory']
            if not os.path.exists(self._log_dir):
                logger.info('Log dir {} not exist.'.format(self._log_dir))
            elif not os.path.isdir(self._log_dir):
                raise NotADirectoryError(
                    'log dir {} is not a directory'.format(self._log_dir))

        if 'Directory settings' in self.config.sections():
            dir_set = self.config['Directory settings']
            self._include_subfolder = (
                dir_set.getboolean('Include subfolders', fallback=False))

        if 'Directories' in self.config.sections():
            self._directories = list(self.config['Directories'].values())
            for directory in self._directories:
                if not os.path.isdir(directory):
                    logger.warning(
                        '{} is not a directory. Ignoring'.format(directory))
                    self._directories.remove(directory)

        self.paths = []
        if self._include_subfolder:
            for directory in self._directories:
                for (root, _, files) in os.walk(directory):
                    for file in files:
                        path = os.path.join(root, file)
                        self._try_read_diaggui(path)
        else:
            for directory in self._directories:
                for file in os.listdir(directory):
                    path = os.path.join(directory, file)
                    self._try_read_diaggui(path)

        if 'Paths' in self.config.sections():
            for path in list(self.config['Paths'].values()):
                self._try_read_diaggui(path)

        self._remove_duplicated_paths()

    def _try_read_diaggui(self, path):
        try:
            dtt2hdf.read_diaggui(path)
            self.paths.append(path)
        except xml.etree.ElementTree.ParseError:
            logger.warning(
                '{} is not a diaggui XML file.'\
                ' Ignoring...'.format(path))
        except IsADirectoryError:
            logger.warning('{} is a directory. Ignoring...'\
                ''.format(path))
        except FileNotFoundError:
            logger.warning('{} not exist. Ignoring...'.format(path))

    def _remove_duplicated_paths(self):
        self.paths.reverse()
        for path in self.paths:
            if self.paths.count(path) > 1:
                logger.warning('Duplicated path {} removed'.format(path))
                self.paths.remove(path)
        self.paths.reverse()
