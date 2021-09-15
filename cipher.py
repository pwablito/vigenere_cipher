#!/usr/bin/env python3

import argparse
import sys


def get_valid_characters(message):
    return ''.join(
        [character.lower() for character in message if character.isalpha()]
    )


def character_to_number(character):
    return ord(character) - ord('a')


def number_to_character(number):
    return chr(number + ord('a'))


def encrypt_number(number, key_number):
    return (number + key_number) % 26


def decrypt_number(number, key_number):
    return (number - key_number) % 26


def expand_key(key, length):
    key_len = len(key)
    expanded_key = ""
    for i in range(length):
        expanded_key += key[i % key_len]
    return expanded_key


def encrypt(message, key):
    expanded_key = expand_key(key, len(message))
    result = ""
    for i in range(len(message)):
        result += number_to_character(
            encrypt_number(
                character_to_number(message[i]),
                character_to_number(expanded_key[i])
            )
        )
    return result


def decrypt(message, key):
    expanded_key = expand_key(key, len(message))
    result = ""
    for i in range(len(message)):
        result += number_to_character(
            decrypt_number(
                character_to_number(message[i]),
                character_to_number(expanded_key[i])
            )
        )
    return result


def main():
    parser = argparse.ArgumentParser("Vigenere cipher")
    parser.add_argument("-k", "--key", help="key", required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("encrypt", help="Encrypt a message")
    subparsers.add_parser("decrypt", help="Decrypt a message")
    args = parser.parse_args()
    message = get_valid_characters(sys.stdin.read())
    if args.command == 'encrypt':
        print(encrypt(message, args.key))
    elif args.command == 'decrypt':
        print(decrypt(message, args.key))
    else:
        exit("Invalid command")


if __name__ == '__main__':
    main()
