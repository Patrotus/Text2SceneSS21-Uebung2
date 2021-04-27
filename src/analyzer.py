from dict_functions import update_dict_occurences, update_dict_amount
import matplotlib.pyplot as plt


class Analyzer:
    sentences = {}
    total_pos = {}
    total_tag = {}
    qs_type_dict = {}
    verbs = {}
    link_pre = {}

    def __init__(self, fas):
        self.fas = fas
        self.analyze()

        # Brings the sentences and verbs in the required format
        sent_items = list(self.sentences.items())
        sent_items.sort(key=lambda tup: tup[0])
        self.sentences_array = sent_items
        verbs = list(self.verbs.items())
        verbs.sort(key=lambda tup: tup[1], reverse=True)
        self.verbs_array = verbs[:5]

    def debug(self):
        print(self.total_tag)
        print(self.total_pos)
        print(self.verbs_array)
        print(self.qs_type_dict)
        print(self.link_pre)

    def analyze(self):
        for fa in self.fas:
            fa_pos_counter = fa.get_pos_counter()
            self.update_total_pos(fa_pos_counter)

            fa_tags = fa.get_tags()
            self.update_tag_dicts(fa_tags)

            fa_sentences = fa.get_sentences()
            self.update_sentence_lengths(fa_sentences)

    def update_tag_dicts(self, fa_tags):
        """
        Performs all neccesary updates for the tags of a documents
        :param fa_tags:
        """
        for item in fa_tags:
            tag = item.tag
            # Updates QSLINK type distribution
            if tag == 'QSLINK':
                update_dict_occurences(self.qs_type_dict, item.attrib['relType'])
            # Updates the preposition distribution for QS and OLINK
            if tag == 'QSLINK' or tag == 'OLINK':
                if item.attrib['trigger']:
                    tag_list = fa_tags.findall(f"./SPATIAL_SIGNAL[@id='{item.attrib['trigger']}']")
                    if len(tag_list) > 0:
                        pre = tag_list[0].attrib['text']
                        update_dict_occurences(self.link_pre, pre)
            # Updates the distribution for motion verbs
            elif tag == 'MOTION':
                update_dict_occurences(self.verbs, item.attrib['text'])
            update_dict_occurences(self.total_tag, tag)

    def update_sentence_lengths(self, sentences):
        """
        Updates the distribution of sentence lenghts
        :param sentences:
        """
        for sent in sentences:
            update_dict_occurences(self.sentences, sent)

    def update_total_pos(self, fa_pos_counter):
        """
        Updates the distribution of the pos tags
        :param fa_pos_counter:
        """
        for key in fa_pos_counter:
            update_dict_amount(self.total_pos, key, fa_pos_counter[key])

    def plot_sentence_distribution(self):
        """
        Plots the distribution of the sentences lengths
        """
        x_val, y_val = [], []
        for x in self.sentences_array:
            x_val.append(x[0])
            y_val.append(x[1])
        plt.scatter(x_val, y_val, s=2, c="black", marker='o')
        plt.ylabel('Occurrences')
        plt.xlabel('Sentence Length')
        plt.show()
