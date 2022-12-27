:og:description: convert chmod modes to octal and back to letters
:og:keywords: chmod, chmod modes, octal, symbolic, rwx, python, ayoub malek, blog post
:og:image: ../../../../_static/meta_images/chmod_modes.png
:og:image:alt: chmod_modes_from_symbolic_to_octal_and_back

Chmod modes: from symbolic to octal and back
=============================================

.. post:: Oct 25, 2020
   :tags: Linux, Bash
   :category: linux
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

Often you will be faced with permission limitations, that will hinder you from manipulating a certain file or directory.
To overcome this on Unix-based systems, one can use the **chmod** command to edit permissions and enable more manipulations possibilities.
In this blog, we examine the **chmod** command and its different modes.


Viewing file permissions
~~~~~~~~~~~~~~~~~~~~~~~~
Chmod is part of the essentials packet coreutils_, which comes as part of Ubuntu.
Before getting to changing some file's permissions, we need first to determine them.
For that you can use the following command :code:`ls -l [filename]` or -*if you don't want to see any extra unrelated information*- use :code:`ls -l [filename] | awk {'print $1"    "$9'}`.

Understanding file permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
File permissions can be defined in two modes, each divided in 3 user categories:

- **Symbolic mode** : In this mode each user category [u, g, o] and permission/right [r, w, x] is defined using a combination of letters, where **r** stands for read rights, **w** for write rights and **x** for execution rights.
- **Octal mode** : In this mode the rights are defined using a three-digit octal number, where each digit represents the rights of a certain user category.

+-----------------------------+-----------------+---------------+
| User category               | Symbolic mode   | Octal mode    |
+-----------------------------+-----------------+---------------+
| Owner                       |  u              | 1. digit      |
+-----------------------------+-----------------+---------------+
| Group                       |  g              | 2. digit      |
+-----------------------------+-----------------+---------------+
| Other                       |  o              | 3. digit      |
+-----------------------------+-----------------+---------------+
| all: Owner, Group and Other |  a              |               |
+-----------------------------+-----------------+---------------+

.. raw:: html

  <div class="clt">
  <center><a href="../tables/table5.html" >Table 5: User categories representation in symbolic and octal modes </a> </center>
  </div>

Converting chmod permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Chmod changes the permissions of a given file/ directory according a to a rights description in a certain mode.
A mode can be octal (description with numbers) or symbolic (description with letters).
Whereas letters are easier to understand, octals are more practical and conversion from one mode to another can be done as follows:

- :math:`\text{r = 4}`
- :math:`\text{w = 2}`
- :math:`\text{x = 1}`

the :math:`\textbf{-}` stands for not defined so in a way, you can use: :math:`\textbf{- = 0}`

  To give an example of how this conversion works. Assume you have the following permissions :math:`\text{-rwx-wx--x}`.
  First you divide the permission string in the three sub-groups after skipping the first character used to reflect the type of the file/ directory.
  For the resulting three groups, characters are substituted with their integer values and each group values are summed.
  The resulting code is:

  - :math:`\small{\text{rwx: r + w + x = 4 + 2 + 1 = 7}}`
  - :math:`\small{\text{-wx: - + w + x = 0 + 2 + 1 = 3}}`
  - :math:`\small{\text{--x: - + - + x = 0 + 0 + 1 = 1}}`

  so the resulting octal code is :math:`\text{731}`.

The following converter tool can be used to compute the symbolic/ octal code to describe a certain set of rules/ permissions:

.. raw:: html

  <div class="chmod-converter">
  <form name="chmod" style="display: grid;">
  <table name="converter" class="docutils align-default">
  <colgroup>
  <col style="width: 50%">
  <col style="width: 25%">
  <col style="width: 25%">
  </colgroup>
      <tbody>
          <tr>
              <td>Permissions: </td>
              <td><input type="text" name="chmod_numeric"  value="751"        size="8"   onkeyup="numeric2symbolic()"> </td>
              <td><input type="text" name="chmod_symbolic" value="-rwxr-x--x" size="12"  onkeyup="symbolic2numeric()"> </td>
          </tr>
      </tbody>
  </table>
  <br>

  <table name="permission-per-group" class="docutils align-default">
  <colgroup>
  <col style="width: 50%">
  <col style="width: 15%">
  <col style="width: 15%">
  <col style="width: 15%">
  </colgroup>
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
  <center><a href="../../../../projects/chmod_converter.html" > chmod modes converter and interpreter</a> </center>
  </div>



Changing chmod permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to change the permissions of a file (file.sh for example) or directory using chmod, you can use any of the following commands:

- In **symbolic** mode: :code:`chmod u=rwx,g=rw-,o=r-- file.sh`
- In **octal** mode:    :code:`chmod 764 file.sh`

One can also edit an already defined permission with the help of the following operators **+**, **-** and **=**. The following list includes some examples, that illustrate the use of those operators:


- :code:`chmod a+x file.sh` or :code:`chmod ugo+x file.sh` or :code:`chmod +x file.sh` allow file to be executed by all user categories (any user). So if the initial file permissions was :code:`-rw-rw-r--`, after running the permissions, the resulting permissions is :code:`-rwxrwxr-x`.
- :code:`chmod o+w file.sh` allow other users to write/ edit the file. So if the initial file permissions was :code:`-rw-rw-r--`, after running the permissions, the resulting permissions is :code:`-rw-rw-rw-`.
- :code:`chmod g-w file.sh` deny groups to write/edit the file. So if the initial file permissions was :code:`-rw-rw-r--`, after running the permissions, the resulting permissions is :code:`-rw-r--r--`.
- :code:`chmod o=r file.sh`	allow other uses only to read the file.
- :code:`chmod a-w file.sh` deny write permission to everyone.
- :code:`chmod go+rw file.sh` make a file readable and writable by the group and other users.  So if the initial file permissions was :code:`-rwx---r--`, after running the permissions, the resulting permissions is :code:`-rwxrw-rw-`.

Additionally, you can use the **-R** argument to change permissions recursively or combine **chmod** with the `find`_ command to change permissions of multiple files. For more on **chmod** check its manual using :code:`man chmod`.

Conclusion
~~~~~~~~~~

This blog post provided a small introduction to the **chmod** function used to change files/directories permissions.
Moreover, the post included a description of the different modes used with chmod and how to convert from one to the other.

Share this blog
~~~~~~~~~~~~~~~~

.. raw:: html

  <div id="share">
    <a class="facebook" href="https://www.facebook.com/share.php?u=https://superkogito.github.io/blog/2020/10/25/chmod_modes.html&title=Chmod%20modes:%20from%20symbolic%20to%20octal%20and%20back"                target="blank"><i class="fa fa-facebook"></i></a>
    <a class="twitter"  href="https://twitter.com/intent/tweet?url=https://superkogito.github.io/blog/2020/10/25/chmod_modes.html&text=Chmod%20modes:%20from%20symbolic%20to%20octal%20and%20back"                 target="blank"><i class="fa fa-twitter"></i></a>
    <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&url=https://superkogito.github.io/blog/2020/10/25/chmod_modes.html&title=Chmod%20modes:%20from%20symbolic%20to%20octal%20and%20back" target="blank"><i class="fa fa-linkedin"></i></a>
    <a class="reddit"   href="http://www.reddit.com/submit?url=https://superkogito.github.io/blog/2020/10/25/chmod_modes.html&title=Chmod%20modes:%20from%20symbolic%20to%20octal%20and%20back"                    target="blank"><i class="fa fa-reddit"></i></a>
  </div>


.. update:: 8 Apr 2022

   👨‍💻 edited and review were on 08.04.2022

References and Further readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- chmod, ss64, https://ss64.com/bash/chmod.html
- chmod, ubuntuusers, https://wiki.ubuntuusers.de/chmod/
- chmod, Wikipedia, https://en.wikipedia.org/wiki/Chmod


.. raw:: html

  <script src="../../../../_static/js/chmod-converter.js"></script>


.. _coreutils : https://www.gnu.org/software/coreutils/
.. _find : https://ss64.com/bash/find.html
