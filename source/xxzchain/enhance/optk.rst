.. _optk:

Optimization of ``Initializer.K``
===========================================


The library 'xxzchain_' has several basis initializer when user want to see specific region of Hilbert space.
I saw there is useless double for loop in code, so I make it single. In that process, I felt the code of saving is not pythonic but C-style code,
I make it pythonic. See below

.. _xxzchain: https://xxzchain.readthedocs.io/



Code (Before) :

.. literalinclude:: ../code/before1209.py
  :language: python
  :emphasize-lines: 26-48
  :linenos:


Code (After) :

.. literalinclude:: ../code/diff1209.py
  :language: python
  :emphasize-lines: 26-56
  :linenos:
