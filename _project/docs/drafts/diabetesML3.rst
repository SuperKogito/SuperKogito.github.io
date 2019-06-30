[24-06-2019] Applied machine learning to diabetes detection (part I)
====================================================================

.. meta::
   :description: applied machine learning to diabetics detection
   :keywords: machine learning, ml, k-nearest neighbor, kNN, knn, Ayoub Malek
   :author: Ayoub Malek

.. post:: Jun 24, 2019
   :tags: [Machine learning],[Data processing],[Visualization]
   :category: Machine learning
   :author: Ayoub Malek
   :location: Munich
   :language: English

.. toctree::
  :maxdepth: 2

  +----------------------------------------+---------------------------------------------------------+
  |                                        |            raw correct data                             |
  +----------------------------------------+---------------------------------------------------------+
  | K-Nearest Neighbors (distance weights) | Accuracy: 0.68 | Sensitivity: 0.61 | Specificity: 0.71  |
  | K-Nearest Neighbors (uniform weights)  | Accuracy: 0.70 | Sensitivity: 0.66 | Specificity: 0.71  |
  | Linear Support Vector Machine          | Accuracy: 0.77 | Sensitivity: 0.80 | Specificity: 0.76  |
  | RBF Support Vector Machine             | Accuracy: 0.63 | Sensitivity: nan  | Specificity: 0.63  |
  | Gaussian Process                       | Accuracy: 0.66 | Sensitivity: 0.55 | Specificity: 0.72  |
  | Decision Tree                          | Accuracy: 0.77 | Sensitivity: 0.74 | Specificity: 0.78  |
  | Random Forest                          | Accuracy: 0.75 | Sensitivity: 0.79 | Specificity: 0.75  |
  | AdaBoost                               | Accuracy: 0.75 | Sensitivity: 0.70 | Specificity: 0.76  |
  | Naive Bayes                            | Accuracy: 0.76 | Sensitivity: 0.70 | Specificity: 0.79  |
  | Quadratic Discriminant Analysis        | Accuracy: 0.78 | Sensitivity: 0.78 | Specificity: 0.79  |
  +----------------------------------------+---------------------------------------------------------+


  +----------------------------------------+---------------------------------------------------------+
  |                                        |                   data without outliers                 |
  +----------------------------------------+---------------------------------------------------------+
  | K-Nearest Neighbors (distance weights) | Accuracy: 0.74 | Sensitivity: 0.58 | Specificity: 0.84  |
  | K-Nearest Neighbors (uniform weights)  | Accuracy: 0.74 | Sensitivity: 0.60 | Specificity: 0.84  |
  | Linear Support Vector Machine          | Accuracy: 0.83 | Sensitivity: 0.74 | Specificity: 0.89  |
  | RBF Support Vector Machine             | Accuracy: 0.67 | Sensitivity: nan  | Specificity: 0.67  |
  | Gaussian Process                       | Accuracy: 0.69 | Sensitivity: 0.53 | Specificity: 0.79  |
  | Decision Tree                          | Accuracy: 0.74 | Sensitivity: 0.58 | Specificity: 0.85  |
  | Random Forest                          | Accuracy: 0.78 | Sensitivity: 0.74 | Specificity: 0.79  |
  | AdaBoost                               | Accuracy: 0.70 | Sensitivity: 0.54 | Specificity: 0.80  |
  | Naive Bayes                            | Accuracy: 0.82 | Sensitivity: 0.68 | Specificity: 0.92  |
  | Quadratic Discriminant Analysis        | Accuracy: 0.83 | Sensitivity: 0.70 | Specificity: 0.91  |
  +----------------------------------------+---------------------------------------------------------+

This blog post is part of 3 posts providing an in depth introduction to diabetes detection using various machine learning approaches.
In this first post, we focus on exploring the data at hand and preparing it for machine learning related processing.

The pima indians diabetes dataset
----------------------------------
iabetes  mellitus  is  one  of  the  most  serious  health  challenges facing American Natives in the United States today.
The publicly available  Pima  Indian  diabetic  database  (PIDD)  at  the  UCI Machine  Learning  Lab  has  become  a  standard  for  testing  data mining
 algorithms  to  see  their  accuracy  in  predicting  diabetic status  from  the  8  variables  given.

he Pima Indian diabetes database, donated by Vincent Sigillito, is a collection of medical diagnostic reports from 768 records of female patients at least 21 years old of Pima Indian heritage, a population living near Phoenix, Arizona, USA.The  database  has  n=768  patients  each  with  9  numeric variables: (1) number of times pregnant, (2) 2-hour OGTT plasma  glucose,  (3)  diastolic  blood  pressure,  (4)  triceps skin fold thickness, (5) 2-hour serum insulin, (6) BMI, (7) diabetes  pedigree  function,  (8)  age,  (9)  diabetes  onsetwithin 5 years (0, 1). The goal is to use the first 8 variables to predict #9.There are 500 non-diabetic patients (class = 0) and 268 diabetic  ones  (class  =  1)  for  an  incidence  rate  of  34.9%. Thus  if  you  simply  guess  that  all  are  non-diabetic,  your accuracy rate is 65.1% (or error rate of 34.9%). We expect a  useful  data  mining  or  prediction  tool  to  do  much  better than this. There  are  a  few  errors  in  the  data.  Although  the database  is  labeled  as  having  no  missing  values,  someone liberally  added  zeros  wherethere  were  missing  values. Five patients had a glucose of 0, 11 more had a body mass index  of  0,  28  others  had  a  diastolic  blood  pressure  of  0, 192  others  had  skin  fold  thickness  readings  of  0,  and  140 others  had  serum  insulin  levels  of  0.  None  of  these  are physically possible, and after they were deleted there were 392  cases  with  no  missing  values.  Studies  that  did  not realize  the  previous  zeros  were  in  fact  missing  variables essentially  used  a  rule  of  substituting  zero  for  the  missing variables.  Ages  range  from  21  to  81  and  all  are  female. Table 1 shows the characteristics of the selected data sets.

For Each Attribute: (all numeric-valued)

1. Number of times pregnant
2. Plasma glucose concentration a 2 hours in an oral glucose tolerance test
3. Diastolic blood pressure (mm Hg)
4. Triceps skin fold thickness (mm)
5. 2-Hour serum insulin (mu U/ml)
6. Body mass index (weight in kg/(height in m)^2)
7. Diabetes pedigree function
8. Age (years)
9. Class variable (0 or 1

  Data Exploration and Profiling


  Once the data is collected, it’s time to assess the condition of it, including looking for trends, outliers, exceptions, incorrect, inconsistent, missing, or skewed information.
  This is important because your source data will inform all of your model’s findings, so it is critical to be sure it does not contain unseen biases.
  For example, if you are looking at customer behavior nationally, but only pulling in data from a limited sample, you might miss important geographic regions.
  This is the time to catch any issues that could incorrectly skew your model’s findings, on the entire data set, and not just on partial or sample data sets.


  Step 3: Formatting data to make it consistent


  The next step in great data preparation is to ensure your data is formatted in a way that best fits your machine learning model.
  If you are aggregating data from different sources, or if your data set has been manually updated by more than one stakeholder, you’ll likely discover anomalies in how the data is formatted (e.g. USD5.50 versus $5.50).
  In the same way, standardizing values in a column, e.g. State names that could be spelled out or abbreviated) will ensure that your data will aggregate correctly.
  Consistent data formatting takes away these errors so that the entire data set uses the same input formatting protocols.


  Step 4: Improving data quality


  Here, start by having a strategy for dealing with erroneous data, missing values, extreme values, and outliers in your data.
   Self-service data preparation tools can help if they have intelligent facilities built in to help match data attributes from disparate datasets to combine them intelligently.
   For instance, if you have columns for FIRST NAME and LAST NAME in one dataset and another dataset has a column called CUSTOMER that
    seem to hold a FIRST and LAST NAME combined, intelligent algorithms should be able to determine a way to match these and join the datasets to get a singular view of the customer.

  For continuous variables, make sure to use histograms to review the distribution of your data and reduce the skewness.
  Be sure to examine records outside an accepted range of value.
  This “outlier” could be an inputting error, or it could be a real and meaningful result that could inform future events as duplicate or similar values could carry the same information and should be eliminated.
   Similarly, take care before automatically deleting all records with a missing value, as too many deletions could skew your data set to no longer reflect real-world situations.


  Step 5: Feature engineering


  This step involves the art and science of transforming raw data into features that better represent a pattern to the learning algorithms.
   For example, data can be decomposed into multiple parts to capture more specific relationships, such as analyzing sales performance by the day of the week, not only the month or year.
    In this situation, segregating the day as a separate categorical value from the date (e.g. “Mon; 06.19.2017”) may provide the algorithm with more relevant information.


  Step 6: Splitting data into training and evaluation sets


  The final step is to split your data into two sets; one for training your algorithm, and another for evaluation purposes.
   Be sure to select non-overlapping subsets of your data for the training and evaluation sets in order to ensure proper testing.
    Invest in tools that provide versioning and cataloging of your original source as well as your prepared data for input to machine learning algorithms, and the lineage between them.
     This way, you can trace the outcome of your predictions back to the input data to refine and optimize your models over time.


  Accelerating business performance – How DP enables ML and solves data challenges


  Data preparation has long been recognized for helping business leaders and analysts to ready and prepare the data needed for analytics, operations, and regulatory requirements.
  Self-service data preparation that runs on Amazon Web Services (AWS) and Azure takes it to the next level by leveraging many valuable attributes of a cloud-based environment.

  As a result, business users who are closest to the data and most knowledgeable about its business context, can prepare data sets quickly and accurately, with the help of built-in intelligence and smart algorithms.
   They can work within an intuitive, visual application to access, explore, shape, collaborate and publish data with clicks, not code, with complete governance and security.
    IT professionals are able to maintain the scale of data volumes and variety across both enterprise and cloud data sources to support business scenarios for immediate and repeatable data service needs.

  Solutions like DP solve many data challenges and enable ML and data science workflows that enhance applications with machine intelligence.
   More importantly, it enables them to transform data into information on-demand to empower every person, process, and system in the organization to be more intelligent.




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

Well this is a basic and vital Machine Learning (ML) concept. You have a dataset=[inputs, associated_outputs] and you want to build a ML algorithm that well learn to relate the inputs to their associated_outputs.
 This is a two step procedure. At first, you train/teach your algorithm how it is done. At this stage, you simply give it the inputs and the answers like you do with a kid.
 The second step is testing; now that the kid has learned, you want to test her/him. So you give her/him similar inputs and check if her/his answers are correct.
 Now, you do not want to give her/him the same inputs he learned because even if she/he gives the correct answers, she/he possibly just memorized the answers from the learning phase (this is called overfitting) and so she/he did not learn a thing.

Similarly you do with your algorithm, you first split your dataset into training data and testing data.
 Then you fit your training data into your algorithm or classifier in this case. This is called the training phase.
  After that you test how good is your classifier and whether he can classify new data correctly. That is the testing phase.
  Based on the testing results, you evaluate the performance of your classification using different evaluation-metrics like accuracy for example.
   The rule of thumbs here is to use 2/3 of the data for the training and 1/3 for the testing.

Plotting 8 features?

The simple answer is no you can't and if you can, please tell me how.

The funny answer: to visualize 8 dimensions, it is easy...just imagine n-dimensions and then let n=8 or just visualize 3-D and scream 8 at it.

The logical answer: So we live in the physical word and the objects we see are 3-dimensional so that is technically kind of the limit.
 However, you can visualize the 4th dimension as the color like in here you can also use the time as your 5th dimension and make your plot an animation.
 @Rohan suggested in his answer shapes but his code did not work for me, and I do not see how that would provide a good representation of the algorithm performance.
 Anyway, colors, time, shapes ... after a while you run out of those and you find yourself stuck. This is one of the reasons people do PCA. You can read about this aspect of the problem under dimensionality-reduction.

So what happens if we settle for 2 features after PCA and then train, test, evaluate and plot?.

Well you can use the following code to achieve that:
 code


-------------------------------------------------------------------------------------------------
data['Insulin'] = data['Insulin'] * .001
plt.figure(figsize = (12, 12))
plt.subplots_adjust(left = 0.45,    # the left side of the subplots of the figure
                    right = 0.95,   # the right side of the subplots of the figure
                    bottom = 0.1,   # the bottom of the subplots of the figure
                    top = 0.9,      # the top of the subplots of the figure
                    wspace = 0.65,  # the amount of width reserved for space between subplots,
                                    # expressed as a fraction of the average axis width
                    hspace = 0.2,   # the amount of height reserved for space between subplots,
                                    # expressed as a fraction of the average axis height
                    )
plt.subplot(5, 1, 1)
data.boxplot(vert=False, labels = column_names,patch_artist=True)
plt.show()
# test various machine learning approaches
ml_tests = MLtests()
ml_tests.run(data)

plt.subplot(5, 1, 2)
data = data[(np.abs(stats.zscore(data)) < 3).all(axis=1)]
data.boxplot(vert=False, labels = column_names,patch_artist=True)
plt.show()
# test various machine learning approaches
ml_tests = MLtests()
ml_tests.run(data)

plt.subplot(5, 1, 3)
scaler = MinMaxScaler(feature_range=(0, 1)) # Making a scaler between 0 and 1
data   = pd.DataFrame(scaler.fit_transform(data.values),  columns = column_names)
data.boxplot(vert=False, labels = column_names,patch_artist=True)
plt.show()
# test various machine learning approaches
ml_tests = MLtests()
ml_tests.run(data)
