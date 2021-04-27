import os

from file_handler import analyze_all_files, analyze_and_graph

if __name__ == '__main__':
    print(os.path.abspath(os.getcwd()))
    training_data_location = os.path.join('..', 'resources', 'training', 'Training')
    bicyles = os.path.join(training_data_location, 'RFC', 'Bicycles.xml')
    hightlights_prado_museum = os.path.join(training_data_location, 'ANC', 'WhereToMadrid',
                                            'Highlights_of_the_Prado_Museum.xml')
    analyze_all_files(training_data_location)
    analyze_and_graph([bicyles, hightlights_prado_museum])

