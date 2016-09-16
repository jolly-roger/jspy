langjs
======

langjs is an implementation of javascript programming language, written in
Python using RPython.

You will need to install some dependencies. You can do it with::

    pip install -r requirements.txt

And make sure you have `PyPy_` on your ``PYTHONPATH``.

To run tests::

    $ PYTHONPATH=. py.test

.. _`PyPy`: https://bitbucket.org/pypy/pypy

Translating the interpreter to C 
================================

Just as you can translate PyPy's Python interpreter, you can also translate the
Javascript interpreter to C::

    pypy$ cd translator/goal
    pypy/translator/goal$ python translate.py targetjsstandalone.py

The translated interpreter is not interactive, you can only pass a javascript
file for execution.
