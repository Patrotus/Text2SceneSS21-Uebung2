import xml.etree.ElementTree as EleTr
from dict_functions import update_dict_occurences


class FileAnalyzer:
    def __init__(self, path, nlp):
        """
        Initializer for the FileAnalyzer
        :param path: path of the file to be analyzed
        :param nlp: the nlp provided by spacy
        """
        self.path = path
        root = EleTr.parse(path).getroot()

        text = root.findall('TEXT')[0].text
        self.tags = root.findall('TAGS')[0]
        self.doc = nlp(text)
        self.pos_counter = self.create_pos_counter_dict()
        self.sentences = self.create_sentences_array()

    def create_pos_counter_dict(self):
        pos_counter = {}
        for token in self.doc:
            pos = token.pos_
            update_dict_occurences(pos_counter, pos)
        return pos_counter

    def create_sentences_array(self):
        sentences = []
        for sent in self.doc.sents:
            sentences.append(len(sent.text))
        return sentences

    def get_pos_counter(self):
        return self.pos_counter

    def get_tags(self):
        return self.tags

    def get_sentences(self):
        return self.sentences





