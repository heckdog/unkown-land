from time import sleep as wait
import data


# default settings
class Settings:
    def __init__(self):
        self.enter_dialog = True
        self.test_setting = True
        self.quickdeath = True


settings = data.load_settings()

# load defaults if none are loaded
if not settings:
    settings = Settings()

# weapons and dmg values
weapons = {"Sword": 70,
           "RPG": 5000,
           "Fists": 10,
           "UNKOWN": 123918312,
           "digional sword": 1000,
           "Beyblade" : 1500,
           "Longsword": 300,
           "Rusty Sword": 30,
           "Longbow": 275}

# below are health values of healing items
health_items = {"bread": 15,
                "Apple": 20,
                "Test Food": 99,
                "Health Potion": 200,
                "Mini Health Potion": 110}

# below items can only be used in battles as item triggers
quest_items = ["Burnt Popcorn", "UNKOWN", "Nap Time"]


def add_commas(number):
    number = round(number)  # should drop any decimals
    number = int(number)  # if broke, this is why
    # variables
    count = 0
    withcommas = ""
    negative = False

    # is it a negative?
    if str(number)[0] == "-":
        negative = True

    for digit in reversed(str(number)):
        withcommas += digit
        count += 1
        if count == 3:
            withcommas += ","
            count = 0

    new = []
    for i in reversed(withcommas):
        new.append(i)

    # stray comma removal
    if negative and new[1] == ",":  # if negative & errored comma
        new[1] = ""
    elif new[0] == ",":  # if postive and error comma
        new[0] = ""

    new_string = ""

    for i in new:
        new_string += i

    return new_string


def talk(dialog, time: float=1):
    if settings.enter_dialog:
        input(dialog)
    else:
        print(dialog)
        wait(time)


def choose(question, choices: list):
    check = True
    lower_choices = [c.lower() for c in choices]

    while check:
        print(question)
        # Show Choices
        for c in choices:
            print("[{}] {}".format(choices.index(c)+1, c))  # give index+1 number and choice
        choice = input(">>>").strip()  # standard input icon

        if choice in choices:  # if the string is in the list
            return choice  # just plop it back as a string
        elif choice in lower_choices:
            return choices[lower_choices.index(choice)]  # return the choice that was in the same index as lower_choices
        else:
            try:  # have to do it this way bc it's very error prone
                if int(choice) <= len(choices):  # this is hoping that the choice is an int at all
                    return choices[int(choice)-1]
            except ValueError:  # we know it will happen. no doubt
                print("'{}' is not a valid option, please try again.".format(choice))


