Headless - Asynchronous HTTP client framework
=============================================

The most common errors interfacting with external services using their
Application Programming Interfaces (APIs) are:

- The service rate limiting the client (i.e. your application), causing
  errors.
- Unpredictable code execution paths because of weak typing,
  especially when the vendors' client library returns simple
  dictionaries or lists.
- Validation and type checking logic scattered all over the codebase.
- Unmaintainable spaghetti code when traversing a hierarchical
  object model.
- Temporary failures in DNS resolution, connection timeouts or other
  *temporary* network conditions.

The :mod:`headless` module, built on top of :mod:`pydantic` solves
exactly these problems. It provides an framework to type check API
resources and consume it without having to worry about unexpected
input, rate limits, or temporary service failures. The :mod:`headless`
module is:

- Asynchronous, because that is how external services should be consumed
  during HTTP requests. It works great with :mod:`fastapi`, too!
- Easy, because you don't have to worry about the implementation
  details of asynchronous code. Define your resource models and you're
  ready to go!
- Robust, because using :mod:`headless` leads to a significant reduction
  of production incidents.


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


Building your own client
========================
It is likely that the :mod:`headless` extensions library does not contain a
client for your service. But no worries, implementing your custom client
consist of only three easy steps, that will get your started in *minutes*.

The examples below implement a fictional API that provides ``Author``
and ``Book`` resources.

Define your resources
---------------------
A resource is a structured object that is returned from a specific endpoint
exposed by a service through its API. A resource schema is described using Python
classes, by subclassing :class:`headless.core.Resource`.

Each implementation **must** declare an inner ``Meta`` class that declares the
``base_endpoint`` attribute. This attribute is used by :mod:`headless` to
dynamically construct the API endpoints through which operations on the
resource may be performed, such as creating, retrieving or listing.

.. code:: python

   from headless.core import Resource


   class AuthorResource(Resource):
      id: int
      name: str

      class Meta:
         base_endpoint: str = '/v1/authors'


   class BookResource(Resource):
      id: int
      title: str
      authors: list[AuthorResource]

      class Meta:
         base_endpoint: str = '/v1/books'


Implement authentication
------------------------
Most APIs have some sort of authentication. To quickly, but consistently, implement
authentication procedures that are compatible with :mod:`headless`, a helper class
is provided: :class:`headless.types.ICredential`.

All an implementation has to do is to override
:meth:`headless.types.ICredential.add_to_request`,
which must then add the credentials to a request.

.. code:: python

   from typing import Any

   from headless.types import ICredential
   from headless.types import IRequest


   class AccessTokenCredential(ICredential):
         token: str

         def __init__(self, token: str):
               self.token = token

         # Note that ICredential.add_to_request() is an async method.
         async def add_to_request(self, request: IRequest[Any]) -> None:
               request.add_header('Authorization', f'Bearer {self.token}')


Using your client
-----------------


.. code:: python

   from headless.core.httpx import Client


   client = Client(
         base_url='https://api.example.com',
         credential=AccessTokenCredential('access token')
   )
   async with client:
      # Get all Books.
      await client.listall(Book)

      # Get a single book.
      await client.retrieve(Book, 1)