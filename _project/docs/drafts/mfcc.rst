[01-09-2020] Computing the Mel-filterbanks and the mel frequency cepstrum coefficients
==================================================================================

.. meta::
   :description: Voice based gender recognition using support vector machines post
   :keywords: Gender recognition by voice, Voice based gender recognition, Gaussian mixture model, gender classification, Ayoub Malek
   :author: Ayoub Malek

.. post:: Sep 09, 2020
   :tags: [Voice],[Gender recognition]
   :category: Machine learning
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

The aforementioned implementation, uses The Free ST American English Corpus data-set (SLR45_), which is a free American English corpus by Surfingtech_, containing utterances from 10 speakers (5 females and 5 males).


Keywords: Gender recognition, Mel-frequency cepstrum coefficients, The Free ST American English Corpus data-set, Gaussian mixture models

Introduction
--------------
The idea here is to recognize the gender of the speaker based on pre-generated Gaussian mixture models (GMM).
Once the data is properly formatted, we train our Gaussian mixture models for each gender by gathering Mel-frequency cepstrum coefficients (MFCC) from their associated training wave files.
Now that we have generated the models, we identify the speakers genders by extracting their MFCCs from the testing wave files and scoring them against the models.
These scores represent the likelihood that user MFCCs belong to one of the two models. The gender models with the highest score represents the probable gender of the speaker.
In the following table, we summarize the previous main steps, as for a detailed modeling of the processing steps, you can refer to the Workflow graph in Fig_5_.



- Pre-emphasis
- Fourier-Transform and Power Spectrum

filterbanks
----------------------

mfccs
---------------


mean normalization
------------------

add energy
----------
