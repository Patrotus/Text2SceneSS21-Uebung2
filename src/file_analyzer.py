import os
import xml.etree.ElementTree as EleTr
from dict_functions import update_dict_occurences
import graphviz as gviz

NODE_TAGS = {
    'PLACE': 'green',
    'LOCATION': 'lightblue',
    'SPATIAL_ENTITY': 'yellow',
    'NONMOTION_EVENT': 'red',
    'MOTION': 'purple',
    'PATH': "orange"
}

EDGE_TAGS = {
    'QSLINK': 'solid',
    'OLINK': 'dashed'
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
        sentences = [len(sent) for sent in self.doc.sents]
        return sentences

    def get_pos_counter(self):
        return self.pos_counter

    def get_tags(self):
        return self.tags

    def get_sentences(self):
        return self.sentences

    def visualize(self):
        file_name = self.path.split(os.sep)[-1][0:-4]

        graph = gviz.Digraph(comment=file_name, engine='circo')

        tags = self.tags
        metalink_tags = [tag for tag in tags if tag.tag == 'METALINK']
        rest_tags = [tag for tag in tags if tag.tag != 'METALINK']
        for tag in metalink_tags:
            from_id, to_id = tag.attrib['fromID'], tag.attrib['toID']
            rest_tags = self.remove_and_replace(from_id, to_id, rest_tags)

        # TODO: Tags vorher mergen
        merged_tags = []

        node_tags = [tag for tag in rest_tags if tag.tag in NODE_TAGS]
        edge_tags = [tag for tag in rest_tags if tag.tag in EDGE_TAGS]

        # Renders all Nodes
        count = 0
        for tag in node_tags:
            count += 1
            graph.node(name=tag.attrib['id'], label=tag.attrib['text'], fillcolor=NODE_TAGS[tag.tag], style='filled')

        # Renders all Edges
        for tag in edge_tags:
            tag_name = tag.tag
            graph.edge(tail_name=tag.attrib['fromID'], head_name=tag.attrib['toID'], label=tag.attrib['relType'],
                       style=EDGE_TAGS[tag_name])

        # Renders a legend explaining the colors and arrows
        label = '<<TABLE>'
        for tag in NODE_TAGS:
            label += f'<TR><TD BGCOLOR="{NODE_TAGS[tag]}">{tag}</TD></TR>'
        label += '<TR><TD>QSLINK --- &gt;</TD></TR><TR><TD>OLINK - - - &gt;</TD></TR>'
        label += '</TABLE>>'
        graph.attr(label=label)

        print(count)

        file_name = f'test-output/{file_name}.gv'
        graph.render(file_name, view=True)
        os.remove(file_name)

    #FIXME: Ist das richtig so?
    def remove_and_replace(self, old, new, tags):
        for tag in tags:
            if tag.attrib['id'] == old:
                tags.remove(tag)
            elif 'fromID' in tag.attrib and tag.attrib['fromID'] == old:
                tag.attrib['fromID'] = new
            elif 'toID' in tag.attrib and tag.attrib['toID'] == old:
                tag.attrib['toID'] = new
        return tags
