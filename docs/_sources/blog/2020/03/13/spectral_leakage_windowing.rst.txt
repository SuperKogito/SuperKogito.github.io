:og:description: Audio signal windowing and spectral leakage
:og:keywords: windowing, spectral leakage, python, ayoub malek, blog post
:og:image: ../../../../_static/meta_images/spectral_leakage.png
:og:image:alt: spectral_leakage

Spectral leakage and windowing
==============================

.. post:: Mar 13, 2020
   :tags: Audio, Python
   :category: Signal processing, 2020
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

Windowing is an important part of almost any signal processing system, that helps remove/ reduce spectral leakage when processing a non-periodic signal.
This blog post provides a small overview of what is spectral usage, when does it occur and how to use windowing to suppress it.

| *** keywords:  *** Windowing, Spectral leakage


What is spectral leakage ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~
As *Allen B. Downey* mentions in his book *Think DSP*, in order to understand windowing, we must first understand spectral leakage and for that we have first to understand the Discrete Fourier Transform (DFT) and its related assumptions.
When using DFT to compute spectograms, we assume signals to be periodic. In practice, this assumption is often not fulfilled, resulting in inaccurate transform computations containing extra residual frequency components :footcite:`downey2014`.
This phenomenon is known as spectral leakage, which is a smearing of power across a frequency spectrum that occurs when the processed signal is not periodic in the sample interval.
It occurs because of the discrete sampling in the effective Fourier series computations of a waveform having discontinuities results in additional frequency components :footcite:`roberts`.
Leakage is a common error encountered in digital signal processing, that cannot be entirely eliminated but may be reduced using windowing.


What is windowing ?
~~~~~~~~~~~~~~~~~~~
Windowing is a counter-measure against spectral leakage that reduces the amplitudes of the samples at the start and end of a signal window :footcite:`lyon2009`.
This eliminates the discontinuities, helps with the periodicity of the signal and consequently reduces any leakage :footcite:`downey2014`.
Therefore, windowing is none other than a multiplication of the input signal with a predefined function.

.. math::
  :nowrap:

  \begin{eqnarray}
      S = \sum_{i=0}^{\#F-1} F[i] . w
  \end{eqnarray}

where:

- :math:`S`   : Signal array.
- :math:`\#F` : Number of frames.
- :math:`w`   : window function.


How to implement it?
~~~~~~~~~~~~~~~~~~~~
This is depending on the type of the windowing function to use as there are many.
However, since it is just a multiplication, the window samples are simply generated using a predefined function and multiplied with the signal samples.
In python this can be done easily using numpy_ which offers a wide variety of windowing_function_

Code
-----
Here is a small code snippet implementing windowing that I wrote as part of a python audio features extraction library named spafe_

.. code-block:: python
 :caption: Windowing
 :linenos:

  import numpy as np


  def windowing(frames, frame_len, win_type="hamming", beta=14):
      """
      generate and apply a window function to avoid spectral leakage.

      Args:
        frames  (array) : array including the overlapping frames.
        frame_len (int) : frame length.
        win_type  (str) : type of window to use.
                          Default is "hamming"

      Returns:
        windowed frames.
      """
      if   win_type == "hamming" : windows = np.hamming(frame_len)
      elif win_type == "hanning" : windows = np.hanning(frame_len)
      elif win_type == "bartlet" : windows = np.bartlett(frame_len)
      elif win_type == "kaiser"  : windows = np.kaiser(frame_len, beta)
      elif win_type == "blackman": windows = np.blackman(frame_len)
      windowed_frames = frames * windows
      return windowed_frames



Conclusion
~~~~~~~~~~~
This blog presented windowing, which is a fundamental signal processing technique that helps eliminate discontinuities in a the frames and consequently avoid spectral leakage.
This method is often used before any spectrum computations. There are various types of windowing, each having its own pros and cons.
In the python code introduced in this post, we included some of the most used functions but these can be customized to the user's discretion.

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

   👨‍💻 edited and review were on 08.04.202

References and Further readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. footbibliography::

.. _numpy : https://numpy.org/
.. _windowing_function : https://docs.scipy.org/doc/numpy/reference/routines.window.html
.. _spafe : https://github.com/SuperKogito/spafe
