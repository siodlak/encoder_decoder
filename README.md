# encoder_decoder

### Requirements

* Python 3.6

### Installation

To download script go to chosen local directory and clone that repository

```commandline
cd dir_of_your_choice
git clone https://github.com/siodlak/encoder_decoder
```
There is also implemented dockerfile to simplify build microservice and separate it from environment.

### Usage

It is Py script to encode and decode text. Just use it in any directory you wish.
The script is designed to encode and decode text in that way: for each original word in the original text,
there are left the first and last character and shuffle all the characters in the middle of the word.   
Warning:
    Decoder module is designed to unambiguous handle text. In conflict case only raise exception and stop execution.
Passing -t or --test [text to handle] argument is mandatory. User can choice explicit script mode: decode or encode.
There is possible to pass text to decode and original words list in separate arguments.
Passing optional argument -l or --list_original [original words list] enable that mode.

### Command-line options

The following is the output when `-h` or `--help` option is passed to the main script, which should be self-explanatory:

```commandline
usage: encoder_decoder.py [-h] -t TEXT
                          [-l [LIST_ORIGINAL [LIST_ORIGINAL ...]]] [-e] [-d]
                          [-v]

Script to encode and decode text

arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text to handle
  -l [LIST_ORIGINAL [LIST_ORIGINAL ...]], --list_original [LIST_ORIGINAL [LIST_ORIGINAL ...]]
                        Original words list
  -e, --encode          Encode text with attached original words
  -d, --decode          Decode text
  -v, --verbose         Enable to print output
```

### Usage examples

#### Automatic mode

Default behavior of script is recognize test state (encoded/decoded) and handle it automatically.
```commandline
encoder_decoder.py -t "Text to handle"
```

#### Encoding

It is flag to force encoding mode
```commandline
encoder_decoder.py -e -t "Text to handle"
```

#### Decoding

It is flag to force decoding mode
```commandline
encoder_decoder.py -d -t "Text to handle"
```

#### Verbose

To verbose result pass -v or --verbose flag in every case
```commandline
encoder_decoder.py -v -t "Text to handle"
```

#### Separate original words list from text to decode

Script have additional mode to take test to decode and original words list separately.list
To verbose result pass -v or --verbose flag in every case
```commandline
encoder_decoder.py -v -t "Text to handle"
```

### Known issues

There may be an exception raised when in decoded string are two or more words matched to pattern.
The purpose of that behaviour is assurance encode text unambiguously or not at all

### Notes

In case you have any ideas for new features or spotted a bug, either let me know or post an issue here.

### Links

https://github.com/siodlak/encoder_decoder/tree/master
