:og:description: Audio signal FFmpeg piping + pass it a Python variable
:og:keywords: ffmpeg, pipe, python, audio, Ayoub Malek, blog post
:og:image: ../../../../_static/meta_images/ffmpeg_pipe.png
:og:image:alt: ffmpeg_pipe

How to pipe an FFmpeg output and pass it to a Python variable?
==============================================================

.. post:: Mar 19, 2020
   :tags: Python, Ffmpeg, Audio
   :category: Signal processing
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

When writing code, the key optimization points are speed and efficiency.
I often face this dilemma when using FFmpeg with Python.
For example: when I need to convert an mp3 to a wave file and then do some processing to it in Python.
The simple way to  do this, is by using FFmpeg to convert the mp3 input to a wave, then read the wave in Python and do process it.
Although this works, but clearly it is neither optimal nor the fastest solution.
In this blog post, I will present an improved solution to this inconvenience by piping the output of FFmpeg to Python and directly pass it to a numpy variable.

| *** keywords:  *** FFmpeg pipe output


Piping the FFmpeg output
~~~~~~~~~~~~~~~~~~~~~~~~
Assuming a simple task of converting an mp3 file to a wave using FFmpeg, which can be done using the following shell command:

.. code-block:: shell

 $ ffmpeg -i mp3_path -o wav_path

This results in a wave file saved under :code:`wav_path`.
Alternatively, we can pipe the output and return it as an output instead of writing it to a file.
This can be done using the following shell command:

.. code-block:: shell

 $ ffmpeg -i mp3_path -f wav pipe:1

At this point, executing this command results in a binary mess printed in your terminal, but we will make sense of the output in a second.

Reading the FFmpeg output in Python as a numpy variable?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FFmpeg shell commands can be executed in python with the help of the subprocess package and the resulting output can read from the subprocess pipe.
The following code snippet shows how is this done.

.. code-block:: python
 :linenos:

  import subprocess
  import numpy as np

  # init command
  ffmpeg_command = ["ffmpeg", "-i", mp3_path,
                    "-ab", "128k", "-acodec", "pcm_s16le", "-ac", "0", "-ar", target_fs, "-map",
                    "0:a", "-map_metadata", "-1", "-sn", "-vn", "-y",
                    "-f", "wav", "pipe:1"]

  # excute ffmpeg command
  pipe = subprocess.run(ffmpeg_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        bufsize=10**8)

  # debug
  print(pipe.stdout, pipe.stderr)

  # read signal as numpy array and assign sampling rate
  audio_np = np.frombuffer(buffer=pipe.stdout, dtype=np.uint16, offset=8*44)
  sig, fs  = audio_np, target_fs


Note that the used FFmpeg command is slightly changed, to define the channel of choice and the encoding to use.
For more on that you can refer either to :footcite:`zulko` or :footcite:`ffmpeg`.
We also define a buffer size to receive the read data.
The read data is essentially a wave file data including the header which must be ignored when passing the data to the
numpy variable. In order to know how many bytes to ignore, we need to examine the following table :footcite:`digaud` of the wave data:

|

.. list-table:: Table 4: Wave file structure and content
   :widths: 10 15 75
   :header-rows: 1

   * - Positions
     - Sample Value
     - Description
   * - 1 - 4
     - RIFF
     - Marks the file as a riff file.  Characters are each 1 byte long.
   * - 5 - 8
     - File size (integer)
     - Size of the overall file - 8 bytes, in bytes (32-bit integer).  Typically, you'd fill this in after creation.
   * -  9 - 12
     - "WAVE"
     - File Type Header.  For our purposes, it always equals "WAVE".
   * - 13 - 16
     - "fmt "
     - Format chunk marker.  Includes trailing null
   * - 17 - 20
     - 16
     - Length of format data as listed above
   * - 21 - 22
     - 1
     - Type of format (1 is PCM) - 2 byte integer
   * -  23 - 24
     -  2
     -  Number of Channels - 2 byte integer
   * -  25 - 28
     -  44100
     -  Sample Rate - 32 byte integer.  Common values are 44100 (CD), 48000 (DAT).  Sample Rate = Number of Samples per second, or Hertz.
   * -  29 - 32
     -  176400
     - (Sample Rate * BitsPerSample * Channels) / 8.
   * -  33 - 34
     -  4
     - (BitsPerSample * Channels) / 8.1 - 8 bit mono2 - 8 bit stereo/16 bit mono4 - 16 bit stereo
   * -  35 - 36
     -  16
     -  Bits per sample
   * - 37 - 40
     - "data"
     - "data" chunk header.  Marks the beginning of the data section.
   * -  41 - 44
     -  File size (data)
     -  Size of the data section.
   * -  45
     - ..
     - Sample values are given above for a 16-bit stereo source.

In the above table we notice that the audio data bytes start at byte 45 and therefore the first 44 bytes are the offset.

Conclusion
~~~~~~~~~~
This blog post introduced a small example of reading the ffmpeg command pipe output and parsing the resulting wave data into a numpy array.
This approach is a simpler and faster alternative to the classical convert, save then read.


Share this blog
~~~~~~~~~~~~~~~~

.. raw:: html

  <div id="share">
    <a class="facebook" href="https://www.facebook.com/share.php?u=https://superkogito.github.io/blog/2020/03/19/ffmpeg_pipe.html&title=How%20to%20pipe%20an%20FFmpeg%20output%20and%20pass%20it%20to%20a%20Python%20variable?"                target="blank"><i class="fa-brands fa-facebook"></i></a>
    <a class="twitter"  href="https://twitter.com/intent/tweet?url=https://superkogito.github.io/blog/2020/03/19/ffmpeg_pipe.html&text=How%20to%20pipe%20an%20FFmpeg%20output%20and%20pass%20it%20to%20a%20Python%20variable?"                 target="blank"><i class="fa-brands fa-twitter"></i></a>
    <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&url=https://superkogito.github.io/blog/2020/03/19/ffmpeg_pipe.html&title=How%20to%20pipe%20an%20FFmpeg%20output%20and%20pass%20it%20to%20a%20Python%20variable?" target="blank"><i class="fa-brands fa-linkedin"></i></a>
    <a class="reddit"   href="http://www.reddit.com/submit?url=https://superkogito.github.io/blog/2020/03/19/ffmpeg_pipe.html&title=How%20to%20pipe%20an%20FFmpeg%20output%20and%20pass%20it%20to%20a%20Python%20variable?"                    target="blank"><i class="fa-brands fa-reddit"></i></a>
  </div>


.. update:: 8 Apr 2022

   👨‍💻 edited and review were on 08.04.202

References and Further readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. footbibliography::
