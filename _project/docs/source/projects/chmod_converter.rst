Chmod modes Converter
=====================

-------------

This is a small chmod modes converter, to convert from octal/ numeric modes to symbolic and vice versa.
The converter is written in Javascript and its source code can be found under `chmod-converter.js`_

|

.. raw:: html

  <div class="chmod-converter">
  <form name="chmod" style="display: grid;">
  <table name="converter">
      <tbody>
          <tr>
              <td>Permissions: </td>
              <td><input type="text" name="chmod_numeric"  value="751"        size="1.75"   onkeyup="numeric2symbolic()"> </td>
              <td><input type="text" name="chmod_symbolic" value="-rwxr-x--x" size="8"  onkeyup="symbolic2numeric()"> </td>
          </tr>
      </tbody>
  </table>
  <br>
  <table name="permission-per-group">
      <tbody>
          <tr>
              <td> </td>
              <td class="chmod">Owner</td>
              <td class="chmod">Group</td>
              <td class="chmod">Other</td>
          </tr>
          <tr>
              <td class="ch2">Read</td>
              <td class="ch3"><input type="checkbox" name="ownerr" value="4" onclick="chmod2table()"></td>
              <td class="ch4"><input type="checkbox" name="groupr" value="4" onclick="chmod2table()"></td>
              <td class="ch3"><input type="checkbox" name="otherr" value="4" onclick="chmod2table()"></td>
          </tr>
          <tr>
              <td class="ch2">Write</td>
              <td class="ch3"><input type="checkbox" name="ownerw" value="2" onclick="chmod2table()"></td>
              <td class="ch4"><input type="checkbox" name="groupw" value="2" onclick="chmod2table()"></td>
              <td class="ch3"><input type="checkbox" name="otherw" value="2" onclick="chmod2table()"></td>
          </tr>
          <tr>
              <td class="ch2">Execute</td>
              <td class="ch3"><input type="checkbox" name="ownerx" value="1" onclick="chmod2table()"></td>
              <td class="ch4"><input type="checkbox" name="groupx" value="1" onclick="chmod2table()"></td>
              <td class="ch3"><input type="checkbox" name="otherx" value="1" onclick="chmod2table()"></td>
          </tr>
      </tbody>
  </table>
  </form>
  </div>
  <div class="clt">
  <center><a href="#" >chmod modes converter and interpreter</a> </center>
  </div>
  <br>



.. _`chmod-converter.js` : https://gist.github.com/SuperKogito/a67e15a7057a754dc20af42bf4f860cb
