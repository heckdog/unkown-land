from essentials import add_commas
from time import sleep

#the store contents is housed all within this dict
store = {"bread": 20, "Test Item": 200, "Health Potion": 100}
weapon_store = {"Sword": 100, "digional sword": 100000}


def shop(player):
    print("\n----{SHOP}----")
    print("-Welcome to the Shop! Whatcha lookin' for?")
    print("[B]uy [S]ell [L]eave [Q]uest")
    option = input(">>>").strip().lower()

    #Buying
    if option == "b" or option == "buy":
        print("-Here's what I've got in stock:")
        print("----------------")
        for item in store:
            price = store[item]
            print("{} -- {}G".format(item, add_commas(price)))
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
                print("Sold! You now have {}G.".format(add_commas(player.money)))
                if choice in player.inventory:  # if the item already exists in player inventory
                    player.inventory[choice] += amount  # set the items amount higher
                else:  # else, if its a new item
                    player.inventory.update({choice: amount}) # create it using this method. idk why it has to be this way, otherwise throws KeyError
            else:
                print("-ok then nvm u wont get it smh")
        else:
            print("-\"{}\" is not one of my options rarted. Even if it was, you'd need to bring some cash.".format(choice))
    elif option == "l" or option == "leave":
        print("-See ya bruv.")
    elif option == "q" or option == "quest":
        print("-Eh? You want a quest?")
        sleep(1)
        print("-Alright, I've got one. There's been this one guy, he keeps coming in here with tons of money but robs me anyways.")
        sleep(3)
        print("-He comes in, summons buckets of money, buys 1000s of bread, then the money just vanishes!")
        sleep(1.5)
        print("-I'm not sure how this guy does it, but I don't trust him.")
        sleep(1)
        print("-He's up to something for sure, I tell ye. Here's where I last saw the nard, go give him a piece of your mind, will ye?")
        sleep(3)
        choice = input("Accept Quest? (y/n) \n>>>").lower()
        if choice.find("ye") != -1 or choice == "y":
            print("-Thanks a lot mate, I'll be sure to reward ye once yer back.")
            if player.quest:
                print("-Oh, ye already have a quest. '{}'. Come back once ye done that yeh?")
            else:
                print("-Aight lad, I've updated yer quest log for ye.")
                player.quest = "Beat up the Developer"
        else:
            print("-Aight then lad, come again some other time. I'm sure he's still out and about, robbin me mates' stores or sum'n."
                  "\n-Keep yer eye out tho, who knows where 'eel turn up next, I tell ye.")
    else:
        print("lol not available rn sorry")
