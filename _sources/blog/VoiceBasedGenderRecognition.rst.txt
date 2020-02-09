[09-05-2019] Voice based gender recognition using Gaussian mixture models
===========================================================================

.. meta::
   :description: Voice based gender recognition post
   :keywords: Gender recognition by voice, Voice based gender recognition, Gaussian mixture model, gender classification, Ayoub Malek
   :author: Ayoub Malek

.. post:: May 09, 2019
   :tags: [Voice],[Gender recognition]
   :category: Machine learning
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

.. image:: ../_static/vbgraph.png
  :align: center
  :scale: 85%

.. raw:: html

  <div class="clt">
  <br>
  <center><a href="../figures/fig4.html" > Fig 4: Voice based gender recognition overview</a> </center>
  <br>
  </div>
  <p>
  This blog presents an approach to recognizing a Speaker's gender by voice using the Mel-frequency cepstrum coefficients (MFCC) and Gaussian mixture models (GMM).
  The post provides an explanation of the following GitHub-project <a href="https://github.com/SuperKogito/Voice-based-gender-recognition" title="vbgr"><i class="fa fa-github"></i>Voice-based-gender-recognition</a>.
  </p>
  <table align="center" style="width:100%">
    <tr>
        <th> <a class="github-button" href="https://github.com/SuperKogito/Voice-based-gender-recognition/subscription" data-size="large" data-show-count="true" aria-label="Watch SuperKogito/Voice-based-gender-recognition on GitHub">Watch</a> </th>
        <th> <a class="github-button" href="https://github.com/SuperKogito/Voice-based-gender-recognition" data-size="large" data-show-count="true" aria-label="Star SuperKogito/Voice-based-gender-recognition on GitHub">Star</a> </th>
        <th> <a class="github-button" href="https://github.com/SuperKogito/Voice-based-gender-recognition/fork" data-size="large" data-show-count="true" aria-label="Fork SuperKogito/Voice-based-gender-recognition on GitHub">Fork</a> </th>
        <th> <a class="github-button" href="https://github.com/SuperKogito/Voice-based-gender-recognition/archive/master.zip" data-size="large" aria-label="Download SuperKogito/Voice-based-gender-recognition on GitHub">Download</a> </th>
        <th> <a class="github-button" href="https://github.com/SuperKogito" data-size="large" data-show-count="true" aria-label="Follow @SuperKogito on GitHub">Follow @SuperKogito</a> </th>
    </tr>
  </table>
  <script async defer src="https://buttons.github.io/buttons.js"></script>

The aforementioned implementation, uses The Free ST American English Corpus data-set (SLR45_), which is a free American English corpus by Surfingtech_, containing utterances from 10 speakers (5 females and 5 males).


Keywords: Gender recognition, Mel-frequency cepstrum coefficients, The Free ST American English Corpus data-set, Gaussian mixture models

Introduction
--------------
The idea here is to recognize the gender of the speaker based on pre-generated Gaussian mixture models (GMM).
Once the data is properly formatted, we train our Gaussian mixture models for each gender by gathering Mel-frequency cepstrum coefficients (MFCC) from their associated training wave files.
Now that we have generated the models, we identify the speakers genders by extracting their MFCCs from the testing wave files and scoring them against the models.
These scores represent the likelihood that user MFCCs belong to one of the two models. The gender models with the highest score represents the probable gender of the speaker.
In the following table, we summarize the previous main steps, as for a detailed modeling of the processing steps, you can refer to the Workflow graph in Fig_5_.

|

+------------------------------------------------------+--------------------------------------------------------------+
| I. Training phase:                                   | II. Testing phase                                            |
+------------------------------------------------------+--------------------------------------------------------------+
| 1. Data formatting and management                    | 4. Extracting MFCC features from the testing data            |
| 2. Extracting MFCC features from the training data   | 5. Scoring the extracted MFCCs against the GMMs              |
| 3. Training gender GMMs                              | 6. Recognizing the speaker's gender based on the scores      |
+------------------------------------------------------+--------------------------------------------------------------+

.. raw:: html

  <div class="clt">
  <br>
  <center><a href="../tables/table1.html" >Table 1: Main steps of the voice based gender recognition</a> </center>
  </div>

Workflow graph
---------------

.. image:: ../_static/genderspeaker.png
   :align: center
   :scale: 85%

.. raw:: html

  <div class="clt">
  <br>
  <center><a href="../figures/fig5.html" >Fig 5: Voice based gender recognition</a> </center>
  </div>


Data formatting
----------------
Once you download your data-set, you will need to split it into two different sets:

- Training set: This set will be used to train the gender models.
- Testing set: This one will serve for testing the accuracy of the gender recognition.

I usually use 2/3 of the the data for the training and 1/3 for the testing, but you can adjust that to your needs/ wishes.
The code provides an option for running the whole cycle using "Run.py" or you can go step by step and for the data management just run the following in your terminal:

.. code-block:: shell

  $ python3 Code/DataManager.py


Voice features extraction
--------------------------
The Mel-Frequency Cepstrum Coefficients (MFCC) are used here, since they deliver the best results in speaker verification.
MFCCs are commonly derived as follows:

1. Take the Fourier transform of (a windowed excerpt of) a signal.
2. Map the powers of the spectrum obtained above onto the mel scale, using triangular overlapping windows.
3. Take the logs of the powers at each of the mel frequencies.
4. Take the discrete cosine transform of the list of mel log powers, as if it were a signal.
5. The MFCCs are the amplitudes of the resulting spectrum.

To extract MFCC features I usually use the python_speech_features_ library, it is simple to use and well documented:

.. code-block:: python
  :caption: FeaturesExtraction.py
  :name: FeaturesExtraction
  :linenos:

   import numpy as np
   from sklearn import preprocessing
   from scipy.io.wavfile import read
   from python_speech_features import mfcc
   from python_speech_features import delta

   def extract_features(audio_path):
       """
       Extract MFCCs, their deltas and double deltas from an audio, performs CMS.

       Args:
           audio_path (str) : path to wave file without silent moments.
       Returns:
           (array) : Extracted features matrix.
       """
       rate, audio  = read(audio_path)
       mfcc_feature = mfcc(audio, rate, winlen = 0.05, winstep = 0.01, numcep = 5, nfilt = 30,
                           nfft = 512, appendEnergy = True)

       mfcc_feature  = preprocessing.scale(mfcc_feature)
       deltas        = delta(mfcc_feature, 2)
       double_deltas = delta(deltas, 2)
       combined      = np.hstack((mfcc_feature, deltas, double_deltas))
   return combined

Gaussian Mixture Models
------------------------
According to D. Reynolds in Gaussian_Mixture_Models_:

  << A Gaussian Mixture Model (GMM) is a parametric probability density function represented as a weighted sum of Gaussian component densities. GMMs are commonly used as a parametric model of the probability distribution of continuous measurements or features in a biometric system, such as vocal-tract related spectral features in a speaker recognition system. GMM parameters are estimated from training data using the iterative Expectation-Maximization (EM) algorithm or Maximum A Posteriori(MAP) estimation from a well-trained prior model. >>

In a some way, you can consider a Gaussian mixture model as a probabilistic clustering representing a certain data distribution as a sum of Gaussian density functions (check Fig_6_).
These densities forming a GMM are also called the components of the GMM. The likelihood of data points (feature vectors) for a model is given by following equation [6]_ :math:`\begin{equation}
P(X | \lambda)=\sum_{k=1}^{K} w_{k} P_{k}\left(X | \mu_{k}, \Sigma_{k}\right)
\end{equation}`, where :math:`\begin{equation} P_{k}\left(X | \mu_{k}, \Sigma_{k}\right)=\frac{1}{\sqrt{2 \pi\left|\Sigma_{k}\right|}} e^{\frac{1}{2}\left(X-\mu_{k}\right)^{T} \Sigma^{-1}\left(X-\mu_{k}\right)} \end{equation}`
is the Gaussian distribution, with:

- :math:`\lambda` represents the training data.
- :math:`\mu` is the mean.
- :math:`\Sigma` is co-variance matrices.
- :math:`w_{k}` represent the weights.
- :math:`k` refers the index of the GMM components.


.. image:: ../_static/blog-plots/voice-based-gender-recognition/gmm.png
   :align: center
   :scale: 85%

.. raw:: html

  <div class="clt">
  <center><a href="../figures/fig6.html" >Fig 6: Gaussian mixture model </a> </center>
  </div>

|

To train a Gaussian mixture models based on some collected features, you can use scikit-learn-library_ specifically the scikit-learn-gmm_:

.. code-block:: python
  :caption: GmmGeneration.py
  :name: GmmGeneration
  :linenos:

  import os
  import pickle
  from sklearn.mixture import GMM


  def save_gmm(gmm, name):
      """ Save Gaussian mixture model using pickle.
          Args:
              gmm        : Gaussian mixture model.
              name (str) : File name.
      """
      filename = name + ".gmm"
      with open(filename, 'wb') as gmm_file:
          pickle.dump(gmm, gmm_file)
      print ("%5s %10s" % ("SAVING", filename,))

  ...
  # get gender_voice_features using FeaturesExtraction
  # generate gaussian mixture models
  gender_gmm = GMM(n_components = 16, n_iter = 200, covariance_type = 'diag', n_init = 3)
  # fit features to models
  gender_gmm.fit(gender_voice_features)
  # save gmm
  save_gmm(gender_gmm, "gender")


Gender identification
----------------------
The identification is done over three steps: first you retrieve the voice features, then you compute their likelihood of belonging to a certain gender and finally your compare both scores and make a decision on the probable gender.
The computation of the scores is done as follows [1]_:

  Given a speech Y and speaker S, the gender recognition test can be restated into a basic hypothesis test between :math:`H_{f}` and :math:`H_{m}`, where:

  - :math:`H_{f}` : Y is a FEMALE
  - :math:`H_{f}` : Y is a MALE

  .. math::
    :nowrap:
    :label: euler

    \begin{eqnarray}
        \frac{p\left(Y | H_{f}\right)}{p\left(Y | H_{m}\right)} = \left\{\begin{array}{ll}{ \geq 1} & {\text { accept } H_{f}} \\ {< 1} & {\text { reject } H_{m}}\end{array} \right.
    \end{eqnarray}

  where :math:`\begin{eqnarray} p\left(Y | H_{i}\right) \end{eqnarray}`, is the probability density function for the hypothesis :math:`H_{i}` evaluated for the observed speech segment Y, also called *the likelihood of the hypothesis* :math:`H_{i}` given the speech segment Y [1]_.


.. code-block:: python
  :caption: GenderIdentification.py
  :name: GenderIdentification
  :linenos:

  import pickle
  import numpy as np
  from FeaturesExtractor import FeaturesExtractor

  def identify_gender(vector):
      # female hypothesis scoring
      is_female_scores         = np.array(self.females_gmm.score(vector))
      is_female_log_likelihood = is_female_scores.sum()

      # male hypothesis scoring
      is_male_scores         = np.array(self.males_gmm.score(vector))
      is_male_log_likelihood = is_male_scores.sum()

      # print scores
      print("%10s %5s %1s" % ("+ FEMALE SCORE",":", str(round(is_female_log_likelihood, 3))))
      print("%10s %7s %1s" % ("+ MALE SCORE", ":", str(round(is_male_log_likelihood,3))))

      # find the winner aka the probable gender of the speaker
      if is_male_log_likelihood > is_female_log_likelihood: winner = "male"
      else                                                : winner = "female"
      return winner


  # init instances and load models
  features_extractor  = FeaturesExtractor()
  females_gmm         = pickle.load(open(females_model_path, 'rb'))
  males_gmm           = pickle.load(open(males_model_path, 'rb'))

  # read the test directory and get the list of test audio files
  file   = "speaker-test-file.wav"
  vector = features_extractor.extract_features(file)
  winner = identify_gender(vector)
  expected_gender = file.split("/")[1][:-1]

  print("%10s %6s %1s" %  ("+ EXPECTATION",":", expected_gender))
  print("%10s %3s %1s" %  ("+ IDENTIFICATION", ":", winner))




Code & scripts
---------------

.. raw:: html
  <p>
  The full code for this approach to voice based gender identification can be found on GitHub under <a href="https://github.com/SuperKogito/Voice-based-gender-recognition" title="vbgr"><i class="fa fa-github"></i>Voice-based-gender-recognition</a>.
  </p>

Obviously the code provided on GitHub is more structured and advanced than what provided here since it is used to process multiple files,and to compute the accuracy level

Results summary
----------------
The results of the gender recognition tests can be summarized in the following table/ confusion matrix:

|

+----------------+-----------------+---------------+
|                | Female expected | Male expected |
+----------------+-----------------+---------------+
| Female guessed |  563            |  28           |
+----------------+-----------------+---------------+
| Male guessed   |  21             | 376           |
+----------------+-----------------+---------------+

.. raw:: html

  <div class="clt">
  <center><a href="../tables/table2.html" >Table 2: Gender recognition results summary (confusion matrix) </a> </center>
  </div>

|

Using the previous results we can compute the following system characteristics:

- Precision for female recognition = 563 / (563 + 28) = 0.95
- Precision for   male recognition = 376 / (376 + 21) = 0.94
- Accuracy  =  939 / 988 = 0.95

Conclusions
-----------

- The system results in a **95%** accuracy of gender detection, but this can be different for other data-sets.
- The code can be further optimized using multi-threading, acceleration libs and multi-processing.
- The accuracy can be further improved using GMM normalization aka a UBM-GMM system.

References and Further readings
--------------------------------

.. [1] Reynolds, Douglas A., Thomas F. Quatieri, and Robert B. Dunn. Speaker Verification Using Adapted Gaussian Mixture Models, Digital signal processing 10.1 (2000): 19-41. http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.117.338&rep=rep1&type=pdf
.. [2] Sérgio R. F. Vieira, Eduardo M. B. de A. Tenório and Tsang Ing Ren, Speaker Verification Using Adapted Gaussian Mixture Models, August, 2014, https://github.com/embatbr/speech-verify/blob/master/report/report.pdf
.. [3] Sina Khanmohammadi, Chun-AnChou, A Gaussian mixture model based discretization algorithm for associative classification of medical data, July, 2015, https://www.sciencedirect.com/science/article/pii/S0957417416301440
.. [4] Hanilçi, Cemal & Ertas, Figen. (2013). Investigation of the effect of data duration and speaker gender on text-independent speaker recognition. Computers & Electrical Engineering. 39. 10.1016/j.compeleceng.2012.09.014. https://www.researchgate.net/publication/235995473_Investigation_of_the_effect_of_data_duration_and_speaker_gender_on_text-independent_speaker_recognition
.. [5] The present and future of voiceprint based security PDF_ and Lecture-video_.
.. [6] Machine Learning in Action: Voice Gender Detection using GMMs : A Python Primer, https://appliedmachinelearning.blog/2017/06/14/voice-gender-detection-using-gmms-a-python-primer/

.. _PDF: http://www.apsipa.org/doc/APSIPA%20Distinguished%20Lecture%20Presentation%20Slides%20-%20Professor%20Eliathamby%20Ambikairajah%2021%20October%202013.pdf
.. _Lecture-video: https://www.youtube.com/watch?v=mA5nxayMfFs

.. _SLR45: http://www.openslr.org/45/
.. _Surfingtech: https://www.surfing.ai
.. _Gaussian_Mixture_Models: https://pdfs.semanticscholar.org/734b/07b53c23f74a3b004d7fe341ae4fce462fc6.pdf
.. _Voice-based-gender-recognition: https://github.com/SuperKogito/Voice-based-gender-recognition
.. _python_speech_features: https://python-speech-features.readthedocs.io/en/latest/
.. _scikit-learn-gmm: https://scikit-learn.org/stable/modules/mixture.html
.. _scikit-learn-library: https://scikit-learn.org
..  _Fig_5: ../figures/fig5.html
..  _Fig_6: ../figures/fig6.html


.. |img1| image:: ../_static/github.png
   :target: https://github.com/SuperKogito/Voice-based-gender-recognition
   :scale: 65%
