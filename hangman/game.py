import random
from .exceptions import *


class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        if hit and miss:
            raise InvalidGuessAttempt()

        self.letter = letter
        self.hit = hit
        self.miss = miss

    def is_hit(self):
        if self.hit:
            return True
        return False

    def is_miss(self):
        if self.miss:
            return True
        return False



class GuessWord(object):
    def __init__(self, word):
        if not word:
            raise InvalidWordException()

        self.answer = word
        self.masked = '*' * len(word)

    def unveil_word(self, letter):
        s = ""
        for i in range(len(self.answer)):
            word_letter = self.answer[i]
            mask_letter = self.masked[i]

            if mask_letter != '*':
                s += mask_letter
            elif letter == word_letter.lower():
                s += word_letter.lower()
            else:
                s += '*'
        return s

    def perform_attempt(self, letter):
        if len(letter) > 1:
            raise InvalidGuessedLetterException()

        letter = letter.lower()
        if letter in self.answer.lower():
            attempt = GuessAttempt(letter, hit=True)
            self.masked = self.unveil_word(letter)
        else:
            attempt = GuessAttempt(letter, miss=True)
        return attempt


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, word_list=None, number_of_guesses=5):
        if word_list is None:
            word_list = self.WORD_LIST

        self.remaining_misses = number_of_guesses

        selected_word = self.select_random_word(word_list)
        self.word = GuessWord(selected_word)
        self.previous_guesses = []

    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException()
        self.previous_guesses.append(letter.lower())

        attempt = self.word.perform_attempt(letter)
        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException()

        if self.is_won():
            raise GameWonException()

        return attempt

    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False

    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        return False

    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False

    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
