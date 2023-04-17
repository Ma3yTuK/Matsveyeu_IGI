import re

from zmq import Enum

BEFORE_RE = r'(?<![^\s])'
BEFORE_WORD_RE = r'(?<![^\s\"\(])'

AFTER_END_RE = r'(?=\s*$)'
AFTER_ANY_RE = r'(?=\s+[^\s])'
AFTER_WORD_END_RE = r'(?=[\.\,\:\!\?\"\)\s]*$)'
AFTER_WORD_UPPER_RE = r'(?=[\.\,\:\!\?\"\)]*\s+[A-B])'
AFTER_WORD_LOWER_RE = r'(?=[\.\,\:\!\?\"\)]*\s+[^\sA-B])'

FORMAT_PARAMETERS_RE = dict(
    br=BEFORE_RE,
    bwr=BEFORE_WORD_RE, 
    aer=AFTER_END_RE, 
    aar=AFTER_ANY_RE, 
    awer=AFTER_WORD_END_RE,
    awur=AFTER_WORD_UPPER_RE,
    awlr=AFTER_WORD_LOWER_RE, 
)

WORD_ENDS_RE_LIST = [
    r'{bwr}(?i:etc\.)({awer}|{awur})',
    r'{bwr}(?i:i\.e\.)({awer}|{awur})',
    r'{bwr}(?i:e\.g\.)({awer}|{awur})',
    r'{bwr}(?i:c\.)({awer}|{awur})',
    r'{bwr}(?i:et\sal\.)({awer}|{awur})',
    r'{bwr}Dr\.{awer}',
    r'{bwr}Mr\.{awer}',
    r'{bwr}Mrs\.{awer}',
    r'{bwr}Lt\.{awer}',
    r'{bwr}Rep\.{awer}',
    r'{bwr}Jan\.({awer}|{awur})',
    r'{bwr}Feb\.({awer}|{awur})',
    r'{bwr}Mar\.({awer}|{awur})',
    r'{bwr}Apr\.({awer}|{awur})',
    r'{bwr}Aug\.({awer}|{awur})',
    r'{bwr}Sept\.({awer}|{awur})',
    r'{bwr}Oct\.({awer}|{awur})',
    r'{bwr}Nov\.({awer}|{awur})',
    r'{bwr}Dec\.({awer}|{awur})',
    r'{bwr}\.\s\.\s\.({awer}|{awur})'
]

WORD_OMISS_RE_LIST = [
    r'{bwr}(?i:etc\.){awlr}',
    r'{bwr}(?i:i\.e\.){awlr}',
    r'{bwr}(?i:e\.g\.){awlr}',
    r'{bwr}(?i:c\.){awlr}',
    r'{bwr}(?i:et al\.){awlr}',
    r'{bwr}Dr\.({awlr}|{awur})',
    r'{bwr}Mr\.({awlr}|{awur})',
    r'{bwr}Mrs\.({awlr}|{awur})',
    r'{bwr}Lt\.({awlr}|{awur})',
    r'{bwr}Rep\.({awlr}|{awur})',
    r'{bwr}([A-Z]\.\s+)*[A-Z]\.({awlr}|{awur})',
    r'{bwr}Jan\.{awlr}',
    r'{bwr}Feb\.{awlr}',
    r'{bwr}Mar\.{awlr}',
    r'{bwr}Apr\.{awlr}',
    r'{bwr}Aug\.{awlr}',
    r'{bwr}Sept\.{awlr}',
    r'{bwr}Oct\.{awlr}',
    r'{bwr}Nov\.{awlr}',
    r'{bwr}Dec\.{awlr}',
    r'{bwr}\.\s\.\s\.{awlr}'
]

def list_to_re(re_list):
    return '(' + '|'.join(re_list).format(**FORMAT_PARAMETERS_RE) + ')'

def find_matches(regex, text, capture_group):
    match_list = list()

    for m in re.finditer(regex, text):

        if m[capture_group] != None:
            match_list.append(m[capture_group])

    return match_list

def raw_words(text):
    raw_word_re = r'{bwr}[^\.\,\:\!\?\"\)\(\s]+({awer}|{awlr}|{awur})'.format(**FORMAT_PARAMETERS_RE)
    return find_matches(raw_word_re, text, 0)

def words(text):
    word_group = 'wg'
    word_re = r'({0}|{1})|(?P<{2}>{bwr}[a-zA-Z][a-zA-Z0-9\']*({awer}|{awlr}|{awur}))'.format(list_to_re(WORD_ENDS_RE_LIST), list_to_re(WORD_OMISS_RE_LIST), word_group, **FORMAT_PARAMETERS_RE)
    return find_matches(word_re, text, word_group)

def sentences(text):
    sentence_re = r'{br}({0}|[^\.\!\?])+[\.\!\?][\.\!\?\"\)]*'.format(list_to_re(WORD_OMISS_RE_LIST), **FORMAT_PARAMETERS_RE)
    return find_matches(sentence_re, text, 0)

def non_declarative_sentences(text):
    non_declarative_sentence_re = r'{br}({0}|[^\.\!\?])+[\!\?][\.\!\?\"\)]*'.format(list_to_re(WORD_OMISS_RE_LIST), **FORMAT_PARAMETERS_RE)
    return find_matches(non_declarative_sentence_re, text, 0)

def sentence_count(text):
    return len(sentences(text))

def non_declarative_sentence_count(text):
    return len(non_declarative_sentences(text))

def avg_sentence_length(text):
    characters_count = 0
    sentence_list = sentences(text)

    for sentence in sentence_list:
        word_list = words(sentence)

        for word in word_list:
            characters_count += len(word)

    try:
        return characters_count/len(sentence_list)
    except:
        return 0

def avg_word_length(text):
    characters_count = 0
    word_list = words(text)

    for word in word_list:
        characters_count += len(word)

    try:
        return characters_count/len(word_list)
    except:
        return 0

def top_n_grams(text: str, n):
    raw_word_list = raw_words(text.lower())
    n_gram_list = list()

    for i in range(len(raw_word_list)+1-n):
        n_gram_list.append(raw_word_list[i:i+n])

    n_gram_dict = dict()

    for n_gram in n_gram_list:
        n_gram_dict[' '.join(n_gram)] = n_gram_list.count(n_gram)
        
    return sorted(n_gram_dict.items(), key=lambda x:x[1], reverse=True)