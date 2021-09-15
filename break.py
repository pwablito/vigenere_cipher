#!/usr/bin/env python3

import cipher
import argparse
import sys


natural_character_frequencies = {
    'a': 0.08167,
    'b': 0.01492,
    'c': 0.02782,
    'd': 0.04253,
    'e': 0.12702,
    'f': 0.02228,
    'g': 0.02015,
    'h': 0.06094,
    'i': 0.06966,
    'j': 0.00153,
    'k': 0.00772,
    'l': 0.04025,
    'm': 0.02406,
    'n': 0.06749,
    'o': 0.07507,
    'p': 0.01929,
    'q': 0.00095,
    'r': 0.05987,
    's': 0.06327,
    't': 0.09056,
    'u': 0.02758,
    'v': 0.00978,
    'w': 0.02360,
    'x': 0.00150,
    'y': 0.01974,
    'z': 0.00074,
}


def get_offness_score(text):
    scores = {}
    for character in natural_character_frequencies.keys():
        actual = text.count(character) / len(text)
        expected = natural_character_frequencies[character]
        difference = abs(actual - expected)
        scores[character] = difference
    return sum(scores.values()) / len(scores)


def best_at_size(ciphertext, key_size):
    best_key = ""
    for key_position in range(key_size):
        indexed_ciphertext = ""
        for index in range(len(ciphertext)):
            if index % key_size == key_position:
                indexed_ciphertext += ciphertext[index]
        best_scores = {}
        for i in range(26):
            key = cipher.number_to_character(i)
            score = get_offness_score(cipher.decrypt(indexed_ciphertext, key))
            best_scores[i] = {
                "score": score,
                "char_index": i,
            }
        best_key += cipher.number_to_character(
            min(best_scores.keys(), key=lambda x: best_scores[x]["score"])
        )
    plaintext = cipher.decrypt(ciphertext, best_key)
    return get_offness_score(plaintext), best_key, plaintext


def main():
    parser = argparse.ArgumentParser("Break a Viginere ciphertext")
    parser.add_argument(
        "-k", "--key-length",
        help="max key length to try",
        type=int, default=20
    )
    args = parser.parse_args()
    ciphertext = cipher.get_valid_characters(sys.stdin.read())
    solutions_dict = {}
    for current_key_size in range(1, args.key_length + 1):
        score, key, plaintext = best_at_size(ciphertext, current_key_size)
        solutions_dict[current_key_size] = {
            "score": score,
            "key": key,
            "plaintext": plaintext
        }
    best_solution_key = min(
        solutions_dict.keys(), key=lambda x: solutions_dict[x]["score"]
    )
    print(f"Key: {solutions_dict[best_solution_key]['key']}")
    print(solutions_dict[best_solution_key]["plaintext"])


if __name__ == '__main__':
    main()
