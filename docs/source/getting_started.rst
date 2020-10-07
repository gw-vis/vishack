.. _Getting Started:

Getting Started
===============

Dependencies
------------

Required
^^^^^^^^
* numpy  (for basic calculations)
* dtt2hdf  (for handling diaggui XML files)

Optional
^^^^^^^^

Planned
^^^^^^^
* tqdm  (for displaying progress bar)

Installation guide
------------------
We recommend using VISHack under Conda environment. Conda is available on
k1ctr1 and k1ctr7 in KAGRA.

We will create an environment called *vishack*.

.. code:: bash

   conda create -n vishack

Then, we can activate it using:

.. code:: bash

   conda activate vishack

You should see a bracket with the environment name in front of the command
prompt.

We proceed to install the required packages. The standard rule for installing
packages under a Conda environment is to install everything using
:code:`conda install`. If a package is not available, then fallback using
:code:`pip install`. In our case, numpy is available in conda-forge while
dtt2hdf is not. So, we do the following. Notice the order of operation,
it matters because the first :code:`conda install` will install an
environment specific :code:`pip`.

.. code:: bash

   conda install -c conda-forge numpy

Then, we confirm that we are using the environment :code:`pip`, not the global
:code:`pip` by typing :code:`which pip`. If it shows the global :code:`pip`,
then proceed to install pip by :code:`conda install pip`. After confirming
we are using environment specific :code:`pip`, then we can install *dtt2hdf*.

.. code:: bash

   pip install dtt2hdf

At last, we can install VISHack, by first cloning the repository. Then,
change into the downloaded directory and then install it using :code:`pip`

.. code:: bash

   git clone https://github.com/gw-vis/vishack.git
   cd vishack
   pip install .

This is it.

To deactivate the environment, simply type

.. code:: bash

   conda deactivate
