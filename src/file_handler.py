import os

import spacy
import xml.etree.ElementTree as EleTr

from progress_bar import progress

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
                read_file(file_path)
            prog += 1
            progress(prog, file_count, 'Reading files')


def read_file(name):
    """
    Opens a file and reads its content
    :param name: Path of the file
    """
    f = open(name, "r", encoding="utf8")

    doc = nlp(f.read())
    for token in doc:
        pass
        # print(token.text)

    # Creates a XML-Tree for given file
    tree = EleTr.parse(name)
    root = tree.getroot()
    text = root.findall('TEXT')[0]
    tags = root.findall('TAGS')[0]
    # Gets Attributes for a Tag
    for i in tags.findall('PLACE'):
        pass
        # print(i.attrib)


def get_data(file):
    pass
