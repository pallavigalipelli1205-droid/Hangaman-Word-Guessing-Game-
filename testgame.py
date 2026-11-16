
from game_logic import (
    select_word,
    display_word,
    check_guess,
    check_win
)

# Select a word
word = select_word("Easy")

guessed_letters = []
attempts = 6

print("Welcome to Hangman!")

while attempts > 0:

    print("\nWord:", display_word(word, guessed_letters))
    print("Attempts remaining:", attempts)

    if check_win(word, guessed_letters):
        print("Congratulations! You won!")
        break

    guess = input("Guess a letter: ").lower()

    if len(guess) != 1 or not guess.isalpha():
        print("Enter a single alphabet!")
        continue

    if guess in guessed_letters:
        print("Already guessed!")
        continue

    guessed_letters.append(guess)

    if check_guess(word, guess):
        print("Correct guess!")
    else:
        print("Wrong guess!")
        attempts -= 1

else:
    print("Game Over!")
    print("Correct word:", word)
