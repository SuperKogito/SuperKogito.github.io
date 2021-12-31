Basic aiohttp Server
====================

.. raw:: html

  <div class="blog-post-tags">
    <ul class="blog-posts-details">
    <li id="Date"><span>Date:</span>                 31 December 2021 </li>
    <li id="author"><span>Author:</span>            <a href="author/ayoub-malek.html">Ayoub Malek</a> </li>
    <li id="location"><span>Location:</span>        <a href="location/monastir.html">Monastir</a>
    </li>  <li id="language"><span>Language:</span> <a href="language/english.html">English</a>
    </li>  <li id="category"><span>Category:</span> <a href="category/server-client.html">Server-client</a>
    </li>
    <li id="tags"><span>Tags:
          </span>
          <a class="post-tags" href="tag/audio.html">Server-Client</a>
          <a class="post-tags" href="tag/python.html">Python</a>
    </li>
    </ul>
  </div>

.. meta::
   :description: aiohttp server
   :keywords: server, client, python
   :author: Ayoub Malek


.. post:: December 31, 2021
   :tags: Python, Server, Asynchronousrous
   :category: Server-client, 2021
   :author: Ayoub Malek
   :location: Monastir
   :language: English

-----------------------

When it comes to deploying an application on a server online, a crucial aspect is its response time since no user wants to wait long for a response.
Hence, optimizations and asynchronous processing are the way to go. within this context, aiohttp is a python library that helps implementing asynchronous HTTP Client/Server.
The following blog one of a series of 4 that will introduce a server implementation, followed by a token based authentication and some stress testing.

What is aiohttp ?
-----------------
aiohttp is an HTTP client/server for asyncio.
Basically it allows you to write asynchronous clients and servers.
The aiohttp package also supports Server WebSockets and Client WebSockets.

what is asyncio?
----------------
asyncio is a library to write concurrent code.
It is used at the core of many asynchronous applications to deliver high-performance and speedy processing, etc.

what is concurrency?
--------------------
In simple words, concurrency can be described as having multiple computations happening at the same time.
In a little more complex formulation, it can be described as the execution of different parts a program out-of-order or in partial order.
Hence, you can say concurrency is sort of partial parallelism of computations.

Why is concurrency useful in server/client communications?
----------------------------------------------------------
The ability to have multiple units of your code running in parallel allows you to handle more requests or even send multiple calls without requiring more physical resources.
In other words, by asynchronously running your functions you can push your system to its limits but you should mind your processing order to avoid unexpected behaviors.

How to implement it?
---------------------
Aiohttp includes a variey of examples on how to do this. In the following steps, I will only include here, what worked best for me:

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
-----
The previously listed steps, should look together in Python as follows:

.. code-block:: python
  :caption: Framing 1
  :linenos:

  from aiohttp import web

  async def ping(request):
      return web.Response(text="pong")

  app = web.Application()
  app.add_routes([web.get('/', ping)])


The previous code, can require slight changes when creating the application and registering the handler in the case of using multi-processing for example.

Testing
-------
The previous code when executed will start a server running on to http://localhost:8080/.
To test your server either type in your browser http://localhost:8080/ping simply curl_ it using `curl http://localhost:8080/ping`.
The response should be the following json.

Conclusion
-------------
This blog presented aiohttp and its usefulness within regard to concurrency. It further provided a simple example of a server that will respond with pong if it is alive.


References and Further readings
--------------------------------

.. _aiohttp : https://docs.aiohttp.org/en/stable/
.. _curl : https://curl.se/
