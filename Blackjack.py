import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        complete_deck = ''
        for card in self.deck:
            complete_deck += "\n" + card.__str__()
        return "The deck has:" + complete_deck

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("What Is The Amount That You Would Like To Bet:"))
        except:
            print('That Bet Is Invalid!')
        else:
            if chips.bet > chips.total:
                print("Sorry The Bet Can't Exceed The Total")
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        decision = input('Does The Player Want To Hit Or Stand?')

        if decision == 'Hit':
            hit(deck, hand)
            print('Player Has Hit')

        elif decision == 'Stand':
            print("Player Stands. It Is The Dealer's Turn")
            playing = False

        else:
            print('Sorry Please Try Again')
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(chips):
    chips.lose_bet()
    print('Player Has Lost Bet')


def player_wins(chips):
    chips.win_bet()
    print('Player Has Won Bet')


def dealer_busts(chips):
    chips.win_bet()
    print('Player Has Won Bet')


def dealer_wins(chips):
    chips.lose_bet()
    print('Player Has Lost Bet')


def push():
    print('The game is a tie')


while True:
    # Print an opening statement
    print('Welcome To The Blackjack Game')

    # Create & shuffle the deck, deal two cards to each player
    game_deck = Deck()
    game_deck.shuffle()
    player = Hand()
    player.add_card(game_deck.deal())
    player.add_card(game_deck.deal())

    dealer = Hand()
    dealer.add_card(game_deck.deal())
    dealer.add_card(game_deck.deal())

    # Set up the Player's chips
    chips = Chips()

    # Prompt the Player for their bet
    take_bet(chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(game_deck, player)

        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts(chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player.value <= 21:
        while dealer.value < 17:
            hit(game_deck, dealer)

        # Show all cards
        show_all(player, dealer)

        # Run different winning scenarios
        if dealer.value > 21:
            dealer_busts(chips)

        elif dealer.value > player.value:
            dealer_wins(chips)

        elif dealer.value < player.value:
            player_wins(chips)

        else:
            push()

    # Inform Player of their chips total
    print("Player's chip total is: ", chips.total)

    # Ask to play again
    new_game = input('Do you want to play again? Y or N')

    if new_game == 'Y':
        playing = True
        continue
    else:
        print('Thanks for Playing!')
        break