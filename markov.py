"""
Use a Markov process to generate random sentences based on a source text.
"""

import random


def build_word_list(source_text):
    """
    Splits an input string into just the words and punctuation, getting
    rid of whitespace.

    Inputs:
        String: source_text. The text to be split

    Outputs:
        List: word_list. The input string split into words with whitespace
        removed
    """
    newlines_to_spaces = source_text.replace('\n', ' ')
    split = newlines_to_spaces.split(' ')
    removed_blanks = [i for i in split if i != '']

    word_list = removed_blanks
    return word_list


def build_next_words(word_list):
    """
    Takes an input list of ordered words and returns a dictionary of
    those words as keys and the words following them as corresponding
    items.

    Inputs:e 
        List: word_list. The list of words for which the dictionary is formed.

    Outputs:
        Dict: next_words. The dictionary with words from word_list as keys
        and the list of words following those keys words as items.
    """
    next_words = {"": [word_list[0]]}
    for i in range(len(word_list)):
        item = word_list[i]
        if item not in next_words.keys():
            if i < len(word_list) - 1:
                if item[-1] in [".", "!", "?"]:
                    next_words[item] = [""]
                    next_words[""].append(word_list[i+1])
                else:
                    next_words[item] = [word_list[i + 1]]
            else:
                if item[-1] in [".", "!", "?"]:
                    next_words[item] = [""]
        else:
            if item[-1] in [".", "!", "?"]:
                try:
                    next_words[""].append(word_list[i+1])
                except:
                    pass
            else:
                next_words[item].append(word_list[i + 1])
    return next_words

def build_next_two_words(word_list):
    next_two_words = {"": [(word_list[0], word_list[1])]}
    word_index = 0
    next_word_start_sentence = True
    for i in range(len(word_list)):
        item = word_list[i]
        if next_word_start_sentence:
            next_word_start_sentence = False
        else:
            if (word_list[i-1], item) not in next_two_words.keys():
                if i < len(word_list) - 1:
                    if item[-1] in [".", "!", "?"]:
                        try:
                            next_two_words[item] = [""]
                            next_two_words[""].append((word_list[i+1], word_list[i+2]))
                        except:
                            pass
                        next_word_start_sentence = True
                    else:
                        next_two_words[(word_list[i-1], item)] = [word_list[i+1]]
                else:
                    if item[-1] in [".", "!", "?"]:
                        next_word_start_sentence = True
                        next_two_words[(word_list[i-1], item)] = [""]
            else:
                if item[-1] in [".", "!", "?"]:
                    next_word_start_sentence = True
                    try:
                        next_two_words[""].append((word_list[i+1], word_list[i+2]))
                    except:
                        pass
                else:
                    next_two_words[(word_list[i-1], item)].append(word_list[i + 1])
    return next_two_words

def generate_sentence_two(next_two_words):
    sentence_finished = False
    previous_word = ""
    first_words = next_two_words[""][random.choice(range(len(next_two_words[""])))]
    if len(first_words) == 1:
        return first_words[0]
    sentence_two = f"{first_words[0]} {first_words[1]} "
    if first_words[1][-1] in [".","!","?"]:
        return sentence_two
    previous_words = (first_words[0], first_words[1])
    while not sentence_finished:
        next_word = next_two_words[previous_words][random.choice(
            range(len(next_two_words[previous_words])))]
        sentence_two = sentence_two + next_word + " "
        previous_words = (previous_words[1], next_word)
        if next_word[-1] in [".", "!", "?"]:
            sentence_finished = True
            sentence_two = sentence_two[:-1]
    return sentence_two



def generate_sentence(next_words):
    """
    Takes an input of words and following words and returns a markov-generated
    sentence.

    Inputs:
        Dict: next_words. The dictionary from which words and their potential
        following words are pulled from.

    Outputs:
        String: sentence. The markov-generated sentence from next_words.
    """
    sentence_finished = False
    previous_word = ""
    sentence = ""
    while not sentence_finished:
        next_word = next_words[previous_word][random.choice(
            range(len(next_words[previous_word])))]
        sentence = sentence + next_word + " "
        previous_word = next_word
        if previous_word[-1] in [".", "!", "?"]:
            sentence_finished = True
            sentence = sentence[:-1]
    return sentence


def generate_text(next_words, num_sentences):
    """
    Takes an input of words and following words and returns a markov-generated
    sentence.

    Inputs:
        Dict: next_words. The dictionary from which words and their potential
        following words are pulled from.
        Int: num_sentences. The number of sentences to be generated

    Outputs:
        String: sentences. The markov-generated sentences from next_words.
    """
    sentences_finished = 0
    previous_word = ""
    sentences = ""
    while sentences_finished < num_sentences:
        next_word = next_words[previous_word][random.choice(
            range(len(next_words[previous_word])))]
        sentences = sentences + next_word + " "
        previous_word = next_word
        if previous_word != "":
            if previous_word[-1] in [".", "!", "?"]:
                sentences_finished += 1
                sentences = sentences[:-1]
    return sentences