from dict_functions import update_dict_occurences
import matplotlib.pyplot as plt


class Analyzer:
    def __init__(self, fas):
        self.fas = fas
        self.sentences = []
        self.total_pos, self.total_tag, self.verbs, self.sentences = self.analyze()

    def analyze(self):
        sentence_length = {}
        total_pos = {}
        total_tag = {}
        verbs = {}

        for fa in self.fas:
            fa_pos_counter = fa.get_pos_counter()
            fa_tag_dict = fa.get_tag_dict()
            fa_sentences = fa.get_sentences()

            sentence_length = self.get_sentence_distribution(sentence_length, fa_sentences)
        sentence_items = list(sentence_length.items())
        sentence_items.sort(key=lambda tup: tup[0])


        return self.count_pos_tags(), self.count_tags(), self.count_motion_verb(), sentence_items

    def get_sentence_distribution(self, sent_dict, sentences):
        for sent in sentences:
            update_dict_occurences(sent_dict, sent)
        return sent_dict

    # TODO: Refacotring: Dont iterate over fas multiple times
    def count_pos_tags(self):
        total_pos = {}
        for fa in self.fas:
            fa_pos_counter = fa.get_pos_counter()
            for key in fa_pos_counter:
                if key in total_pos:
                    total_pos[key] += fa_pos_counter[key]
                else:
                    total_pos[key] = fa_pos_counter[key]
        return total_pos

    def count_tags(self):
        total_tag = {}
        for fa in self.fas:
            fa_tag_dict = fa.get_tag_dict()
            for key in fa_tag_dict:
                if key in total_tag:
                    total_tag[key] += len(fa_tag_dict[key])
                else:
                    total_tag[key] = len(fa_tag_dict[key])
        return total_tag

    def sentence_distribution(self):
        sentence_length = {}
        for fa in self.fas:
            sentences = fa.get_sentences()
            for sent in sentences:
                if sent in sentence_length:
                    sentence_length[sent] += 1
                else:
                    sentence_length[sent] = 1
        # Orders the dict ascending before returning it.
        sent_items = list(sentence_length.items())
        sent_items.sort(key=lambda tup: tup[0])
        return sent_items

    def count_motion_verb(self):
        verbs = {}
        for fa in self.fas:
            fa_tag_dict = fa.get_tag_dict()
            if 'MOTION' in fa_tag_dict:
                for verb in fa_tag_dict['MOTION']:
                    motion_verb = verb['text']
                    if motion_verb in verbs:
                        verbs[motion_verb] += 1
                    else:
                        verbs[motion_verb] = 1
        # Sorts the dictionary and returns the 5 tuples with the most entries
        dict_items = list(verbs.items())
        dict_items.sort(key=lambda tup: tup[1], reverse=True)
        return dict_items[:5]

    def plot_sentence_distribution(self):
        x_val, y_val = [], []
        for x in self.sentences:
            x_val.append(x[0])
            y_val.append(x[1])
        plt.scatter(x_val, y_val, s=2, c="black", marker='o')
        plt.ylabel('Occurrences')
        plt.xlabel('Sentence Length')
        plt.show()
