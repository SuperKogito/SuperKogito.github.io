:og:description: Audio signal RMS normalization in Python
:og:keywords: root mean square, signal normalization, python, Audio normalization, RMS normalization, python, ayoub malek, blog post
:og:image: ../../../../_static/meta_images/spectral_leakage.png
:og:image:alt: root mean square normalization in python

Root mean square normalization in Python
========================================

.. post:: Apr 30, 2020
   :tags: Python, Augmentation, Audio
   :category: Signal processing, 2020
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

Audio normalization is a fundamental audio processing technique that consists of applying a constant amount of gain to an audio in order to bring its amplitude to a target level.
A commonly used normalization technique is the Root Mean Square (RMS) normalization. This blog post introduces RMS normalization and provides a Python implementation of it.


What is RMS normalization?
~~~~~~~~~~~~~~~~~~~~~~~~~~
In general there are two principal types of audio normalization:

- Peak normalization which adjusts the recording based on its highest signal level.
- Loudness normalization which adjusts the recording based its perceived loudness.

RMS normalization falls under the latter, where the perceived loudness level is determined using the root mean square of the signal.
The result is then used to compute the gain value used in the normalization.
Since the gain value is constant and applied across the entire recording, the normalization does not affect the signal-to-noise ratio and the relative dynamics :footcite:`shelvock`.
The approach to RMS normalization can be summarized in the following mathematical formula :footcite:`malek`:

.. math::
  :nowrap:
  :label: rms

  \begin{equation}
      y[n]=\sqrt{\frac{N-10\left(\frac{r}{20}\right)}{\sum_{i=0}^{N-1} x^{2} \left[ i\right]}} \cdot x[n]
  \end{equation}

where:

- :math:`x[n]` is the original signal.
- :math:`y[n]` is the normalized signal.
- :math:`N` is the length of :math:`x[n]`.
- :math:`r` is the input RMS level in dB.


How to implement it in Python?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Implementing the RMS normalization is fairly simple in Python and the algorithm can be summarized in the following steps:

- Read audio as an array.
- Compute the linear RMS level and its scaling factor
- Normalize using the scaling factor.
- Write the resulting array as an audio.

.. code-block:: python
   :linenos:

   def normalize(infile, rms_level=0):
       """
       Normalize the signal given a certain technique (peak or rms).
       Args:
           - infile    (str) : input filename/path.
           - rms_level (int) : rms level in dB.
       """
       # read input file
       fs, sig = read_file(filename=infile)

       # linear rms level and scaling factor
       r = 10**(rms_level / 10.0)
       a = np.sqrt( (len(sig) * r**2) / np.sum(sig**2) )

       # normalize
       y = sig * a

       # construct file names
       output_file_path = os.path.dirname(infile)
       name_attribute = "output_file.wav"

       # export data to file
       write_file(output_file_path=output_file_path,
                  input_file_name=infile,
                  name_attribute=name_attribute,
                  sig=y,
                  fs=fs)

This implementation is available as part of the Pydiogment_library_

Conclusion
~~~~~~~~~~
This blog post provided a small introduction of the RMS normalization technique, which is commonly used in speech processing to improve the quality of recordings.
We also provided a small implementation of the approach that is part of the Pydiogment_library_.

Share this blog
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
.. footbibliography::


.. _Pydiogment_library : https://github.com/SuperKogito/pydiogment/
