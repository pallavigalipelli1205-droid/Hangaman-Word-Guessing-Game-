
import random

# Word collection
words = {
    "Easy": ["cat", "dog", "sun", "pen"],
    "Medium": ["python", "school", "tiger"],
    "Hard": ["computer", "elephant", "developer"]
}


def select_word(difficulty):
    word_list = words[difficulty]
    return random.choice(word_list)


def display_word(word, guessed_letters):
    display = ""

    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "

    return display.strip()


def check_guess(word, guess):
    return guess.lower() in word.lower()


def check_win(word, guessed_letters):
    return all(
        letter in guessed_letters
        for letter in word.lower()
    )
