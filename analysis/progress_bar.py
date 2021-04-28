import sys


def progress(count, total, text=''):
    """
    Renders a simple progress bar
    :param count: Current count
    :param total: Total count of objects
    :param text: Message at the end of the bar
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write(f'|{bar}| {percents}% ...{text}\r')
    sys.stdout.flush()
