The Ferris Framework
====================

Ferris is a web framework written in Python for App Engine, inspired by: Ruby on Rails, CakePHP, Django, and Flask. Unlike most other frameworks, Ferris is designed specifically for App Engine.

For information and documentation:

    http://ferrisframework.org/

For help and questions: 

    https://groups.google.com/forum/?fromgroups#!forum/ferris-framework


Starting a new project
----------------------

Checkout a copy of Ferris using git:

    git clone git@bitbucket.org:cloudsherpas/ferris-framework.git
    cd ferris-framework

Use git to export ferris to your project directory (trailing slash is important!):

    git checkout-index -a -f --prefix=/project-directory/

You're ready to go, just open your project directory and  run the app engine server.

License
-------

Ferris is licensed under the Apache License, Version 2.

Third-party libraries that are in the packages directory have varying licenses. Please check the license file that's with each package.

WTForms: BSD
ProtoPigeon: Apache License v2
PyTZ: MIT
GData Client Library: Apache License v2
Google API Python Client Library: Apache License v2
OAuth2 Client: Apache License v2
