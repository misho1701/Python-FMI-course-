import os
import tempfile
import unittest

from bangaranga import does_the_banga_rang, TheBangaDoesNotRangError


class DoesTheBangaRangTests(unittest.TestCase):
    def create_temp_file(self, content):
        temp = tempfile.NamedTemporaryFile(mode="w", delete=False)
        self.addCleanup(lambda: os.remove(temp.name) if os.path.exists(temp.name) else None)

        temp.write(content)
        temp.close()

        return temp.name

    def test_returns_minimum_number_of_words(self):
        filename = self.create_temp_file(
            "bang a banga ranga bangaranga"
        )

        self.assertEqual(1, does_the_banga_rang(filename))

    def test_finds_bangaranga_from_two_words(self):
        filename = self.create_temp_file(
            "The banga is doing some ranga!"
        )

        self.assertEqual(2, does_the_banga_rang(filename))

    def test_finds_bangaranga_from_multiple_words(self):
        filename = self.create_temp_file(
            "bang a small ranga"
        )

        self.assertEqual(3, does_the_banga_rang(filename))

    def test_returns_zero_when_words_are_in_wrong_order(self):
        filename = self.create_temp_file(
            "ranga before banga"
        )

        self.assertEqual(0, does_the_banga_rang(filename))

    def test_returns_zero_when_bangaranga_cannot_be_formed(self):
        filename = self.create_temp_file(
            "Does the banga rang?"
        )

        self.assertEqual(0, does_the_banga_rang(filename))

    def test_search_is_case_insensitive(self):
        filename = self.create_temp_file(
            "BaNgA RANGA"
        )

        self.assertEqual(2, does_the_banga_rang(filename))

    def test_uses_only_whole_words(self):
        filename = self.create_temp_file(
            "xxbangayy rangazz"
        )

        self.assertEqual(0, does_the_banga_rang(filename))

    def test_words_can_be_separated_by_non_word_content(self):
        filename = self.create_temp_file(
            "bang...a!!!ranga"
        )

        self.assertEqual(3, does_the_banga_rang(filename))

    def test_raises_custom_error_when_file_cannot_be_read(self):
        with self.assertRaises(TheBangaDoesNotRangError):
            does_the_banga_rang("missing_file.txt")

if __name__ == "__main__":
    unittest.main()