import os
import spacy

from progress_bar import progress
from file_analyzer import FileAnalyzer

nlp = spacy.load("en_core_web_sm")


def load_data():
    """
    Loads all .xml-files form the resources folder
    """
    training_data_location = os.path.join('.', 'resources', 'training', 'Training')
    print(training_data_location)

    file_count = sum(len(files) for _, _, files in os.walk(training_data_location))
    prog = 0

    # Root = current_folder, dirs = list of dirnames, files = list of filenames
    for root, dirs, files in os.walk(training_data_location):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                fa = FileAnalyzer(file_path, nlp)
                fa.analyse_text()
            prog += 1
            progress(prog, file_count, 'Reading files')


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

