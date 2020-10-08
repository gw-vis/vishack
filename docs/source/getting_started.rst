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

.. code-block:: bash

   conda create -n vishack

Then, we can activate it using:

.. code-block:: bash

   conda activate vishack

You should see a bracket with the environment name in front of the command
prompt.

We proceed to install the required packages. The standard rule for installing
packages under a Conda environment is to install everything using
:code:`conda install`. If a package is not available, then fallback using
:code:`pip install`. In our case, numpy is available in conda-forge while
:code:`dtt2hdf` is not. So, we do the following. Notice the order of operation,
it matters because the first :code:`conda install` will install an
environment specific :code:`pip`.

.. code-block:: bash

   conda install -c conda-forge numpy

Then, we confirm that we are using the environment :code:`pip`, not the global
:code:`pip` by typing :code:`which pip`. If it shows the global :code:`pip`,
then proceed to install pip by :code:`conda install pip`. After confirming
that we are using environment specific :code:`pip`,
then we can install :code:`dtt2hdf`.

.. code-block:: bash

   pip install dtt2hdf

At last, we can install VISHack, by first cloning the repository. Then,
change into the downloaded directory and then install it using :code:`pip`

.. code-block:: bash

   git clone https://github.com/gw-vis/vishack.git
   cd vishack
   pip install .

This is it.

To deactivate the environment, simply type

.. code-block:: bash

   conda deactivate

Using VISHack
-------------
Check out :ref:`Quick Example` for a quick guide and :ref:`Tutorial` for a
detailed step-by-step guide on how to use VISHack on both command line
interface and Python interface. Don't forget to check out
:ref:`Command Line Utilities` and :ref:`VISHack Library Reference` for detailed
descriptions of VISHack as well.
