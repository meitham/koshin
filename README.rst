================================
KOSHIN (Japanese for Renovation)
================================


This project builds on top of ``lib2to3`` to provide extra fixers, refer to
`lib2to3 documentation`_ for its own docs.


Installation
============

To install koshin, simply run::

    pip install koshin


Usage
=====

To print a diff of changes that koshin will make against a
particular source file or directory::

    koshin source_folder

To have those changes written to the files::

    koshin -w source_folder

To have those changes written to another directory::

    koshin -w source_folder --output-dir /some/where/else

By default, this will create backup files for each file that will be
changed. You can add the `-n` option to not create the backups. Please
do not do this if you are not using a version control system.

For more options about running particular fixers, run
``koshin --help`` or read the `lib2to3 documentation`_. This
tool is built on top of that one.


Fixes
=====

A list of the available fixers can be found with the following::

    $ koshin -l
    Available transformations for the -f/--fix option:
    rename_import


.. _`lib2to3 documentation`: http://docs.python.org/library/2to3.html


