Structure for Scripts
=====================

For scripts:

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