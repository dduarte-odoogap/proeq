ProEQ's documentation!
======================

Introduction
------------

ProEQ is a commandline utility for executing scripts into your servers.
The Utility also provides a project database with the references to all
ssh servers and other type of useful technical information.

How Does It Work?
-----------------

ProEQ will read information from a user folder, default location in (~/.proeq).
The user folder will have the following basic structure:

* ~/.proeq
   * projects
   * scripts

Then inside the scripts folder you will need:

* :doc:`How to build a scripts folder <scripts>`

Then inside the projects folder you will need:

* :doc:`How to build a project folder <project>`


Install Development
-------------------


.. code:: bash

    virtualenv .env
    pip install -e
    echo 'eval "$(_PROEQ_COMPLETE=source proeq)"' << ~/.bashrc



Create User Folder
------------------

Use the following structure:

* .proeq
   * scripts
      * script-one
         * manifest.yml
      * ...

   * projects
      * project-one
         * project.yml
      * ...


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`


.. toctree::
   :caption: Table of Contents
   :maxdepth: 2

   projects
   scripts