Tests for `MI-PYT <https://github.com/cvut/MI-PYT>`__ WaTor homework
====================================================================

Usage
-----

 1. Copy the tests files to your project.
 2. In your virtual environment, install pytest-timeout: ``python -m pip install pytest-timeout``.
 3. Build your module (``python setup.py develop`` or ``python setup.py build_ext -i``)
 4. Run ``python -m pytest tests/``.


Tolerance to bad randomness
---------------------------

In order to make the tests as simple as possible, the tests only test if the
results are correct, not if they are truly random. Some examples:

* If you are supposed to put 5 fish and 3 sharks randomly on
  the Wa-Tor planet, the tests will check whether there are
  indeed 5 fish and 3 sharks. The tests will not check how
  random their position is.
* If a creature can move down or left, the tests will check whether
  the final location is valid, but the tests will not check whether the creature
  picks it's destination randomly.
* If you are supposed to choose a random age between 1 and 10, the tests will only
  check whether all the values are within the limits (i.e. using 4 as the
  hardcoded value will pass).
* As an exception, ``test_fish_move_over_border`` relies on randomness a bit,
  see the comment in it if you want to know more.

Please **be random where you are supposed to be random**. When in doubt, ask us.

This will pass the tests (but not the manual check
when grading the task):

.. image:: https://imgs.xkcd.com/comics/random_number.png
   :target: https://xkcd.com/221/



License
-------

This code has been dedicated to the Public Domain, it is licensed with
`CC0 1.0 Universal Public Domain
Dedication <https://creativecommons.org/publicdomain/zero/1.0/>`__,
full text of the license is available in the LICENSE file in this
repository.

The above xkcd comics by Randall Munroe is licensed with `Creative Commons
Attribution-NonCommercial 2.5 License <https://creativecommons.org/licenses/by-nc/2.5/>`_.
