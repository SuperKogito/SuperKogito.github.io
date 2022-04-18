:og:description: authenticated aiohttp servver
:og:keywords: authentication, server, client, python, ayoub malek, blog post
:og:image: ../../../../_static/meta_images/aiohttp_server_with_token.png
:og:image:alt: authenticated_aiohttp_server

Token authenticated aiohttp server
==================================

.. post:: December 31, 2021
   :tags: Python, Server-client
   :category: Server-client
   :author: Ayoub Malek
   :location: Monastir
   :language: English

-----------------------

In the previous blog post, a simple aiohttp server was introduced.
In the following post we improve the previous server by introducing a simple token authentication mechanism.

Why authenticate?
~~~~~~~~~~~~~~~~~
Authentication is a crucial part when dealing with server-client connections.
If your resources are limited and your server has no filtering mechanism of whom to serve, an overload of requests would break your server.
This the one of the simplest yet efficient Denial of Service attacks (DOS).
Hence an authentication mechanism will help filter unrecognized requests and will spare you the computational power and attention.

Why use tokens?
~~~~~~~~~~~~~~~
Token based authentication is one of the cheapest and the simplest approaches.
It is an efficient filtering approach if the data communicated is not that important.
Depending on how you generate your valid tokens, how you communicate/ store them you can improve your security but this will not be discussed here.

Implementation
~~~~~~~~~~~~~~
To improve the previous implementation, we will push all the config variables into one JSON file and we will name it `config.json`.
This will include all the configuration parameters for our script. It will look like the following.

.. code-block:: bash
 :caption: config.json
 :linenos:

 {
   "server": {
     "http": {
       "host": "127.0.0.1",
       "port": 8000,
       "request_max_size": 1048576,
       "allowed_tokens": ["token1","token2"]
     }
   },
   "log": {
     "level": [{
       "logger": "server_logger",
       "level": "DEBUG"
     }]
   }
 }

As you see in the config, we are now able to configure the host and the port to run the server on.
We are also able to constraint the size of the accepted requests along with providing a list of accepted valid tokens.
Furthermore, we added a logger and a debug level to investigate possible errors.
The following section will detail the work.

1. **First we configure the logger.**

   .. code-block:: python
    :linenos:

    import logging

    # init loggging
    logger = logging.getLogger(__name__)
    logging.basicConfig(format="[%(asctime)s.%(msecs)03d] p%(process)s {%(pathname)s: %(funcName)s: %(lineno)d}: %(levelname)s: %(message)s", datefmt="%Y-%m-%d %p %I:%M:%S")
    logger.setLevel(10)

2. **Load the configuration infos.**

   .. code-block:: python
    :linenos:

    import json

    # parse conf
    with open("config.json", "rb") as config_file:
        conf = json.loads(config_file.read())

3. **Write a request handler.**
   Requests in aiohttp are processed using coroutines that will serve as the actual functions called by the client.

   .. code-block:: python
    :linenos:

    import asyncio
    from aiohttp import web

    @asyncio.coroutine
    def ping(request):
        return web.json_response({"text": "pong", "status": "success"})

4. **Write the authentication and token handler**

   .. code-block:: python
    :linenos:

    import asyncio
    from aiohttp import web
    from typing import Callable, Coroutine, Tuple

    def token_auth_middleware(user_loader: Callable,
                              request_property: str = 'user',
                              auth_scheme: str = 'Token',
                              exclude_routes: Tuple = tuple(),
                              exclude_methods: Tuple = tuple()) -> Coroutine:
        """
        Checks a auth token and adds a user from user_loader in request.
        """
        @web.middleware
        async def middleware(request, handler):
            try               : scheme, token = request.headers['Authorization'].strip().split(' ')
            except KeyError   : raise web.HTTPUnauthorized(reason='Missing authorization header',)
            except ValueError : raise web.HTTPForbidden(reason='Invalid authorization header',)

            if auth_scheme.lower() != scheme.lower():
                raise web.HTTPForbidden(reason='Invalid token scheme',)

            user = await user_loader(token)
            if user : request[request_property] = user
            else    : raise web.HTTPForbidden(reason='Token doesn\'t exist')
            return await handler(request)
        return middleware

5. **Write the server init function and wrap it all.**

   .. code-block:: python
    :linenos:

    import asyncio
    from aiohttp import web

    async def init():
       """
       Init web application.
       """
       async def user_loader(token: str):
           user = {'uuid': 'fake-uuid'} if token in conf["server"]["http"]["allowed_tokens"] else None
           return user

       app = web.Application(client_max_size=conf["server"]["http"]["request_max_size"],
                             middlewares=[token_auth_middleware(user_loader)])
       app.router.add_route('GET', '/ping', ping)
       return app


    web.run_app(init(),)


Code
~~~~
The previously listed steps, should look together in Python as follows:

.. code-block:: python
  :caption: aiohttp-server-with-token-auth
  :linenos:

  import json
  import asyncio
  import logging
  from aiohttp import web
  from typing import Callable, Coroutine, Tuple


  # init loggging
  logger = logging.getLogger(__name__)
  logging.basicConfig(format="[%(asctime)s.%(msecs)03d] p%(process)s {%(pathname)s: %(funcName)s: %(lineno)d}: %(levelname)s: %(message)s", datefmt="%Y-%m-%d %p %I:%M:%S")
  logger.setLevel(10)

  # parse conf
  with open("config.json", "rb") as config_file:
      conf = json.loads(config_file.read())

  @asyncio.coroutine
  def ping(request):
      logger.debug("-> Received PING")
      response = web.json_response({"text": "pong", "status": "success"})
      return response

  def token_auth_middleware(user_loader: Callable,
                            request_property: str = 'user',
                            auth_scheme: str = 'Token',
                            exclude_routes: Tuple = tuple(),
                            exclude_methods: Tuple = tuple()) -> Coroutine:
      """
      Checks a auth token and adds a user from user_loader in request.
      """
      @web.middleware
      async def middleware(request, handler):
          try               : scheme, token = request.headers['Authorization'].strip().split(' ')
          except KeyError   : raise web.HTTPUnauthorized(reason='Missing authorization header',)
          except ValueError : raise web.HTTPForbidden(reason='Invalid authorization header',)

          if auth_scheme.lower() != scheme.lower():
              raise web.HTTPForbidden(reason='Invalid token scheme',)

          user = await user_loader(token)
          if user : request[request_property] = user
          else    : raise web.HTTPForbidden(reason='Token doesn\'t exist')
          return await handler(request)
      return middleware

  async def init():
      """
      Init web application.
      """
      async def user_loader(token: str):
          user = {'uuid': 'fake-uuid'} if token in conf["server"]["http"]["allowed_tokens"] else None
          return user

      app = web.Application(client_max_size=conf["server"]["http"]["request_max_size"],
                            middlewares=[token_auth_middleware(user_loader)])
      app.router.add_route('GET', '/ping', ping)
      return app

  if __name__ == '__main__':
      web.run_app(init(),)



Testing
~~~~~~~~
The previous code when executed will start a server running on :code:`http://localhost:8080/`.
To test your server either type in your browser :code:`http://localhost:8080/ping` or simply curl_ it while passing your token using :code:`curl -H 'Authorization: Token token1' http://127.0.0.1:8080/ping`.
The response should be a json including pong and a success status.

Conclusion
~~~~~~~~~~
This blog presented an improved aiohttp server that implements token based authentication to filter out unwanted traffic and protect itself against possible spamming attacks
that could be part of DOS attacks.

Share this blog
~~~~~~~~~~~~~~~~

.. raw:: html

  <div id="share">
    <a class="facebook" href="https://www.facebook.com/share.php?u=https://superkogito.github.io/blog/2021/12/31/aiohttp_server_with_token.html&title=Token%20authenticated%20aiohttp%20Server"                target="blank"><i class="fa fa-facebook"></i></a>
    <a class="twitter"  href="https://twitter.com/intent/tweet?url=https://superkogito.github.io/blog/2021/12/31/aiohttp_server_with_token.html&text=Token%20authenticated%20aiohttp%20Server"                 target="blank"><i class="fa fa-twitter"></i></a>
    <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&url=https://superkogito.github.io/blog/2021/12/31/aiohttp_server_with_token.html&title=Token%20authenticated%20aiohttp%20Server" target="blank"><i class="fa fa-linkedin"></i></a>
    <a class="reddit"   href="http://www.reddit.com/submit?url=https://superkogito.github.io/blog/2021/12/31/aiohttp_server_with_token.html&title=Token%20authenticated%20aiohttp%20Server"                    target="blank"><i class="fa fa-reddit"></i></a>
  </div>


.. update:: 8 Apr 2022

   👨‍💻 edited and review were on 08.04.2022


.. _aiohttp : https://docs.aiohttp.org/en/stable/
.. _curl : https://curl.se/
