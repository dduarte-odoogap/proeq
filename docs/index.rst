Welcome to ProEQ's documentation!
=================================


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

YAML Structure
--------------


.. toctree::
   :maxdepth: 2

   project
   scripts



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
