import os


def load_data():
    """
    Loads all .xml-files form the resources folder
    """
    training_data_location = os.path.join('.', 'resources', 'training', 'Training')
    print(training_data_location)

    # Root = current_folder, dirs = list of dirnames, files = list of filenames
    for root, dirs, files in os.walk(training_data_location):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                read_file(file_path)


def read_file(name):
    """
    Opens a file and reads its content
    :param name: Path of the file
    """
    f = open(name, "r", encoding="utf8")
    print(f.read())
