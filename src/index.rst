.. superkogito documentation master file, created by
   sphinx-quickstart on Mon Apr  4 18:32:55 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Home
====
.. meta::
  :description: This is the homepage of Ayoub Malek's blog and website
  :keywords: Ayoub Malek, Ayoub, Malek, Ayoub Malek Blog, Ayoub Malek Website, SuperKogito, Ayoub SuperKogito
  :author: Ayoub Malek


.. toctree::
   :maxdepth: 5
   :hidden:

   index
   projects
   blog
   about


Welcome to my personal website and blog 💙

List of posts
--------------

.. postlist:: 10
  :author: Ayoub Malek
  :language: en
  :date: %Y-%m-%d
  :format: {date} {title}
  :list-style: circle


Publications
------------

- Malek, A., (2023). Spafe: Simplified python audio features extraction. Journal of Open Source Software, 8(81), 4739, https://doi.org/10.21105/joss.04739


Libraries
---------

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - `Zorch`_
     - Zorch implements the basic deep learning concepts in the Zig programming language.
   * - `fastft`_
     - Fastft aims to provide a Short Time Fourier Transform implementation similar to Python's Librosa implementation in C. The STFT is demoed in a machine learning example (e.g. Mean Opinion Score Neural Network).
   * - `Spafe`_
     - spafe aims to simplify features extractions from mono audio files. The library can extract of the following features: BFCC, LFCC, LPC, LPCC, MFCC, IMFCC, MSRCC, NGCC, PNCC, PSRCC, PLP, RPLP, Frequency-stats etc. It also provides various filterbank modules (Mel, Bark and Gammatone filterbanks) and other spectral statistics.
   * - `Pydiogment`_
     - Pydiogment aims to simplify audio augmentation. It generates multiple audio files based on a starting mono audio file. The library can generates files with higher speed, slower, and different tones etc.



.. _`Zorch`: https://superkogito.github.io/Zorch
.. _`Fastft`: https://superkogito.github.io/fastft
.. _`Spafe`: https://superkogito.github.io/spafe
.. _`Pydiogment`: https://superkogito.github.io/pydiogment
