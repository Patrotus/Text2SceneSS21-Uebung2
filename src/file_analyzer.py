import xml.etree.ElementTree as EleTr


class FileAnalyzer:
    pos_dict = { }

    def __init__(self, name, nlp):
        self.name = name
        self.root = EleTr.parse(name).getroot()

        text = self.root.findall('TEXT')[0].text
        self.doc = nlp(text)

    def analyse_text(self):
        for token in self.doc:
            pos = token.pos_
            self.handle_pos(pos)

    def handle_pos(self, pos):
        if pos in self.pos_dict:
            self.pos_dict[pos] = self.pos_dict[pos] + 1
        else:
            self.pos_dict[pos] = 1
