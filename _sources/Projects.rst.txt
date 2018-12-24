Projects
============

.. contents::

Motivation
~~~~~~~~~~~
In order to ensure that only authorized agents can access protected resources, a personal unique identification
system must be put in place.  However, keys and passwords, despite their utility are easily lost, stolen, or counterfeited.
Furthermore, an agent simple identity claim using a username and password set is proven to be insufficient and none
practical in avoiding the access sharing of one agent's account. Hence, an identity verification
mechanism is needed.

This can be achieved using the agents biometric features, retinal pattern, face, voice etc. or by examining certain
features derived from an agent’s unique behavior such keyboard typing. In each approach the detected features are
compared against a previously stored pattern of the claimed agent and an authentication decision is made accordingly.

In the Yoummday speaker verification system, we focus on verifying the agents based on their
voice biometrics/ features.


What is Speaker verification / authentication?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Speaker Verification:** Determines/ verifies if the detected voice is from a particular claimed speaker.
Also referred to as Speaker authentication.

.. note::

   Not to confuse with:

   - **Speaker Identification:** Determines who is speaking given a set of enrolled speakers.
   - **Speaker Diarization:** Partition an input audio stream into homogeneous segments according to the speaker identities.
