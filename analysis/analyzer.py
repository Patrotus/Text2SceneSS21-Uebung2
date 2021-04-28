import os
import matplotlib.pyplot as plt
from analysis.dict_functions import update_dict_occurences, update_dict_amount, sort_dict, output_csv, print_dict_or_tuple_list
from analysis.progress_bar import progress


class Analyzer:
    """
    The Analyuer object recieves a list of FileAnalyzer and performs an overall analysis on them and outputs the
    results to some .csv files

    :param fas: List of FileAnalyzer
    """
    # Sets variables
    __sentences = {}
    __total_pos = {}
    __total_tag = {}
    __qs_type_dict = {}
    __verbs = {}
    __link_pre = {
        'QSLINK': {},
        'OLINK': {}
    }

    def __init__(self, fas):
        self.__fas = fas
        self.__analyze()

        # Brings the sentences and __verbs in the required format
        self.__sentences_array = sort_dict(self.__sentences, True)
        self.__verbs_array = sort_dict(self.__verbs, True)[:5]

    def __analyze(self):
        """
        Runs an Analysis over all FileAnalyzers in the Analyzer
        """
        print('[INFO] Starting Analysis')

        prog = 0
        total_length = len(self.__fas)

        for fa in self.__fas:
            # Updates Total PoS
            fa_pos_counter = fa.get_pos_counter()
            [update_dict_amount(self.__total_pos, key, fa_pos_counter[key]) for key in fa_pos_counter]

            # Updates everything tag related
            fa_tags = fa.get_tags()
            self.__update_all_tag_dicts(fa_tags)

            # Updates the sentences distribution
            [update_dict_occurences(self.__sentences, sent) for sent in fa.get_sentences()]

            # Prints progressbar
            prog += 1
            progress(prog, total_length, 'Analysing')
        print('\n[INFO] Analysis done')

    def __update_all_tag_dicts(self, fa_tags):
        """
        Performs all necessary updates for the tags of a documents
        :param fa_tags: List of all tags of an FileAnalyzer
        """
        # Gets all SPATIAL_SIGNAL from the tags
        spatial_signal_tags = {item.attrib['id']: item.attrib['text'] for item in fa_tags.findall("SPATIAL_SIGNAL")}

        for item in fa_tags:
            tag = item.tag

            # Updates QSLINK type distribution
            if tag == 'QSLINK':
                update_dict_occurences(self.__qs_type_dict, item.attrib['relType'])
                self.__update_trigger_dict(item, spatial_signal_tags, 'QSLINK')

            # Updates the preposition distribution for QS and OLINK
            elif tag == 'OLINK':
                self.__update_trigger_dict(item, spatial_signal_tags, 'OLINK')

            # Updates the distribution for motion __verbs
            elif tag == 'MOTION':
                update_dict_occurences(self.__verbs, item.attrib['text'])

            # Updates total Tag-Count
            update_dict_occurences(self.__total_tag, tag)

    def __update_trigger_dict(self, tag, signal_dict, key):
        """
        Updates the dictionary keeping the amounts of triggers for QS-/OLINK
        :param tag: Tag
        :param signal_dict: Dictionary of spatial Signals
        :param key: Defines which dictionary in link_pre should be updates
        """
        if 'trigger' in tag.attrib:
            trigger = tag.attrib['trigger']
            if trigger in signal_dict:
                update_dict_occurences(self.__link_pre[key], signal_dict[trigger])

    def plot_sentence_distribution(self, show=True):
        """
        Plots the distribution of the sentences lengths
        """
        file_path = os.path.join(__file__, '..', '..', 'results')
        x_val, y_val = [], []
        for x in self.__sentences_array:
            x_val.append(x[0])
            y_val.append(x[1])
        plt.scatter(x_val, y_val, s=2, c="black", marker='o')
        plt.ylabel('Occurrences')
        plt.xlabel('Sentence Length')
        if show:
            plt.show()

        if not os.path.exists(file_path):
            os.makedirs(file_path)
        plt.savefig(os.path.join(file_path, 'sentence_distribution.png'))

    def output_results_files(self):
        """
        Puts all results of the analysis in a .csv
        :rtype: string: Path to file
        """
        file_path = os.path.join(__file__, '..', '..', 'results', 'csv')
        output_csv(file_path, 'total_pos', sort_dict(self.__total_pos, True), ['PoS', 'Amount'])
        output_csv(file_path, 'total_tag', sort_dict(self.__total_tag, True), ['Tag', 'Amount'])
        output_csv(file_path, 'total_qs_type', sort_dict(self.__qs_type_dict, True), ['QSLINK-relType', 'Amount'])
        output_csv(file_path, 'top_5_verbs', self.__verbs_array, ['Verb', 'Amount'])
        [output_csv(file_path, f'total_link_{key}', sort_dict(self.__link_pre[key], True), ['Trigger', 'Amount'])
         for key in self.__link_pre]
        return file_path

    def debug(self):
        """
        Prints out all the results of the analysis
        """
        print_dict_or_tuple_list(self.__total_pos, 'Verteilung der PoS')
        print_dict_or_tuple_list(self.__total_tag, 'Verteilung der Tags')
        print_dict_or_tuple_list(self.__qs_type_dict, 'Verteilung der "relTypen" in QSLINK')
        print_dict_or_tuple_list(self.__verbs_array, '5 häufigste MOTION-Verben')
        [print_dict_or_tuple_list(self.__link_pre[tag_type], f'Verteilung von {tag_type}') for tag_type in self.__link_pre]
