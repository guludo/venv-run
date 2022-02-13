========
venv-run
========

Doing this...

.. code:: bash

    venv-run myapp.py

...is *more convenient* than this...

.. code:: bash

    source myvenv/bin/activate
    python myapp.py
    deactivate

That is the main motivation of this tool!

.. contents::

``venv-run`` is a tool for running commands with a Python virtual environment
without *explicitly* activating it (and deactivating it when you are done).
Essentially it runs your command with the virtual environment's binary path
prepended to the system's ``PATH`` environment variable. Another nice thing
about ``venv-run`` is that it tries to find the environment's directory from
your current working directory so you can save some typing.

Installation
============

Using ``pip``
-------------

.. code:: bash

    pip install venv-run

From source
-----------

If you have ``pip`` available in your system, then the recommended way to
install from source is doing:

.. code:: bash

    # From the source root
    pip install .

Alternatively, you can call ``setup.py`` directly, but remember that it *does
not provide an "uninstall" command* (this form is useful for OS distribution
packagers):

.. code:: bash

    python setup.py install

Usage
=====

``venv-run`` can be called directly as a shell command:

.. code:: bash

    venv-run [OPTIONS] [--] [CMD]

When called, the first thing ``venv-run`` does is to look for a (single)
virtual environment under your current working directory. After it encounters
the environment's directory, it runs your command with the environment's binary
path prepended to the system's binary path.

All the examples in this section assume you have a virtual environment created
in the working directory.

Running a Python script
-----------------------

Suppose you have a Python project in ``my-python-project`` and have created a
virtual environment like the example below:

.. code:: bash

    $ cd my-python-project
    $ python -m venv myvenv

You can call a Python script of your project using that environment with the
command:

.. code:: bash

    $ venv-run myapp.py

If ``myapp.py`` accepts arguments, you can pass them normally:

.. code:: bash

    $ venv-run myapp.py --foo --bar baz

.. note::
    Running Python scripts like this is possible because ``venv-run`` guesses
    that you want to run ``myapp.py`` with the environment's Python
    interpreter. If myapp.py has execution permission for your user, then
    ``venv-run`` *will not* invoke the interpreter for you. You can call
    ``venv-run python myapp.py`` for such cases.

Calling Python
--------------

The virtual environment's Python interpreter is implicitly called in the
following situations:

    - When no command is passed to ``venv-run``;

    - When the first word of ``CMD`` is not an executable and either starts
      with ``-`` or ends with ``.py``. In this case, ``python`` is prepended to
      ``CMD`` (the example in the previous section falls under this condition).

Thus, for example, you can start an interactive session with the environment's
Python by simply calling:

.. code:: bash

    $ venv-run

And you can call a module installed in the environment with:

.. code:: bash

    $ venv -m path.to.module

For both cases, it's also okay to explicitly call the interpreter (e.g.
``venv-run python -m path.to.module``).

Calling executables
-------------------

If you want to call an executable installed in your virtual environment, you
can call it like in the example below:

.. code:: bash

    # Suppose I'm using flask to develop a Web application and want to start
    # the development server
    $ venv-run flask run

The executable does not need to be really installed in the environment. The
next example starts the system's ``bash`` with ``venv/bin`` prepended to
``PATH``:

.. code:: bash

    $ venv-run bash


Locally installing and using a Python package
---------------------------------------------

Let's say you want to use `bpython <https://bpython-interpreter.org/>`_ to
interactively use and test your project's modules.

You can install it:

.. code:: bash

    $ venv-run pip install bpython


And the run it at will:

.. code:: bash

    $ venv-run bpython

Multiple virtual environments
-----------------------------

``venv-run`` refuses to continue if it finds more than one virtual environment.
You can pass ``--venv PATH_TO_VENV`` to point the environment to be used for
such cases.

Options ambiguity
-----------------

If ``CMD`` uses options conflicting with ``venv-run``'s own options, then you
can prepend ``CMD`` with ``--`` to mark the beginning of ``CMD``. Example:

.. code:: bash

    $ venv-run python -h # Shows venv-run's help message
    $ venv-run -- python -h # Shows python's help message


Use cases
=========

With pre-commit
---------------

A common specific use case is to be able to run pre-commit_ ``system``
and ``script`` hooks written in Python so that they're run within the
virtual environment of the project, even if it hadn't been activated
beforehand. This may happen for example when ``pre-commit`` is
launched when committing from an IDE that is not virtualenv
self-aware, initially launched in an environment different from the
project's virtual one.

Another one is to get tools that need to be run in the project's
virtual environment to work properly -- such as mypy_, pylint_, and
pytype_ to name a few -- to actually run in it. To do this, instead of
using the usual project provided hooks, install the respective tool
package along with its dependencies and plugins in the project's
virtual environment and use a ``local`` pre-commit hook like:

.. code:: yaml

  - repo: local
    hooks:
      - id: pylint
        name: pylint
        language: python
        additional_dependencies: [venv-run]
        entry: venv-run pylint
        types: [python]

Be sure to look into the project provided hooks to see if there are
any additional needed settings, for example ``args``, anything special
in ``entry``, ``require_serial`` or the like, and replicate in your
local hook as applicable.

.. _pre-commit: https://pre-commit.com
.. _mypy: http://mypy-lang.org
.. _pylint: https://pylint.org
.. _pytype: https://google.github.io/pytype/


Author
======

Gustavo José de Sousa
