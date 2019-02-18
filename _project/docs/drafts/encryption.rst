
Block Ciphers
^^^^^^^^^^^^^^
In block ciphers the data is encrypted and decrypted one block at a time using the same key :cite:`Oak,Tamimi`. In its simplest mode (Electronic codebook mode), the plain text is divided into equally long blocks, which are then fed into the cipher system to produce blocks of cipher text :cite:`Kessler`. This type of ciphers requires padding before encryption to ensure that the data length is a multiple of the block’s length. Block ciphers can operate in one of several modes; here are the most important ones:\\

    - **Electronic Codebook (ECB) mode** is the simplest mode where the secret key is used to transform a plaintext block into a ciphertext block :cite:`Kessler`.
    In ECB identical plaintext blocks always generate the same ciphertext block which makes it vulnerable against a variety of brute-force attacks as well as deletion and insertion attacks :cite:`Kessler`.
    Therefore, it is advised to use ECB for only one block long data. Figure 4.3 gives an insight on the ECB mode functionality.

    - **Cipher Block Chaining (CBC) mode** adds a feedback mechanism to the encryption process where the plaintext is XORed with the previous ciphertext block before being encrypted :cite:`Kessler`.
    This ensures that two identical plaintext blocks will generate different ciphertexts and consequently CBC is more secure against many brute-force and deletion attacks :cite:`Kessler`.

    - **Cipher Feedback (CFB) mode** is a block cipher mode similar to CBC and self-synchronizing stream ciphers :cite:`Kessler`.
    It allows data -smaller than the block size- to be encrypted, which might come handy in many cases :cite:`Kessler`.

    -Output Feedback (OFB) mode** is a block cipher implementation resembling to synchronous stream cipher :cite:`Kessler`.
    Using an internal feedback mechanism, it prevents same plaintext blocks from generating the same ciphertext block. This mode generates the key-stream independently from the plaintext and ciphertext bit-streams :cite:`Kessler`.


Although CBC, CFB and OFB have good resistance against brute-force and deletion attacks, they are not very resistant to single bit errors which will propagate through different blocks in some modes :cite:`Kessler`.
On top of all, there is also \textbf{the Counter (CTR) mode` is a relatively modern approach that provides a good compromise.
Like CFB and OFB, it operates on the blocks as in a stream cipher but also it processes them independently as in ECB :cite:`Kessler`.
Using different key inputs, CTR guarantees resistance against brute forcing. Moreover, it allows parallel processing making it superior on performance and speed level.

Stream Ciphers
^^^^^^^^^^^^^^
Unlike block ciphers, stream ciphers operate on streams of data bit by bit :cite:`Tamimi`. A stream cipher consists essentially of a key stream generator and a mixing function :cite:`Kessler`.
The mixing function is usually a XOR, and the key stream generator is the main unit of the encryption :cite:`Kessler,Tamimi`. There are several types of stream ciphers but only two are worth mentioning here:

    - **Self-synchronizing stream cipher** calculate each bit in the key-stream by using the previous n bits in the key-stream.
    In this approach the decryption and encryption are synchronized, which causes problematic propagation errors :cite:`Kessler`.
    - **Synchronous stream ciphers** generate the key-stream independently and use the same generation function at both sender and receiver :cite:`Tamimi`.
    While in this case propagation errors are not an issue, their periodic nature (The key-stream will eventually repeat) poses a vulnerability that can be exploited :cite:`Kessler`.



Padding
~~~~~~~~~
Within the context of classical cryptography, padding aims essentially to prevent any type of predictability that might reveal a plain-text or its exact length.
Such revelations can be beneficial for an attacker and help in breaking the encryption :cite:`Welchman`.
For example, Advanced Encryption Standard-128 (AES-128) is a symmetric block cipher that processes data by blocks of 128 bits, which means that additional random data must be added to packages with size different from 128 bits multiples.
This makes the data generically processable and is called padding. There are various approaches to padding, but the most popular (as defined in PKCS#5) appends the missing bytes N with the value N :cite:`Knudsen`.
Remark: When using a combination of Message Authentication code (MAC) and encryption with the purpose of ensuring data authenticity and secrecy, the combinations order is very important and can result in some cases in vulnerabilities.
This is due to the fact that the receiver has to remove the padding that was originally introduced during the encryption process before decrypting the received cipher-text, which can be exploited by a padding oracle attack :cite:`Moxie`.
This is further explained in the following post(post name up coming).
