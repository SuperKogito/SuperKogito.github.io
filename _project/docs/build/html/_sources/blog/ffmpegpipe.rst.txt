[19-03-2020] How to pipe an FFmpeg output and pass it to a Python variable?
===========================================================================

.. meta::
   :description: Audio signal FFmpeg piping + pass it a Python variable
   :keywords: framing, frame blocking, Ayoub Malek, Blogging
   :author: Ayoub Malek


.. post:: Mar 19, 2020
   :tags: [Signal processing]
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
------------------------
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
--------------------------------------------------------
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
For more on that you can refer either to :cite:`zulko` or :cite:`ffmpeg`.
We also define a buffer size to receive the read data.
The read data is essentially a wave file data including the header which must be ignored when passing the data to the
numpy variable. In order to know how many bytes to ignore, we need to examine the following table :cite:`digaud` of the wave data:

|

.. raw:: html

  <table summary="WAV File Header" class="wav">
  <tbody>
  <tr>
   <td width="10%">  Positions     </td>
   <td width="15%">  Sample Value  </td>
   <td width="75%">  Description   </td>
  </tr>

  <tr>
   <td>   1 - 4   </td>
   <td>  "RIFF"   </td>
   <td>  Marks the file as a riff file.  Characters are each 1 byte long. </td>
  </tr>

  <tr>
   <td> 5 - 8 </td>
   <td> File size (integer) </td>
   <td> Size of the overall file - 8 bytes, in bytes (32-bit integer).  Typically, you'd fill this in after creation. </td>
  </tr>

  <tr>
   <td>  9 - 12  </td>
   <td> "WAVE"  </td>
   <td> File Type Header.  For our purposes, it always equals "WAVE". </td>
  </tr>

  <tr>
   <td> 13 - 16  </td>
   <td> "fmt " </td>
   <td> Format chunk marker.  Includes trailing null </td>
  </tr>

  <tr>
   <td> 17 - 20 </td>
   <td> 16    </td>
   <td> Length of format data as listed above </td>
  </tr>

  <tr>
   <td> 21 - 22 </td>
   <td> 1     </td>
   <td> Type of format (1 is PCM) - 2 byte integer </td>
  </tr>
  <tr>
   <td>  23 - 24    </td>
   <td>  2        </td>
   <td>  Number of Channels - 2 byte integer </td>
  </tr>

  <tr>
   <td>  25 - 28 </td>
   <td>  44100 </td>
   <td>  Sample Rate - 32 byte integer.  Common values are 44100 (CD), 48000 (DAT).  Sample Rate = Number of Samples per second, or Hertz. </td>
  </tr>

  <tr>
   <td>  29 - 32  </td>
   <td>  176400 </td>
   <td> (Sample Rate * BitsPerSample * Channels) / 8. </td>
  </tr>

  <tr>
   <td>  33 - 34 </td>
   <td>  4     </td>
   <td> (BitsPerSample * Channels) / 8.1 - 8 bit mono2 - 8 bit stereo/16 bit mono4 - 16 bit stereo </td>
  </tr>

  <tr>
   <td>  35 - 36 </td>
   <td>  16    </td>
   <td>  Bits per sample </td>
  </tr>

  <tr>
   <td> 37 - 40  </td>
   <td> "data" </td>
   <td> "data" chunk header.  Marks the beginning of the data section. </td>
  </tr>

  <tr>
   <td>  41 - 44 </td>
   <td>  File size (data) </td>
   <td>  Size of the data section. </td>
  </tr>

  <tr>
    <td>  45 - .. </td>
    <td colspan="2"> Sample values are given above for a 16-bit stereo source. </td>
  </tr>
  </tbody>
  </table>
  <div class="clt">
  <br>
  <center><a href="../tables/table4.html" >Table 4: Wave file structure and content </a> <a class="reference internal" href="#digaud" id="id1">[topherleecom]</a></center>
  </div>

In the above table we notice that the audio data bytes start at byte 45 and therefore the first 44 bytes are the offset.

Conclusion
-------------
This blog post introduced a small example of reading the ffmpeg command pipe output and parsing the resulting wave data into a numpy array.
This approach is a simpler and faster alternative to the classical convert, save then read.

References and Further readings
--------------------------------

.. bibliography:: references/ffmpegpipe.bib
   :cited:
