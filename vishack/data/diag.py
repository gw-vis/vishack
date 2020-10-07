"""Library for interfacing with the diagnostic tools command `diag`.
"""

import os, stat
import vishack.data.output

bash_header = '# !/bin/bash\n'

def make_script(path, lines, overwrite=False):
    """Create a script and make it executable

    Parameters
    ----------
    path: string
        The path of the script
    lines: list of strings
        Scripting commands to be written on the script.
    overwrite: boolean, optional
        Overwrite if the path exists, if not, the file will be saved as
        a different name.
        Defaults to False.
    """

    if not overwrite:
        path = vishack.data.output.rename(path=path, method='utc')

    with open(path, 'w') as f:
        for line in lines:
            f.write(line)
            f.write('\n')

def run_measurement(path, saveas=None, remove_tmp=True):
    """Run a measurement set up by a diaggui XML file.

    Parameters
    ----------
    path: string
        The path of the diaggui XML file
    saveas: string, optional
        Save the measurement as a different file when finished measurement.
        Defaults to None. If None, it is same as `path`
    remove_tmp: boolean, optional
        Remove any temporary files that are used to trigger this measurement.
        Defaults to True.
    """

    if not os.path.exists(path):
        raise FileNotFoundError('{} not exists'.format(path))

    if saveas is None:
        saveas = path

    lines = [
        bash_header,
        'open',
        'restore {}'.format(path),
        'run -w',
        'save {}'.format(saveas),
        'quit',
    ]

    script_path = vishack.data.output.rename('tmp', method='utc')
    make_script(path=script_path, lines=lines, overwrite=False)

    os.system('diag -f {}'.format(script_path))

    if remove_tmp:
        os.remove(script_path)
