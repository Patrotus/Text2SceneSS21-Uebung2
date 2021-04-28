def question(text):
    """
    Asks a question and returns True, if the answer is y
    :param text: Text of the question
    :return: boolean: Question answered with yes?
    """
    return input(f'{text} y/n ---> ').lower() == 'y'
