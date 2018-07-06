from .exceptions import *
from random import choice


class GuessAttempt(object):
    def __init__(self, guess, hit=False, miss=False):
        if hit == miss:
            raise InvalidGuessAttempt
        self.guess = guess
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        return self.hit
        
    def is_miss(self):
        return self.miss


class GuessWord(object):
    def __init__(self, word):
        if word == "":
            raise InvalidWordException
        self.answer = word
        self.masked = "*" * len(word)
        
    def perform_attempt(self, char):
        if len(char) > 1:
            raise InvalidGuessedLetterException
        if char.lower() in self.answer.lower():
            masked_list = list(self.masked)
            for i in range(len(self.answer)):
                if self.answer[i].lower() == char.lower():
                    masked_list[i] = char.lower()
            self.masked = "".join(masked_list)
            return GuessAttempt(char, hit=True)
        return GuessAttempt(char, miss=True)
        


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    @classmethod
    def select_random_word(cls, list_of_words):
        if not list_of_words or any(type(word) != str for word in list_of_words):
            raise InvalidListOfWordsException
        return choice(list_of_words)
    
    def __init__(self, word_list=None, number_of_guesses=5):
        word = choice(word_list) if word_list else choice(HangmanGame.WORD_LIST)
        self.word = GuessWord(word)
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        
    def guess(self, char):
        if self.is_finished():
            raise GameFinishedException
        attempt = self.word.perform_attempt(char)
        self.previous_guesses.append(char.lower())
        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.remaining_misses == 0:
                raise GameLostException
        if "*" not in self.word.masked:
            raise GameWonException
        return attempt

    def is_finished(self):
        return self.remaining_misses == 0 or "*" not in self.word.masked
        
    def is_won(self):
        return "*" not in self.word.masked
        
    def is_lost(self):
        return self.remaining_misses == 0