import random


class Card:
    order = ["dop", "wer", "min", "mas", "see", "rob", "tro", "dru", "ins", "tan", "vil", "hun"]

    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def _get_abbrev(self):
        return self._name.lower()[0:3]

    def get_order(self):
        abbrev = self._get_abbrev()
        return self.order.index(abbrev)

    def __eq__(self, other):
        return self._name == other

    def __lt__(self, other):
        return self.get_order() < other

    def __gt__(self, other):
        return self.get_order() > other

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name


class Player:
    def __init__(self, user, card):
        self._user = user
        self._nickname = user.name
        self._card = card

    def get_name(self):
        return self._nickname

    def set_name(self, other):
        self._nickname = other

    def get_card(self):
        return self._card

    def set_card(self, other):
        self._card = other

    def get_user(self):
        return self._user


options = ["Villager", "Werewolf", "Robber", "Seer", "Troublemaker", "Tanner", "Doppelganger", "Drunk", "Minion",
           "Insomniac", "Mason", "Hunter"]


def instructions(role):
    if role == "Werewolf":
        return "Your goal is to convince everyone that you are *not* a werewolf in order to survive the night and win" \
               " the game."
    elif role == "Seer":
        return "You are a villager. You have the ability to find out one player's role during the night, or at least " \
               "what it was at the beginning of the night."
    elif role == "Minion":
        return "You are a villager, but your goal is to help the werewolves (you will find out who they are). You win" \
               " if the werewolves win."
    elif role == "Robber":
        return "You are a villager. During the night you have the ability to steal someone else's role, exchanging" \
               " it for your own and becoming whatever your new role is instead."
    elif role == "Troublemaker":
        return "You are a villager. During the night you have the ability to swap any two players' cards with each " \
               "other or with a card from the centre, although you will not know what roles they have."
    else:
        return "You have no night action. Your goal is to find out who the werewolf or werewolves are and kill them."


def deal(players, deck):
    for n in players:
        card = random.choice(deck)
        deck.remove(card)
        players[n] = card


def default_deck(player_num):
    global options
    deck = [Card("Seer"), Card("Troublemaker"), Card("Werewolf"), Card("Werewolf"), Card("Robber"), Card("Minion")]
    if player_num <= 5:
        for i in range(player_num-1):  # change to 2
            deck.append(Card("Villager"))
    else:  # separate function for this
        for i in range(3):
            deck.append(Card("Villager"))
        for i in range(player_num-5):
            card = input("Input number to select card:\n1. Tanner 2. Doppelganger 3. Drunk 4. Minion 5. Insomniac"
                         "6. Mason 7. Hunter\n")
            deck.append(Card(options[int(card)+5]))
    return deck


def deck_config():
    global options
    deck = []
    card = input("Input number to select cards\n1. Villager 2. Werewolf 3. Robber 4. Seer 5. Troublemaker 6. Tanner"
                 " 7. Doppelganger 8. Drunk 9. Minion 10. Insomniac 11. Mason 12. Hunter\n")
    while card != "done":
        deck.append(Card(options[int(card)-1]))
        card = input("Input more cards or input 'done' to end deck config: ")
    return deck


def sort_players(players):
    player_cards = []
    player_names = []
    for n in players:
        player_cards.append(players[n])
        player_names.append(n)
    swapped = True
    last_unsorted = len(player_cards) - 1
    while swapped:
        swapped = False
        for i in range(last_unsorted):
            if player_cards[i] > player_cards[i+1]:
                player_cards[i], player_cards[i+1] = player_cards[i+1], player_cards[i]
                player_names[i], player_names[i+1] = player_names[i+1], player_names[i]
                swapped = True
        last_unsorted -= 1
    for i in range(len(player_cards)):
        if player_cards[i] == "Villager" or player_cards[i] == "Tanner" or player_cards[i] == "Hunter":
            player_cards.remove(player_cards[i])
            player_names.remove(player_names[i])
    return player_names


def werewolf(players, deck):
    werewolves = []
    for p in players:
        if players[p] == "Werewolf":
            werewolves.append(p.name)  # currently it sends both names lmao
    if len(werewolves) > 1:
        msg = "Your fellow werewolf is: "
        for n in werewolves:
            msg += f'{n} '
    else:
        card = random.choice(deck)
        msg = f'You are the only werewolf so you may look at a card from the centre. That card is a {card.get_name()}.'\
              f'Type -next to continue.'
    return msg


def seer(players, player_id):  # you might want to add a feature where people input their "game names"
    for n in players:
        if n.name == player_id:
            return f'{player_id}\'s card is {players[n].get_name()}. Type -next to continue.'
    return "error"


def robber(players, robber_id, player_id):
    for n in players:
        if n.name == player_id:
            players[robber_id], players[n] = players[n], players[robber_id]
            return f'Your new card is {players[robber_id]}. Type -next to continue'
    return "error"


def troublemaker(players, first_player, second_player):
    index1 = ""
    index2 = ""
    for n in players:
        if n.name == first_player:
            index1 = n
        elif n.name == second_player:
            index2 = n
    players[index1], players[index2] = players[index2], players[index1]
    return f'You have swapped {index1.name} and {index2.name}\'s cards. Type -next to continue'


def minion(players):
    werewolves = []
    for n in players:
        if players[n] == "Werewolf":
            werewolves.append(n.name)
    if len(werewolves) == 0:
        return "There are no werewolves. That's rough buddy /shrug"
    msg = "The werewolves are: "
    for n in werewolves:
        msg += f'{n}'
        if len(werewolves) > 1 and werewolves.index(n) < len(werewolves) - 1:
            msg += ', '
    return msg
