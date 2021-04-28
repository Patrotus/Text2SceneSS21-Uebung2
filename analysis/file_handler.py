import os
import spacy
from analysis.analyzer import Analyzer
from analysis.file_analyzer import FileAnalyzer
from analysis.progress_bar import progress
from analysis.question import question

# Loads the nlp model
NLP = spacy.load("en_core_web_sm")


def analyze_all_files(path):
    """
    Loads all .xml-files form the resources folder and analyzes them
    :param path: Path to the resources folder
    """
    file_count = sum(len(files) for _, _, files in os.walk(path))
    prog = 0

    fa_array = []
    # Iterates over all files in the path
    for root, _, files in os.walk(path):
        for file in files:
            # Analyses file, if it is of type .xml
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                Fa = FileAnalyzer(file_path, NLP)
                fa_array.append(Fa)
            prog += 1
            progress(prog, file_count, 'Reading files')
    print('\n[INFO] Done reading files.')

    if len(fa_array) > 0:
        # Outputs stuff
        A = Analyzer(fa_array)

        A.plot_sentence_distribution(question('Do you want to see the sentence distribution?'))

        # TODO: Remove me
        A.debug()

        path = A.output_results_files()
        print(f'[INFO] Files saved at: {os.path.abspath(path)}')


def analyze_and_graph(files):
    """
    Performs an analysis on a list of files and visualizes their graph
    :param files: List of files to be visualized
    """
    print('[INFO] Starting analysis of the single files.')
    for file in files:
        fa = FileAnalyzer(file, NLP)
        fa.visualize()
