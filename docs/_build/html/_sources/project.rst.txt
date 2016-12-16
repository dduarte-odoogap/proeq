Structure for Projects
======================

For projects:

.. code:: yaml

   project:
     name: Super Server
     customer: Mario
     ssh-server:
       - host: 10.0.0.11
         name: Pre-Production
         user: dd
         port: 22
       - host: 10.0.0.12
         name: Production
         user: dd
         port: 22
     repo:
       url: http://github/odoogap/proj1
       tag: v10.20
     comments: >
       This project lorem ipsum lorem
       lorem ipsum lorem lorem ipsum lorem
       lorem ipsum lorem lorem ipsum lorem
