# Name: Ganesh Kumar
# Date: 03/11/2025
# Instructor: Professor Andres Calle
# Course ID: CIST-005B-34571
# Project Information: For this lab, you will be joining with a new group to create
# a homebrewed card game of your own in the style of games like:
# Uno
# Magic: The Gathering
# Hearthstone
# This card game will familiarize you with the use of inheritance and polymorphism in python,
# as well as implementing a linked list data structure.
# Import random library
import random

# Linked List Implementation for Card Deck
class Node:
    # Default Constructor
    def __init__(self, card):
        self.card = card
        self.next = None


# LinkedList class to manipulate the list with append, remove, and shuffle methods.
class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    # Append method appends a card to the end of the linked list.
    # Time complexity of append is O(n) - Linear Time Complexity.
    def append(self, card):
        # Create a reference
        newNode = Node(card)

        # Loop
        # Case 1: List is empty.
        if(self.head == None):
            self.head = newNode
            newNode.next = None
            self.size += 1
            return
        # Case 2: List is not empty.
        # Start from the head node.
        currNode = self.head
        while(currNode.next != None):
            currNode = currNode.next
        # Attach the new node at the end.
        currNode.next = newNode
        newNode.next = None
        self.size += 1
        return

    # Remove method removes the first card from the head.
    # Time complexity is O(1) - Constant Time Complexity.
    def remove(self):
        # If the list is empty, return None.
        if self.head is None:
            return None
        # Otherwise return the first card and move the head to the next card.
        else:
            # Get the first data from the head.
            card = self.head.card
            # Move the head to the next node.
            self.head = self.head.next
            # Decrement the size by 1.
            self.size -= 1
            # Return the card from the head of the list.
            return card

    # Shuffle method shuffles the deck of cards by converting it into a list and then shuffling.
    def shuffle(self):
        # Collect the cards in the linked list into a list.
        cards = []
        card = self.remove()
        # current = self.head
        # Place the cards on the cards list.
        while card != None:
            cards.append(card)
            card = self.remove()
        # Use the random function shuffle to randomize the cards in the list.
        random.shuffle(cards)
        # self.head = None
        # Put them back into the linked list.
        for card in cards:
            self.append(card)

    def display(self):
        # Create a reference/pointer that
        # allows up to keep track of the current node
        # Loop through the list
        currNode = self.head
        if(currNode == None):
            print("The list is empty!")
            return
        while(currNode != None):
            print(currNode.card, end=" ->")
            #print(currNode)
            currNode = currNode.next
        print("Null")
        return


# Base Card abstract class for common card functionality
# Children classes inherit the attributes and implement the method 
# functions specific to the children classes.
class Card:
    # Default contructor
    def __str__(self):
        return f"{self.color} {self.name}"

    # Constructor
    def __init__(self, name, color, card_type):
        self.name = name
        self.color = color  # Color for Uno (Red, Blue, Green, Yellow)
        self.card_type = card_type  # Regular or special cards (e.g., Skip, Reverse, Wild)

    # Abstract method to play a card
    def play(self, player, game):
        # Abstract method: No effect.
        pass


# Regular Card (Numbered cards) class implements a numbered card.
# The cards consist of 4 colors (Red, Green, Yellow, and Blue) and are numbered from 0-9.
class NumberedCard(Card):
    def __init__(self, color, number):
        self.number = number # Initialize NumberedCard data
        # Initialize the parent class data.
        super().__init__(f"{number}", color, "Regular")

    # Method function to play a numbered card.
    # In the simplified implementation of this UNO game, the numbered cards are played without
    # any restrictions- prints a message saying that the numbered card has been played.
    def play(self, player, game):
        # Number cards are simply played without additional effects.
        print(f"{player.name} played {self.color} {self.name}")


# Special Card SkipCard forces the opponent to skip their turn
# A player plays this card to force the opponent to skip their turn.
class SkipCard(Card):
    def __init__(self, name, color, card_type):
        super().__init__(name, color, card_type)

    def play(self, player, game):
        # Special cards change the game rules, checks if the card is a skip card and prints a message
        # saying the turn is skipped and calls the skip_turn method.
        if self.card_type == "Skip":
            print(f"{player.name} played Skip!")
            game.skip_turn()


# Color Change Card changes the color of the card by randomly picking a new color
# ColorChangeCard makes an effect to change the current color played by
# randomly choosing a new color. Player plays this card to force a new color.
class ColorChangeCard(Card):
    def __init__(self, name, card_type):
        super().__init__(name, None, card_type)

    # Use a random choice library function to pick a random color
    # and change the current color of the game.
    def play(self, player, game):
        # Color change cards can change the current color being played.
        print(f"{player.name} played a Color Change Card!")
        # Automatically choose a color for simplicity
        new_color = random.choice(['Red', 'Blue', 'Green', 'Yellow'])
        print(f"New color chosen: {new_color}")
        game.change_color(new_color)

# DoubleTroubleCard is a special card and the player forces the opponent to draw two cards
# from the shuffled deck.
class DoubleTroubleCard(Card):
    def __init__(self, name, card_type):
        super().__init__(name, None, card_type)
        self.double_draw = 0

    # Play method to force the user to draw two cards from the deck.
    def play(self, player, game):
        print(f"{player.name} played a Double Trouble Card!")
        self.double_draw = 2
        game.double_trouble(self.double_draw)


# Game Class that manages the game state
# Attributes of the Game class are:
# 1. A list of players
# 2. Current players
# 3. Current color
# 4. Deck is a linked list, which consists of numbered cards.
# 5. Special cards such as skip, color change, and double trouble.
# The deck will be randomly shuffled before the game starts.
# Game Class also implements a method for log and display player actions.
class Game:
    def __init__(self, players):
        # Players is a list
        self.players = players
        # Track the current players turn, bounces between 0 and 1.
        self.current_player_index = random.randint(0, 1)
        # Tracks the current color of the game.
        self.current_color = None
        self.deck = LinkedList() # Deck is a linked list of cards.
        # Discard pile collects all the cards that are drawn during the game.
        self.discard_pile = []

        # Initialize deck with regular and special cards
        self.initialize_deck()
        # Shuffles deck of cards.
        self.shuffle_deck()
        # Game logging list2
        self.log = []

    # Create a deck of cards with:
    # 1. Four colors
    # 2. Numbered cards ranged from 0-9.
    # Adds 8 skip cards.
    def initialize_deck(self):
        # Fill the deck with regular and special cards.
        colors = ['Red', 'Blue', 'Green', 'Yellow']
        # Add numbered cards (0-9)
        for color in colors:
            for number in range(10):
                # Append the cards to the end of the linked list.
                self.deck.append(NumberedCard(color, number))
            # Add special skipCards to the deck.
            for _ in range(2):  # Two of each special card
                self.deck.append(SkipCard("Skip", color, "Skip"))


        # Add 4 color change cards and double trouble cards to the deck.
        for _ in range(4):
            self.deck.append(ColorChangeCard("Color Change", "Color Change"))
            self.deck.append(DoubleTroubleCard("Double Trouble", "Double Trouble"))

        self.deck.display()

    # Game class method shuffle_deck shuffles the cards using the linked list method shuffle.
    def shuffle_deck(self):
        # Shuffle the deck.
        self.deck.shuffle()
        print("After shuffle: ")
        self.deck.display()

    # Draw the card from the linked list deck.
    # Append it to the player's hand.
    def draw_card(self, player):
        # Draw a card from the deck.
        card = self.deck.remove()
        if card:
            player.hand.append(card)
            self.log_action(f"{player.name} drew {card}")
            print(f"{player.name} drew {card}")

    # Method play_card calls the play method for different types of cards.
    # Rules of the game:
    # 0. Each player is dealt 7 cards from the randomized deck.
    # 1. The player who as an active turn will draw one card from their hand.
    # 2. If it is a numbered card, check the color and number.
    # If the color or number matches, then the player discards the card and the card
    # is removed from their hand and is placed in the discard pile.
    # 3. If the player draws a skip turn card, the player forces the opponent
    # to skip their turn.
    # 4. The player changes the game color until the next color change card.
    # 5. If the player draws a double trouble card, the player forces the
    # opponent to draw 2 cards.
    # 6. The player exhausts all their cards in their hand.
    def play_card(self, player, card_index):
        # Play a card from a player's hand.
        if 0 <= card_index < len(player.hand):
            card = player.hand.pop(card_index)
            if len(self.discard_pile):
                if card.color == self.current_color or card.name == self.discard_pile[-1]:
                    self.discard_pile.append(card)
                    self.log_action(f"{player.name} played {card}")
                    card.play(player, self)
                else:
                    # put the card back in payers hand
                    player.hand.append(card)
                    self.skip_turn()
        else:
            print("Invalid card selection.")

    # Color change method function changes the game color until the next color change card forces it
    # to a different color.
    def change_color(self, color):
        # Change the current color of the game.
        self.current_color = color
        self.log_action(f"Current color is now {self.current_color}.")
        print(f"Current color is now {self.current_color}.")

    # Player uses the skip_turn card to force the opponent to skip their turn(s).
    def skip_turn(self):
       # Skip the current player's turn.
       self.log_action(f"Skip turn {(self.current_player_index + 1) % len(self.players)}.")
       self.current_player_index = (self.current_player_index + 1) % len(self.players)

    # Player uses the double_trouble card to force the opponent to draw 2 cards.
    def double_trouble(self, draw_count):
        next_player = self.players[(self.current_player_index + 1) % len(self.players)]
        while draw_count:
            draw_count -= 1
            self.draw_card(next_player)

    # The winner of the game is when the player empties their hand
    def check_for_winner(self):
       # Check if a player has won.
        for player in self.players:
            if not player.hand:
                self.log_action(f"{player.name} has won!")
                print(f"{player.name} has won!")
                return True
        return False

    def next_turn(self):
       # Move to the next player.
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.log_action(f"Next turn: {self.current_player_index}")

    def log_action(self, action):
        self.log.append(action)

    def show_log(self):
        print("\nGame Log:")
        for entry in self.log:
            print(entry)


# Player Class that represents a player
# Player card attributes include the hand to store the cards dealt at the beginning.
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    # Player implements a turn mechanism to play one card and allow the opponent to take their turn.
    # The opponent turn can be skipped by special cards.
    def take_turn(self, game):
       # Allow the player to take their turn.
        print(f"{self.name}'s turn!")
        self.show_hand()
        # Automatically play the first card in the hand for simplicity
        if self.hand:
            card_index = 0
            print(f"{self.name} played {self.hand[card_index]}")
            game.play_card(self, card_index)
            if game.check_for_winner():  # Check for winner after the turn is played
                return True
        else:
            print(f"{self.name} has no cards to play and skips their turn.")
            game.next_turn()
        return False

    def show_hand(self):
       # Display the player's hand.
        for i, card in enumerate(self.hand):
            print(f"{i}. {card}")


# Main game loop
def start_game():
    # Create player1 and player2 objects.
    player1 = Player(str(input("Please enter player 1 name: ")))
    player2 = Player(str(input("Please enter player 2 name: ")))

    # Create the game object with the players
    game = Game([player1, player2])

    # Deal initial cards
    for _ in range(7):
        for player in game.players:
            game.draw_card(player)

    # Start the game
    while True:
        current_player = game.players[game.current_player_index]
        if current_player.take_turn(game):  # Check if the player won after their turn
            break

    # Ask if they want to play again
    play_again = input("Do you want to play again? (y/n): ").strip().lower()

    # Check for various cases of input (y, Y, yes, YES, n, N, no, NO)
    if play_again in ['y', 'yes']:
        start_game()  # Restart the game
    elif play_again in ['n', 'no']:
        print("Goodbye! Exiting the game.")  # Exit the game
    else:
        print("Invalid input. Exiting the game.")  # Exit if input is not recognized


    game.show_log()


# Run the game
start_game()
# Result 1 (Valid input with option to exit the game after one game):
# C:\AdvancedPython\ADVANCEDPYTHON-2025\.venv\Scripts\python.exe C:\AdvancedPython\ADVANCEDPYTHON-2025\SimpleUNOCardGame.py
# Please enter player 1 name: Thor
# Please enter player 2 name: Iron Man
# Red 0 ->Red 1 ->Red 2 ->Red 3 ->Red 4 ->Red 5 ->Red 6 ->Red 7 ->Red 8 ->Red 9 ->Red Skip ->Red Skip ->Blue 0 ->Blue 1 ->Blue 2 ->Blue 3 ->Blue 4 ->Blue 5 ->Blue 6 ->Blue 7 ->Blue 8 ->Blue 9 ->Blue Skip ->Blue Skip ->Green 0 ->Green 1 ->Green 2 ->Green 3 ->Green 4 ->Green 5 ->Green 6 ->Green 7 ->Green 8 ->Green 9 ->Green Skip ->Green Skip ->Yellow 0 ->Yellow 1 ->Yellow 2 ->Yellow 3 ->Yellow 4 ->Yellow 5 ->Yellow 6 ->Yellow 7 ->Yellow 8 ->Yellow 9 ->Yellow Skip ->Yellow Skip ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->Null
# After shuffle:
# Blue 2 ->Red 6 ->Yellow 6 ->Red 2 ->None Color Change ->None Color Change ->Blue 9 ->None Color Change ->Red 8 ->Blue Skip ->Blue 4 ->Red 4 ->None Double Trouble ->Green 6 ->Blue 1 ->Yellow 9 ->Yellow 1 ->Blue 7 ->Green 0 ->None Double Trouble ->Red 0 ->Red 7 ->Green Skip ->Yellow 3 ->Green 9 ->None Double Trouble ->Green 4 ->Green 5 ->Red Skip ->Yellow 8 ->Blue 3 ->Green 3 ->Green 2 ->Blue 5 ->Green 8 ->Red 1 ->Red 3 ->Blue Skip ->Red 9 ->Green Skip ->Red Skip ->Yellow Skip ->None Double Trouble ->Blue 0 ->Green 1 ->Red 5 ->Yellow 4 ->Blue 6 ->Yellow 0 ->Yellow Skip ->Blue 8 ->Yellow 5 ->Yellow 2 ->Green 7 ->Yellow 7 ->None Color Change ->Null
# Thor drew Blue 2
# Iron Man drew Red 6
# Thor drew Yellow 6
# Iron Man drew Red 2
# Thor drew None Color Change
# Iron Man drew None Color Change
# Thor drew Blue 9
# Iron Man drew None Color Change
# Thor drew Red 8
# Iron Man drew Blue Skip
# Thor drew Blue 4
# Iron Man drew Red 4
# Thor drew None Double Trouble
# Iron Man drew Green 6
# Iron Man's turn!
# 0. Red 6
# 1. Red 2
# 2. None Color Change
# 3. None Color Change
# 4. Blue Skip
# 5. Red 4
# 6. Green 6
# Iron Man played Red 6
# Iron Man's turn!
# 0. Red 2
# 1. None Color Change
# 2. None Color Change
# 3. Blue Skip
# 4. Red 4
# 5. Green 6
# Iron Man played Red 2
# Iron Man's turn!
# 0. None Color Change
# 1. None Color Change
# 2. Blue Skip
# 3. Red 4
# 4. Green 6
# Iron Man played None Color Change
# Iron Man's turn!
# 0. None Color Change
# 1. Blue Skip
# 2. Red 4
# 3. Green 6
# Iron Man played None Color Change
# Iron Man's turn!
# 0. Blue Skip
# 1. Red 4
# 2. Green 6
# Iron Man played Blue Skip
# Iron Man's turn!
# 0. Red 4
# 1. Green 6
# Iron Man played Red 4
# Iron Man's turn!
# 0. Green 6
# Iron Man played Green 6
# Iron Man has won!
# Do you want to play again? (y/n): NO
# Goodbye! Exiting the game.
#
# Game Log:
# Thor drew Blue 2
# Iron Man drew Red 6
# Thor drew Yellow 6
# Iron Man drew Red 2
# Thor drew None Color Change
# Iron Man drew None Color Change
# Thor drew Blue 9
# Iron Man drew None Color Change
# Thor drew Red 8
# Iron Man drew Blue Skip
# Thor drew Blue 4
# Iron Man drew Red 4
# Thor drew None Double Trouble
# Iron Man drew Green 6
# Iron Man has won!
#
# Process finished with exit code 0
# Result 2 (Playing the game multiple times and exiting with the valid input):
# C:\AdvancedPython\ADVANCEDPYTHON-2025\.venv\Scripts\python.exe C:\AdvancedPython\ADVANCEDPYTHON-2025\SimpleUNOCardGame.py
# Please enter player 1 name: 100
# Please enter player 2 name: 200
# Red 0 ->Red 1 ->Red 2 ->Red 3 ->Red 4 ->Red 5 ->Red 6 ->Red 7 ->Red 8 ->Red 9 ->Red Skip ->Red Skip ->Blue 0 ->Blue 1 ->Blue 2 ->Blue 3 ->Blue 4 ->Blue 5 ->Blue 6 ->Blue 7 ->Blue 8 ->Blue 9 ->Blue Skip ->Blue Skip ->Green 0 ->Green 1 ->Green 2 ->Green 3 ->Green 4 ->Green 5 ->Green 6 ->Green 7 ->Green 8 ->Green 9 ->Green Skip ->Green Skip ->Yellow 0 ->Yellow 1 ->Yellow 2 ->Yellow 3 ->Yellow 4 ->Yellow 5 ->Yellow 6 ->Yellow 7 ->Yellow 8 ->Yellow 9 ->Yellow Skip ->Yellow Skip ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->Null
# After shuffle:
# Green 6 ->None Color Change ->Red 2 ->Red 9 ->Yellow 6 ->Green 4 ->Blue Skip ->Yellow 8 ->None Double Trouble ->Red 6 ->Yellow 7 ->Blue 9 ->Green 1 ->Red 1 ->Green 2 ->None Double Trouble ->Red 4 ->Green 0 ->Red Skip ->Green Skip ->Green 7 ->Red 5 ->Yellow 2 ->Yellow 1 ->Green 5 ->Blue 1 ->Yellow 5 ->None Double Trouble ->Blue 4 ->Blue 2 ->Green 3 ->Yellow 3 ->Green Skip ->Yellow Skip ->None Color Change ->Yellow 4 ->Blue 3 ->Red 0 ->Blue 6 ->Blue 7 ->Red 3 ->Red 7 ->Red 8 ->Red Skip ->None Color Change ->Yellow 0 ->Blue 0 ->None Double Trouble ->Yellow 9 ->Blue 5 ->Yellow Skip ->Blue 8 ->Blue Skip ->Green 9 ->None Color Change ->Green 8 ->Null
# 100 drew Green 6
# 200 drew None Color Change
# 100 drew Red 2
# 200 drew Red 9
# 100 drew Yellow 6
# 200 drew Green 4
# 100 drew Blue Skip
# 200 drew Yellow 8
# 100 drew None Double Trouble
# 200 drew Red 6
# 100 drew Yellow 7
# 200 drew Blue 9
# 100 drew Green 1
# 200 drew Red 1
# 200's turn!
# 0. None Color Change
# 1. Red 9
# 2. Green 4
# 3. Yellow 8
# 4. Red 6
# 5. Blue 9
# 6. Red 1
# 200 played None Color Change
# 200's turn!
# 0. Red 9
# 1. Green 4
# 2. Yellow 8
# 3. Red 6
# 4. Blue 9
# 5. Red 1
# 200 played Red 9
# 200's turn!
# 0. Green 4
# 1. Yellow 8
# 2. Red 6
# 3. Blue 9
# 4. Red 1
# 200 played Green 4
# 200's turn!
# 0. Yellow 8
# 1. Red 6
# 2. Blue 9
# 3. Red 1
# 200 played Yellow 8
# 200's turn!
# 0. Red 6
# 1. Blue 9
# 2. Red 1
# 200 played Red 6
# 200's turn!
# 0. Blue 9
# 1. Red 1
# 200 played Blue 9
# 200's turn!
# 0. Red 1
# 200 played Red 1
# 200 has won!
# Do you want to play again? (y/n): YES
# Please enter player 1 name: ABC
# Please enter player 2 name: 123
# Red 0 ->Red 1 ->Red 2 ->Red 3 ->Red 4 ->Red 5 ->Red 6 ->Red 7 ->Red 8 ->Red 9 ->Red Skip ->Red Skip ->Blue 0 ->Blue 1 ->Blue 2 ->Blue 3 ->Blue 4 ->Blue 5 ->Blue 6 ->Blue 7 ->Blue 8 ->Blue 9 ->Blue Skip ->Blue Skip ->Green 0 ->Green 1 ->Green 2 ->Green 3 ->Green 4 ->Green 5 ->Green 6 ->Green 7 ->Green 8 ->Green 9 ->Green Skip ->Green Skip ->Yellow 0 ->Yellow 1 ->Yellow 2 ->Yellow 3 ->Yellow 4 ->Yellow 5 ->Yellow 6 ->Yellow 7 ->Yellow 8 ->Yellow 9 ->Yellow Skip ->Yellow Skip ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->Null
# After shuffle:
# Green 9 ->Red 0 ->Red Skip ->Yellow 9 ->Blue 1 ->Green 3 ->Green Skip ->Blue Skip ->Blue 0 ->None Double Trouble ->Green 0 ->None Color Change ->Yellow 4 ->Red 6 ->Blue 5 ->Green 5 ->Red 4 ->Green Skip ->Yellow Skip ->Green 7 ->None Color Change ->Blue 2 ->Green 4 ->None Color Change ->Green 2 ->Blue 3 ->Red 9 ->None Double Trouble ->Blue Skip ->Yellow 0 ->Green 6 ->Yellow 5 ->Yellow 3 ->Red 3 ->Green 1 ->None Double Trouble ->Blue 9 ->Yellow 1 ->Red 1 ->Blue 7 ->Blue 4 ->None Color Change ->Blue 8 ->Blue 6 ->Red 7 ->Yellow 2 ->Yellow 8 ->Red 5 ->None Double Trouble ->Yellow Skip ->Green 8 ->Red Skip ->Yellow 7 ->Yellow 6 ->Red 8 ->Red 2 ->Null
# ABC drew Green 9
# 123 drew Red 0
# ABC drew Red Skip
# 123 drew Yellow 9
# ABC drew Blue 1
# 123 drew Green 3
# ABC drew Green Skip
# 123 drew Blue Skip
# ABC drew Blue 0
# 123 drew None Double Trouble
# ABC drew Green 0
# 123 drew None Color Change
# ABC drew Yellow 4
# 123 drew Red 6
# ABC's turn!
# 0. Green 9
# 1. Red Skip
# 2. Blue 1
# 3. Green Skip
# 4. Blue 0
# 5. Green 0
# 6. Yellow 4
# ABC played Green 9
# ABC's turn!
# 0. Red Skip
# 1. Blue 1
# 2. Green Skip
# 3. Blue 0
# 4. Green 0
# 5. Yellow 4
# ABC played Red Skip
# ABC's turn!
# 0. Blue 1
# 1. Green Skip
# 2. Blue 0
# 3. Green 0
# 4. Yellow 4
# ABC played Blue 1
# ABC's turn!
# 0. Green Skip
# 1. Blue 0
# 2. Green 0
# 3. Yellow 4
# ABC played Green Skip
# ABC's turn!
# 0. Blue 0
# 1. Green 0
# 2. Yellow 4
# ABC played Blue 0
# ABC's turn!
# 0. Green 0
# 1. Yellow 4
# ABC played Green 0
# ABC's turn!
# 0. Yellow 4
# ABC played Yellow 4
# ABC has won!
# Do you want to play again? (y/n): NO
# Goodbye! Exiting the game.
#
# Game Log:
# ABC drew Green 9
# 123 drew Red 0
# ABC drew Red Skip
# 123 drew Yellow 9
# ABC drew Blue 1
# 123 drew Green 3
# ABC drew Green Skip
# 123 drew Blue Skip
# ABC drew Blue 0
# 123 drew None Double Trouble
# ABC drew Green 0
# 123 drew None Color Change
# ABC drew Yellow 4
# 123 drew Red 6
# ABC has won!
#
# Game Log:
# 100 drew Green 6
# 200 drew None Color Change
# 100 drew Red 2
# 200 drew Red 9
# 100 drew Yellow 6
# 200 drew Green 4
# 100 drew Blue Skip
# 200 drew Yellow 8
# 100 drew None Double Trouble
# 200 drew Red 6
# 100 drew Yellow 7
# 200 drew Blue 9
# 100 drew Green 1
# 200 drew Red 1
# 200 has won!
#
# Process finished with exit code 0
# Result 3 (With blanks):
# C:\AdvancedPython\ADVANCEDPYTHON-2025\.venv\Scripts\python.exe C:\AdvancedPython\ADVANCEDPYTHON-2025\SimpleUNOCardGame.py
# Please enter player 1 name:
# Please enter player 2 name:
# Red 0 ->Red 1 ->Red 2 ->Red 3 ->Red 4 ->Red 5 ->Red 6 ->Red 7 ->Red 8 ->Red 9 ->Red Skip ->Red Skip ->Blue 0 ->Blue 1 ->Blue 2 ->Blue 3 ->Blue 4 ->Blue 5 ->Blue 6 ->Blue 7 ->Blue 8 ->Blue 9 ->Blue Skip ->Blue Skip ->Green 0 ->Green 1 ->Green 2 ->Green 3 ->Green 4 ->Green 5 ->Green 6 ->Green 7 ->Green 8 ->Green 9 ->Green Skip ->Green Skip ->Yellow 0 ->Yellow 1 ->Yellow 2 ->Yellow 3 ->Yellow 4 ->Yellow 5 ->Yellow 6 ->Yellow 7 ->Yellow 8 ->Yellow 9 ->Yellow Skip ->Yellow Skip ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->Null
# After shuffle:
# Red 8 ->Blue 7 ->Yellow 8 ->None Color Change ->Blue 8 ->Green 9 ->Green 6 ->Red 3 ->None Double Trouble ->Blue 5 ->Green 5 ->Red 9 ->None Color Change ->Blue 6 ->Green 2 ->None Color Change ->Blue 9 ->Red 4 ->Yellow 1 ->Yellow Skip ->None Double Trouble ->Blue 1 ->Red Skip ->Green 8 ->Green 0 ->Yellow 4 ->Blue 2 ->Blue 0 ->Yellow 0 ->Yellow 5 ->None Double Trouble ->Green 4 ->Blue 4 ->Red 0 ->Green 1 ->Yellow 7 ->Yellow 6 ->Green Skip ->Yellow 3 ->Blue 3 ->Yellow Skip ->None Color Change ->Yellow 9 ->Green 3 ->Blue Skip ->Red Skip ->Yellow 2 ->None Double Trouble ->Red 2 ->Blue Skip ->Red 6 ->Red 5 ->Red 7 ->Green 7 ->Green Skip ->Red 1 ->Null
#  drew Red 8
#  drew Blue 7
#  drew Yellow 8
#  drew None Color Change
#  drew Blue 8
#  drew Green 9
#  drew Green 6
#  drew Red 3
#  drew None Double Trouble
#  drew Blue 5
#  drew Green 5
#  drew Red 9
#  drew None Color Change
#  drew Blue 6
# 's turn!
# 0. Red 8
# 1. Yellow 8
# 2. Blue 8
# 3. Green 6
# 4. None Double Trouble
# 5. Green 5
# 6. None Color Change
#  played Red 8
# 's turn!
# 0. Yellow 8
# 1. Blue 8
# 2. Green 6
# 3. None Double Trouble
# 4. Green 5
# 5. None Color Change
#  played Yellow 8
# 's turn!
# 0. Blue 8
# 1. Green 6
# 2. None Double Trouble
# 3. Green 5
# 4. None Color Change
#  played Blue 8
# 's turn!
# 0. Green 6
# 1. None Double Trouble
# 2. Green 5
# 3. None Color Change
#  played Green 6
# 's turn!
# 0. None Double Trouble
# 1. Green 5
# 2. None Color Change
#  played None Double Trouble
# 's turn!
# 0. Green 5
# 1. None Color Change
#  played Green 5
# 's turn!
# 0. None Color Change
#  played None Color Change
#  has won!
# Do you want to play again? (y/n): NO
# Goodbye! Exiting the game.
#
# Game Log:
#  drew Red 8
#  drew Blue 7
#  drew Yellow 8
#  drew None Color Change
#  drew Blue 8
#  drew Green 9
#  drew Green 6
#  drew Red 3
#  drew None Double Trouble
#  drew Blue 5
#  drew Green 5
#  drew Red 9
#  drew None Color Change
#  drew Blue 6
#  has won!
#
# Process finished with exit code 0
# Result 4 (With invalid input):
# C:\AdvancedPython\ADVANCEDPYTHON-2025\.venv\Scripts\python.exe C:\AdvancedPython\ADVANCEDPYTHON-2025\SimpleUNOCardGame.py
# Please enter player 1 name: VIAC
# Please enter player 2 name: UN
# Red 0 ->Red 1 ->Red 2 ->Red 3 ->Red 4 ->Red 5 ->Red 6 ->Red 7 ->Red 8 ->Red 9 ->Red Skip ->Red Skip ->Blue 0 ->Blue 1 ->Blue 2 ->Blue 3 ->Blue 4 ->Blue 5 ->Blue 6 ->Blue 7 ->Blue 8 ->Blue 9 ->Blue Skip ->Blue Skip ->Green 0 ->Green 1 ->Green 2 ->Green 3 ->Green 4 ->Green 5 ->Green 6 ->Green 7 ->Green 8 ->Green 9 ->Green Skip ->Green Skip ->Yellow 0 ->Yellow 1 ->Yellow 2 ->Yellow 3 ->Yellow 4 ->Yellow 5 ->Yellow 6 ->Yellow 7 ->Yellow 8 ->Yellow 9 ->Yellow Skip ->Yellow Skip ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->None Color Change ->None Double Trouble ->Null
# After shuffle:
# Red 3 ->None Double Trouble ->Blue Skip ->Yellow 2 ->Yellow 7 ->None Double Trouble ->Green 8 ->Blue 1 ->Blue Skip ->Yellow 0 ->Red 2 ->None Double Trouble ->Green 0 ->Green 6 ->Green 3 ->Green 7 ->Red 5 ->Yellow 4 ->Red 6 ->None Color Change ->Blue 4 ->Green Skip ->Blue 5 ->Red Skip ->Yellow 3 ->Green 2 ->None Color Change ->Yellow 1 ->Yellow 5 ->Green 5 ->Blue 9 ->Yellow 9 ->Yellow 6 ->Blue 2 ->None Double Trouble ->None Color Change ->Red 0 ->Yellow 8 ->None Color Change ->Blue 8 ->Yellow Skip ->Blue 6 ->Blue 0 ->Red Skip ->Red 4 ->Green 9 ->Blue 7 ->Red 7 ->Red 9 ->Green 1 ->Blue 3 ->Red 8 ->Red 1 ->Green Skip ->Yellow Skip ->Green 4 ->Null
# VIAC drew Red 3
# UN drew None Double Trouble
# VIAC drew Blue Skip
# UN drew Yellow 2
# VIAC drew Yellow 7
# UN drew None Double Trouble
# VIAC drew Green 8
# UN drew Blue 1
# VIAC drew Blue Skip
# UN drew Yellow 0
# VIAC drew Red 2
# UN drew None Double Trouble
# VIAC drew Green 0
# UN drew Green 6
# UN's turn!
# 0. None Double Trouble
# 1. Yellow 2
# 2. None Double Trouble
# 3. Blue 1
# 4. Yellow 0
# 5. None Double Trouble
# 6. Green 6
# UN played None Double Trouble
# UN's turn!
# 0. Yellow 2
# 1. None Double Trouble
# 2. Blue 1
# 3. Yellow 0
# 4. None Double Trouble
# 5. Green 6
# UN played Yellow 2
# UN's turn!
# 0. None Double Trouble
# 1. Blue 1
# 2. Yellow 0
# 3. None Double Trouble
# 4. Green 6
# UN played None Double Trouble
# UN's turn!
# 0. Blue 1
# 1. Yellow 0
# 2. None Double Trouble
# 3. Green 6
# UN played Blue 1
# UN's turn!
# 0. Yellow 0
# 1. None Double Trouble
# 2. Green 6
# UN played Yellow 0
# UN's turn!
# 0. None Double Trouble
# 1. Green 6
# UN played None Double Trouble
# UN's turn!
# 0. Green 6
# UN played Green 6
# UN has won!
# Do you want to play again? (y/n): AAA
# Invalid input. Exiting the game.
#
# Game Log:
# VIAC drew Red 3
# UN drew None Double Trouble
# VIAC drew Blue Skip
# UN drew Yellow 2
# VIAC drew Yellow 7
# UN drew None Double Trouble
# VIAC drew Green 8
# UN drew Blue 1
# VIAC drew Blue Skip
# UN drew Yellow 0
# VIAC drew Red 2
# UN drew None Double Trouble
# VIAC drew Green 0
# UN drew Green 6
# UN has won!
#
# Process finished with exit code 0