History
=======

2.0 (2018-03-24)
----------------

* removing 'freckles' profile and enable custom default profile to be added easily
* preparing for use with *luci* ( https://github.com/makkus/luci )
* adding FORCE_SUDO & FORCE_NON_SUDO options
* moving the main execution body into it's function, to prevent the script from running partially if download is interrupted
* using 'get-pip.py' script for Mac OS X elevated permission install
* removing default CommandLineTools install for Mac OS X (it is left as an option though)

1.2
---

* added virtualenv conda dependency

1.1 (2018-02-16)
----------------

* fix for special characters in external commands output

1.0 (2018-01-30)
----------------

* started versioning
