weapons = {"Sword": 70, "RPG": 5000, "Fists": 10, "UNKOWN": 123918312, "digional sword": 1000, "Beyblade" : 1500, "Longsword" : 300}
# below are health values of healing items
health_items = {"bread": 15, "Apple": 20, "Test Food": 99, "Health Potion": 200}


def add_commas(number):
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
