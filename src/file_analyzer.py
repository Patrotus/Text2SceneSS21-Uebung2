import time
import xml.etree.ElementTree as EleTr
from dict_functions import update_dict_occurences
import networkx as nx
import matplotlib.pyplot as plt


VISUALIZED_TAGS = {
    'PLACE': 'red',
    'LOCATION': 'green',
    'SPATIAL_ENTITY': 'blue',
    'NONMOTION_EVENT': 'yellow',
    'PATH': 'orange'
}


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

    def visualize(self):
        G = nx.Graph()
        color_map = []
        i = 1
        for tag in self.tags:
            tag_name = tag.tag
            if tag_name in VISUALIZED_TAGS:
                text = tag.attrib['text']
                print(tag.attrib['id'])
                G.add_node(i, id=tag.attrib['id'], label=text, tag=tag_name)
                # color_map.append(VISUALIZED_TAGS[tag_name])
                i += 1
            if tag_name == 'METALINK':
                # TODO: Wie mit dem mergen in diesen Fällen umzugehen?
                from_id = tag.attrib['fromID']
                to_id = tag.attrib['toID']
                print(from_id, to_id)
                from_node_id = list((n, d['id']) for n, d in G.nodes().items() if d['id'] == from_id)
                to_node_id = list((n, d['id']) for n, d in G.nodes().items() if d['id'] == to_id)
                if len(from_node_id) > 0 and len(to_node_id) > 0:
                    G = nx.contracted_nodes(G, from_node_id[0][0], to_node_id[0][0])

        # Use label attribute as value instead of id
        labels = nx.get_node_attributes(G, 'label')
        # nx.draw(G, labels=labels, node_color=color_map, with_labels=True)
        nx.draw(G, labels=labels, with_labels=True)
        plt.show()



# M = nx.contracted_nodes(G, u, v)






