============================
Environment YAML File Setup
============================
In order to ensure control over which packages are created, PyEnvBuilder requires an YAML file 
that defines a certain environment.
Only packages from the *conda-forge* mirror and *PyPI* are accepted since those two combined cover most if not all packages widely available to Python. 
Custom packages should use ``PYTHONPATH`` or should be added to one of the two locations:

* PyPI

	* `Packaging Python Projects <https://packaging.python.org/tutorials/packaging-projects/>`_

* conda-forge

	* `Add conda-forge recipe <https://conda-forge.org/#add_recipe>`_

.. note:: If the code for a certain python package is available at GitHub but not yet at PyPI or conda-forge, it can still be installed via pip using the proper URL.


--------------------------

YAML File
----------

	YAML file example:

.. image:: _static/images/yaml.png
   :width: 600pt
   :align: center

The table below explains the attributes of the YAML file:

+----------------+------------------------------+-------------------+----------+----------+
|Attributes      | Description                  | Example           | Type     | Required |
+================+==============================+===================+==========+==========+
| name           | name of the environment      | python3.7env      | string   | Yes      |
+----------------+------------------------------+-------------------+----------+----------+
| version        | version of the environment   | v1.0 or "1.0.0"   | string   | Yes      | 
+----------------+------------------------------+-------------------+----------+----------+
| conda_packages | packages to be installed     | \- python=3.7     | array    | Yes      |
|                | through conda-forge channel  |                   |          |          |
+----------------+------------------------------+-------------------+----------+----------+
| pip_packages   | packages to be installed     | \- pyenvbuilder   | array    | No       | 
|                | through pip                  |                   |          |          |
+----------------+------------------------------+-------------------+----------+----------+
| tests          | python scripts to test       | \- python test.py | array    | No       |
|                | the environment              |                   |          |          |
+----------------+------------------------------+-------------------+----------+----------+




