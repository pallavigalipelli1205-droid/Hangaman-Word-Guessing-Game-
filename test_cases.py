
import unittest

from game_logic import (
    select_word,
    display_word,
    check_guess,
    check_win
)


class TestHangmanGame(unittest.TestCase):

    def test_select_word(self):
        word = select_word("Easy")
        self.assertIn(word, ["cat", "dog", "sun", "pen"])

    def test_display_word(self):
        result = display_word("python", ["p", "t"])
        self.assertEqual(result, "p _ t _ _ _ ")

    def test_correct_guess(self):
        self.assertTrue(check_guess("python", "p"))

    def test_wrong_guess(self):
        self.assertFalse(check_guess("python", "z"))

    def test_check_win(self):
        self.assertTrue(
            check_win("cat", ["c", "a", "t"])
        )

    def test_check_not_win(self):
        self.assertFalse(
            check_win("cat", ["c", "a"])
        )


if __name__ == "__main__":
    unittest.main()
