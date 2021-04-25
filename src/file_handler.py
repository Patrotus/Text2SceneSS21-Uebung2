import os
import spacy
from analyzer import Analyzer
from file_analyzer import FileAnalyzer
from progress_bar import progress

nlp = spacy.load("en_core_web_sm")


def analyze_all_files(path):
    """
    Loads all .xml-files form the resources folder and analyzes them
    """

    file_count = sum(len(files) for _, _, files in os.walk(path))
    prog = 0

    fa_array = []
    # Root = current_folder, dirs = list of dirnames, files = list of filenames
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                Fa = FileAnalyzer(file_path, nlp)
                fa_array.append(Fa)
            prog += 1
            progress(prog, file_count, 'Reading files')
    print('\n' + 'Done reading files. Analysis is starting.')

    A = Analyzer(fa_array)
    A.plot_sentence_distribution()

    A.debug()

def analyze_and_graph(files):
    print('Starting analysis of the single files.')
    for file in files:
        fa = FileAnalyzer(file, nlp)
        fa.visualize()
