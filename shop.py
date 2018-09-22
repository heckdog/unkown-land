# the store contents is housed all within this dict
store = {"bread": 20, "Test Item": 200, "Health Potion": 100}


def shop(player):
    print("\n----{SHOP}----")
    print("Welcome to the Shop! Whatcha lookin' for?")
    print("[B]uy [S]ell [L]eave [Q]uest")
    option = input(">>>").strip().lower()

    #Buying
    if option == "b" or option == "buy":
        print("Here's what I've got in stock:")
        print("----------------")
        for item in store:
            price = store[item]
            print("{} -- {}G".format(item, price))
        print("----------------")
        print("You have {}G".format(player.money))
        choice = input("What would you like?\n>>>")
        if choice in store:
            price = store[choice]
            try:
                amount = int(input("How many?\n>>>"))
            except TypeError:
                amount = 1  # if u dunno how to put numbers u get one deal with it
            total = amount * price
            confirm = input("Buy {} {} for {}G? (y/n)\n>>>".format(amount, choice, total)).lower().strip()
            if confirm == "y" or confirm == "yes":
                player.money += -total
                print("Sold! You now have {}G.".format(player.money))
                if choice in player.inventory:  # if the item already exists in player inventory
                    player.inventory[choice] += amount  # set the items amount higher
                else:  # else, if its a new item
                    player.inventory.update({choice: amount})  # create it using this method. idk why it has to be this way, otherwise throws KeyError
            else:
                print("ok then nvm u wont get it smh")
        else:
            print("\"{}\" is not one of my options u silly goose. Even if it was, you'd need to bring some cash.".format(choice))
    elif option == "s" or option == "sell":
        print("[Sell] is currently being worked on.")
    elif option == "q" or option == "quest":
        print("You would get a quest here whenever one gets coded.")
    else:
        print("lol not available rn sorry")
