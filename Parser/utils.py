# coding=utf-8
from collections import Counter
from copy import deepcopy

import numpy
import re
import nltk

from positive_words import positive_words
from negative_words import negative_words
from stopwords import stop_words

full_pattern = re.compile(r'[^a-zA-Z \'´`]|_')

nltk.download('averaged_perceptron_tagger')

def re_replace(string):
    return re.sub(full_pattern, '', string)


def median(lst):
    return numpy.median(numpy.array(lst))


def mean(lst):
    return float(sum(lst)) / len(lst) if len(lst) > 0 else float('nan')


def count_words_from_string(string, speakernames=None):
    string = string.lower()
    string = re_replace(string)

    result_list, positive_results, negative_results, names_called = [], [], [], []

    word_list = string.split()
    word_list = [word for word in deepcopy(word_list) if word not in stop_words]

    pos_tagging = nltk.pos_tag(word_list)
    counts = Counter(tag for word, tag in pos_tagging)

    distinct_nouns = list(set([item[0] for item in pos_tagging if item[1].startswith('NN')]))
    distinct_adj = list(set([item[0] for item in pos_tagging if item[1].startswith('JJ')]))
    distinct_adv = list(set([item[0] for item in pos_tagging if item[1].startswith('RB')]))
    distinct_ver = list(set([item[0] for item in pos_tagging if item[1].startswith('VB')]))

    noun_count = int(counts.get('NN', 0)) + int(counts.get('NNS', 0)) + int(counts.get('NNP', 0)) + int(counts.get('NNPS', 0))
    adjective_count = int(counts.get('JJ', 0)) + int(counts.get('JJR', 0)) + int(counts.get('JJS', 0))
    verb_count = int(counts.get('VB', 0)) + int(counts.get('VBD', 0)) + int(counts.get('VBG', 0)) + \
                 int(counts.get('VBN', 0)) + int(counts.get('VBP', 0)) + int(counts.get('VBZ', 0))
    adverb_count = int(counts.get('RB', 0)) + int(counts.get('RBR', 0)) + int(counts.get('RBS', 0))

    print counts

    positive_word_list = [word for word in deepcopy(word_list) if word.decode('utf-8') in positive_words]
    negative_word_list = [word for word in deepcopy(word_list) if word.decode('utf-8') in negative_words]
    name_word_list = [word for word in deepcopy(word_list) if word.decode('utf-8') in speakernames]

    distinct_words = list(set(word_list))
    distinct_positive = list(set(positive_word_list))
    distinct_negative = list(set(negative_word_list))
    distinct_names = list(set(name_word_list))

    for word in distinct_words:
        result_list.append([word, word_list.count(word)])

    for word in distinct_negative:
        negative_results.append([word, negative_word_list.count(word)])

    for word in distinct_positive:
        positive_results.append([word, positive_word_list.count(word)])

    for name in distinct_names:
        names_called.append([name, name_word_list.count(name)])

    return {"count": len(word_list), "list": result_list}, {"count": len(positive_word_list),"list": positive_results}, {"count": len(negative_word_list), "list": negative_results}, {"count": len(names_called),"list": names_called}, len(distinct_words), len(distinct_nouns), len(distinct_adv), len(distinct_adj), len(distinct_ver)
