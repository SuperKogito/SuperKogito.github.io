:og:description: cryptography overview
:og:keywords: cryptography overview, encryption, hashing, security, ayoub malek, cybersecurity post, blog introduction
:og:image: ../../../../_static/meta_images/cryptography_overview.png
:og:image:alt: cryptography_overview

Cryptography overview
=====================

.. post:: Feb 17, 2019
   :tags: Encryption, Hashing
   :category: Cybersecurity
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

Cryptography is mostly associated with the development and creation of mathematical algorithms, which are used to insure various security aspects See :footcite:`Tamimi,Oak`.
It is the cornerstone of modern communications security and is based on various mathematical concepts and theories such as: number theory, computational complexity theory and probability theory :footcite:`Kessler`.
The following post provides a quick overview of various cryptography concepts such as encryption, decryption and hashing.

Types of cryptography algorithms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cryptography algorithms can be classified according to various criteria :footcite:`Kessler`. One can distinguish them, according to the number of their deployed keys, which results in the following three categories:

- **Secret Key Cryptography (SKC):** or “Symmetric encryption”, uses one single shared key for both encryption and decryption to provide privacy and confidentiality :footcite:`Kessler,Tamimi`.
- **Public Key Cryptography (PKC):** or “Asymmetric encryption” uses one keys couple: A public key for encryption and a private key for decryption :footcite:`Kessler`. It is essentially used for authentication, non-repudiation, and key exchange :footcite:`Tamimi`.
- **Hash Functions:** Irreversible mathematical transformations that generates a checksum/a digital fingerprint used for checking the data integrity or none-corruptness :footcite:`Kessler`.

Encryption vs Hashing
~~~~~~~~~~~~~~~~~~~~~~

**Encryption** transforms a plain-text into something unintelligible called cipher-text using a key. The essential thing about encryption is that it is reversible :footcite:`Oak`.
A unique cipher-text & plain-text couple can be determined using encryption, decryption and a key. Encryption is used essentially in confidentiality.
For example, in an electronic exchange, you encrypt messages to prevent a third party lacking the key from reading the messages :footcite:`Ssl`.

**Hashing**, unlike encryption, transforms the input data into a (usually fixed length) sequence of characters often called checksum/hash-sum or a tag.
Moreover, hashing is a one-way operation that does not require a key and so the quality of a hashing algorithm depends on the uniqueness of the generated hashes.
Two different messages with the same hash values are a case of “collision”. Hashing is used to maintain data integrity :footcite:`Ssl`.
For example, if a hash sum is generated based on a message text, any future changes on the text would be detected due the mismatch between the previously generated hash and the current one.

Encryption and Decryption
~~~~~~~~~~~~~~~~~~~~~~~~~~

Encryption transforms a plain-text into a cipher-text using an encryption key. The process of reversing this operation uses also a key and is called "decryption" :footcite:`Kessler`.
These operations can be explained by the following formulas: :math:`C=E_{k}(P)` and :math:`P=D_{k}(C)`, where P = plain-text, C = cipher-text, E = the encryption method, D = the decryption method, and k = the key :footcite:`Kessler`.
There exist several types of encryption (**symmetric/asymmetric**) and several ciphering techniques (**block/stream**) and modes etc :footcite:`Kessler`.
The major differences between those will be explained in the following post :ref:`encryption-post-label`.

A summary of cryptography algorithms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are several practical implementations and algorithms of the aforementioned concepts.
Some of these are widely used standards defined by the National Institute of Standards and Technology (NIST) such the Advanced Encryption Standard (AES) and the Secure Hashing Algorithm (SHA) etc.
The most known algorithms are summarized below:

|

.. raw:: html

    <div class="clt">
    <ul>
       Cryptographic algorithms
            <ul>
                 <li> Symmetric encryption
                      <ul>
                          <li> Block cipher
                              <ul>
                                  <li> AES </li>
                                  <li> DES </li>
                                  <li> Twofish </li>
                                  <li> Blowfish </li>
                              </ul>
                          </li>

                          <li> Stream cipher
                              <ul>
                                  <li> RC4 </li>
                                  <li> ChaCha </li>
                              </ul>
                          </li>
                     </ul>
                </li>

                <li> Asymmetric encryption
                    <ul>
                        <li> RSA </li>
                        <li> ECC </li>
                    </ul>
                </li>

                <li> Hashing functions
                    <ul>
                        <li> RSA </li>
                        <li> ECC </li>
                    </ul>
                </li>
            </ul>
    </ul>
    <center>Figure 1: Cryptographic algorithms</center>
    </div>

Share this blog
~~~~~~~~~~~~~~~~

.. raw:: html

  <div id="share">
    <a class="facebook" href="https://www.facebook.com/share.php?u=https://superkogito.github.io/blog/2019/02/17/cryptography_overview.html&title=Cryptography%20overview"                target="blank"><i class="fa fa-facebook"></i></a>
    <a class="twitter"  href="https://twitter.com/intent/tweet?url=https://superkogito.github.io/blog/2019/02/17/cryptography_overview.html&text=Cryptography%20overview"                 target="blank"><i class="fa fa-twitter"></i></a>
    <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&url=https://superkogito.github.io/blog/2019/02/17/cryptography_overview.html&title=Cryptography%20overview" target="blank"><i class="fa fa-linkedin"></i></a>
    <a class="reddit"   href="http://www.reddit.com/submit?url=https://superkogito.github.io/blog/2019/02/17/cryptography_overview.html&title=Cryptography%20overview"                    target="blank"><i class="fa fa-reddit"></i></a>
  </div>


.. update:: 18 Apr 2022

   👨‍💻 edited and review were on 08.04.202

References and Further readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. footbibliography::
