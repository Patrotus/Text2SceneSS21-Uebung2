import xml.etree.ElementTree as EleTr


class FileAnalyzer:
    pos_dict = {}

    def __init__(self, path, nlp):
        """
        Initializer for the FileAnalyzer
        :param name: path of the file to be analyzed
        :param nlp: the nlp provided by spacy
        """
        self.path = path
        self.root = EleTr.parse(path).getroot()

        text = self.root.findall('TEXT')[0].text
        self.doc = nlp(text)

    def analyse_text(self):
        """
        Analyses the loaded text
        """
        for token in self.doc:
            pos = token.pos_
            self.handle_pos(pos)

    def handle_pos(self, pos):
        """
        Deals with every pos of a text and counts up the amount of occurences
        :param pos: Selected PartOfSpeech-Element
        """
        if pos in self.pos_dict:
            self.pos_dict[pos] = self.pos_dict[pos] + 1
        else:
            self.pos_dict[pos] = 1
