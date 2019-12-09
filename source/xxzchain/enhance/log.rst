.. _logging:

Logging
============

2019.12.08
-------------
When the library has growing, it is too big that maintenance is really hard.
So, I tried to tag and make logging system of my library, which is whole progress can be recorded.
So that, whenever one find some bug in my code, he can find easily.

.. note::
  I used `logging` of python built-in module which is very convenient to log for my system.
  It throw log to another thread, so the main routine won't be aborted by `logging`.
  Futhermore, syntax of `logging` is same as `print` (python built-in console out function).


Inside of `logging` module, there is logger which is logging `unit`. I seperate logger into each class.
So, when the error or bug occured, we can find where at.

Basically, there is same tree structure between logger and library. Simply, see below.

- System  (system.logger)

  - Intializaer (system.Initializer.logger(child of system.logger))

    - routines (~.Intializer.<routine_name>.logger)

  - Saver (system.Saver.logger)

    - even with above

And logging has 5 basiclevel of log.
- debug : only for debugging
- info  : information
- warning : not critical, but it may cause error.
- critical : It will make error
- error : literally.

I put every calculation and information from my library into debug.
Therefore, debug level will return bunch of lines.
In contrast, info is consist of more important content than debug. (i.e. skipping  calculation and saving)
for now, I just only use info and debug.
