==========
inaugurate
==========

Features
--------

*inaugurate* is a generic bootstrap script that:

- lets you install (mainly python, but potentially also other) applications and run them in the same go
- can (optionally) delete itself and the application it bootstrapped after the command was executed
- has no dependencies except for either ``curl`` or ``wget``
- supports 'non-root'-permission installs (via conda_)
- creates seperate environments for each package it installs (either via python virtualenv or conda)
- has it's own 'official' app_store_, or lets you use your own local one
- supports Debian-, RedHat- based Linux distros, as well as Mac OS X


Examples
--------

So here's an example on how you 'inaugurate' frecklecute_, which comes bundled with freckles_ and lets you run 'declarative' scripts (basically wrapped *ansible* playbooks). This is a good example of when it's useful to be able to install and run at the same time, since in some cases you might not ever need to run *frecklecute* again (for example, if you use it to build a Docker container within a ``Dockerfile``):

.. code-block:: console

   curl https://inaugurate.sh | bash -s -- frecklecute --help

As mentioned, *inaugurate* also executes the application once it's installed, which is why the ``--help`` option is provided in this example. This behaviour can be turned off, if needed:

.. code-block:: console

   curl https://inaugurate.sh | NO_EXEC=true bash -s -- frecklecute --help

Of course, we can also use ``wget`` instead of ``curl``:

.. code-block:: console

   wget -O - https://inaugurate.sh | SELF_DESTRUCT=true bash -s -- frecklecute --help

In this last example, *inaugurate* will delete itself and the application it just installed after that application ran. Again, this might for example be useful if you build a container, and want the end-product be as slim as possible.

Description
-----------

*inaugurate* was written for freckles_ to enable 'one-line' bootstrap of whole working environments. It turned out to be fairly easy to make it more generic, so it got its own project here. *inaugurate* (obviously) is not useful for simple cases where you just need to install an application, in 95% of all cases you can do that by just using your system package manager (``apt install the-package-you-want``).

Some applications require a bit more effort to install (e.g. ansible_ using pip). While still being fairly trivial, you need to install some system dependencies, then, if you want to do it properly, create a virtualenv_ and ``pip install`` the package into it. Those are the cases where *inaugurate* is of some use as it can do those things automatically.

The main reason for writing *inaugurate* was the aforementioned 'one-line' bootstrap though. Admittedly, I have no idea how often this can be of use for the general public, but I figure its a basic enough pattern that I haven't seen implemented elsewhere (yet -- also I might not have looked well enough), at least not in a generic fashion, so I imagine there are a few situations where it will make sense. You'll know it when you see it, sorta thing.


Usage
-----

cli
^^^

Here's how the commandline interface looks on a high level:

.. code-block:: console

    <curl_or_wget_command> https://inaugurate.sh | ENV_KEY_1=<env_value_1> ENV_KEY_2=<env_value> bash -s -- <application> <app_args>
    |                    | |                   |   |                                           |           |                      |
     - download command -   ------- url -------     ---------- control behaviour --------------             ---- app execution ---

Or, using ``sudo``:

.. code-block:: console

    <curl_or_wget_command> https://inaugurate.sh | sudo ENV_KEY_1=<env_value_1> ENV_KEY_2=<env_value> bash -s -- <application> <app_args>
    |                    | |                   |        |                                           |           |                      |
     - download command -   ------- url -------          ---------- control behaviour --------------             ---- app execution ---

*download command*
    either ``curl`` (or use ``curl -s`` if you don't want to see its progress), or ``wget -O -``

*url*
    always ``https://inaugurate.sh`` (you can also use ``https://freckles.io`` if you want, though)

*control behaviour*
    see the list below for available options

*app execution*
    this is the same you'd use if you would execute the application if it was already installed and available in your ``PATH``, for example: ``ansible-playbook --ask-become-pass play.yml``

apps descriptions
^^^^^^^^^^^^^^^^^

*inaugurate* uses text files that describe the requirements that are needed to install an application. This is an example for such a description, for the application *ansible*:

.. code-block:: console

    ENV_NAME=ansible
    EXECUTABLES_TO_LINK=ansible ansible-playbook ansible-galaxy ansible-vault ansible-console ansible-doc ansible-pull
    EXTRA_EXECUTABLES=
    # conda
    CONDA_PYTHON_VERSION=2.7
    CONDA_DEPENDENCIES=pip cryptography pycrypto git
    # deb
    DEB_DEPENDENCIES=curl build-essential git python-dev python-virtualenv libssl-dev libffi-dev
    # rpm
    RPM_DEPENDENCIES=epel-release wget git python-virtualenv openssl-devel gcc libffi-devel python-devel
    # pip requirements
    PIP_DEPENDENCIES=ansible

By default, *inaugurate* will check whether the first argument is a path to a locally existing file. If it is, this file will be read. If not, a file named after the provided app name (the first argument to the script) in ``$HOME/.inaugurate/local-store``. If there is, this will be read and the application described therein will be 'inaugurated'. If no such file exists, *inaugurate* will check whether such a file exists on the official inaugurate app_store_.

Here's what the different vars mean:

*ENV_NAME*
    the name of the conda or virtualenv that will be created

*EXECUTABLES_TO_LINK*
    a list of executables that should be linked ot ``$HOME/.local/bin``

*EXTRA_EXECUTABLES*
    an optional list of secondary executables. this is mainly used within freckles_. executables in this list are linked into ``$HOME/.local/inaugurate/bin``

*CONDA_PYTHON_VERSION*
    if using conda, this is the python version that is used in the new environment

*CONDA_DEPENDENCIES*
    if using conda, those are the packages that will be installed into the new environment

*DEB_DEPENDENCIES*
    if using sudo/root-permissions, and running on a Debian-based platform, those are the packages that should be installed using apt

*RPM_DEPENDENCIES*
    if using sudo/root-permissions, and running on a RedHat-based platform those are the packages that should be installed using yum

*PIP_DEPENDENCIES*
    the python packages to install in the conda or virtualenv environment

downloading *inaugurate.sh*
^^^^^^^^^^^^^^^^^^^^^^^^^^^

As already mentioned, you can either use ``curl`` or ``wget`` to download *inaugurate.sh*. Actually, any other tool you have at hand that can download files from the internet, and pipe out their content. I focus on ``curl`` and ``wget`` since the likelyhood one of them is installed is highest.

curl
++++

As mentioned above, this is how to invoke *inaugurate* using ``curl``:

.. code-block::

    curl https://inaugurate.sh | bash -s -- <app_name> <app_args>>

wget
++++

And using ``wget``:

.. code-block::

    wget -O - https://inaugurate.sh | bash -s -- <app_name> <app_args>

For the following examples I'll always use ``curl``, but of course you can use ``wget`` interchangeably.

alternative for interactive command
+++++++++++++++++++++++++++++++++++

In case the command you are trying to inaugurate requires interactive input, you can use either of those formats:

.. code-block::

    bash <(wget -O- https://inaugurate.sh) <app_name> <app_args>

or

.. code-block::

    bash <(curl https://inaugurate.sh) <app_name> <app_args>


I haven't figured out yet how to do that with sudo though.

sudo/non-sudo
^^^^^^^^^^^^^

One of the main features of *inaugurate* is the option to install whatever you want to install without having to use ``root`` or ``sudo`` permissions. This only works for applications that are available via conda_, or python packages.

The way to tell *inaugurate* whether to use *conda* or not is by either calling it via sudo (or as ``root`` user) or as a 'normal' user. In the former case *inaugurate* will install system packages, in the latter it will install conda (if not already available) and contain all other dependencies within a *conda* environment.

To call *inaugurate* using ``sudo``, potentially/optionally using a environment variable to control its behaviour, you do something like:

.. code-block:: console

   curl https://inaugurate.sh | sudo NO_EXEC=true bash -s -- frecklecute --help

environment variables
^^^^^^^^^^^^^^^^^^^^^

Here's a list of environment variables that can be used to change *inaugurate's* default behaviour, by default all variables are set to false or are empty strings:

*NO_ADD_PATH*
    if set to true, *inaugurate* won't add ``$HOME/.local/bin`` to the path in the ``$HOME/.profile`` file

*NO_EXEC*
    if set to true, *inaugurate* won't execute the inaugurated application after install

*SELF_DESTRUCT*
    if set to true, *inaugurate* will delete everything it installed in this run (under ``$HOME/.local/inaugurate``)

*PIP_INDEX_URL*
    if set, a file ``$HOME/.pip/pip.conf`` will be created, and the provided string will be set as as ``index-url`` (only if ``pip.conf`` does not exist already)

*CONDA_CHANNEL*
    if set, a file ``$HOME/.condarc`` will be created, and the provided string will be set as the (sole) conda channel (only if ``.condarc`` does not exist yet)

*CHINA*
    if set to true, ``PIP_INDEX_URL`` and ``CONDA_CHANNEL`` will be set to urls that are faster when used within China as they are not outside the GFW, also, this will try to set debian mirrors to ones withing China (if host machine is Debian, and *inaugurate* is run with sudo permissions) -- this is really only a convenience setting I used when staying in Beijing, but I imagine it might help users in China -- if there ever will be any


How does this work? What does it do?
------------------------------------

*inaugurate* is a `shell script <https://github.com/makkus/inaugurate/blob/master/inaugurate.sh>`_ that, in most cases, will be downloaded via ``curl`` or ``wget`` (obviously you can just download it once and invoke it directly). It's behaviour can be controlled by environment variables (see examples above).

*inaugurate* touches two things when it is run. It adds a line to ``$HOME/.profile``, and it creates a folder ``$HOME/.local/inaugurate`` where it puts all the application data it installs. In addition, if invoked using root permissions, it will also potentially install dependencies via system packages.

.profile
^^^^^^^^

By default, *inaugurate* adds those lines to your ``$HOME/.profile`` (which will be created if it doesn't exist):

.. code-block::

    # add inaugurate environment
    LOCAL_BIN_PATH="$HOME/.local/bin"
    if [ -d "$LOCAL_BIN_PATH" ]; then
        PATH="$PATH:$LOCAL_BIN_PATH"
    fi

Obviously, this won't be in effect after your first *inaugurate* run, as the ``.profile`` file wasn't read since then. You can 'force' picking up the new ``PATH`` by either logging out and logging in again, or sourcing ``.profile``:

.. code-block

    source $HOME/.profile

Adding the *inaugurate* path to ``.profile`` can be disable by specifying the ``NO_ADD_PATH`` environment variable when running *inaugurate*:

.. code-block::

    curl https://inaugurate.sh | NO_ADD_PATH=true bash -s -- cookiecutter gh:audreyr/cookiecutter-pypackage

You'll have to figure out a way to manually add your inaugurated applications to your ``$PATH``, or you always specify the full path.

package install locations
^^^^^^^^^^^^^^^^^^^^^^^^^

Everything is installed in the users home directory, under ``$HOME/.local/inaugurate``. Each application you 'inaugurate' gets its own environemnt (a python *virtualenv* in case of a *sudo* install, or a `conda environment <https://conda.io/docs/user-guide/tasks/manage-environments.html>`_ otherwise). The executables that are specified in the *inaugurate* app description (for example: https://github.com/inaugurate/store/blob/master/ansible) will be linked into the folder ``$HOME/.local/bin``.

By containing everything under ``$HOME/.local/inaugurate``, deleting this folder will delete all traces of *inaugurate* and 'inaugurated' apps (except for the added ``PATH`` in ``.profile``) and free up all space (except for potentially installed system dependency packages).

As mentioned, if invoked using ``sudo`` (or as user *root*), *inaugurate* will try to install dependencies using system packages (and python packages using virtualenv), otherwise *conda* is used to perform an entirely non-root install. This is the reason why both cases differ slightly in the folders that are created and used:

'sudo'/'root'-permissoins
+++++++++++++++++++++++++

.. code-block:: console

    .local/
    ├── bin
    └── inaugurate
        ├── bin
        ├── logs
        ├── tmp
        └── virtualenvs
            └── inaugurate
            └── <other app>

In this case, new application environments are created under ``.local/inaugurate/virtualenvs``. So, for example, if you want to activate one of those virtualenvs (something you usually don't need to do as the executables you probably want are all linked into ``.local/bin`` which is in your ``PATH`` by now), you can do:

.. code-block:: console

   source .local/inaugurate/virtualenvs/<app_name>/bin/activate

deactivate it issuing:

.. code-block:: console

   deactivate

'non-root'-permissions
++++++++++++++++++++++

.. code-block:: console

   .local/
   ├── bin
   └── inaugurate
       ├── bin
       ├── conda
       │   ├── bin
       │   ├── conda-meta
       │   ├── envs
       │   │   └── inaugurate
       │   │   └── <other app>
       │   ├── etc
       │   ├── include
       │   ├── lib
       │   ├── pkgs
       │   ├── share
       │   └── ssl
       └── logs

Conda app environments can be found under ``.local/inaugurate/conda/envs``. In this case, if you'd wanted to activate a specific conda environment (again, usually you don't need to do this), you can do:

.. code-block:: console

   source .local/inaugurate/conda/bin/activate <env_name>

and to deactivate:

.. code-block:: console

   source deactivate

Is this secure?
---------------

What? Downloading and executing a random script from the internet? Duh.

That being said, you can download the `inaugurate.sh <https://raw.githubusercontent.com/makkus/inaugurate/master/inaugurate.sh>`_ script and host it yourself on github (or somewhere else). If you then only use app descriptions locally (or, as those app descriptions are fairly easy to parse and understand, you read the ones the are hosted on the 'official' inaugurate app_store_) you have the same sort of control you'd have if you'd do all the things *inaugurate* does manually.

I'd argue it's slightly better to have one generic, widely-used and looked upon script, that uses easy to parse configurations for the stuff it installs, than every app out there writing their own bootstrap shell script. *inaugurate* (possibly in combination with *frecklecute* to support more advanced setup tasks) could be such a thing, but I'd be happy if someone else writes a better alternative. It's more practical to not have to read a whole bash script every time you want to bootstrap a non-trivial-to-install application, is all I'm saying.

Supported platforms
-------------------

Those are the platforms I have tested so far, others might very well work too. I did my development mainly on Debian-based systems, so other Linux distributions might not (yet) be up to scratch:

- Linux

  - Debian

    - Stretch
    - Jessie

  - Ubuntu

    - 17.04
    - 16.10
    - 16.04

  - CentOS

    - 7

- Mac OS X

  - El Capitan
  - Sierra

- Windows

  - Windows 10 (Ubuntu subsystem) -- not tested/working yet


License
-------

GNU General Public License v3

.. _freckles: https://github.com/makkus/freckles
.. _frecklecute: https://docs.freckles.io/en/latest/frecklecute_command.html
.. _conda: https://conda.io
.. _app_store: https://github.com/inaugurate/store
.. _ansible: http://docs.ansible.com/ansible/latest/intro_installation.html
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
