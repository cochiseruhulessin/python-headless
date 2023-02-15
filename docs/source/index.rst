=============================================
Headless - Asynchronous HTTP client framework
=============================================

The most common errors interfacting with external services using their
Application Programming Interfaces (APIs) are:

- The service rate limiting the client (i.e. your application), causing
  errors.
- Unpredictable code execution paths because of weak typing,
  especially when the vendors' client library returns simple
  dictionaries or lists.
- Unmaintainable spaghetti code when traversing a hierarchical
  object model.
- Temporary failures in DNS resolution, connection timeouts or other
  *temporary* network conditions.

The :mod:`headless` module, built on top of :mod:`pydantic` solves
exactly these problems. It provides an framework to type check API
resources and consume it without having to worry about unexpected
input, rate limits, or temporary service failures.


Getting started
===============
There are many asynchronous HTTP frameworks for Python, and :mod:`headless`
intends to support all of them. For now, the supported framework is :mod:`httpx`.
Install :mod:`headless` with :mod:`httpx` by running the below command in a
terminal:

.. code::

   pip3 install headless[httpx]


Consuming APIs with :mod:`headless`
===================================
Interacting with APIs becomes super easy with the :mod:`headless` module. Check
out the examples below to get an idea of the value that :mod:`headless` adds to
your project.

In these examples we will use the Picqer and Shopify API clients, but of course you
can substitute these with your own, in-house API! Building a robust, asynchronous
Python client library for your API is a small effort, with great rewards.

Fetching a list of resources
----------------------------
.. literalinclude:: ../../examples/shopify-get-orders.py
   :language: python
   :lines: 9-


Gracefully handling rate limits
-------------------------------
.. literalinclude:: ../../examples/shopify-ratelimit.py
   :language: python
   :lines: 9-


Traversing the resource hierarchy
---------------------------------
.. literalinclude:: ../../examples/picqer-traverse-api.py
   :language: python
   :lines: 9-


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
