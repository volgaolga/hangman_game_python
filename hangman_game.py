import os
import random
import requests
import string
import time
from bs4 import BeautifulSoup


SLEEP = 3    # time sleep
LEVEL_WORD_LENGTH = {'1': 4, '2': 6, '3': 8}    # length of words for level
ATTEMPT_NUM = 6    # max number of attempts


def get_format_text(text):
    """makes text colored and bold"""
    return text.format(
        red='\033[91m',
        green='\033[92m',
        yellow='\033[93m',
        bold='\033[1m',
        no='\033[0m'
    )


def get_clear_screen():
    """makes screen clear (without previous output)"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_start():
    """show rules of the game"""
    rules = '''
{bold}HANGMAN GAME
____
|  |
|  O
| /|\\
| / \\
|
H _ N G M _ N{no}

Welcome to Hangman!
The computer thinks the word, you try to guess what it is letter by letter.
You can see the gallows and some dashes below. The number of dashes equivalent
to the number of letters in the word. If you suggest a letter that occurs in 
the word, the computer fills in the blanks with that letter in the right 
places. If the word does not contain the suggested letter, the computer draws 
one element of a hangman's gallows. As the game progresses, a segment of 
a victim is added for every suggested letter not in the word. The number 
of incorrect guesses before the game ends is 6, you will see the hanged man and
the inscription, {red}{bold}GAME OVER!{no}
If you win, you will receive several rating stars {yellow}{bold}*****{no} and 
possibly {green}{bold}CHAMPION{no} title. 
If you guess all the letters without mistakes, you will get 5 stars and 
champion title.
If you make a mistake once, you will get just 5 stars, if twice - 4 stars,
three times - 3 stars, four times - 2 stars, five times - 1 star, 
six times... {red}{bold}your man will get hang{no}!
You can choose one out of three levels:
{green}{bold}level 1{no} - four letter word,
{yellow}{bold}level 2{no} - six letter word,
{red}{bold}level 3{no} - eight letter word.

{red}{bold}GUESS THE WORD BEFORE YOUR MAN GETS HUNG!{no}
    '''

    print(get_format_text(rules), '\n')
    time.sleep(SLEEP)
    time.sleep(SLEEP)


def get_agreement():
    """asks to continue or quit"""
    agreement = '''
{bold}Are you ready to start the game?
Enter YES or NO:{no} 
    '''

    while True:
        answer = input(get_format_text(agreement)).lower()

        if answer == 'yes':
            print(get_format_text(
                '''{bold}{green}Great! Let's get started!{no}'''))
            time.sleep(SLEEP)
            get_clear_screen()
            return True

        elif answer == 'no':
            get_clear_screen()
            print(get_format_text(
                '{bold}{yellow}See you next time, yellow-belly!{no}'))
            return False

        else:
            print(get_format_text(
                '{bold}{red}Something is wrong! Use only yes or no words.{no}')
            )
            time.sleep(SLEEP)
            get_clear_screen()


def set_level():
    """choose the level"""
    level_description = '''
Choose one out of three levels:
{green}{bold}level 1{no} - four letter word,
{yellow}{bold}level 2{no} - six letter word,
{red}{bold}level 3{no} - eight letter word.
'''
    print(get_format_text(level_description))
    while True:
        answer = input(
            get_format_text('{bold}Choose the level, enter 1 or 2 or 3:{no} '))
        if answer in ['1', '2', '3']:
            get_clear_screen()
            return LEVEL_WORD_LENGTH[answer]
        print(get_format_text(
            '{bold}{red}Something is wrong! Use only digits 1 or 2 or 3.{no}'
        ))
        time.sleep(SLEEP)
        get_clear_screen()


def get_word_list(num_letters):
    """get list of words for current level"""
    url = f'https://www.wordexample.com/list/nouns-with-{num_letters}-letters'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    words_soup = soup.find_all('span', attrs={'class': "word-popover"})
    words = []
    [words.append(
        word.text.replace('\n', '').replace('\t', '')
    ) for word in words_soup]
    return words


def get_word(num_letters):
    """choose one word from the list"""
    word_list = get_word_list(num_letters)
    return random.choice(word_list).upper()


def set_picture(shown_word, correct_letters, wrong_letters):
    """visualize picture, correct and incorrect letters"""
    pictures = ['''{bold}
____
|  |
|
|
|
|
    {no}''', '''{bold}
____
|  |
|  O
|
|
|
    {no}''', '''{bold}
____
|  |
|  O
|  |
|
|
    {no}''', '''{bold}
____
|  |
|  O
| /|
|
|
    {no}''', '''{bold}
____
|  |
|  O
| /|\\
|
|
    {no}''', '''{bold}
____
|  |
|  O
| /|\\
| /
|
    {no}''']
    picture = get_format_text(pictures[len(wrong_letters)])
    print(picture)
    print(*shown_word, '\n', sep=' ')
    print(get_format_text('{green}Correct letters:{no} '), *correct_letters,
          sep=' ')
    print(get_format_text('{red}Wrong letters:{no}'), *wrong_letters, '\n',
          sep=' ')


def get_letter_guess(word, shown_word, correct_letters, wrong_letters):
    """the player try to guess correct letter"""
    def _map_letters():
        for i in range(len(word)):
            if word[i] == letter:
                shown_word[i] = letter
        return shown_word

    alphabet = []
    alphabet[:] = string.ascii_uppercase
    set_picture(shown_word, correct_letters, wrong_letters)
    while True:
        letter = input(
            get_format_text('{bold}Please, enter a letter:{no} \n')).upper()
        if letter in wrong_letters or letter in correct_letters:
            print(get_format_text('{red}You have already guessed this letter! '
                                  'Please, enter another one.{no}\n'))
            time.sleep(SLEEP)
            get_clear_screen()
        elif letter not in alphabet:
            print(get_format_text('{red}Please, enter ONE LETTER.{no}\n'))
            time.sleep(SLEEP)
            get_clear_screen()
        else:
            if letter not in word:
                print(get_format_text('\n{red}Wrong!{no}\n'))
                time.sleep(SLEEP)
                get_clear_screen()
                wrong_letters.append(letter)
                return shown_word, correct_letters, wrong_letters

            print(get_format_text("\n{green}That's right!{no}\n"))
            time.sleep(SLEEP)
            get_clear_screen()
            correct_letters.append(letter)
            shown_word = _map_letters()
            return shown_word, correct_letters, wrong_letters


def set_rating(wrong_letters, word):
    """determines if a player won or lost, set rating"""

    ratings = {
        0: '{yellow}{bold}*****{no} {green}{bold}CHAMPION{no}',
        1: '{yellow}{bold}*****{no}',
        2: '{yellow}{bold}****{no}',
        3: '{yellow}{bold}***{no}',
        4: '{yellow}{bold}**{no}',
        5: '{yellow}{bold}*{no}'
    }
    picture = '''{bold}
____
|  |
|  O
| /|\\
| / \\
|
    {no}'''

    attempt = len(wrong_letters)

    if attempt == ATTEMPT_NUM:
        print(get_format_text(picture),
              get_format_text('{bold}YOU LOSE! {red}GAME OVER{no}\n'),
              'The hidden word is: {}\n'.format(word), sep='\n')
        time.sleep(SLEEP)
    else:
        rating = ratings[len(wrong_letters)]
        print(get_format_text('{bold}{yellow}CONGRATS, YOU WIN!{no}\n'),
              'Your rating is {}\n'.format(get_format_text(rating)),
              'The hidden word is: {}\n'.format(word), sep='\n')
        time.sleep(SLEEP)

    print(get_format_text('{bold}{green}You can try again!{no}'))
    time.sleep(SLEEP)
    get_clear_screen()


def main():
    get_clear_screen()
    get_start()
    while True:
        start_game = get_agreement()
        if not start_game:
            break
        level_word_length = set_level()
        word = get_word(level_word_length)
        correct_letters = []
        wrong_letters = []
        shown_word = ['_' for _ in range(level_word_length)]
        while '_' in shown_word and len(wrong_letters) < ATTEMPT_NUM:
            shown_word, correct_letter, wrong_letters = get_letter_guess(
                word,
                shown_word,
                correct_letters,
                wrong_letters
            )
        set_rating(wrong_letters, word)


if __name__ == '__main__':
    main()
