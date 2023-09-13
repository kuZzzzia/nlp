import re

EMPTY_STRING = r''
WORD_REGEX = r'\b((?:[a-zа-я]+)(?:(?:[-\'][a-zа-я]+)*))\b'

def read_file(file_name):
    f = open(file_name, 'r')
    return f.read()

word_regex = re.compile(WORD_REGEX)

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
    text = read_file('./dz_1/dostoevski_igrok.txt')
    words = extract_words(text)
    freq_dict = count_frequency(words)
    save_dict_to_file(freq_dict, './dz_1/frequency_dict.csv')
     

if __name__ == '__main__':
    main()