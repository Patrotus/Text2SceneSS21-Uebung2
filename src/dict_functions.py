def update_dict_occurences(up_dict, key):
    """
    Deals with key and counts up its occurences
    :param key: Selected Key-Element
    :param up_dict: Dcitionary to be updated
    """
    if key in up_dict:
        up_dict[key] += 1
    else:
        up_dict[key] = 1


def update_dict_amount(up_dict, key, value):
    if key in up_dict:
        up_dict[key] += value
    else:
        up_dict[key] = value
