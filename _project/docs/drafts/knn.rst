[09-05-2019] k-Nearest-Neighbor
============================================

.. meta::
   :description: k-nearest-neighbor post
   :keywords: k-nearest neighbor, kNN, knn, Ayoub Malek
   :author: Ayoub Malek

.. post:: Jun 12, 2019
   :tags: [Voice],[Recognition],[Gender]
   :category: Machine learning
   :author: Ayoub Malek
   :location: Munich
   :language: English


Table of contents:

- Relationships between features
- The desired graph
- Why fit & predict?
- Plotting 8 features?

Relationships between features:

The scientific term characterizing the "relationship" between features is correlation.
This area is mostly explored during PCA (Principal Component Analysis).
The idea is that not all your features are important or at least some of them are highly correlated.
Think of this as similarity: if two features are highly correlated so they embody the same information and consequently you can drop one of them.
Using pandas this looks like this:

code

The output is the following correlation matrix: enter image description here

.. image:: ../_static/corr.png
    :align: center
    :scale: 85%

.. raw:: html

    <div class="clt">
    <center><a href="../_static/figures/fig6.html" >Fig 6: Gaussian mixture model </a> </center>
    </div>

So here 1 means total correlation and as expected the diagonal is all ones because a feature is totally correlated with its self. Also, the lower the number, the less correlated are the features.

Here we need to consider the feature-to-feature correlations and the outcome-to-feature correlations.
Between features: higher correlations mean we can drop one of them. However, high correlation between a feature and the outcome means that the feature is important and holds a lot of information.
In our graph, the last line represents the correlation between features and the outcome. Accordingly, the highest values/ most important features are 'Glucose' (0.47) and 'MBI' (0.29).
Furthermore, the correlation between these two is relatively low (0.22), which means they are not similar.

We can verify these results using the density plots for each feature with relevance to the outcome.
This is not that complex since we only have two outcomes: 0 or 1. So it would look like this in code:

code

The output is the following density plots: enter image description here

.. image:: ../_static/densities.png
    :align: center
    :scale: 85%

.. raw:: html

    <div class="clt">
    <center><a href="../_static/figures/fig6.html" >Fig 6: Gaussian mixture model </a> </center>
    </div>

In the plots, when the green and red curves are almost the same (overlapping), it means the feature does not separate the outcomes. I
n the case of the 'BMI' you can see some separation (the slight horizontal shift between both curves), and in 'Glucose' this is much clearer (This is in agreement with the correlation values).

=> The conclusion of this: If we have to choose just 2 features, then 'Glucose' and 'MBI' are the ones to choose.

The desired graph

I do not have much to say about this except that the graph represents a basic explanation of the concept of k-nearest neighbor. It is simply not a representation of the classification.

Why fit & predict

Well this is a basic and vital Machine Learning (ML) concept. You have a dataset=[inputs, associated_outputs] and you want to build a ML algorithm that well learn to relate the inputs to their associated_outputs. This is a two step procedure. At first, you train/teach your algorithm how it is done. At this stage, you simply give it the inputs and the answers like you do with a kid. The second step is testing; now that the kid has learned, you want to test her/him. So you give her/him similar inputs and check if her/his answers are correct. Now, you do not want to give her/him the same inputs he learned because even if she/he gives the correct answers, she/he possibly just memorized the answers from the learning phase (this is called overfitting) and so she/he did not learn a thing.

Similarly you do with your algorithm, you first split your dataset into training data and testing data. Then you fit your training data into your algorithm or classifier in this case. This is called the training phase. After that you test how good is your classifier and whether he can classify new data correctly. That is the testing phase. Based on the testing results, you evaluate the performance of your classification using different evaluation-metrics like accuracy for example. The rule of thumbs here is to use 2/3 of the data for the training and 1/3 for the testing.

Plotting 8 features?

The simple answer is no you can't and if you can, please tell me how.

The funny answer: to visualize 8 dimensions, it is easy...just imagine n-dimensions and then let n=8 or just visualize 3-D and scream 8 at it.

The logical answer: So we live in the physical word and the objects we see are 3-dimensional so that is technically kind of the limit. However, you can visualize the 4th dimension as the color like in here you can also use the time as your 5th dimension and make your plot an animation. @Rohan suggested in his answer shapes but his code did not work for me, and I do not see how that would provide a good representation of the algorithm performance. Anyway, colors, time, shapes ... after a while you run out of those and you find yourself stuck. This is one of the reasons people do PCA. You can read about this aspect of the problem under dimensionality-reduction.

So what happens if we settle for 2 features after PCA and then train, test, evaluate and plot?.

Well you can use the following code to achieve that:
 code


Improvements:

The full code can be found in this gist
