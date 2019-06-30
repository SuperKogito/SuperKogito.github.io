[25-03-2019] Authenticated Encryption
======================================

.. post:: Mar 25, 2019
   :tags: [Authenticated Encryption],[Encryption],[Hashing],[Security]
   :category: Cybersecurity
   :author: Ayoub Malek
   :location: Munich
   :language: English


Advanced Seminar for Security in Information Technology, Winter Term 2017
---------------------------------------------------------------------------
With growing dependency on information technology and more at stake, the security aspect has become more vital than ever.
Within this context acts authenticated encryption(AE) as a shared-key based transform whose goal is to provide secrecy, Integrity and authenticity of the encapsulated data \cite{bellare}.
AE combines traditional Symmetric Encryption (SE) with a Message Authentication Code (MAC) in different orders \cite{nampere}.
This article examines the different combinations of authenticated encryption and introduces the most secure approach of all three.

|


Keywords: Authenticated Encryption, MAC-and-Encrypt, Encrypt-then-MAC, MAC-then-Encrypt, Symmetric Encryption, Message Authentication Code.

Introduction
------------

Nowadays, the traditional approach to secure communications is to establish a “secure channel” between two endpoints and then exchange encrypted data \cite{hugo}.
Typically, this is done by initiating a secure key-exchange (or multiple keys), which will be later used to encrypt/decrypt the exchanged data.
This approach is used in many protocols such as: Secure Sockets Layer (SSL: predecessor of TLS), Internet Protocol security (IPsec), Secure Shell (SSH) etc. \cite{hugo}.
An authenticated encryption is composed by two main blocks; Message Authentication Code (MAC) and a Symmetric Encryption (SE).
The MAC is a piece of information (often called a tag) generated based on the data at hand and is transmitted throughout the channel within the sent package.
The tag is then used in the receiving end to verify the data integrity and the authenticity of its source.
SE on the other hand refers to an encryption algorithms using the same cryptographic key for both encryption and decryption.
Encryption transforms a plaintext into unreadable text (Ciphertext), to ensure the privacy of the interactions.
The authenticated encryption combination of MAC and SE provides Integrity and Authenticity using the MAC and Privacy through SE.
There are various approaches to authenticated encryption that differs essentially in the way the MAC and the SE are combined.
Although these two components can be independently secure, their combination is not necessarily unbreakable.
To describe these three methods effectively, we consider P as Plaintext, C as Ciphertext, E is a symmetric encryption function, K stands for Key, MAC is a message authentication code, T is the generated tag and || denotes concatenation.
This results in the following three different approaches:\\

|

- **MAC and Encrypt (M\&E):** In this approach the sender computes a MAC of the P, encrypts the P, and then appends the MAC to the C \cite{moxie}.
  This is how SSH works and can be described by:
  :math:`Sent Data = E_{k1}(P) || MAC_{k2}(P)`
|

- **MAC-then-Encrypt (MtE):** Here the sender computes a MAC of the P, then encrypts both the P and the MAC \cite{moxie}.
  This is approximately how SSL works.
  `Sent Data = E_{k1}(P || MAC_{k2}(P))`
|

- **Encrypt-then-MAC (EtM):** This is the most secure approach. It consists of encrypting the P first and then appending a MAC of the result \cite{moxie}.
  This scheme is used in IPsec and can be summed by:
  `Sent Data = E_{k1}(P) || MAC_{k2}(E_{k1}(P))`

|


.. image:: ../_static/macs.png
   :align: center
SE and MAC combinations \cite{aumasson}



MAC-then-Encrypt and its flaws
------------------------------
The focus of this research is the MAC-then-Encrypt approach, hence we hence it will be the focus in this paper.
MtE consists of producing a MAC based on a plain text then concatenates both and encrypts the outcome to produce a Cipher text.
On the receiver side this will be reversed by decrypting the received message first and then extract the MAC and verify it.
This clearly violates what many experts call the doom principle, which states:
say When you receive a message, the very first thing you can do is verify the MAC \cite{moxie}.


Subsubsection Heading Here
^^^^^^^^^^^^^^^^^^^^^^^^^^
When using MtE, one needs to remove the padding that was originally introduced during the encryption process before decrypting \cite{moxie}.
Within the context of classical cryptography padding aims essentially to prevent any type of predictability that might reveal a known plaintext or its exacts length, which aids in breaking the encryption \cite{welchman}.
Taking the case of Advanced Encryption Standard-128 (AES-128) which is a Symmetric block cipher that processes data by blocks of 128 bits.
This means that additional random data must be added to packages with size different from 128 bits multiples in order to make the input data generically processable.
So, in the case of MtE, the decryption is proceeded by a removal of padding \cite{moxie}. There are various approaches to padding, but the most popular (as defined in PKCS\#5) appends the missing bytes N of value N. The following figure shows how this is done:


.. image:: ../_static/pkcs.png
   :align: center
\caption{ PKCS\#5 block padding \cite{java}}


This un-padding decryption order reveals a huge vulnerability since the receiver throws a padding error if the padding is incorrect.
As the MAC is part of the payload this must happen before verifying the authenticity \cite{moxie}.
Knowing that the receiver always checks the last byte first to process padding, an attacker can build a ciphertext to be decrypted arbitrarily by modifying the last byte of the second to last ciphertext block \cite{moxie}.
When processing the message, the receiver has two possible crypto-related errors: a padding error, or a MAC error \cite{moxie}.
This revelation of the error can be result in the following scenario: For simplification purposes, we assume a cipher with a block size L = 8 bytes. This means a message of 2 bytes is padded with 6 (view figure 3).
The attacker first intercepts a ciphertext of 2 blocks using sniffing for instance. The nature of CBC-decryption uses the previous block as an Initialization Vector (IV) for the decryption process of the current ciphertext.
This can be summarized in the following formula, where D stands for decryption, c is the 2nd block of the ciphertext and p is its associated plaintext block:
\[D(c)  \oplus IV = p\]

With the help of this combination of MAC and CBC the attacker first sends to the receiver a packet where the L byte of the IV is altered, if a success message is received, then he changes the L-1 byte and so on until he receives an error at L-6 for example.
This use of a package to interact with the AE is called a padding oracle and would enable the attacker to determine the used padding and the length of the data as shown in figure 4.
The attacker then seeks to introduce a higher padding by changing the IV values, while changing the second byte. Once he doesn’t receive a padding error, using some basic math the value of the plaintext second byte is determined as in figure 5.
Using these steps, the attacker can determine a full plaintext block that he can later use alongside its associated ciphertext block to determine the key. O
nce the key is known, the whole interaction becomes open to the attacker. This attack is called a Padding oracle attack or the Vaudenay attack \cite{moxie}[8].

At first glance this may seem avoidable by simply not revealing the type of error, whether it is a padding or MAC-error (note that some error feedback is practical to have specially in web-services).
However, the threat is still unavoidable since the attacker can analyze the time taken to respond as shown in figure 6.
This helps the attacker to determine, whether a padding error or MAC-error was detected (A MAC error obviously takes longer since the receiver must first remove the padding, decrypt and then verify the MAC).
This is known as a timing attack [9]. These type of attacks are part of chosen ciphertext attacks.


Security notions in authenticated encryption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Before mathematically explaining how secure MtE is, we first examine security notions and the relations among them.
As mentioned above SE has for goal the secrecy but it can also have different notions depending on its requirements such:

- **Indistinguishability(IND):** requires the infeasibility of learning more about the plaintext than its length based on its ciphertext \cite{desai}.
- **Non-malleability(NM):** defines the requirement that it is impossible to generate two different ciphertexts with related respective plaintexts \cite{dolev}.

Depending whether they act on a chosen plain-text or a cipher text, these notions result in the following:

- **IND-CPA:**  indistinguishability under chosen P attack.
- **IND-CCA:**  indistinguishability under (non-adaptive) chosen C attack.
- **IND-CCA2:** indistinguishability under adaptive chosen C attack \cite{course}.
- **NM-CPA:**   non-malleable under chosen P
- **NM-CCA2:**  non-malleable under adaptive chosen C \cite{coretti}.
- **INT-PTXT:** integrity of P, which requires the computational inaptitude to produce a C decrypting a message, that the sender had never encrypted.
- **INT-CTXT:** integrity of C, which requires the computational inaptitude to produce a C, that was not previously produced by the sender. \cite{coretti}

**Remark:** The NM-notions are originally defined for asymmetric encryption but can be generalized to symmetric encryption \cite{coretti}. \\

Authenticity and the privacy notions are quite disjoint, and each notion/ combination reflects a different level of security  \cite{bellare}..
For useful comparisons, we consider the weakest privacy notion (IND-CPA) and the authenticity notions to create the following combinations:
INT-PTXT \^{} IND-CPA and INT-CTXT \^{} IND-CPA, between whom the relations are resumed in figure 7,
where an implication A -> B means that all SE schemes meeting notion A also meet B and A not-> B means that there exists a SE scheme meeting notion A but not necessarily B,
if some scheme meeting A exists (=minimal assumption).


.. image:: ../_static/notions.png
   :align: center
caption{Notions. \cite{canvel}}

On top of all comes the notion of unforgeability which reflects how secure is the scheme against chosen message attacks, and it can be:

- **Weak Unforgeability (WUF):** states that an adversary can’t create a new valid message-tag pair \cite{bellare}.
- **Strong Unforgeability (SUF):** states that an adversary can’t create a new tag for an existing message  \cite{bellare}.

Mathematical proof of MAC-then-Encrypt security
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Assuming the weakest notions provided by a generic scheme which are INT\-PTXT \^{} IND-CPA, more precisely if the MAC is WUF\-CMA then the resulting EtM is INT\-PTXT secure.
Furthermore, if the SE is IND\-CPA then so is the composite scheme. \textbf{Theorem 1} as declared in \cite{hugo} and proven in \cite{canetti} states that if SE is IND\-CPA and MAC is a secure MAC family then EtM implements a secure channel \cite{hugo}.
Unfortunately this does not hold for MtE and so unlike EtM, MtE is not generically secure.
However this theorem can be extended to the case of MtE assuming stronger notions of SE, which can be used to deduce that MtE is secure in the case of OTP and CBC since it results in CUF-CPA scheme.\\

Furthermore \cite{hugo} describes a chosen ciphertext attack (similar to the padding oracle attack ) on a stream cipher based MtE, proving that the scheme is still be insecure despite the SE being IND-CPA secure and the MAC being UF.
And so one cannot claim the security of MtE and stronger properties are required.
Therefore we examine stronger notions but first we point out that the following theorem 2 proven in \cite{canetti} states: SE is IND-CPA and MAC is a MAC function.
If MtE is CUF-CPA when considered as an encryption scheme then MtE is secure.
The research by \cite{hugo} goes one step further into proving in theorem 3 that using OTP in MtE and a MAC that resists one-query attacks results in the MtE being CUF-CPA, which according to theorem 2 implies the security of the scheme.
Where as in the case of using CBC for SE and a secure MAC family results in CFU-CPA and consequently MtE security as stated in Theorem 4 proved in \cite{hugo}.
It is important here to stress on the MAC one query resistance condition tightness in theorem 3 and the necessity of a strong MAC in theorem 4. However the above theorems are still valid in the case of multi-valued MACs.
Moreover the results in theorem 3 are relatively fragile and slight changes in the scheme such as encrypting the MAC and the message separately can be catastrophic.
These results mentioned above can be summarized in the following table:

.. image:: ../_static/table2.png
   :align: center
\caption{Notions. \cite{canvel}}

Conclusion
----------
To summarize, Encrypt-then-MAC is the recommended approach to authenticated encryption. However, MAC-then-encrypt is still a safe and fast approach under certain conditions.
These conditions are in some cases with little tolerance and so the error probability is relatively high, yet one can still build a secure system using MAC-then-Encrypt.
In the case of SSL for instance, the use of MAC does not jeopardize the communications, since it is relatively safe when using certain encryption modes such CBC or OTP as for chosen text attacks they are countered by restarting a new session once a padding/ authentication error is thrown.



.. toctree::
   references/References
