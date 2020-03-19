Table 3: Wave file structure and content
========================================

-----------------------

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

.. raw:: html

  <div class="clt">
  <br>
  <center><a href="table4.html" >Table : Wave file structure and content </a> <a class="reference internal" href="#digaud" id="id1">[topherleecom]</a></center>
  </div>
