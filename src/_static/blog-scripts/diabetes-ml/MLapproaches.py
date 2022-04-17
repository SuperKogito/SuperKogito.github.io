import seaborn as sns
from sklearn import metrics
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

class MLtests:
    def __init__(self):
        # init classifiers and labels dictionaries
        self.classifiers = {
                            "K-Nearest Neighbors (distance weights)": KNeighborsClassifier(weights = 'distance'),
                            "K-Nearest Neighbors (uniform weights)" : KNeighborsClassifier(weights = 'uniform'),
                            "Linear Support Vector Machine"         : SVC(kernel = "linear"),
                            "RBF Support Vector Machine"            : SVC(kernel = "rbf"),
                            "Gaussian Process"                      : GaussianProcessClassifier(),
                            "Decision Tree"                         : DecisionTreeClassifier(),
                            "Random Forest"                         : RandomForestClassifier(),
                            "AdaBoost"                              : AdaBoostClassifier(),
                            "Naive Bayes"                           : GaussianNB(),
                            "Quadratic Discriminant Analysis"       : QuadraticDiscriminantAnalysis()
                            }

        plot_labels =  ["KNN (distance)", "KNN (uniform)", "SVC (linear)",
                        "SVC (rbf)","Gaussian Process" ,"Decision Tree",
                        "Random Forest", "AdaBoost", "Naive Bayes", "QDA"]

        self.labels = dict(zip(list(self.classifiers.keys()),plot_labels))

        # define column names
        self.column_names = ["Pregnancies",                "Glucose", "Blood_pressure",
                             "Skin_thickness",             "Insulin", "Bmi",
                             "Diabetes_Pedigree_Function", "Age",     "Outcome"]

        # init results dictionaries
        self.results            = {}
        self.accuracies         = {}
        self.confusion_matrices = {}
        self.specificities      = {}
        self.sensitivities      = {}
        # folder path to save plots under
        self.plots_path = "../../blog-plots/diabetes-ml/"

    def run(self, data, title):
        self.test(data)
        self.print_results(title)
        self.plot_results(title)

    def test(self, data):
        # split data
        X = data.iloc[:, :-1]
        y = data.iloc[:,  -1]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33,
                                                            random_state = 0)

         # train, fit, test and score
        for name, clf in self.classifiers.items():
            # test using cross-validation
            scores             = cross_val_score(clf, X_train, y_train, cv=5)
            self.results[name] = scores
            # test using fit, predict and score
            clf.fit(X_train, y_train)
            prediction                    = clf.predict(X_test)
            self.accuracies[name]         = metrics.accuracy_score(y_test, prediction)
            self.confusion_matrices[name] = metrics.confusion_matrix(y_test, prediction)
            self.specificities[name]      = self.confusion_matrices[name][0][0] / (self.confusion_matrices[name][0][0] + self.confusion_matrices[name][1][0])
            self.sensitivities[name]      = self.confusion_matrices[name][1][1] / (self.confusion_matrices[name][1][1] + self.confusion_matrices[name][0][1])

    def print_title(self, title):
        '''
        Print titles in style
        '''
        print('------------------------------------------------------------------------------------------------------------')
        print("%70s" % title)
        print('------------------------------------------------------------------------------------------------------------')

    def print_results(self, title):
        # print results for cross-validation
        self.print_title('Results using Cross-validation')
        for name, scores in self.results.items():
            print("%40s | Accuracy: %0.2f%% (+/- %0.2f%%)" % (name,
                                                              100*scores.mean(),
                                                              100*scores.std() * 2))

        # print results for the test using fit, predict and score
        self.print_title(title)
        for name, accuracy in self.accuracies.items():
            print("%40s -> Accuracy: %0.2f | Sensitivity: %0.2f | Specificity: %0.2f | Avg: %0.2f" % (name, accuracy, self.sensitivities[name], self.specificities[name],
                                                                                          (accuracy+ self.sensitivities[name]+ self.specificities[name])/3))

    def plot_results(self, title):
        # plot confusion matrices
        plt.rcParams.update({'font.size': 12})
        fig1 = plt.figure(figsize = (15, 5))
        plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.85,
                            wspace = 0.25, hspace = 0.5)
        for name, confusion_matrix in self.confusion_matrices.items():
            i = list(self.results.keys()).index(name)
            plt.subplot(2, 5, i + 1)
            sns.heatmap(confusion_matrix, annot=True, cbar=False)
            plt.title(self.labels[name])

        fig1.suptitle("Confusion matrices for " + title.replace("accuracies", "confusion matrix"))
        plt.show()
        fig1.savefig(self.plots_path +'_'.join(title.split(" ")) + "-CM.png", transparent=True)

        colors = ["#20639B", "#3CAEA3", "#FF5733", "#FF5700", "y", "b", "g", "w", "r", "m"]
        fig2 = plt.figure(figsize = (20, 10))
        plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.9,
                            wspace = 0.15, hspace = 0.30)
        plt.subplot(3,1,1)
        plt.bar(range(len(self.accuracies)), self.accuracies.values(), width=.5,
                align='center', #color=colors[:len(self.accuracies)]
                )
        plt.xticks(range(len(self.accuracies)), list(self.labels.values()))
        plt.ylim(min(self.accuracies.values()), max(self.accuracies.values()))
        plt.yticks([i/100 for i in range(50, 101, 5)])
        plt.title("Accuracies for " + title)

        plt.subplot(3,1,2)
        plt.bar(range(len(self.sensitivities)), self.sensitivities.values(), width=.5,
                align='center', #color=colors[:len(self.sensitivities)]
                )
        plt.xticks(range(len(self.sensitivities)), list(self.labels.values()))
        plt.ylim(min(self.sensitivities.values()), max(self.sensitivities.values()))
        plt.yticks([i/100 for i in range(50, 101, 5)])
        plt.title("Sensitivities for " + title)

        plt.subplot(3,1,3)
        plt.bar(range(len(self.specificities)), self.specificities.values(), width=.5,
                align='center', #color=colors[:len(self.specificities)]
                )
        plt.xticks(range(len(self.specificities)), list(self.labels.values()))
        plt.ylim(min(self.specificities.values()), max(self.specificities.values()))
        plt.yticks([i/100 for i in range(70, 101, 5)])
        plt.title("Specificities for " + title)

        plt.suptitle("Accuracies, sensitivities and specificities using " + title)
        plt.show()
        fig2.savefig(self.plots_path +'_'.join(title.split(" ")) + "-BAR.png", transparent=True)
