import csv
import os


def update_dict_occurences(up_dict, key):
    """
    Deals with key and counts up its occurences
    :param key: Selected Key-Element
    :param up_dict: Dictionary to be updated
    """
    if key in up_dict:
        up_dict[key] += 1
    else:
        up_dict[key] = 1


def update_dict_amount(up_dict, key, value):
    """
    Updates a dictionary by adding up a value to a key
    :param up_dict: Dictionary to be updated
    :param key: Selected Key-Element
    :param value: Value to be added
    """
    if key in up_dict:
        up_dict[key] += value
    else:
        up_dict[key] = value


def sort_dict(dictionary, descending=False):
    """
    Sorts a dictionary using the value
    :param dictionary: Dictionary to be sorted
    :param descending: True if the dictionary should be sorted descending
    :return: list: List of Tuples
    """
    return sorted(dictionary.items(), key=lambda x: x[1], reverse=descending)


def sort_tuple_list(unsorted_list, descending=False):
    """
    Sorts a tuple list using the second element of
    :param unsorted_list: List to be sorted
    :param descending: True if the dictionary should be sorted descending
    :return: list: List of Tuples
    """
    return sorted(unsorted_list, key=lambda x: x[1], reverse=descending)


def print_dict_or_tuple_list(print_object, text=''):
    """
    Prints out a Dictionary or a list of tuples
    :param print_object: Dictionary or List of Tuples
    :param text: Heading to be printed above
    """
    if text != '':
        print(f'=== {text} ===')

    if isinstance(print_object, list):
        sorted_object = sort_tuple_list(print_object, True)
    else:
        sorted_object = sort_dict(print_object, True)
    [print(f'{item[0]} - {item[1]}') for item in sorted_object]


def output_csv(path, name, output_list, heading):
    """
    Outputs a list to a .csv file
    :param path: Path where the file should be saved
    :param name: Name of the file
    :param output_list: list of tuples which should be added to file
    :param heading: Header of the .csv file
    """
    # Creates folder if it doesn´t exist
    if not os.path.exists(path):
        os.makedirs(path)

    file_path = os.path.join(path, f'{name}.csv')

    # Writes row to .csv file
    with open(file_path, 'w', newline='') as new_file:
        writer = csv.writer(new_file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(heading)
        for entry in output_list:
            writer.writerow(entry)
