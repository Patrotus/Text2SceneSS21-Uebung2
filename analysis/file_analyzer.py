import os
import xml.etree.ElementTree as EleTr
import graphviz as gviz

from analysis.dict_functions import update_dict_occurences
from analysis.question import question

# Constants defining the color and arrow style for some tags
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
    """
    Handles the analysis of one file
    :param path: path of the file to be analyzed
    :param nlp: the NLP provided by spacy
    """
    def __init__(self, path, nlp):
        # Sets variables
        self.path = path
        root = EleTr.parse(path).getroot()
        text = root.findall('TEXT')[0].text

        self.doc = nlp(text)
        self.tags = root.findall('TAGS')[0]
        self.pos_counter = self.create_pos_counter()
        self.sentences = [len(sent) for sent in self.doc.sents]

    def create_pos_counter(self):
        """
        Creates a dictionary holding the distribution of all PoS-
        :return: dict: A dictionary of the PoS distribution
        """
        pos_counter = {}
        for token in self.doc:
            update_dict_occurences(pos_counter, token.pos_)
        return pos_counter

    def get_pos_counter(self):
        """
        :return: dict: A dictionary of the PoS distribution
        """
        return self.pos_counter

    def get_tags(self):
        """
        :return: The elment of the element-tree holding all tags
        """
        return self.tags

    def get_sentences(self):
        """
        :return: List of all sentence-lengths
        """
        return self.sentences

    def visualize(self):
        """
        Creates a Graph showing the relation between the different Tags
        """
        file_name = self.path.split(os.sep)[-1][0:-4]
        print(f'--- {file_name} ---')

        graph = gviz.Digraph(comment=file_name, engine='circo')

        # Filters the tags in METALINK and non METALINK tags
        metalink_tags = [tag for tag in self.tags if tag.tag == 'METALINK']
        non_metalink_tags = [tag for tag in self.tags if tag.tag != 'METALINK']

        # Iterates over all Metalinks and merges two tags if necessary
        for tag in metalink_tags:
            from_id, to_id = tag.attrib['fromID'], tag.attrib['toID']
            non_metalink_tags = self.remove_and_replace(from_id, to_id, non_metalink_tags)

        # Filters the non METALINK tags in Nodes and Endges
        node_tags = [tag for tag in non_metalink_tags if tag.tag in NODE_TAGS]
        edge_tags = [tag for tag in non_metalink_tags if tag.tag in EDGE_TAGS]

        # Renders all Nodes
        for tag in node_tags:
            graph.node(name=tag.attrib['id'], label=tag.attrib['text'], fillcolor=NODE_TAGS[tag.tag], style='filled')

        # Renders all Edges
        for tag in edge_tags:
            graph.edge(tail_name=tag.attrib['fromID'], head_name=tag.attrib['toID'],
                       label=tag.attrib['relType'], style=EDGE_TAGS[tag.tag], arrowhead='none')

        # Renders a legend explaining the colors and arrows
        label = '<<TABLE>'
        for tag in NODE_TAGS:
            label += f'<TR><TD BGCOLOR="{NODE_TAGS[tag]}">{tag}</TD></TR>'
        label += '<TR><TD>QSLINK --- &gt;</TD></TR><TR><TD>OLINK - - - &gt;</TD></TR>'
        label += '</TABLE>>'
        graph.attr(label=label)

        # Outputs the files
        save_location = os.path.join('results', 'graph')
        if not os.path.exists(save_location):
            os.makedirs(save_location)

        graph.render(os.path.join(save_location, f'{file_name}.gv'),
                     view=question('Do you want to see the resulting graph?'))

    @staticmethod
    def remove_and_replace(old, new, tags):
        """
        Updates the list of non_metalink_tags on a merge by updating the ids to the tag leftover and removing the
        merged 'old' tag.
        :param old: ID of the old tag
        :param new: ID of the new tag
        :param tags: List of all tags
        :return: list: List of updated tags
        """
        for tag in tags:
            if tag.attrib['id'] == old:
                tags.remove(tag)
            elif 'fromID' in tag.attrib and tag.attrib['fromID'] == old:
                tag.attrib['fromID'] = new
            elif 'toID' in tag.attrib and tag.attrib['toID'] == old:
                tag.attrib['toID'] = new
        return tags
