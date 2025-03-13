# Name: Ganesh Kumar
# Date: 03/12/2025
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

   # Prepend method appends a card to the beginning of the linked list.
   # Time complexity of append is O(1) - Constant Time Complexity.
   def prepend(self, card):
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
       else:
           # Attach the new node at the end.
           newNode.next = self.head
           self.head = newNode
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
           # Get the first data from the head.
           self.head = self.head.next
           # Decrement the size by 1.
           self.size -= 1
           # Return the card from the head of the list.
           return card


   # Shuffle method shuffles the deck of cards by converting it into a list and then shuffling.
   def shuffle(self):
       # Collect the cards in the linked list into a list to shuffle the cards.
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
       # Put them back in the list.
       for card in cards:
           self.prepend(card)


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


   def play(self, player, game):
       # Abstract method: Number cards are simply played without additional effects.
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
       # Abstract method: Number cards are simply played without additional effects.
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
           game.skip_turn() # Skip the turn of the opponent.


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
       game.change_color(new_color) # Change the color used by the game to a new color.

# DoubleTroubleCard is a special card and the player forces the opponent to draw two cards
# from the shuffled deck.
class DoubleTroubleCard(Card):
   def __init__(self, name, card_type):
       super().__init__(name, None, card_type)
       self.double_draw = 0

   # Play method to force the user to draw two cards from the deck.
   def play(self, player, game):
       print(f"{player.name} played a Double Trouble Card!")
       # Randomly choose the number of cards to draw for the opponent.
       self.double_draw = random.randint(2,4)
       # Force the opponent to draw 2 to 4 cards.
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
       # Deck is a linked list of cards.
       self.deck = LinkedList()
       # Discard pile collects all the cards that are drawn during the game.
       self.played_cards = []


       # Initialize deck with regular and special cards
       self.initialize_deck()
       # Shuffles deck of cards.
       self.shuffle_deck()
       # Game logging list
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
               self.deck.prepend(NumberedCard(color, number))
           # Add special cards (Skip, Reverse, Draw Two)
           for _ in range(2):  # Two of each special card
               self.deck.prepend(SkipCard("Skip", color, "Skip"))




       # Add 4 color change cards and double trouble cards to the deck.
       for _ in range(4):
           self.deck.prepend(ColorChangeCard("Color Change", "Color Change"))
           self.deck.prepend(DoubleTroubleCard("Double Trouble", "Double Trouble"))


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
           if len(self.played_cards):
               if card.color == self.current_color or card.name == self.played_cards[-1]:
                   self.played_cards.append(card)
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
           card_index = random.randint(0, (len(self.hand) - 1))
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
