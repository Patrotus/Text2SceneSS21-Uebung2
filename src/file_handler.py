import os
import spacy

from progress_bar import progress
from file_analyzer import FileAnalyzer
from analyzer import Analyzer

import matplotlib.pyplot as plt
import numpy as np


nlp = spacy.load("en_core_web_sm")


def load_data():
    """
    Loads all .xml-files form the resources folder
    """
    training_data_location = os.path.join('.', 'resources', 'training', 'Training')
    print(training_data_location)

    file_count = sum(len(files) for _, _, files in os.walk(training_data_location))
    prog = 0

    fa_array = []
    # Root = current_folder, dirs = list of dirnames, files = list of filenames
    for root, dirs, files in os.walk(training_data_location):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                fa = FileAnalyzer(file_path, nlp)
                fa_array.append(fa)
            prog += 1
            progress(prog, file_count, 'Reading files')
    print('\n' + 'Done reading files. Analysis is starting.')

    a = Analyzer(fa_array)
    a.count_pos_tags()
    a.count_tags()
    sent_distr = a.sentence_distribution()
    a.count_motion_verb()
    plot_sentence_distribution(sent_distr)


def plot_sentence_distribution(dist):
    x_val = [x[0] for x in dist]
    y_val = [x[1] for x in dist]
    plt.scatter(x_val, y_val, s=2, c="black", marker='o')
    plt.ylabel('Occurrences')
    plt.xlabel('Sentence Length')
    plt.show()
    # plt.hist(x_val, bins=25)
    # plt.hist(x_val, y_val, 'or')



##### DEAD CODE: Only as Lookup ############
#
# def read_file(name):
#     """
#     Opens a file and reads its content
#     :param name: Path of the file
#     """
#     f = open(name, "r", encoding="utf8")
#     tree = EleTr.parse(name)
#     root = tree.getroot()
#
#     # List of tags
#     tags = root.findall('TAGS')[0]
#     # Creates a processed doc
#
#     # Creates a XML-Tree for given file
#     # Gets Attributes for a Tag
#     for i in tags.findall('PLACE'):
#         pass
#         # print(i.attrib)
############################################

