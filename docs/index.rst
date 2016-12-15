.. ProEQ documentation master file, created by
   sphinx-quickstart on Thu Dec 15 19:52:55 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ProEQ's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

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

.. code:: yaml

      manifest:
        #id: install-odoo
        name: Install Odoo 10.0 Ubuntu 16.04LTS
        category: Install
        scripts:
          - order: 2
            name: Secure the ssh server
            description: Secures de ssh server then installs Odoo
            file: sh/secure-ssh.sh
            type: bash
            ssh-server:
              host: 10.167.140.205
              user: root
              port: 22
          - order: 1
            name: Loads the ssh keys
            description: Loads the ssh keys from Carlos and me
            file: sh/load-keys.sh
            type: bash
            ssh-server:
              host: 10.167.140.205
              user: root
              port: 1033
        environment:
          xmlrpc:
            host: 10.167.140.205
            database: v10_odoo
            port: 8069
            user: admin
            pass: admin

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
