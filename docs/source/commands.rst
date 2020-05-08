=====================
Commands and Options
=====================

To display information about pyenvbuilder's builtin commands run::
	
	pyenvbuilder --help

To display more information about a particular command run::
	
	pyenvbuilder <command> --help

To see the current version of pyenvbuilder run::

	pyenvbuilder --version

----------------------------------

check command
---------------

The ``check`` command validates one or multiple YAML files against a schema.
It takes both *.yml* and *.yaml* file format::

	pyenvbuilder check my_env.yml 

or::

	pyenvbuilder check my_env.yml my_other_env.yml

or you can check all the YAML files located in a directory::

	pyenvbuilder check my_env_dir/

-------------------------------------

create command
---------------

The ``create`` command creates a *conda* environment from an YAML file. To create an environment run::

	pyenvbuilder create my_env.yml 

to create multiple environments run::
	
	pyenvbuilder create my_env.yml my_other_env.yml

or::

	pyenvbuilder create my_env_dir/

to create all the environments from YAML files located in *my_env_dir* directory.


.. topic:: create --options


	By default, the ``create`` command runs the tests provided (if provided) in *my_env.yml* file. You can choose to skip tests by running the ``--skip-tests`` option::

		pyenvbuilder create --skip-tests my_env.yml

	By default, the ``create`` command will create the environment in the current directory. You can choose to create it at a different location by providing a destination with the ``--dest`` option::

		pyenvbuilder create my_env.yml --dest my_destination_path/

--------------------------------------

pack command
-------------

The ``pack`` command packs an environment into a tarball. To pack an environment run::

	pyenvbuilder pack my_env

to pack multiple environments run::

	pyenvbuilder pack my_env my_other_env

or to pack all the environments located in a directory run::

	pyenvbuilder pack my_env_dir/


.. topic:: pack --options

	By default the ``pack`` command will remove the environment after it has been packed. You can keep the environment by providing the ``--keep-env`` option::

		pyenvbuilder pack --keep-env my_env

	By default the ``pack`` command will pack the environment in the current directory. You can choose to pack it at a different location by providing a destination with the ``--dest`` option::

		pyenvbuilder pack my_env --dest my_destination_path/


unpack command
---------------

The ``unpack`` command unpacks the tarball into an environment. To unpack a tarball run::


	pyenvbuilder unpack my_env.tar.gz

to unpack multiple tarballs run::

	pyenvbuilder unpack my_env.tar.gz my_other_env.tar.gz

or, to unpack all the tarballs located in a directory run::

	pyenvbuilder unpack tarball_dir/

.. topic:: unpack --options

	By default the ``unpack`` command will unpack the environment in the current directory. You can choose to unpack it at a different location by providing a destination with the ``--dest`` option::
	
		pyenvbuilder unpack my_env.tar.gz --dest my_destination_path/


