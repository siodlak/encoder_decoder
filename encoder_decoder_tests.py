"""
It is module to test encoder_decoder script
"""

import unittest

import encoder_decoder


class TestEncoderMethods(unittest.TestCase):
    encoder = encoder_decoder.TextEncoder(r"This is a long looong test sentence,\nwith some big (biiiiig) words!")

    def test_shuffle_middle(self):
        self.assertNotEqual(self.encoder.shuffle_middle("looong"), "looong")

    def test_decode_encoded(self):
        enc_txt = self.encoder.encode_text()
        decoder = encoder_decoder.TextDecoder(enc_txt)
        dec_txt = decoder.decode_text()
        self.assertEqual(self.encoder._original_text, dec_txt)


class TestDecoderMethods(unittest.TestCase):
    handler = encoder_decoder.TextHandler()
    separator = handler.separator
    decoder_1 = encoder_decoder.TextDecoder(
        r"\n—weird—\nTihs is a lnog lonoog tset scennete,\ntwih smoe big (biiiiig) "
        r"wdros!\n—weird—\ntest long sentence words This nwith some looong")
    decoder_2 = encoder_decoder.TextDecoder(
        r"\n—weird—\nTihs is a lnog lonoog tset snceente,\nwtih smoe big (biiiiig) wrdos!\n—weird—\n",
        r"looong test This some words nwith sentence long".split(' '))

    def test_decode_word(self):
        self.assertEqual(self.decoder_1.decode_word("Ala"), "Ala")


if __name__ == '__main__':
    unittest.main()
