Diabetes detection using machine learning (part II)
===================================================
.. raw:: html

  <div class="blog-post-tags">
    <ul class="blog-posts-details">
    <li id="Date"><span>Date:</span>                 30 June 2019 </li>
    <li id="author"><span>Author:</span>            <a href="author/ayoub-malek.html">Ayoub Malek</a> </li>
    <li id="location"><span>Location:</span>        <a href="location/munich.html">Munich</a>
    </li>  <li id="language"><span>Language:</span> <a href="language/english.html">English</a>
    </li>  <li id="category"><span>Category:</span> <a href="category/machine-learning.html"> Machine learning</a>
    </li>
    <li id="tags"><span>Tags:
          </span>
          <a class="post-tags" href="tag/data-processing.html">Data processing</a>
          <a class="post-tags" href="tag/visualization.html">Visualization</a>
          <a class="post-tags" href="tag/python.html">Python</a>
    </li>
    </ul>
  </div>

.. meta::
   :description: applied machine learning to diabetics detection
   :keywords: machine learning, Pima, classification, diabetes detection, data scaling, knn, svc, gaussian, Ayoub Malek
   :author: Ayoub Malek

.. post:: Jun 30, 2019
   :tags: Python, Data processing, Visualization
   :category: Machine learning, 2019
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

In this 2nd post on detecting diabetes with the help of machine learning and using the Pima Indian diabetic database (PIDD_), we will dig into testing various classifiers and evaluating their performances.
We will also examine the performance improvements by the data transformations explained in the previous post.

The tested machine learning detection approaches
-------------------------------------------------
The idea of the detection in this context is distinguishing based on the provided features if the person has diabetes or not. This is a clear classification problem.
For which we test the following classifiers:

- K-Nearest_Neighbors_ (KNN)

  - K-Nearest Neighbors (distance weights)
  - K-Nearest Neighbors (uniform weights)

- Support_Vector_Classifier_ (SVC)

  - Linear Support Vector Classifier
  - RBF Support Vector Classifier

- Gaussian_Process_
- Decision_Tree_
- Random_Forest_
- AdaBoost_
- Naive_Bayes_
- Quadratic_Discriminant_Analysis_ (QDA)

Code and implementation
-------------------------

.. raw:: html

  <p>
  The code for this section is to be found in this script_.
  However, the whole project is available in the following  <a href="https://github.com/SuperKogito/Diabetes-detection-using-machine-learning" title="vbgr"><i class="fa fa-github"></i> Diabetes detection</a>.
  </p>

  <table align="center" style="width:100%">
    <tr>
        <th> <a class="github-button" href="https://github.com/SuperKogito/Diabetes-detection-using-machine-learning/subscription" data-size="large" data-show-count="true" aria-label="Watch SuperKogito/Diabetes-detection-using-machine-learning on GitHub">Watch</a> </th>
        <th> <a class="github-button" href="https://github.com/SuperKogito/Diabetes-detection-using-machine-learning" data-size="large" data-show-count="true" aria-label="Star SuperKogito/Diabetes-detection-using-machine-learning on GitHub">Star</a></th>
        <th> <a class="github-button" href="https://github.com/SuperKogito/Diabetes-detection-using-machine-learning/fork" data-size="large" data-show-count="true" aria-label="Fork SuperKogito/Diabetes-detection-using-machine-learning on GitHub">Fork</a> </th>
        <th> <a class="github-button" href="https://github.com/SuperKogito/Diabetes-detection-using-machine-learning/archive/master.zip" data-size="large" aria-label="Download SuperKogito/Diabetes-detection-using-machine-learning on GitHub">Download</a></th>
        <th> <a class="github-button" href="https://github.com/SuperKogito" data-size="large" data-show-count="true" aria-label="Follow @SuperKogito on GitHub">Follow @SuperKogito</a> </th>
    </tr>
  </table>
  <script async defer src="https://buttons.github.io/buttons.js"></script>

The dataset can be Downloaded from here_.

Evaluation techniques
-------------------------
When facing a typical machine learning classification problem, accuracy values can be deceiving and inaccurate.
Therefore, other metrics such as the confusion matrix, Sensitivity_ and Specificity_ are used to provide a better assessment of the algorithms.

.. math::
  :nowrap:
  :label: specificity_and_sensitivity

  \begin{eqnarray}
      Sensitivity &= \frac{True~Positives}{True~Positives + False~Negatives}\\  \\
      Specificity &= \frac{True~Negatives}{True~Negatives + False~Positives}
  \end{eqnarray}

Consequently, in order to compare the performance of the data transformations and the observed improvements, a plot of their respective accuracy, sensitivity and specificity values is provided.
As for the differences between machine learning approaches, a bars plot is provided to highlight the accuracy, sensitivity and specificity values of each approach.
On top of all, we use the confusion_matrix_ to visualize the performance of an approach and its efficiency.
In this matrix the rows represent the expected outcome and the columns correspond to the predicted ones as shown in the following:

.. raw:: html

    <table class="docutils align-default">
      <tr>
          <th>                                </th>
          <th> <h4>Predicted outcome is 0 </h4></th>
          <th> <h4>Predicted outcome is 1 </h4></th>
      </tr>
      <tr>
          <td> <h4> Actual outcome is 0 </h4> </td>
          <td> <h4><font color="green"> True Negatives               </font></h4> </td>
          <td> <h4><font color="red">   False Negatives (misses)     </font></h4> </td>
      </tr>
      <tr>
        <td> <h4> Actual outcome is 1 </h4> </td>
        <td> <h4><font color="red">   False Positives (false alarms) </font></h4> </td>
        <td> <h4><font color="green"> True Positives                 </font></h4> </td>
      </tr>
    </table>

.. raw:: html

  <div class="clt">
  <br>
  <center><a href="../tables/table3.html" >Table 3: Confusion matrix </a> </center>
  </div>


Sensitivity and Specificity are two complementary metrics. Therefore, to judge which of these two metrics to prioritize is dependent on the nature of the problem.
In order to have a better differentiation between these two, let us consider two classification systems:

.. raw:: html

    <br/>

1. First an airport system that based on a passenger behavior and emotions, decides whether the person is suspicious or not and according to the system output the authorities stop the passenger for a chat or not.
   So suspicious is outcome 0 (Negative) and not suspicious is outcome 1 (Positive): Now we can have a system that is perfect at detecting the none suspicious passengers but that is worthless in this scenario.
   If you let all the possible criminals through, you can simply not even have a system. So in this case, we prioritize the detection of True Negatives and as a side effect we will have some False Negatives (misses).
   This means, you achieve the goal of stopping and questioning every criminal but every now and then you will stop some peaceful passengers for some questions.

.. raw:: html

   <br/>

2. Now imagine some pre-selection system for some candidates. The idea here is to select candidates who full-fill certain requirements (features).
   Assume 0 for candidates that do not full-fill (Negative) the requirements and 1 for those who do (Positive). In this case, we need to do the opposite of the previous one.
   The system is supposed to detect candidates that are good at the expense of some candidates, that might not full-fill all the requirements, getting though.
   Therefore, we need to maximize True Positives count and accept the presence of some False Positive (False alarms).


Data transformations influence on results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In the previous post, the utility of some data transformations has been discussed as a method to improve the data quality and consequently improve the classification.
the following plots, confirm this as we can clearly see that employing these data transformations (scaling, equalization and outliers removal) results overall in better accuracy, sensitivity and specificity.

.. image:: ../_static/blog-plots/diabetes-ml/original/dataTrafos.png
   :align: center
   :scale: 100%

.. raw:: html

   <div class="clt">
   <center><a href="../figures/fig13.html" >Figure 13: Influence of data transformations  </a> </center>
   </div>

Classifiers comparison
^^^^^^^^^^^^^^^^^^^^^^^
In this section, we examine the performances of the aforementioned machine learning approaches approaches to diabetes detection.
The plots and the results summary prove that the Support Vector Classifiers clearly results in the best prediction rates.
In this case, we prioritize True Positives detection (sensitivity over simplicity) as we want to detect all of those having diabetes even if it means getting some False Positives (healthy patients diagnosed as diabetics) as that can be dismissed with some extra tests.

.. image:: ../_static/blog-plots/diabetes-ml/original/scaled_and_equalized_data_without_outliers-BAR.png
  :align: center
  :scale: 75%

.. raw:: html

  <div class="clt">
  <center><a href="../figures/fig14.html" >Figure 14: Performance comparison for different classifiers </a> </center>
  </div>

|

.. image:: ../_static/blog-plots/diabetes-ml/original/scaled_and_equalized_data_without_outliers-CM.png
   :align: center
   :scale: 75%

.. raw:: html

   <div class="clt">
   <center><a href="../figures/fig15.html" >Figure 15: Confusion matrices for different classifiers </a> </center>
   </div>

|

.. code-block:: python
  :caption: Results summary
  :name: Results

   ---------------------------------------------------------------------------------------------------
                                      Classifiers performances
   ---------------------------------------------------------------------------------------------------
    KNN (distance weights) -> Accuracy: 0.80 | Sensitivity: 0.80 | Specificity: 0.80 | Average: 0.80
    KNN (uniform weights)  -> Accuracy: 0.80 | Sensitivity: 0.80 | Specificity: 0.80 | Average: 0.80
    Linear SVC             -> Accuracy: 0.82 | Sensitivity: 0.86 | Specificity: 0.78 | Average: 0.82
    RBF SVC                -> Accuracy: 0.82 | Sensitivity: 0.84 | Specificity: 0.79 | Average: 0.82
    Gaussian Process       -> Accuracy: 0.80 | Sensitivity: 0.84 | Specificity: 0.77 | Average: 0.80
    Decision Tree          -> Accuracy: 0.57 | Sensitivity: 0.59 | Specificity: 0.54 | Average: 0.56
    Random Forest          -> Accuracy: 0.68 | Sensitivity: 0.77 | Specificity: 0.63 | Average: 0.69
    AdaBoost               -> Accuracy: 0.75 | Sensitivity: 0.80 | Specificity: 0.71 | Average: 0.75
    Naive Bayes            -> Accuracy: 0.79 | Sensitivity: 0.83 | Specificity: 0.75 | Average: 0.79
    QDA                    -> Accuracy: 0.80 | Sensitivity: 0.86 | Specificity: 0.76 | Average: 0.81
   ---------------------------------------------------------------------------------------------------


Conclusion
-------------------
In these two blog posts, we investigated the utility of various machine learning approaches to diabetes detection and their efficiency.
Moreover, various data transformations, such as scaling, equalization and outliers removal, have been proven to enhance the diabetes detection process.

References and Further readings
--------------------------------

.. [1] Pima Indians Diabetes Database, https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.names
.. [2] Igor Shvartser, Jason Brownlee, Case Study: Predicting the Onset of Diabetes Within Five Years (part 1 of 3), March 2014 , https://machinelearningmastery.com/case-study-predicting-the-onset-of-diabetes-within-five-years-part-1-of-3/
.. [3] Kaggle, Pima Indians Diabetes Database: Predict the onset of diabetes based on diagnostic measures, https://www.kaggle.com/uciml/pima-indians-diabetes-database
.. [4] Kaggle kernals, Pima Indians Diabetes Database: Predict the onset of diabetes based on diagnostic measures, https://www.kaggle.com/uciml/pima-indians-diabetes-database/kernels


.. _pandas.DataFrame.describe : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.describe.html
.. _PIDD : https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.names
.. _National_Institute_of_Diabetes_and_Digestive_and_Kidney_Diseases : https://www.niddk.nih.gov/
.. _Download_link : https://www.kaggle.com/uciml/pima-indians-diabetes-database
.. _Pima : https://en.wikipedia.org/wiki/Pima_people
.. _Box_plot : https://en.wikipedia.org/wiki/Box_plot
.. _Correlation : https://en.wikipedia.org/wiki/Correlation_and_dependence


.. _here : https://github.com/SuperKogito/Diabetes-detection-using-machine-learning/blob/master/diabetes.csv
.. _K-Nearest_Neighbors : https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm
.. _Support_Vector_Classifier : https://en.wikipedia.org/wiki/Support-vector_machine
.. _Gaussian_Process : https://en.wikipedia.org/wiki/Gaussian_process
.. _Decision_Tree : https://en.wikipedia.org/wiki/Decision_tree_learning
.. _Random_Forest : https://en.wikipedia.org/wiki/Random_forest
.. _AdaBoost : https://en.wikipedia.org/wiki/AdaBoost
.. _Naive_Bayes : https://en.wikipedia.org/wiki/Naive_Bayes_classifier
.. _Quadratic_Discriminant_Analysis : https://en.wikipedia.org/wiki/Quadratic_classifier#Quadratic_discriminant_analysis
.. _confusion_matrix : https://en.wikipedia.org/wiki/Confusion_matrix
.. _Sensitivity : https://en.wikipedia.org/wiki/Sensitivity_and_specificity
.. _Specificity : https://en.wikipedia.org/wiki/Sensitivity_and_specificity
.. _Diabetes_detection_using_machine_learning : https://github.com/SuperKogito/Diabetes-detection-using-machine-learning
.. _script : https://github.com/SuperKogito/Diabetes-detection-using-machine-learning/blob/master/MLapproaches.py

.. |img1| image:: ../_static/github.png
   :target: https://github.com/SuperKogito/Diabetes-detection-using-machine-learning
   :scale: 65%
