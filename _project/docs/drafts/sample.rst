sample
=======

.. postlist::
   :list-style: circle
   :category: Manual
   :format: {title}
   :sort:





.. postlist:: 5
    :author: Ahmet
    :category: Manual
    :location: Pittsburgh
    :language: en
    :tags: tips
    :date: %A, %B %d, %Y
    :format: {title} by {author} on {date}
    :list-style: circle
    :excerpts:
    :sort:





Explaining MAC-then-Encrypt implementation in SSL
--------------------------------------------------
Definition of SSL
^^^^^^^^^^^^^^^^^^
SSL is a cryptographic protocol capable to secure any transmission over Transport Control Protocol (TCP), which gained him huge popularity. SSL is also present in Hypertext Transfer Protocol Secure (HTTPS) [Viega. 10] and it provides the following security aspects [Freier 3.]:

- **Privacy:** encrypted communications
- **Authentication:** Identification using certificates and MACs
- **Reliability:** Maintaining a secure connection through data integrity verification.

How SSL Works?
^^^^^^^^^^^^^^^
The SSL protocol has the four layers that encapsulate all interactions between the communicating parties:

- **Record Layer:** In this layer all application protocol messages are formatted. The formatting consists of adding a header, and a MAC generated Hash. [Thomas, 70].
- **ChangeCipherSpec Protocol:** is composed of one message that signals the secure communications beginning.
- **Alert Protocol:** it reports errors, problems or warnings and is formed by two fields: The Severity Level and Alert Description.
- **Severity Level:** it reports the level of concern suggesting when a new handshake or a session termination is required.
- **Alert Description:** it returns the specific error description that caused the Alert Message to be sent from a party. (Thomas, 73)
- **Handshake Protocol:** represents an exchange of messages used to establish a handshake that begins a secure connection. (Thomas, 40)


SSL despite the vulnerabilities in MtE, it provides various modes of functioning among those CBC and OTP which once combined with the correct MAC can result in a secure implementation of MtE.
Furthermore the SSL implementation restarts the whole session with a new key once an error is thrown (padding or authentication error), eliminating with it the vulnerabilities exploited by most chosen ciphertext attacks.
