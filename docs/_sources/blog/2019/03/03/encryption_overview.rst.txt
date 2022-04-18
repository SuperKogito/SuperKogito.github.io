:og:description: encryption introduction
:og:keywords: encryption overview, encryption, security, ayoub malek, cybersecurity
:og:image: ../../../../_static/meta_images/encryption_overview.png
:og:image:alt: encryption_overview

.. _encryption-post-label:

Encryption overview
===================

.. post:: Mar 03, 2019
   :tags: Encryption
   :category: Cybersecurity
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

Encryption transforms a plain-text into a cipher-text using an encryption key. The process of reversing this operation uses also a key and is called "decryption" :footcite:`Kessler`.
These operations can be explained by the following formulas: :math:`C=E_{k}(P)` and :math:`P=D_{k}(C)`, where P = plain-text, C = cipher-text, E = the encryption method, D = the decryption method, and k = the key :footcite:`Kessler`.
There exist several types of encryption (symmetric/asymmetric) and several ciphering techniques (block/stream) and modes etc :footcite:`Kessler`.

Symmetric Encryption
~~~~~~~~~~~~~~~~~~~~
In secret key cryptography, both parties (a sender and a receiver for example) agree on a single secret (shared) key for encryption and decryption :footcite:`Kessler`. The major concern in this case is to securely share the key between the two peers or else the whole system is jeopardized :footcite:`Tamimi`.
The key management for this encryption is troublesome, especially if a unique secret key is used for each peer-to-peer connection, which results in n(n-1)/2 total number of keys for n-nodes :footcite:`Ssl,Oak`. Symmetric encryption schemes are generally defined as stream ciphers or block ciphers :footcite:`Tamimi`.

Asymmetric Encryption
~~~~~~~~~~~~~~~~~~~~~
It also known as Public Key Cryptography (PKC) :footcite:`Kessler`. It has been considered the most significant development in cryptography in the last 300-400 years. PKC employs two separate keys:

- **The public key:** which is used to encrypt data by anyone.
- **The private key:** which is kept secret and is used to decrypt data.

This double key feature surmounts the symmetric encryption problem of managing keys, but also makes it mathematically more prone to attacks :footcite:`Tamimi`.
Moreover, this duality provides authentication and non-repudiation with the assumption that the private key is kept secret :footcite:`Kessler`.
However, asymmetric encryption techniques are way slower than symmetric techniques, and they require more computational processing power :footcite:`Ssl,Kessler`.\\
It is obvious that each of these two approaches (symmetric/asymmetric) provide a set of advantages and limitations, therefore a hybrid scheme is the best compromise.
Such scheme would apply asymmetric encryption for the secret key distribution and symmetric encryption for the generic data exchange.

Block Ciphers
^^^^^^^^^^^^^
In block ciphers the data is encrypted and decrypted one block at a time using the same key :footcite:`Oak,Tamimi`.
In its simplest mode (Electronic codebook mode), the plain text is divided into equally long blocks, which are then fed into the cipher system to produce blocks of cipher text :footcite:`Kessler`. This type of ciphers requires padding before encryption to ensure that the data length is a multiple of the block’s length. Block ciphers can operate in one of several modes; here are the most famous ones are: Electronic Codebook (ECB) mode, Cipher Block Chaining (CBC), Cipher Feedback (CFB, Output Feedback (OFB) etc.

Although CBC, CFB and OFB have good resistance against brute-force and deletion attacks, they are not very resistant to single bit errors which will propagate through different blocks in some modes :footcite:`Kessler`.
On top of all, there is also \textbf{the Counter (CTR) mode` is a relatively modern approach that provides a good compromise.
Like CFB and OFB, it operates on the blocks as in a stream cipher but also it processes them independently as in ECB :footcite:`Kessler`.
Using different key inputs, CTR guarantees resistance against brute forcing. Moreover, it allows parallel processing making it superior on performance and speed level.

Stream Ciphers
^^^^^^^^^^^^^^
Unlike block ciphers, stream ciphers operate on streams of data bit by bit :footcite:`Tamimi`.
A stream cipher consists essentially of a key stream generator and a mixing function :footcite:`Kessler`.
The mixing function is usually a XOR, and the key stream generator is the main unit of the encryption :footcite:`Kessler,Tamimi`.
There are several types of stream ciphers but only two are worth mentioning here:

- **Self-synchronizing stream cipher** calculate each bit in the key-stream by using the previous n bits in the key-stream. In this approach the decryption and encryption are synchronized, which causes problematic propagation errors :footcite:`Kessler`.
- **Synchronous stream ciphers** generate the key-stream independently and use the same generation function at both sender and receiver :footcite:`Tamimi`. While in this case propagation errors are not an issue, their periodic nature (The key-stream will eventually repeat) poses a vulnerability that can be exploited :footcite:`Kessler`.

Padding
~~~~~~~~~
Within the context of classical cryptography, padding aims essentially to prevent any type of predictability that might reveal a plain-text or its exact length.
Such revelations can be beneficial for an attacker and help in breaking the encryption :footcite:`Welchman`.
For example, Advanced Encryption Standard-128 (AES-128) is a symmetric block cipher that processes data by blocks of 128 bits, which means that additional random data must be added to packages with size different from 128 bits multiples.
This makes the data generically processable and is called padding. There are various approaches to padding, but the most popular (as defined in PKCS#5) appends the missing bytes N with the value N :footcite:`Knudsen`.

.. tikz:: Figure 2: PKCS#5 block padding
   :include: pkcs5_padding.tikz
   :xscale: 50
   :stringsubst:
   :align: center
   :alt: PKCS#5 block padding

|

**Remark:** When using a combination of Message Authentication code (MAC) and encryption with the purpose of ensuring data authenticity and secrecy, the combinations order is very important and can result in some cases in vulnerabilities.
This is due to the fact that the receiver has to remove the padding that was originally introduced during the encryption process before decrypting the received cipher-text, which can be exploited by a padding oracle attack :footcite:`Moxie`.
This is further explained in the following post Authenticated_Encryption_ .



Share this blog
~~~~~~~~~~~~~~~~

.. raw:: html

  <div id="share">
    <a class="facebook" href="https://www.facebook.com/share.php?u=https://superkogito.github.io/blog/2019/03/03/encryption_overview.html&title=Encryption%20overview"                target="blank"><i class="fa fa-facebook"></i></a>
    <a class="twitter"  href="https://twitter.com/intent/tweet?url=https://superkogito.github.io/blog/2019/03/03/encryption_overview.html&text=Encryption%20overview"                 target="blank"><i class="fa fa-twitter"></i></a>
    <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&url=https://superkogito.github.io/blog/2019/03/03/encryption_overview.html&title=Encryption%20overview" target="blank"><i class="fa fa-linkedin"></i></a>
    <a class="reddit"   href="http://www.reddit.com/submit?url=https://superkogito.github.io/blog/2019/03/03/encryption_overview.html&title=Encryption%20overview"                    target="blank"><i class="fa fa-reddit"></i></a>
  </div>


.. update:: 8 Apr 2022

   👨‍💻 Last edit and review were on 08.04.202

References and Further readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. footbibliography::

.. _Authenticated_Encryption : AuthenticatedEncryption.html
