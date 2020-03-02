"""
It is module to test encoder_decoder script
"""

import unittest

import encoder_decoder


class TestEncoderMethods(unittest.TestCase):
    encoder = encoder_decoder.TextEncoder(r"This is a long looong test sentence,\nwith some big (biiiiig) words!")
    enc_txt = encoder.encode_text()

    def test_shuffle_middle(self):
        self.assertNotEqual(self.encoder.shuffle_middle("looong"), "looong")

    def test_decode_encoded(self):
        decoder = encoder_decoder.TextDecoder(self.enc_txt)
        dec_txt = decoder.decode_text()
        self.assertEqual(self.encoder._original_text, dec_txt)

    def test_encode_text_1(self):
        self.assertNotEqual(self.encoder.encoded_text, self.encoder._original_text)

    def test_encode_text_2(self):
        self.assertEqual(self.encoder.encoded_text, self.enc_txt)


class TestDecoderMethods(unittest.TestCase):
    encoder = encoder_decoder.TextEncoder(r"This is a long looong test sentence,\nwith some big (biiiiig) words!")
    decoder_1 = encoder_decoder.TextDecoder(
        r"\n—weird—\nTihs is a lnog lonoog tset scennete,\ntwih smoe big (biiiiig) "
        r"wdros!\n—weird—\ntest long sentence words This nwith some looong")
    decoder_2 = encoder_decoder.TextDecoder(
        r"\n—weird—\nTihs is a lnog lonoog tset snceente,\nwtih smoe big (biiiiig) wrdos!\n—weird—\n",
        r"looong test This some words nwith sentence long".split(' '))

    def test_decode_word_1(self):
        self.assertEqual(self.decoder_1.decode_word("lnog"), "long")

    def test_decode_word_2(self):
        self.assertIs(self.decoder_2.decode_word("is"), "is")

    def test_decode_text_1(self):
        self.assertEqual(self.decoder_1.decode_text(), self.encoder._original_text)

    def test_decode_text_2(self):
        self.assertEqual(self.decoder_2.decode_text(), self.encoder._original_text)


class TestHandlerMethods(unittest.TestCase):
    handler = encoder_decoder.TextHandler()

    def test_possible_to_shuffle_1(self):
        self.assertTrue(self.handler.possible_to_shuffle("Rafal"))

    def test_possible_to_shuffle_2(self):
        self.assertFalse(self.handler.possible_to_shuffle("Ala"))

    def test_surround_string(self):
        self.assertEqual(self.handler.surround_string("Ala", "Rafal"), "RAlal")

    def test_separator(self):
        self.assertIsNotNone(self.handler.separator)


if __name__ == '__main__':
    unittest.main()
