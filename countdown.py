import random

# -------------------------------------------
# Global ------------------------------------
# -------------------------------------------

BOARD_SIZE = 9
MAX_PLAYERS = 4
BOARD_LETTERS = [''] * BOARD_SIZE

# Credits to https://github.com/dwyl/english-words
WORDS_FILE = "data/words_alpha.txt"

ENGLISH_WORDS = []  # call load_data() to update

PLAYERS = []  # call init_players() to update

# -------------------------------------------
# Letters -----------------------------------
# -------------------------------------------

VOWELS = set(list("AIEOU"))
CONSONANTS = set(list("QWRTYPSDFGHJKLZXCVBNM"))

# -------------------------------------------
# Functions ---------------------------------
# -------------------------------------------

def display_player_stats():
  """Display Player stats to the terminal
  """
  print()
  print("Current state of the game is...")
  for player in PLAYERS:
    id = player["id"]
    name = player["name"]
    score = player["score"]
    lead = "*Leading*" if player["leading"] else ""
    print(f"Player {id}. {name}, Score: {score}, {lead}")
  print()

# -------------------------------------------

def guessing_round():
  """Guessing Round, where each player gets to input their
  guesses.
  """
  scores = [0] * len(PLAYERS)
  for i in range(len(PLAYERS)):
    name = PLAYERS[i]["name"]
    word = input(f"{name}'s guess: ")  # get the guess
    score = len(word) if word_is_valid(word) else 0
    if score == BOARD_SIZE:
      score *= 2
    scores[i] = score
  highest_score = max(scores)
  scores = [e if e == highest_score else 0 for e in scores]
  
  # Update scores and determine leader
  player_scores = [0] * len(PLAYERS)
  for i in range(len(PLAYERS)):
    PLAYERS[i]["score"] += scores[i]
    player_scores[i] = PLAYERS[i]["score"]
  for i in range(len(PLAYERS)):
    if player_scores[i] == max(player_scores):
      PLAYERS[i]["leading"] = True
    else:
      PLAYERS[i]["leading"] = False

# -------------------------------------------

def word_is_valid(word):
  """Check if a given word is valid or not.
  A valid word is one that uses only letters on the board
  once (no repeats). If that's valid, return
  True if the word is english.

  Args:
      word (str): Word
      
  Returns:
      boolean: True if word uses board letters properly
  """
  used = [False] * BOARD_SIZE
  word = word.upper()
  for letter in word:
    if letter not in BOARD_LETTERS:
      return False  # immediately fails
    valid = False
    for i in range(BOARD_SIZE):
      # print(f"i:{i} checking letter {letter} against board letter {BOARD_LETTERS[i]} used:{used[i]}")
      if BOARD_LETTERS[i] == letter and not used[i]:
        used[i] = True
        valid = True
        break
    if not valid:
      return False
  return (word.lower() in ENGLISH_WORDS)

# -------------------------------------------

def get_board():
  """Return the current state of the board.

  Returns:
      List: The board
  """
  return BOARD_LETTERS

# -------------------------------------------

def add_letter_to_board(choice_vowel=True):
  """Add a random letter to the board
  """
  i = 0
  while BOARD_LETTERS[i] != '':
    i += 1
    if i >= BOARD_SIZE:
      print('Board is full.')
      return
  letter = rand_element(VOWELS if choice_vowel else CONSONANTS)
  BOARD_LETTERS[i] = letter

# -------------------------------------------

def add_letters_to_board():
  """Choose random letters to put up on the board
  """
  if BOARD_LETTERS != [''] * BOARD_SIZE:
    # reset board
    for i in range(BOARD_SIZE):
      BOARD_LETTERS[i] = ''
  print(f"Choose {BOARD_SIZE} letters to put up on the board.")
  for i in range(BOARD_SIZE):
    choice = True if input(f"{i+1}. Vowel (v) or Consonant (c)? ") == 'v' else False
    add_letter_to_board(choice)
    # print(get_board())
    

# -------------------------------------------

def rand_element(set, replacement=True, n=1):
  """Obtain a random element from a set.
  To sample without replacement, set replacement to False
  """
  e = random.sample(set, n)[0]
  if not replacement:
    set.remove(e)
  return e

# -------------------------------------------

def get_players():
  """Get player names from user input (terminal)

  Returns:
      List: Names of players
  """
  n = int(input(f"How many players are playing (1-{MAX_PLAYERS})? "))
  while n < 0 or n > MAX_PLAYERS:
    print("Invalid number of players.")
    n = int(input(f"How many players are playing (1-{MAX_PLAYERS})? "))
  names = []
  print("Give names for these players:")
  for i in range(n):
    name = input(f"Player {i+1}'s name: ")
    if len(name) <= 1:
      name = f"Player_{i+1}"
    names.append(name)
  return names

# -------------------------------------------

def init_players(n, names=[]):
  """Initialise PLAYERS with player data,
  function will fail if the number of players
  exceed MAX_PLAYERS

  Args:
      n (int): Number of players
      
  Returns:
      boolean: True if success, False otherwise
  """
  print(names, "in init")
  if n < 0 or n > MAX_PLAYERS:
    print("Invalid number of players.")
    return False
  default_names=[f"Player_{i+1}" for i in range(n)]
  if len(names) != n:
    names = default_names
  for i in range(n):
    PLAYERS.append({
      "name": names[i],
      "id": i,
      "score": 0,
      "leading": True,
    })
  return True

# -------------------------------------------

def load_data(filename):
  """Read a file containing English words,
  without extra whitespace.

  Args:
      filename (str): path to words file

  Returns:
      list: List of words
  """
  file = open(filename)
  data = [x.strip() for x in file.readlines()]
  file.close()
  return data

# -------------------------------------------

# -------------------------------------------
# Main --------------------------------------
# -------------------------------------------

def init_game():
  """Initialise the game state
  """
  global ENGLISH_WORDS
  ENGLISH_WORDS = load_data(WORDS_FILE)
  print(len(ENGLISH_WORDS), "words loaded from", WORDS_FILE)
  names = get_players()
  if init_players(len(names), names):
    pass
  print(PLAYERS)
  
  for _ in range(3):
    add_letters_to_board()
    # temp = ['U', 'O', 'A', 'O', 'K', 'G', 'N', 'C', 'Z']
    # for i in range(9):
    #   BOARD_LETTERS[i] = temp[i]
    print("Final board is", get_board())
    print()
    guessing_round()
    display_player_stats()

if __name__ == "__main__":
  init_game()  
