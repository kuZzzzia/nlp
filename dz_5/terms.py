import re
import pymorphy3
import math

EMPTY_STRING = r''
WORD_REGEX = r'\b((?:[a-zа-я]+)(?:(?:[-\'][a-zа-я]+)*))\b'

def read_file(file_name):
    f = open(file_name, 'r')
    return f.read()

word_regex = re.compile(WORD_REGEX)
morph = pymorphy3.MorphAnalyzer(lang='ru')

def extract_words(text):
    return word_regex.findall(text.lower())

def count_frequency(words):
    freq_dict = {}
    for item in words:
        if (item in freq_dict):
            freq_dict[item] += 1
        else:
            freq_dict[item] = 1
    return freq_dict

def to_string_dict_sorted(dict):
    str = EMPTY_STRING
    for v, k in sorted( ((v,k) for k,v in dict.items()), reverse=True):
        str += f'{k},{v}\n'
    return str

def save_dict_to_file(dict, file_name):
    f = open(file_name, "w")
    f.write(to_string_dict_sorted(dict))
    f.close()


def main():
    text = read_file('./dz_5/philosophy.txt')
    words = [ morph.parse(w)[0] for w in extract_words(text) ]
    terms = []
    for i in range(1, len(words)):
        if 'NOUN' in words[i].tag and 'ADJF' in words[i-1].tag:
            terms.append((words[i-1].normal_form, words[i].normal_form))

    freq_dict = count_frequency([word.normal_form for word in words])
    term_freq = count_frequency(terms)
    mi_dict = {}
    for term, freq in term_freq.items():
        mi_dict[term] = math.log2(freq * len(freq_dict) / freq_dict[term[0]] / freq_dict[term[1]])
    save_dict_to_file(term_freq, './dz_5/terms_frequency.csv')
    save_dict_to_file(mi_dict, './dz_5/terms_mutual_information.csv')
     

if __name__ == '__main__':
    main()