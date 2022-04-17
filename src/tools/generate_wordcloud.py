#!/usr/bin/env python
import os
import argparse
import numpy as np
from os import path
from PIL import Image
import matplotlib.pyplot as plt
from collections import OrderedDict
from wordcloud import WordCloud, STOPWORDS


def get_parser():
    # I'm not making this official, these are for my own testing
    parser = argparse.ArgumentParser(description='Word cloud and bar graph')
    parser.add_argument('--ifile', action='store',
                        type=str,
                        default="",
                        dest='ifile',
                        help='File to read text from')

    parser.add_argument('--cloud', action='store_true',
                        default=False,
                        dest='cloud',
                        help='Generate and save word cloud')

    parser.add_argument('--plot', action='store_true',
                        default=False,
                        dest='plot',
                        help='Generate and save the word plot')

    parser.add_argument('--topn', action='store', type=int,
                        default=25,
                        dest='topn',
                        help='Include the top N words in your plot or cloud')
    return parser

# parse args
parser = get_parser()
args   = parser.parse_args()

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text.
text = open(path.join(d, args.ifile)).read()
text = text.lower()

# get stopwords
custom_sw = open(path.join(d, "stopwords.txt")).read().lower().replace("\n", " ").split(" ")
stopwords = set(STOPWORDS)
stopwords = stopwords.union(custom_sw)
print(stopwords)

bender_mask = np.array(Image.open(path.join(d, "diamond_shape.png")))

wc = WordCloud(background_color="#ffffff", max_words=2000, #mask=bender_mask,
               height=707, width=707,
               stopwords=stopwords, contour_width=3, contour_color="grey")

if args.cloud:
    #
    # Create word cloud
    #
    # generate word cloud
    wc.generate(text)

    # save to file
    wc.to_file(path.join(d, "../_static/meta_images/" + os.path.basename(args.ifile).split(".")[0]) + ".png")

elif args.plot:
    #
    # Create plot
    #
    #wc = WordCloud()
    topwords     = wc.process_text(text)
    sorted_words = sorted(topwords.items(), key=lambda x: x[1])
    sorted_words.reverse()
    print(topwords)
    if len(sorted_words) >= args.topn:
        sorted_words = sorted_words[:args.topn]
    od = OrderedDict(sorted_words)

    plt.rcdefaults()
    font = {'size'   : 12}
    import matplotlib
    matplotlib.rc('font', **font)
    fig, ax = plt.subplots(1, 1, figsize=(25,20))
    ypos    = np.arange(len(od.keys()))
    vals    = list(od.values())
    ax.barh(ypos, vals, align='center', height=0.5)
    ax.set_ylim(bottom=-1, top=25) # Removes excess vertical space. Orig: (-5, 25)
    ax.set_yticks(ticks=ypos, rotation=45)
    ax.set_yticklabels(list(od.keys()))
    #ax.invert_yaxis()
    ax.set_title("Individual Word Counts")
    fig.tight_layout()
    fig.subplots_adjust(top=0.95) # Compresses the whole plot
    fig.savefig('plot.png', dpi=fig.dpi)

else:
    print('No options specified')
