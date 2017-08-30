==========
inaugurate
==========

*inaugurate* is a bootstrap script that:

- lets you install (mainly python, but potentially also other) applications and run them in the same go
- can (optionally) delete itself and the application it bootstrapped after the command was executed
- has no dependencies except for either ``curl`` or ``wget``
- can create seperate environments for each package it installs (either via python virtualenv or conda)
- supports 'non-root'-permission installs (via conda_)
- has it's own 'official' app_store_, or lets you use your own local one
- supports Debian-, RedHat- based Linux distros, as well as Mac OS X

*inaugurate* was written for freckles_ to enable 'one-line' bootstrap of whole working environments. It turned out to be fairly easy to make it more generic, so it got its own project here. *inaugurate* (obviously) is not useful for simple cases where you just need to install an application, in 95% of all cases you can do that by just using your system package manager (``apt install the-package-you-want``). Some applications require a bit more effort to install (e.g. ansible_ using pip). While still being fairly trivial, you need to install some system dependencies, then, if you want to do it properly, create a virtualenv_ and ``pip install`` the package into it. Those are the cases where *inaugurate* is of some use as it can do those things automatically.

The main reason for writing *inaugurate* was the aforementioned 'one-line' bootstrap though. Admittedly, I have no idea how often this can be of use for the general public, but its a basic enough pattern that I haven't seen implemented elsewhere (yet -- also I might not have looked well enough), at least not in a generic fashion, so I imagine there are a few situations where it will make sense. You'll know it when you see it, sorta thing.

Example
-------

Right, so here's how you 'inaugurate' frecklecute_, which comes bundled with freckles_ and lets you run 'declarative' scripts (basically wrapped *ansible* playbooks). This is a good example of when it's useful to be able to install and run at the same time, since in some cases you might not ever need to run *frecklecute* again (for example, if you use it to build a Docker container within a ``Dockerfile``:

.. code-block:: console

   curl https://inaugurate.sh | bash -s -- frecklecute --help

As mentioned, *inaugurate* also executes the application once it's installed, which is why the ``--help`` option is provided in this example. This behaviour can be turned off, if needed:

.. code-block:: console

   NO_EXEC=true curl https://inaugurate.sh | bash -s -- frecklecute

Of course, we can also use ``wget`` instead of ``curl``:

.. code-block:: console

   SELF_DESTRUCT=true wget -O - https://freckles.io | bash -s -- frecklecute --help

In this last example, *inaugurate* will delete itself and the application it just installed after that application ran. Again, this might for example be useful if you build a container, and want the end-product be as slim as possible.

Usage
-----

sudo / non-sudo
env vars

How does this work? What does it do?
------------------------------------

*inaugurate* is a `shell script <https://github.com/makkus/inaugurate/blob/master/inaugurate.sh>`_ that, in most cases, will be downloaded via ``curl`` or ``wget`` (obviously you can just download it once and invoke it directly). It's behaviour can be controlled by environment variables (see examples above).

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

    NO_ADD_PATH=true curl https://inaugurate.sh | bash -s -- cookiecutter gh:audreyr/cookiecutter-pypackage

You'll have to figure out a way to manually add your inaugurated applications to your ``$PATH``, or you always specify the full path.

Folders
^^^^^^^

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

That being said, you can download `inaugurate.sh <https://raw.githubusercontent.com/makkus/inaugurate/master/inaugurate.sh>`_ and host it yourself somewhere on github (or somewhere else). If you only use app descriptions locally (or, as those app descriptions are fairly easy to parse and understand, you read the ones the are hosted on the 'official' inaugurate app_store_) you have the same sort of control you'd have if you'd do all the things *inaugurate* does manually.

I'd argue it'd be slightly better to have one generic, widely-used script with easy-to-read app descriptions than every app out there writing their own bootstrap script. *inaugurate* (possibly in combination with *frecklecute* to support more advanced setup tasks) could be such a thing, but I'd be happy if someone else writes a better alternative. Just saying, it's more practical to not have to read a whole bash script everytime you want to bootstrap a non-trivial-to-install application.

License
-------

GNU General Public License v3

.. _freckles: https://github.com/makkus/freckles
.. _conda: https://conda.io
.. _app_store: https://github.com/inaugurate/store
.. _ansible: http://docs.ansible.com/ansible/latest/intro_installation.html
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
