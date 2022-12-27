:og:description: convert chmod modes to octal and back to letters
:og:keywords: server, client, python, ayoub malek, blog post
:og:image: ../../../../_static/meta_images/aiohttp_server.png
:og:image:alt: aiohttp_server

Basic aiohttp server
====================

.. post:: December 31, 2021
   :tags: Python, Server-client
   :category: Server-client
   :author: Ayoub Malek
   :location: Monastir
   :language: English

-----------------------

When it comes to deploying an application on a server online, a crucial aspect is its response time since no user wants to wait long for a response.
Hence, optimizations and asynchronous processing are the way to go. within this context, aiohttp_ is a python library that helps implementing asynchronous HTTP Client/Server.
The following blog is one of a series of four that will introduce a server implementation, followed by a token based authentication and some stress testing.

What is aiohttp ?
~~~~~~~~~~~~~~~~~
aiohttp_ is an HTTP client/server for asyncio.
Basically it allows you to write asynchronous clients and servers.
The aiohttp package also supports Server WebSockets and Client WebSockets.

What is asyncio?
~~~~~~~~~~~~~~~~
asyncio_ is a library to write concurrent code.
It is used at the core of many asynchronous applications to deliver high-performance and speedy processing, etc.

What is concurrency?
~~~~~~~~~~~~~~~~~~~~
In simple words, concurrency can be described as having multiple computations happening at the same time.
In a little more complex formulation, it can be described as the execution of different parts a program out-of-order or in partial order.
Hence, you can say concurrency is sort of partial parallelism of computations.

Why is concurrency useful in server/client communications?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ability to have multiple units of your code running in parallel allows you to handle more requests or even send multiple calls without requiring more physical resources.
In other words, by asynchronously running your functions you can push your system to its limits but you should mind your processing order to avoid unexpected behaviors.

How to implement it?
~~~~~~~~~~~~~~~~~~~~
Aiohttp includes a variey of examples on how to do this. In the following, I will only include here, what worked best for me:

1. **Start with installing aiohttp using**

   .. code-block:: bash
    :caption: Install aiohttp
    :linenos:

     pip install aiohttp

2. **Write a request handler.**
   Requests in aiohttp are processed using coroutines that will serve as the actual functions called by the client.

   .. code-block:: python
    :caption: Write a request handler
    :linenos:

     import numpy as np
     from aiohttp import web

     @asyncio.coroutine
     def ping(request):
         return web.json_response({"text": "pong", "status": "success"})

3. **wrap everything by creating an Application instance and registering the request handler**

   .. code-block:: python
    :caption: Create application and register handler
    :linenos:

     app = web.Application()
     app.add_routes([web.get('/', ping)])


Code
~~~~
The previously listed steps, should look together in Python as follows:

.. code-block:: python
  :caption: Framing 1
  :linenos:

  from aiohttp import web

  async def ping(request):
      return web.Response(text="pong")

  app = web.Application()
  app.add_routes([web.get('/', ping)])

and you are done, you just create a server application that returns a pong when pong'ed.
This code, can require slight changes when creating the application and registering the handler in case of using multi-processing for example.

Testing
~~~~~~~
The previous code when executed will start a server running on http://localhost:8080/.
To test your server either type in your browser http://localhost:8080/ping or simply curl_ it using :code:`curl http://localhost:8080/ping`.
The response should be the following :code:`pong`.

Conclusion
~~~~~~~~~~
This blog presented aiohttp and its usefulness within regard to concurrency.
It further provided a simple example of a server that will respond with pong if it is alive.

Share this blog
~~~~~~~~~~~~~~~

.. raw:: html

  <div id="share">
    <a class="facebook" href="https://www.facebook.com/share.php?u=https://superkogito.github.io/blog/2021/12/31/aiohttp_server.html&title=Basic%20aiohttp%20server"                target="blank"><i class="fa fa-facebook"></i></a>
    <a class="twitter"  href="https://twitter.com/intent/tweet?url=https://superkogito.github.io/blog/2021/12/31/aiohttp_server.html&text=Basic%20aiohttp%20server"                 target="blank"><i class="fa fa-twitter"></i></a>
    <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&url=https://superkogito.github.io/blog/2021/12/31/aiohttp_server.html&title=Basic%20aiohttp%20server" target="blank"><i class="fa fa-linkedin"></i></a>
    <a class="reddit"   href="http://www.reddit.com/submit?url=https://superkogito.github.io/blog/2021/12/31/aiohttp_server.html&title=Basic%20aiohttp%20server"                    target="blank"><i class="fa fa-reddit"></i></a>
  </div>

.. update:: 16 Apr, 2022

   Last edited on 16.04.2022


.. _aiohttp : https://docs.aiohttp.org/en/stable/
.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _curl : https://curl.se/
