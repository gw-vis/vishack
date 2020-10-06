"""VISHack
A health checking system for vibration isolation system in KAGRA

Fetched from:
A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.rst').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
import vishack
VERSION = vishack.__version__

setup(
    name='vishack',  # Required
    version=VERSION,  # Required
    description='A self-diagnostic system for vibration isolation systems in'\
        'KAGRA',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/x-rst',  # Optional (see note above)
    url='https://github.com/gw-vis/vishack',  # Optional
    author='TSANG Terrence Tak Lun',  # Optional
    author_email='ttltsang@link.cuhk.edu.hk, terrencetec@gmail.com',  # Optional
    keywords='KAGRA, gravitational waves, observatory',  # Optional
    packages=find_packages(),
    python_requires='>=3.5, <4',
    install_requires=[
        'numpy',
        'dtt2hdf',
    ], # Dependencies here, Optional
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    # extras_require={  # Optional
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },
    entry_points={
        'console_scripts': [
            'vishack-print=vishack.clitools.print_vishack:main',
            'vishack-sample-config'\
            '=vishack.clitools.generate_sample_config:main',
            'vishack=vishack.clitools.healthcheck:main',
        ],
    }
    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    # project_urls={  # Optional
    #     'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
    #     'Funding': 'https://donate.pypi.org',
    #     'Say Thanks!': 'http://saythanks.io/to/example',
    #     'Source': 'https://github.com/pypa/sampleproject/',
    # },
)
