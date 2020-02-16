import functools
import math
import operator
import re
import time
from collections import Counter


from nltk.corpus import names
labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
    [(name, 'female') for name in names.words('female.txt')])

def counter_wrapper(c, key):
    if c.get(key) is None:
        return 0
    return c.get(key)

def is_male_name(name):
    male_names = [s.lower() for s in names.words('male.txt')]
    print(male_names[:50])
    return name in male_names

def is_female_name(name):
    female_names = [s.lower() for s in names.words('female.txt')]

    return name in female_names



def is_male_story(plot):
    plot = plot.split(" ")
    plot = [re.sub(r'[^\w\s]', '', s) for s in plot]  #remove punctuation
    plot = [ s.lower() for s in plot]  #change all words to lower case
    c = Counter(plot)
    male_signs_str = ["he", "his", "him", "man", "men", "brother", "brothers",
                      "father", "fathers", "king", "kings","cowboy", "cowboys",
                      "boy", "boys", "son"]
    female_signs_str =["she", "her", "women", "woman", "sister", "sisters", "mother",
                       "mothers","daughter", "queen", "queens", "lady"]

    male_count = functools.reduce(operator.add,
                                   [counter_wrapper(c, name) for name in male_signs_str])
    female_count = functools.reduce(operator.add,
                                   [counter_wrapper(c, name) for name in female_signs_str])

    male_names = [s.lower() for s in names.words('male.txt')]
    female_names = [s.lower() for s in names.words('female.txt')]

    #adding to the signs any appearance of male or female names
    male_count += functools.reduce(operator.add,
                                   [counter_wrapper(c, name) for name in male_names])
    female_count += functools.reduce(operator.add,
                                     [counter_wrapper(c, name) for name in female_names])



    return male_count >= female_count



def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)
