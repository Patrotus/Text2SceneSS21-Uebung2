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


def sort_list(unsorted_list, descending=False):
    """
    Sorts a tuple list using the second element of
    :param unsorted_list: List to be sorted
    :param descending: True if the dictionary should be sorted descending
    :return: list: List of Tuples
    """
    return sorted(unsorted_list, key=lambda x: x[1], reverse=descending)
