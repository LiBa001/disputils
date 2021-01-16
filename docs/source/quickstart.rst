Quickstart guide
================

Disputils provides different and customizable utilities for discord.py bot developers.
This quickstart guide aims to help you understand the basic features of those utilities
and get you started as quick as possible.

The library contains two versions of each utility.
Which one to use depends on how you use ``discord.py``:

* basic ``discord.py``, via ``discord.Client``
* ``discord.py``'s commands extension, via ``discord.ext.commands.Bot``

Installation
############

You can easily install the latest version from PyPI via pip:

``pip install disputils``

Pagination
##########

The pagination utility allows you to create and control an interactive paginated
representation of multiple embeds that users can navigate via reactions.

.. image:: https://raw.githubusercontent.com/LiBa001/disputils/master/docs/img/paginate.png

client version
--------------

The simplest way of doing a pagination:

.. literalinclude:: ../../examples/client_test.py
   :language: python
   :lines: 26-33
   :dedent: 8

bot version
-----------

For the commands extension, we need to slightly modify the last two lines:

.. literalinclude:: ../../examples/bot_test.py
   :language: python
   :lines: 18-19
   :dedent: 4

Multiple Choice
###############

This utility gives the power of choice to your users.
Let it be polls, interactive menus or something else, you can take user experience to a new level.

Users can interact via automatically generated reactions under the message.

.. image:: https://raw.githubusercontent.com/LiBa001/disputils/master/docs/img/choice.png

The appearance and behavior is of course customizable.

client version
--------------

A cool way to realize an interactive multiple choice command,
that dynamically changes it's content is this:

.. literalinclude:: ../../examples/client_test.py
   :language: python
   :lines: 13-23
   :dedent: 8

bot version
-----------

This is what a simple multiple choice command could look like:

.. literalinclude:: ../../examples/bot_test.py
   :language: python
   :lines: 33-38

Confirmation
############

This one is pretty simple and straight-forward.
It lets you ask users for confirmation on an action. It's basically a yes-no question.

.. image:: https://raw.githubusercontent.com/LiBa001/disputils/master/docs/img/confirm.png

client version
--------------

An interactive confirmation:

.. literalinclude:: ../../examples/client_test.py
   :language: python
   :lines: 36-42
   :dedent: 8

bot version
-----------

An example confirmation command looks like this:

.. literalinclude:: ../../examples/bot_test.py
   :language: python
   :lines: 22-30
