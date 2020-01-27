import seaborn as sns
import matplotlib.pyplot as plt


class DfPlotter:
    def __init__(self, column_names):
        self.column_names = column_names 
        # folder path to save plots under
        self.plots_path = "../../../docs/source/_static/blog-plots/diabetes-ml/"
    
    def plot_correlation(self, data):
        '''
        plot correlation's matrix to explore dependency between features 
        '''
        #plt.rcParams.update({'font.size': 12})
        # init figure size
        fig = plt.figure(figsize = (23, 23))
        plt.subplots_adjust(left = 0.15, 
                            right = 0.97,
                            bottom = 0.15, 
                            top = 0.97     )
                
        sns.heatmap(data.corr(), annot = True, 
                    annot_kws = {'size':16}, fmt = ".2f", linewidth= .15)
        plt.show()
        fig.savefig(self.plots_path + 'corr.png', transparent=True)
        
    def plot_densities(self, data):
        '''
        Plot features densities depending on the outcome values
        '''
        # separate data based on outcome values 
        outcome_0 = data[data['Outcome'] == 0]
        outcome_1 = data[data['Outcome'] == 1]
        names     = list(data.columns)
        # init figure
        fig, axs = plt.subplots(8, 1, figsize = (20, 15))
        fig.suptitle('Features densities for different outcomes 0/1')
        plt.subplots_adjust(left = 0.1, right = 0.9, bottom = 0.05, top = 0.95,
                            wspace = 0.2, hspace = 0.9)
                 
        # plot densities for outcomes
        for column_name in names[:-1]: 
            ax = axs[names.index(column_name)]
            # plt.subplot(4, 2, names.index(column_name) + 1)
            outcome_0[column_name].plot(kind     = 'density',
                                        ax       = ax,
                                        subplots = True, 
                                        sharex   = False, 
                                        color    = "green", 
                                        legend   = True,
                                        label    = column_name + ' for Outcome = 0')
            outcome_1[column_name].plot(kind     = 'density',
                                        ax       = ax,
                                        subplots = True, 
                                        sharex   = False, 
                                        color    = "red", 
                                        legend   = True,
                                        label    = column_name + ' for Outcome = 1')
            ax.legend(shadow=False, framealpha=0.0, facecolor=None)
            ax.set_xlabel(column_name + ' values')
            ax.set_title(column_name + ' density')
            ax.grid('on')
        plt.show()
        fig.savefig(self.plots_path + 'densities.png', transparent=True)

    def plot_pairplot(self, data):
        try:
            sns_plot = sns.pairplot(data, hue = 'Outcome', palette = ['g', 'r'])
            sns_plot.savefig(self.plots_path + 'pairplot.png', transparent=True)
        except Exception as e: 
            print(e)

    def plot_bars(self, data):
        fig = plt.figure(figsize = (10, 12))
        plt.subplots_adjust(left = 0.1, right = 0.95, bottom = 0.05, top = 0.95,
                            wspace = 0.65, hspace = 0.25)
        for i in range(0, 8):
            plt.subplot(2, 4, i + 1)
            sns.barplot(x       = 'Outcome', 
                        y       = list(data.columns)[i],
                        hue     = "Outcome",
                        data    = data, 
                        palette = ['g', 'r'])
        plt.show()
        fig.savefig(self.plots_path + 'bars.png', transparent=True)

    def plot_overview(self, data):
        f, ax = plt.subplots(1, 2, figsize = (10, 10))
        outcome = data.Outcome.value_counts()
        f.suptitle("Samples count and percentage based on outcome", fontsize = 18.)
        outcome.plot.bar(ax = ax[0], rot = 0, color = ('g', 'r')).set(xticklabels = ["Outcome = 0", "Outcome = 1"])
        outcome.plot.pie(labels = ("Outcome = 0", "Outcome = 1"), 
                        autopct = "%.2f%%", label = "", fontsize = 13.,
                        ax = ax[1], colors = ('g', 'r'), wedgeprops = {"linewidth": 1.5, "edgecolor": "#F7F7F7"})
        ax[1].texts[1].set_color("w")
        ax[1].texts[3].set_color("w")
        f.savefig(self.plots_path + 'samples_overview.png', transparent=True)
         
    def boxplot(self, data):
        data.boxplot(vert=False, labels = self.column_names,patch_artist=True)
        plt.show()