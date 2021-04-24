import os

import spacy

from analyzer import Analyzer
from file_analyzer import FileAnalyzer
from progress_bar import progress

nlp = spacy.load("en_core_web_sm")


def analyze_data():
    """
    Loads all .xml-files form the resources folder and analyzes them
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
    a.plot_sentence_distribution()
