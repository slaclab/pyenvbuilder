About PyEnvBuilder
===================
In order to ensure control over which packages are created, PyEnvBuilder requires an `YAML File`_ that defines a certain environment.
Only packages from the conda-forge mirror and PyPI would be accepted since those two combined cover most if not all packages widely available to Python. 
Custom packages should use ``PYTHONPATH`` or be added to one of the two locations:

* PyPI

	* `Packaging Python Projects <https://packaging.python.org/tutorials/packaging-projects/>`_

* conda-forge

	* `Add conda-forge recipe <https://conda-forge.org/#add_recipe>`_

.. note:: If the code for a certain python package is available at GitHub but not yet at PyPI or conda-forge, it can still be installed via pip but using the proper URL.


--------------------------

YAML File
----------

YAML file example:

.. image:: _static/images/yaml.png
   :width: 1200pt
   :align: center

There are 5 attributes you can provide when writing an YAML file....to be continued

