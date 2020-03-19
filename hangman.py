import sys
from time import sleep, time
from random import choice
from threading import Thread

sa = sys.argv
lsa = len(sa)
if lsa != 2:
    print('Usage: [python] hangman.py mode')
    print('Modes are: easy, medium, hard')
    print('Example: [python] hangman.py easy')
    print('Terminate with Ctrl-C.')
    sys.exit(1)

# get the mode string
try:
    mode = str(sa[1])
except ValueError:
    print('Mode should be a string')
    sys.exit(1)

# mode duration from easy to hard in minutes
mode_duration = [1, 1.5, 2]


# function definitions
def read_file():
    with open('countries') as f:
        words = f.read()
        # converts string to list
        words = words.lower().split('\n')

    return words


def get_time_and_word(mode, mode_duration):
    _minutes = ''
    _ran_word = ''
    if mode == 'easy':
        _minutes = mode_duration[0]
        words = list(filter(lambda x: len(x) <= 5, read_file()))
        _ran_word = choice(words)
    elif mode == 'medium':
        _minutes = mode_duration[1]
        words = list(filter(lambda x: 5 < len(x) <= 7, read_file()))
        _ran_word = choice(words)
    else:
        _minutes = mode_duration[2]
        words = list(filter(lambda x: len(x) >= 8, read_file()))
        _ran_word = choice(words)

    out_put = [_minutes, _ran_word]

    return out_put


def check(word, guesses, guess):
    # guess = guess.upper()
    state = ''
    matches = 0
    for letter in word:
        if letter in guesses:
            state += letter
        else:
            state += ' _ '

        if letter == guess:
            matches += 1

    if matches > 1:
        print('Yes, the word contains ', matches, '"' + guess + '"' + 's')
    elif matches == 1:
        print('Yes, the word contains the letter "' + guess + '"')
    return state


minutes = get_time_and_word(mode, mode_duration)[0]
# convert minutes to seconds
seconds = minutes * 60
run_time = time() + seconds


def time_unit():
    if minutes > 1:
        unit = 'minutes'
    else:
        unit = 'minute'

    return unit


# Main program starts
def main():
    word = get_time_and_word(mode, mode_duration)[1]
    print('FIRST random word is: ', word)
    guesses = []
    # global makes it the variable global everywhere in the script
    global number_guessed
    number_guessed = 0
    print('PLAY TIME is', minutes, time_unit())
    print('The country contains', len(word), 'letters.')

    while True:
        guess = input('Please enter one letter or whole word: ')
        if guess in guesses:
            print('You already guessed "' + guess + '" !' + 'try another letter')
        elif len(guess) == len(word):
            guesses.append(guess)
            if guess == word:
                number_guessed += 1
                # re-assign word variable to new word
                word = get_time_and_word(mode, mode_duration)[1]
                print('NEW random word is: ', word)
                print('The country contains', len(word), 'letters.')
                continue
            else:
                print('Sorry, that is incorrect.')
        elif len(guess) == 1:
            guesses.append(guess)
            result = check(word, guesses, guess)
            if result == word:
                number_guessed += 1
                # re-assign word variable to new word
                word = get_time_and_word(mode, mode_duration)[1]
                print('NEW random word is: ', word)
                print('The country contains', len(word), 'letters.')
                continue
            else:
                print(result)
        else:
            print('Bad input. empty or word with < or > given length')

        # calculate time left in seconds and print
        time_left = run_time - time()
        # Prints overall runtime in format hh:mm:ss
        print("\n--- Time left is: ", str(int((time_left / 3600))) + ":" +
              str(int(((time_left % 3600) / 60))) + ":" +
              str(int(((time_left % 3600) % 60))) + " ---")


# program runs on this thread
t = Thread(target=main)
t.daemon = True
t.start()

try:
    sleep(seconds)
except KeyboardInterrupt:
    print("\nuser stopped program")
finally:
    print('\n' + '*' * 15)
    print('Your {} {} is up!'.format(minutes, time_unit()))
    print('\nCorrectly guessed {} countries. \n'.format(number_guessed))
    print('*' * 15)
