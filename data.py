import os


def load(player):
    filename = get_full_path(player)

    try:
        if os.path.exists(filename):
            num_lines = sum(1 for line in open(filename))
            with open(filename) as fin:  # fin = file input
                name = fin.readline().rstrip()
                weapon = fin.readline().rstrip()
                quest = fin.readline().rstrip()
                health = fin.readline().rstrip()
                max_health = fin.readline().rstrip()
                defence = fin.readline().rstrip()
                xp = fin.readline().rstrip()
                completed = fin.readline().rstrip()
                level = fin.readline().rstrip()
                money = fin.readline().rstrip()
                placeholder = fin.readline().rstrip()  # to skip the "INV" - DO NOT REMOVE
                inventory = {}
                for i in range(num_lines):
                    item = fin.readline().rstrip()
                    count = fin.readline().rstrip()
                    if item == "" or count == "":
                        break
                    inventory[item] = int(count)

        loaded = Player(name, weapon, quest, int(health), int(max_health), int(defence))
        loaded.xp = int(xp)
        loaded.completed = int(completed)
        loaded.level = int(level)
        loaded.money = int(money)
        loaded.inventory = inventory
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

    with open(filename, "w") as fout:
        fout.write("{}\n".format(player.name))
        fout.write("{}\n".format(player.weapon))
        fout.write("{}\n".format(player.quest))
        fout.write("{}\n".format(player.health))
        fout.write("{}\n".format(player.max_health))
        fout.write("{}\n".format(player.defence))
        fout.write("{}\n".format(player.completed))
        fout.write("{}\n".format(player.xp))
        fout.write("{}\n".format(player.level))
        fout.write("{}\n".format(player.money))
        fout.write("INV\n")
        for item in player.inventory:
            fout.write(item + "\n")
            fout.write(str(player.inventory[item]) + "\n")

    print("Saved!")


def get_full_path(name):
    """
    This method takes a string "name" and returns the named file's filepath.

    :param name: The name of the account file
    :return: The full path of a .txt file
    """
    return os.path.abspath(os.path.join('.', 'saves', name + '.sav'))
    # takes the ".", the "accounts", and the "name.txt" to combine into an OS specific path  eg .\accounts\accounts.txt


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
