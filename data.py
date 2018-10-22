import os
import pickle
#TODO: find out how tf pickle works

def load(player):
    filename = get_full_path(player)

    try:
        if os.path.exists(filename):
            with open(filename, 'rb') as fin:  # fin = file input
                loaded = pickle.load(fin)
        return loaded
    except TypeError:
        print("File failed to load! Threw a TypeError")
        return None


def load_version():
    version = "N/A"
    filename = get_full_version("version")

    if os.path.exists(filename):
        with open(filename) as fin:
            version = fin.readline()
    return version


def save_version(version):
    new_version = int(version) + 1
    filename = get_full_version("version")

    if os.path.exists(filename):
        with open(filename, "w") as fout:
            fout.write(str(new_version))


def save(player):
    filename = get_full_path(player.name)
    # debug code below - uncomment to use
    # print("..... saving to: {}".format(filename))
    # print(player)
    # print("..... saving: {}".format(player.name))

    with open(filename, "wb") as fout:
        pickle.dump(player, fout)

    print("Saved!")


def get_full_path(name):
    """
    This method takes a string "name" and returns the named file's filepath.

    :param name: The name of the account file
    :return: The full path of a .txt file
    """
    return os.path.abspath(os.path.join('.', 'saves', name + '.sav'))
    # takes the ".", the "accounts", and the "name.txt" to combine into an OS specific path  eg .\accounts\accounts.txt


def get_saves():
    saves_list = []
    for i in os.listdir(os.path.join(".","saves")):
        if i != "version":
            saves_list.append(i[:-4])
    return saves_list


def get_full_version(name):
    return os.path.abspath(os.path.join('.', 'saves', name))


class Player:
    def __init__(self, name, weapon, quest, health, max_health, defence):
        self.name = name
        self.weapon = weapon
        self.quest = quest
        self.health = health
        self.max_health = max_health
        self.defence = defence
        self.completed = 0
        self.xp = 0
        self.level = 1
        self.inventory = {"Test Item" : 100, "bread" : 1231}


if __name__ == "__main__":
    print(load("test"))

