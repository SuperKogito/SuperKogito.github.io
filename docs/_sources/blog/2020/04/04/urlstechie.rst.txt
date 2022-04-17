:og:description: urlstechie introduction
:og:keywords: cryptography overview, encryption, hashing, security, ayoub malek, cybersecurity post, blog introduction
:og:image: ../../../../_static/meta_images/cryptography_overview.png
:og:image:alt: urlstechie

Introducing urlstechie and its urls checking tools
==================================================

.. meta::
   :description: Introducing urlstechie and urls checking tools
   :keywords: urlstechie, urlchecker, check urls, Ayoub Malek
   :author: Ayoub Malek


.. post:: Apr 04, 2020
   :tags: Continuous integration, urlstechie, Python
   :category: Automation, 2020
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

Continuous testing is a vital part of any healthy software development process.
Urls must always be tested and broken links must be fixed to guarantee a high quality product.
Unfortunately, this is not always trivial and can be tedious.
Moreover, most tools available out there cannot handle in-code urls and lack many other needed features.
A while back, I ran across this particular Problem and I quickly saw the great automation opportunity this was, and how can Python and Regex help me solve this.
This was the start of the urlchecker-action ... from there and with the amazing `@vsoch`_ joining, the tools expanded and this was the start of the urlstechie organization.


What is urlstechie?
~~~~~~~~~~~~~~~~~~~

.. image:: ../../../../_static/logos/urlstechie_logo.png
   :align: center

urlstechie is a small organization and an online project that started on March 2020.
The goal for this project is to provide urls checking tools as part of continuous testing practices.
The urlstechie organization currently provides two main tools:

.. raw:: html

    <ul>
        <li>
            <a href="https://github.com/urlstechie/urlchecker-action" title="github"> <i class="fa fa-github"></i> urlchecker-action</a> :
            A GitHub action to collect and check urls in a project (code and documentation).
            The action aims at detecting and reporting broken links.
        </li>

        <li>
            <a href="https://github.com/urlstechie/urlchecker-python" title="github"> <i class="fa fa-github"></i> urlchecker-python</a> :
            A Python module to collect urls over static files (code and documentation), test them and then report broken links.
        </li>
    </ul>


For more please refer to:

- urlstechie_website_
- urlstechie_github_repository_


How to use the urlstechie tools?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The urlstechie tools, as you will notice, are very intuitive and simple to use.
It also provides various features to customize the run, white-list urls and files etc.
The GitHub action can be set-up as a GitHub workflow like the following:

.. code-block:: yaml
 :caption: GitHub workflow
 :linenos:

  name: Check URLs

  on: [push]

  jobs:
    build:
      runs-on: ubuntu-latest

      steps:
      - uses: actions/checkout@v2
      - name: urls-checker
        uses: urlstechie/urlchecker-action@0.1.7
        with:
          # A subfolder or path to navigate to in the present or cloned repository
          subfolder: docs

          # A comma-separated list of file types to cover in the URL checks
          file_types: .md,.py,.rst

          # Choose whether to include file with no URLs in the prints.
          print_all: false

          # The timeout seconds to provide to requests, defaults to 5 seconds
          timeout: 5

          # How many times to retry a failed request (each is logged, defaults to 1)
          retry_count: 3

          # A comma separated links to exclude during URL checks
          white_listed_urls: https://github.com/SuperKogito/URLs-checker/issues/2

          # A comma separated patterns to exclude during URL checks
          white_listed_patterns: https://github.com/SuperKogito/Voice-based-gender-recognition/issues

          # choose if the force pass or not
          force_pass : true

As for the python urlchecker module, it can be used locally to run the same checks.
The urlchecker can be installed from pypi_ using :code:`pip install urlchecker` or from conda_ using :code:`conda install -c conda-forge urlchecker`.
Here is a small demo by `@vsoch`_ displaying a couple of uses of the tool.

.. image:: ../../../../_static/demo.gif
   :align: center
   :scale: 80%

For more on the tools please refer to:

.. raw:: html

    <ul>
        <li>
            <a href="https://github.com/urlstechie/urlchecker-action" title="github"> <i class="fa fa-github"></i> urlchecker-action</a>
        </li>

        <li>
            <a href="https://github.com/urlstechie/urlchecker-python" title="github"> <i class="fa fa-github"></i> urlchecker-python</a>
        </li>
    </ul>


How to contribute?
~~~~~~~~~~~~~~~~~~
We aim to provide an open welcoming environment at urlstechie.
That's the foundation to a flourishing project and so all contributions are welcome.
Just open an issue and come talk to us, help us improve the code by providing test cases, feedback, suggestions and bug reports.
If you have a fix, that's even better, send us a pull request and join us on this coding ride ;)

Share this blog:
~~~~~~~~~~~~~~~~
.. raw:: html

  <div id="share">
    <a class="facebook" href="https://www.facebook.com/share.php?u={{url}}&title={{title}}" target="blank"><i class="fab fa-facebook-f"></i></a>
    <a class="twitter" href="https://twitter.com/intent/tweet?status={{title}}+{{url}}" target="blank"><i class="fa fa-twitter"></i></a>
    <a class="googleplus" href="https://plus.google.com/share?url={{url}}" target="blank"><i class="fa fa-google-plus"></i></a>
    <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&url={{url}}&title={{title}}&source={{source}}" target="blank"><i class="fa fa-linkedin"></i></a>
    <a class="reddit" href="http://www.reddit.com/submit?url={{url}}&title={{title}}" target="_blank" title="Submit to Reddit" target="blank"><i class="fa fa-reddit"></i></a>
  </div>


.. update:: 8 Apr 2022

   👨‍💻 edited and review were on 08.04.2022

References and Further readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- urlstechie_website_
- `Checking static links with urlchecker by vsoch`_


.. _urlstechie_website : https://urlstechie.github.io/index.html
.. _urlstechie_github_repository : https://github.com/urlstechie
.. _@vsoch : https://github.com/vsoch
.. _`Checking static links with urlchecker by vsoch` : https://vsoch.github.io/2020/urlchecker/
.. _pypi : https://pypi.org/
.. _conda : https://anaconda.org/
