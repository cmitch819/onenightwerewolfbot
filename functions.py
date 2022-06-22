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
    def __init__(self, user, nickname, card):
        self._user = user
        self._nickname = nickname
        self._card = card
        self._voted = False
        self._num_votes = 0

    def get_name(self):
        return self._nickname

    def set_name(self, other):
        self._nickname = other

    def get_card(self):
        return self._card

    def set_card(self, other):
        self._card = Card(other)

    def get_user(self):
        return self._user

    def vote(self):
        self._voted = True

    def get_vote(self):
        return self._voted

    def num_votes(self):
        return self._num_votes

    def add_vote(self):
        self._num_votes += 1

    def __lt__(self, other):
        return self._num_votes < other.num_votes()

    def __gt__(self, other):
        return self._num_votes > other.num_votes()


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
    elif role == "Tanner":
        return "You are a villager, but your only goal in life is to die. The only way you can win is if you convince" \
               "everyone else to kill you."
    elif role == "Doppelganger":
        return "You can look at anyone else's card. Upon looking, your role becomes whatever that role is and you " \
               "perform the action associated with that role."
    elif role == "Drunk":
        return "You are a villager. On your turn, you switch your role out with a random card from the centre without "\
               "looking at it (so you will have no idea what your role is)."
    elif role == "Insomniac":
        return "You are a villager. On your turn, you are able to look at your role again to see if it was switched" \
               " by the robber or the troublemaker."
    else:
        return "You have no night action. Your goal is to find out who the werewolf or werewolves are and kill them."


def deal(players, deck):
    for n in players:
        card = random.choice(deck)
        deck.remove(card)
        players[n] = card.get_name()
        n.set_card(card.get_name())


def default_deck(player_num):
    global options
    deck = [Card("Seer"), Card("Troublemaker"), Card("Werewolf"), Card("Werewolf"), Card("Robber")]
    for i in range(player_num-2):
        deck.append(Card("Villager"))
    # return [Card("Villager"), Card("Werewolf"), Card("Werewolf"), Card("Werewolf"), Card("Seer"), Card("Robber"),
    # Card("Troublemaker"), Card("Doppelganger"), Card("Drunk"), Card("Insomniac"), Card("Mason"), Card("Mason")]
    return deck


def random_deck(player_num):
    global options
    temp_options = options
    deck = []
    for i in range(player_num + 3):
        card = random.choice(options)
        if card != "Werewolf" and card != "Villager":
            deck.append(Card(card))
        elif card == "Mason":
            deck.append(Card(card))
            deck.append(Card(card))
            temp_options.remove(card)
        else:
            deck.append(Card(card))
            temp_options.remove(card)
    return deck


def sort_players(players):
    player_names = []
    for n in players:
        player_names.append(n)
    swapped = True
    last_unsorted = len(player_names) - 1
    while swapped:
        swapped = False
        for i in range(last_unsorted):
            if player_names[i].get_card() > player_names[i+1].get_card():
                player_names[i], player_names[i+1] = player_names[i+1], player_names[i]
                swapped = True
        last_unsorted -= 1
    return player_names


def werewolf(players, deck, player):
    werewolves = []
    for p in players:
        if p.get_card() == "Werewolf":
            werewolves.append(p.get_name())
    if len(werewolves) > 1:
        msg = "Your fellow werewolves are: "
        for n in werewolves:
            if n != player.get_name():
                msg += f'{n} '
        msg += ". Type -next to continue."
    else:
        card = random.choice(deck)
        msg = f'You are the only werewolf so you may look at a card from the centre. That card is a {card.get_name()}.'\
              f' Type -next to continue.'
    return msg


def seer(players, player_id):
    for n in players:
        if n.get_name() == player_id:
            return f'{player_id}\'s card is {players[n]}. Type -next to continue.'
    return "error"


def robber(players, robber_id, player_id):
    for n in players:
        if n.get_name() == player_id:
            robber_id.set_card(players[n])
            n.set_card("Robber")
            return f'Your new card is {robber_id.get_card().get_name()}. Type -next to continue'


def troublemaker(players, first_player, second_player):
    index1 = ""
    index2 = ""
    for n in players:
        if n.get_name() == first_player:
            index1 = n
        elif n.get_name() == second_player:
            index2 = n
    temp = index1.get_card().get_name()
    index1.set_card(index2.get_card().get_name())
    index2.set_card(temp)
    return f'You have swapped {index1.get_name()} and {index2.get_name()}\'s cards. Type -next to continue'


def minion(players):
    werewolves = []
    for n in players:
        if players[n] == "Werewolf":
            werewolves.append(n.get_name())
    if len(werewolves) == 0:
        return "There are no werewolves. You're on your own. Type -next to continue."
    msg = "The werewolves are: "
    for n in werewolves:
        msg += f'{n}'
        if len(werewolves) > 1 and werewolves.index(n) < len(werewolves) - 1:
            msg += ', '
    msg += "Type -next to continue."
    return msg


def doppelganger(players, player_id, copy_id):
    for n in players:
        if n.get_name() == copy_id:
            player_id.set_card(n.get_card().get_name())
            return


def drunk(deck, player_id):
    card = random.choice(deck)
    deck.remove(card)
    deck.append(Card("Drunk"))
    player_id.set_card(card.get_name())
    return f'Your role has been swapped. Type -next to continue.'


def insomniac(player_id):
    return f'Your current role is {player_id.get_card().get_name()}. Type -next to continue.'


def mason(players, player_id):
    for n in players:
        if n.get_card().get_name() == "Mason" and n.get_name() != player_id.get_name():
            return f'Your fellow mason is {n.get_name()}. Type -next to continue.'
    return f'There are no other masons among the players. Type -next to continue.'
