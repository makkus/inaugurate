==========
inaugurate
==========

*'hit-the-ground-running' bootstrap*

*inaugurate* is a bootstrap script that lets you install applications and run them in the same command. This is not useful very often, but in some cases it actually is. You'll know it when you see it :-)

In addition to this, *inaugurate* provides a way to install applications, via a config file that lists all the dependencies of that applications. Again, this is not useful in a lot of cases, especially trivial ones where the application is available via the systems package manager. Sometimes an application doesn't provide that though, or the system packages are too outdated to be useful. An example would be ansible_, which needs a few system packages to be available as well as python package dependencies. The system packages are necessary so that some of the security-related python dependencies can be compiled/installed.

*inaugurate* makes this easy, like so:

.. code-block:: console

   curl https://inaugurate.sh | bash -s -- ansible --help

As mentioned, *inaugurate* also executes the application once it's installed, which is why the ``--help`` option is provided in this example. This behaviour can be turned off, if needed:

.. code-block:: console

   NO_EXEC=true curl https://inaugurate.sh | bash -s -- ansible


Initially *inaugurate* was the bootstrap part of freckles_, but I figured it might be useful in other situations as well.

Features
--------

* no requirements, except for either ``curl`` or ``wget``
* supports non-root permission install via conda
* supported package managers (so far): apt, yum, conda, and pip
* creates seperate environments for each package (either via virtualenv or conda)


License
-------

GNU General Public License v3
