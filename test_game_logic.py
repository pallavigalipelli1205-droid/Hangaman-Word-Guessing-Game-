
from game_logic import (
    select_word,
    display_word,
    check_guess,
    check_win
)

# Test 1
word = select_word("Easy")
print("Selected word:", word)

# Test 2
print("Display:", display_word("apple", ["a", "p"]))

# Test 3
print("Guess:", check_guess("apple", "a"))

# Test 4
print("Win:", check_win("cat", ["c", "a", "t"]))

print("Game logic testing completed!")
