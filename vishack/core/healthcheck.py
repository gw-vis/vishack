"""Health check for KAGRA vibration isolation system
"""

import configparser
import dtt2hdf
import numpy as np
import os
import xml.etree
import vishack.data.diaggui
import vishack.data.output
import vishack.core.evaluate

from vishack.logger import logger

default_header = '*This report is automatically generated by VISHack*\n\n'
rst_content_string = '.. contents::\n   :depth: 4\n\n'

class HealthCheck:
    """Config driven health check class.

    Parameters
    ----------
    config: string
        Path to the config file.

    Attributes
    ----------
    alert: dict
        Some alarming results from the report.
    checklist: dict
        A dictionary of tests checklist
    config: configparser.ConfigParser
        The config parser
    config_path: string
        The path to the config file
    paths: list of strings
        A list of paths to the diaggui XML files to be checked.
    report_header: string
        The report message of the health check
    report: dict
        The report of the health check
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

        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.optionxform = str
        self.config.read(config)
        self.config_path = config

        if 'General' in self.config.sections():
            general = self.config['General']
            self._output_report = general.getboolean('Output report', fallback=False)
            if self._output_report:
                self._report_path = general['Report path']
                self._overwrite_report = general.getboolean('Overwrite report', fallback=False)
            self.alert_threshold = general.getfloat('Alert threshold', fallback=3)

        if 'Directory settings' in self.config.sections():
            dir_set = self.config['Directory settings']
            self._include_subfolder = (
                dir_set.getboolean('Include subfolders', fallback=False))

        if 'Directories' in self.config.sections():
            self._directories = list(self.config['Directories'].keys())
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
            for path in list(self.config['Paths'].keys()):
                self._try_read_diaggui(path)

        self._remove_duplicated_paths()

        typelist = [
            'Transfer function',
            'Power spectral density',
            'Coherence',
            ]
        self.checklist = {}
        for type in typelist:
            self.checklist[type] = {}
        for type in typelist:
            if type in self.config.sections():
                self.checklist[type]['check'] = self.config[type].getboolean('check', fallback=False)
                self.checklist[type]['methods'] = self.config[type]['methods'].replace(' ', '').split(',')

        self.report_header = default_header
        self.report_header += 'Configuration:\n{}'.format(self.config_path)+'\n\n'
        self.report_header += 'Diaggui XML files:\n\n'
        for path in self.paths:
            self.report_header += path + '\n\n'
        self.report_header += rst_content_string
        self.report = {}
        self.alert = {}

    def check(self,
            new_measurement=False,
            typelist=[
                'Transfer function',
                'Power spectral density',
                'Coherence']):
        """Perform health checks.

        Paramters
        ---------
        new_measurement: boolean, optional.
            Trigger new measurement using the diaggui XML file.
            Default False.
        typelist: list of string, optional.
            The type of checks to be performed.
            Defaults to check all transfer functions, power spectral density,
            and coherence in the diaggui XML file.

        Returns
        -------
        report: dict
            The health check report.

        Note
        ----
        Specifying the type of checks here will not override the specification
        in the configuration file. If you wish to perform a particular type
        of tests, you must specify in the configuration file as well as
        specifying here.
        """

        self.report = {}
        id = 0

        for path in self.paths:

            self.report[path] = {}

            dg = vishack.data.diaggui.Diaggui(path)
            if new_measurement:
                dg.measure()

            for type in typelist:
                if type in self.checklist.keys():
                    if self.checklist[type]['check']:

                        self.report[path][type] = {}

                        methods = self.checklist[type]['methods']
                    else:
                        continue
                    if type == 'Transfer function':
                        type_name = 'CSD'
                        reference_key = 'xfer'
                    elif type == 'Power spectral density':
                        type_name = 'PSD'
                        reference_key = 'PSD'
                    elif type == 'Coherence':
                        type_name = 'COH'
                        reference_key = 'coherence'
                else:
                    logger.error('Unknown type {}. Ignoring...'\
                        ''.format(type))
                    continue

                ref_index_list = list(dg.items.references.keys())
                results = dg.get_results(type_name)
                for channel_a in results.keys():
                    if 'channelB' in results[channel_a]:
                        for channel_b in results[channel_a]['channelB']:
                            matching_index = []
                            # See if any references matches the type and channels
                            for ref_index in ref_index_list:
                                ref_dict = dg.get_reference(ref_index)
                                if reference_key in ref_dict.keys():
                                    if ref_dict['channelA'] == channel_a:
                                        if channel_b in ref_dict['channelB']:
                                            matching_index.append(ref_index)

                            # We don't compare if the number of references
                            # is smaller than 2.
                            if len(matching_index) < 2:
                                continue

                            # If it matches, then we don't check it next time.
                            for index in matching_index:
                                ref_index_list.remove(index)

                            self.report[path][type][id] = {}
                            self.report[path][type][id]['References'] = matching_index

                            if type == 'Transfer function':
                                f, result_data = dg.tf(channel_a, channel_b)
                                result_data = result_data.conjugate()
                            elif type == 'Power spectral density':
                                f, result_data = dg.psd(channel_a)
                                print('If you see this message,'\
                                    ' something went wrong.')
                            elif type == 'Coherence':
                                f, result_data = dg.coh(channel_a, channel_b)

                            ref_data = [dg.get_reference(index)[reference_key][0]
                                for index in matching_index]

                            df = dg.get_results(type_name)[channel_a]['df']

                            self.report[path][type][id]['Channel A'] = channel_a
                            self.report[path][type][id]['Channel B'] = channel_b

                            for method in methods:
                                data_mean, _ = self.data_evaluate(
                                    result_data, ref_data, method=method,
                                    df=df)
                                ref_mean, ref_std = self.reference_evaluate(
                                    ref_data, method=method, df=df)

                                self.report[path][type][id][method] = {}
                                self.report[path][type][id][method]['Reference mean'] = ref_mean
                                self.report[path][type][id][method]['Reference standard deviation'] = ref_std
                                self.report[path][type][id][method]['Result (raw)'] = data_mean
                                self.report[path][type][id][method]['Result (sigma)'] = (data_mean-ref_mean) / ref_std

                            id += 1

                    else:
                        matching_index = []
                        # See if any references matches the type and channels
                        for ref_index in ref_index_list:
                            ref_dict = dg.get_reference(ref_index)
                            if reference_key in ref_dict.keys():
                                if ref_dict['channelA'] == channel_a:
                                    matching_index.append(ref_index)

                        # We don't compare if the number of references
                        # is smaller than 2.
                        if len(matching_index) < 2:
                            continue

                        # If it matches, then we don't check it next time.
                        for index in matching_index:
                            ref_index_list.remove(index)

                        self.report[path][type][id] = {}
                        self.report[path][type][id]['References'] = matching_index

                        if type == 'Transfer function':
                            f, result_data = dg.tf(channel_a, channel_b)
                        elif type == 'Power spectral density':
                            f, result_data = dg.psd(channel_a)
                        elif type == 'Coherence':
                            f, result_data = dg.coh(channel_a, channel_b)

                        ref_data = [dg.get_reference(index)[reference_key][0]
                            for index in matching_index]

                        df = dg.get_results(type_name)[channel_a]['df']

                        self.report[path][type][id]['Channel A'] = channel_a

                        for method in methods:
                            data_mean, _ = self.data_evaluate(
                                result_data, ref_data, method=method,
                                df=df)
                            ref_mean, ref_std = self.reference_evaluate(
                                ref_data, method=method, df=df)

                            self.report[path][type][id][method] = {}
                            self.report[path][type][id][method]['Reference mean'] = ref_mean
                            self.report[path][type][id][method]['Reference standard deviation'] = ref_std
                            self.report[path][type][id][method]['Result (raw)'] = data_mean
                            self.report[path][type][id][method]['Result (sigma)'] = (data_mean-ref_mean) / ref_std

                        id += 1

        self.get_alerts(threshold=self.alert_threshold)
        if self._output_report:
            self.print_report(
                path=self._report_path,
                overwrite=self._overwrite_report)
        return (self.report)

    def get_alerts(self, threshold=3):
        """ Store alerting results from report

        Parameters
        ----------
        threshold: float, optional.
            Alert results when the mean of the result is higher than this
            threshold, which has a unit of sigma.
            Defaults to 3. (3 sigma encloses 99.7% of the cases)

        Returns
        -------
        alert: dict
            Some alerting results from the health check report.
        """

        self.alert = {}
        alert = False
        for path in self.report.keys():
            for type in self.report[path].keys():
                for id in self.report[path][type].keys():
                    for method in self.report[path][type][id].keys():
                        if isinstance(self.report[path][type][id][method], dict):
                            if 'Result (sigma)' in self.report[path][type][id][method].keys():
                                if abs(self.report[path][type][id][method]['Result (sigma)']) >= threshold:
                                    # print(id)
                                    alert = True
                    if alert:
                        if not (path in self.alert.keys()):
                            self.alert[path]={}
                        if not (type in self.alert[path].keys()):
                            self.alert[path][type]={}
                        self.alert[path][type][id]=dict(self.report[path][type][id])
                        alert = False  # Resets for each id.

        return (self.alert)

    def print_report(self, path, overwrite=False):
        """Write health check report to file with human readable format.

        Parameters
        ----------
        path: string
            path to the report
        overwrite: boolean, optional
            Overwrite existing file. If false, path will be renamed before
            writing the report.

        Returns
        -------
        full_string: string
            The full string of the report.
        """

        if not overwrite:
            path = vishack.data.output.rename(path, method='utc')

        default_string = self.report_header
        alert_string = self.alert_to_string()
        report_string = self.report_to_string()
        full_string = default_string+alert_string+report_string
        with open(path, 'w') as f:
            f.write(full_string)

    def alert_to_string(self):
        """Convert alert dictionary to human readable string

        Returns
        -------
        alert_string: string
            The human readable alert string
        """

        title = 'Alert Report'
        alert_string = title
        alert_string += '\n'
        alert_string += '='*len(title)
        alert_string += '\n\n'
        string = self.dict_to_string(self.alert)
        if string == '':
            alert_string += ('**No Alerts. VISHack cannot detect any '\
                'problems.**\n\nFor detailed report, check below.\n\n')
        else:
            alert_string += string
        return alert_string

    def report_to_string(self):
        """Convert health check report dictionary to human readable string

        Returns
        -------
        report_string: string
            The human readable report string
        """

        title = 'Health Check Detailed Report'
        report_string = title
        report_string += '\n'
        report_string += '='*len(title)
        report_string += '\n\n'
        report_string += self.dict_to_string(self.report)
        return report_string

    def dict_to_string(self, dictionary):
        """Turns a report type dictionary to human readable string (rst)

        Paramaters
        ----------
        dictionary: dict
            The health check report or the alert

        Returns
        -------
        rst_string: string
            The string in reStructuredText format.
        """

        rst_string = ''
        for path in dictionary.keys():
            rst_string += path
            rst_string += '\n'
            rst_string += '-'*len(path)
            rst_string += '\n\n'
            for type in dictionary[path].keys():
                rst_string += type
                rst_string += '\n'
                rst_string += '^'*len(type)
                rst_string += '\n\n'
                for id in dictionary[path][type].keys():
                    rst_string += 'Test ID {}'.format(id)
                    rst_string += '\n'
                    rst_string += '*'*len('Test ID {}'.format(id))
                    rst_string += '\n\n'
                    for foo in dictionary[path][type][id].keys():
                        if isinstance(dictionary[path][type][id][foo], dict):
                            rst_string += '-\t{}'.format(foo)
                            rst_string += '\n\n'
                            for bar in dictionary[path][type][id][foo].keys():
                                value = dictionary[path][type][id][foo][bar]
                                rst_string += '\t-\t{}:\t{}'.format(bar, value)
                                rst_string += '\n'
                        else:
                            value = dictionary[path][type][id][foo]
                            rst_string += '-\t{}:\t{}'.format(foo, value)
                            rst_string += '\n'
                    rst_string += '\n'
        return(rst_string)


    def evaluate_(self, data, reference, method, df=1.):
        """Evaluate a statistical quantity between two datasets.

        Parameters
        ----------
        data: array
            The data to be evaluated
        reference: array
            The reference data to be referenced
        method: string
            The type of quantity to be evaluated.
            Options are 'RMS', 'WRMS', 'MSE', 'WMSE', 'MAE', 'WMAE'.
        df: float, optional
            The frequency spacing between data points. Default to be 1.
            Only used when calculating RMS and WRMS.
        """

        if method == 'RMS':
            return(vishack.core.evaluate.rms(data=data, df=df))
        elif method == 'WRMS':
            return(vishack.core.evaluate.wrms(
                data=data, df=df, whitening=reference))
        elif method == 'MSE':
            return(vishack.core.evaluate.mse(data=data, reference=reference))
        elif method == 'WMSE':
            return(vishack.core.evaluate.wmse(data=data, reference=reference))
        elif method == 'MAE':
            return(vishack.core.evaluate.mae(data=data, reference=reference))
        elif method == 'WMAE':
            return(vishack.core.evaluate.wmae(data=data, reference=reference))
        else:
            logger.error('Method {} not available. Ignoring...'.format(method))
            return(None)


    def data_evaluate(self, data, listof_references, method, df=1.):
        """Calculate mean and standard deviation of the evaluations

        Parameters
        ----------
        data: array
            The data to be evaluated
        listof_references: list of arrays
            A list of references data to compare the data with.
        method: string
            The type of quantity to be evaluated.
            Options are 'RMS', 'WRMS', 'MSE', 'WMSE', 'MAE', 'WMAE'.
        df: float, optional
            The frequency spacing between data points. Default to be 1.
            Only used when calculating RMS and WRMS.

        Returns
        -------
        mean: float
            The mean of all evaluations
        std: float
            The standard deviation of all evaluations
        """

        values=[]

        for reference in listof_references:
            value = self.evaluate_(
                data=data, reference=reference, method=method, df=df)
            values.append(value)

        mean = np.mean(values)
        std = np.std(values)

        return(mean, std)


    def reference_evaluate(self, listof_references, method, df=1.):
        """Cross evaluations between references

        Parameters
        ----------
        listof_references: list of arrays
            A list of references data.
        method: string
            The type of quantity to be evaluated.
            Options are 'RMS', 'WRMS', 'MSE', 'WMSE', 'MAE', 'WMAE'.
        df: float, optional
            The frequency spacing between data points. Default to be 1.
            Only used when calculating RMS and WRMS.

        Returns
        -------
        mean: float
            The mean of all evaluations
        std: float
            The standard deviation of all evaluations
        """

        values = []
        for i in range(len(listof_references)):
            for j in range(i+1, len(listof_references)):
                value = self.evaluate_(
                    data=listof_references[i],
                    reference=listof_references[j],
                    method=method, df=df)
                values.append(value)

        mean = np.mean(values)
        std = np.std(values)

        return(mean, std)

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
