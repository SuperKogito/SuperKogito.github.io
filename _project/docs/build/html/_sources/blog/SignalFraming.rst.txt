[25-01-2020] Signal framing
============================

.. meta::
   :description: Audio signal framing/ frame blocking
   :keywords: framing, frame blocking, Ayoub Malek, Blogging
   :author: Ayoub Malek


.. post:: Jan 25, 2020
   :tags: [Signal processing]
   :category: Signal processing
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

When it comes to non-stationary signals, spectral features in short parts/ sequences are of great use.
Therefore, decomposing the signal into multiple ranges is the way to go about this type of features extraction.
This technique is known as frame blocking or framing. The following blog explains why do we need framing and how to do it in python.

| *** keywords:  *** Framing, Frame blocking

What is framing ?
-----------------
Frame blocking or framing is a fundamental signal processing technique that consists of dividing
the original signal into :math:`\#F` blocks often called frames with length :math:`N_f` an overlap :math:`M` and a framing hop :math:`H (H = N_f - M)`.
Overlapping the frames help avoiding information loss in between adjacent frames.

|

.. image:: ../_static/blog-plots/framing.png
   :align: center
   :scale: 85%

.. raw:: html

   <center><a href="../figures/fig16.html" >Figure 16: Framing</a> </center>
   </div>


Assuming a signal :math:`S = \sum_{n=0}^{N_s-1} x[n]`, this can be mathematically formulated as follows:
:math:`S = \sum_{n=0}^{N_s} X[n] = \sum_{i=0}^{\#F-1} F[i]` where:

- :math:`S`: Discrete signal.
- :math:`x[n]`: Signal samples in time domain.
- :math:`N_s` : Signal length in samples.
- :math:`f[i]`: Signal frame.
- :math:`\#F` : Number of frames.

Why do we do need framing?
--------------------------
Speech is a non-stationary signal, consequently its statistical properties are not constant over time.
Therefore, its spectral features and other characteristic properties (for example: short-time energy, MFCC etc.) should be extracted from small blocks of the signal.
This is based on the assumption that is the signal is stationary (i.e.  its  statistical properties  are  constant  within this region) in this small frame :cite:`deller`.
On top of it all, frame blocking is often used in real-time systems as it maximizes the efficiency of the system by distributing the fixed process overhead across many samples :cite:``.


How to implement it?
---------------------
The first approach is pretty straight forward and can be summarized in the following steps:

- **Convert hop step and fame length from seconds to samples.**

  To understand this, we need to comprehend the terminology and the difference between a **frame** & a  **sample**.
  Assume a discrete audio signal with  a duration of 3 seconds and a sampling rate of 8 KHz.
  The sampling rate define the the number of samples/ signal measurements per second.
  8 KHz translates to 8000 Hz = 8000 1/s = 8000 **sample** per second.
  So in this case, the signal has 3 x 8000 = 24 000 sample.
  On the other hand, a **frame** is a part of the signal or a series of consecutive samples.
  A 1 second-long, in this case, contains 1 x 8000 = 8000 samples.
  In order to convert the values of the framing hop and length from seconds to samples, we just need to multiply by sampling rate.

  - frame_hop_in_samples = sampling_rate x frame_hop_in_seconds
  - frame_length_in_samples = sampling_rate x frame_length_in_seconds

- **Compute the expected number of frames.**

  The expected number of frames can be compute using the following formula:

  .. math::
    :nowrap:

    \begin{eqnarray}
        \#F =  \left\lfloor \frac{N_s - M}{N_f - M} \right\rfloor
    \end{eqnarray}

  where:

  - :math:`\#F` : Number of frames.
  - :math:`N_s` : Signal length in samples.
  - :math:`N_f` : Frame length in samples.
  - :math:`M`   : Frames overlap.

- **Pad signal if needed.**
  Sometimes, it happens that the signal need to be padded in order to include all samples in frames with equal length.
  Therefore, we also compute the number of rest samples, which equivalent to the amount of samples missing from the last frame to be equally long as the other frames.
  This value will be used in the padding of the last frame, so that all frames will be equally long.

  .. math::
    :nowrap:

    \begin{eqnarray}
        \#R =  \left\lfloor (N_s - M) \bmod (N_f - M) \right\rfloor
    \end{eqnarray}

  where:

  - :math:`\#R` : Number of rest samples.
  - :math:`N_s` : Signal length in samples.
  - :math:`N_f` : Frame length in samples.
  - :math:`M`   : Frames overlap.

  Consequently, the number of samples to pad the signal is equal to :math:`N_f - \#R` and :math:`\#F = \#F + 1`

- **Compute frames indices.**
  There are various ways to do this, but once you have the number frames and their lengths, it is only a matter of computing and where each frame starts and finishes.

- **Get frames**

Code
-----
The previously listed steps, can be implemented in Python as follows:

.. code-block:: python
 :caption: Framing 1
 :linenos:

  import numpy as np


  def framing(sig, fs=16000, win_len=0.025, win_hop=0.01):
      """
      transform a signal into a series of overlapping frames.

      Args:
          sig            (array) : a mono audio signal (Nx1) from which to compute features.
          fs               (int) : the sampling frequency of the signal we are working with.
                                   Default is 16000.
          win_len        (float) : window length in sec.
                                   Default is 0.025.
          win_hop        (float) : step between successive windows in sec.
                                   Default is 0.01.

      Returns:
          array of frames.
          frame length.
      """
      # compute frame length and frame step (convert from seconds to samples)
      frame_length = win_len * fs
      frame_step = win_hop * fs
      signal_length = len(sig)
      frames_overlap = frame_length - frame_step

      # Make sure that we have at least 1 frame+
      num_frames = np.abs(signal_length - frames_overlap) // np.abs(frame_length - frames_overlap)
      rest_samples = np.abs(signal_length - frames_overlap) % np.abs(frame_length - frames_overlap)

      # Pad Signal to make sure that all frames have equal number of samples
      # without truncating any samples from the original signal
      if rest_samples != 0:
          pad_signal_length = int(frame_step - rest_samples)
          z = np.zeros((pad_signal_length))
          pad_signal = np.append(sig, z)
          num_frames += 1
      else:
          pad_signal = sig

      # make sure to use integers as indices
      frame_length = int(frame_length)
      frame_step = int(frame_step)
      num_frames = int(num_frames)

      # compute indices
      idx1 = np.tile(np.arange(0, frame_length), (num_frames, 1))
      idx2 = np.tile(np.arange(0, num_frames * frame_step, frame_step),
                     (frame_length, 1)).T
      indices = idx1 + idx2
      frames = pad_signal[indices.astype(np.int32, copy=False)]
      return frames

|

Alternatively, one can use the stride trick and use a sliding window technique that is
already implemented in matlab to get a much faster framing. This is done like the following.


.. code-block:: python
  :caption: Framing 2
  :linenos:

   import numpy as np



   def stride_trick(a, stride_length, stride_step):
       """
       apply framing using the stride trick from numpy.

       Args:
           a (array) : signal array.
           stride_length (int) : length of the stride.
           stride_step (int) : stride step.

       Returns:
           blocked/framed array.
       """
       nrows = ((a.size - stride_length) // stride_step) + 1
       n = a.strides[0]
       return np.lib.stride_tricks.as_strided(a,
                                              shape=(nrows, stride_length),
                                              strides=(stride_step*n, n))


   def framing(sig, fs=16000, win_len=0.025, win_hop=0.01):
       """
       transform a signal into a series of overlapping frames (=Frame blocking).

       Args:
           sig     (array) : a mono audio signal (Nx1) from which to compute features.
           fs        (int) : the sampling frequency of the signal we are working with.
                             Default is 16000.
           win_len (float) : window length in sec.
                             Default is 0.025.
           win_hop (float) : step between successive windows in sec.
                             Default is 0.01.

       Returns:
           array of frames.
           frame length.

       Notes:
       ------
           Uses the stride trick to accelerate the processing.
       """
       # run checks and assertions
       if win_len < win_hop: print("ParameterError: win_len must be larger than win_hop.")

       # compute frame length and frame step (convert from seconds to samples)
       frame_length = win_len * fs
       frame_step = win_hop * fs
       signal_length = len(sig)
       frames_overlap = frame_length - frame_step

       # compute number of frames and left sample in order to pad if needed to make
       # sure all frames have equal number of samples  without truncating any samples
       # from the original signal
       rest_samples = np.abs(signal_length - frames_overlap) % np.abs(frame_length - frames_overlap)
       pad_signal = np.append(sig, np.array([0] * int(frame_step - rest_samples) * int(rest_samples != 0.)))

       # apply stride trick
       frames = stride_trick(pad_signal, int(frame_length), int(frame_step))
       return frames, frame_length


Conclusion
-------------
This blog presented framing, which is a fundamental signal processing technique to that divides a signal into multiple, equally sized, blocks.
The resulting blocks are considered stationary over time, which helps extract useful characterizing features of the signal.
This operation can be implemented in python in a classical fashion or using the stride trick for a fast processing.


References and Further readings
--------------------------------

.. bibliography:: references/framing_refs.bib
   :cited:
