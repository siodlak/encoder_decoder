"""
It is Py script to encode and decode text. There are shuffled middle char in words and left first and last.
"""
import argparse
import re
from random import shuffle
from itertools import permutations


class ConsolePrompt:
    """
    Parse arguments and initialize encoder/decoder
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Module to encode and decode taxt", add_help=True)
        self.parser.add_argument("-t", "--text", type=str, help="Text to automatic handle")
        self.parser.add_argument("-e", "--encode", type=str, help="Text to encode with attached original words list")
        self.parser.add_argument("-d", "--decode", type=str, help="Text to decode")
        self.parser.add_argument("-l", "--list_original", nargs='*', type=str, default=[], help="Original words list")
        self.parser.add_argument("-v", "--verbose", action="store_true", help="Enable print output")
        self.__args = self.parser.parse_args()

        self._output = None
        self.__take_action()

    def __take_action(self):
        """
        Take action (scenario) base on passed to script arguments
        """
        if bool(self.__args.list_original):  # case with separated list
            text_decoder = TextDecoder(self.__args.text, self.__args.list_original)
            self._output = text_decoder.decode_text()
        elif bool(self.__args.encode):
            text_encoder = TextEncoder(self.__args.encode)
            self._output = text_encoder.encode_text()
        elif bool(self.__args.decode):
            text_decoder = TextDecoder(self.__args.decode)
            self._output = text_decoder.decode_text()
        elif bool(self.__args.text):  # if it is not selected, script try decode passed text in failure case encode it
            try:
                text_decoder = TextDecoder(self.__args.text)
                self._output = text_decoder.decode_text()
            except InputTextException:
                print("Trying to encode")
                text_encoder = TextEncoder(self.__args.text)
                self._output = text_encoder.encode_text()

        if self.__args.verbose:
            print(self._output)


class TextHandler:
    """
    Parent class for encoder and decoder to save separator and define common flow
    """

    def __new__(cls, *args, **kwargs):
        cls._separator = r"\n—weird—\n"
        return super().__new__(cls)

    def possible_to_shuffle(self, word):
        return len(word) > 3 and len(set(word[1:-1])) != 1  # impossible to shuffle words

    def surround_string(self, to_surround, word):
        return word[0] + to_surround + word[-1]

    @property
    def separator(cls):
        return cls._separator


class TextEncoder(TextHandler):
    """
    Build object that encode plain text
    """

    def __init__(self, text):
        """
        Initialize encoder
        """
        super().__init__()
        self._original_text = text
        self._original_words = set()
        self._encoded_text = None

    def shuffle_middle(self, word):
        """
        Shuffle word center and return word where first and last char are left but center is shuffled
        """
        middle = list(word[1:-1])
        shuffled_word = word
        while shuffled_word == word:
            shuffle(middle)
            shuffled_word = self.surround_string(''.join(middle), word)
        return shuffled_word

    def encode_word(self, word):
        """
        Encode and append to list only possible to shuffle words.
        """
        if not self.possible_to_shuffle(word):
            return word
        self._original_words.add(word)
        return self.shuffle_middle(word)

    def encode_text(self):
        """
        Encode whole text and return it
        """
        self._encoded_text = self._original_text
        for word in re.findall(r'\w+', self._original_text, re.U):
            self._encoded_text = re.sub(word, self.encode_word(word), self._encoded_text, 1)

        self._encoded_text = self.separator + self._encoded_text + self.separator + ' '.join(self.original_words)
        return self._encoded_text  # to test and verbose purpose

    @property
    def encoded_text(self):
        return self._encoded_text

    @property
    def original_words(self):
        return sorted(self._original_words, key=str.casefold)


class TextDecoder(TextHandler):
    """
    Build object that decode encoded text
    """

    def __new__(cls, text_to_decode, original_words=None):
        """
        Data validator. Check if passed text was previously encoded in TestEncoder
        """
        separator = super().__new__(cls).separator
        if not bool(text_to_decode):
            raise LackTextToDecodeException()
        if not text_to_decode.startswith(separator) or len(text_to_decode.split(separator)) < 3:
            raise InputTextException(separator)
        return super().__new__(cls)

    def __init__(self, text_to_decode, original_words=None):
        """
        Initialize decoder object. Take one argument - string with encoded text and attached list of original words
        or take two argument -  separate encoded text and original words list
        """
        super().__init__()
        # if text to decode and list are in one string
        self._text_to_decode, self._original_words = text_to_decode.split(self.separator)[1:]
        self._original_words = self._original_words.split(' ')  # change var type
        if original_words is not None:
            self._original_words = original_words  # if text to decode and list are separately
        self._decoded_text = None

    def get_middle_anagrams(self, word):
        """
        Return all possible unique anagrams for  passed word middle.
        E.g. for "Rafal" -> ['afa', 'aaf', 'faa', 'faa', 'aaf', 'afa']
        """
        middle = word[1:-1]
        return set([''.join(chars_tuple) for chars_tuple in permutations(middle)])  # to avoid anagram repetitions

    def decode_word(self, word):
        """
        Decode word by match possible combinations and records in original words list. If there are more than one match
        words raise exception. If there is exacly one matched word method return that word
        """
        if not self.possible_to_shuffle(word):
            return word
        unique_middle_anagrams = self.get_middle_anagrams(word)
        possible_words = [
            self.surround_string(unique_middle_anagram, word) for unique_middle_anagram in unique_middle_anagrams]

        match_words = []
        for possible_word in possible_words:
            for original_word in self._original_words:
                if possible_word == original_word:
                    match_words.append(original_word)

        if len(match_words) != 1:
            raise AmbiguityException(match_words)
        return match_words[0]

    def decode_text(self):
        """
        Decode whole text and return it
        """
        self._decoded_text = self._text_to_decode

        words_to_decode = re.findall(r'\w+', self._text_to_decode)
        for word in words_to_decode:
            decoded_word = self.decode_word(word)
            self._decoded_text = re.sub(word, decoded_word, self._decoded_text)
        return self._decoded_text  # to test and verbose purpose

    @property
    def decoded_text(self):
        return self._decoded_text


class LackTextToDecodeException(Exception):
    """
    Raise exceprion when there is no text to handle
    """

    def __init__(self):
        print("There is no passed text to decode")


class InputTextException(Exception):
    """
    Raise exception when separator is not proper. Do not indicate to encode by this script
    """

    def __init__(self, separator):
        self.separator = separator

        print("There is no proper separator ({}) indicating to encoded text".format(self.separator))


class AmbiguityException(Exception):
    """
    Raise exception when there is more than one word match to pattern
    """

    def __init__(self, match_words):
        self.match_words = match_words

        print("There are more than one word match to pattern:")
        [print(word) for word in self.match_words]


if __name__ == '__main__':
    ConsolePrompt()
