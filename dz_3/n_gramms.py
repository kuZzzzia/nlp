import re
import math
import matplotlib.pyplot as plt 
import numpy as np

EMPTY_STRING = r''
WORD_REGEX = r'\b([a-zа-я]+)\b'
word_regex = re.compile(WORD_REGEX)

learn_text = '''
Вот дом,
Который построил Джек.

А это пшеница,
Которая в тёмном чулане хранится
В доме,
Который построил Джек.

А это весёлая птица-синица,
Которая часто ворует пшеницу,
Которая в тёмном чулане хранится
В доме,
Который построил Джек.
'''

test_text = '''
Вот кот,
Который пугает и ловит синицу,
Которая часто ворует пшеницу,
Которая в тёмном чулане хранится
В доме,
Который построил Джек.
'''

# 1. Достаем словарь из learn и test
# 2. Считаем разбиваем на униграммы и биграммы (для биграмм нужно породить все возможные пары)
# 3. На основе обучающего множества посчитать вероятности
# 4. После того как посчитали вероятности посчитать перплексию для каждого варианта

def extract_words(text):
    return word_regex.findall(text.lower())

def make_vocabulary(texts):
    voc = set()
    for text in texts:
        for word in text:
            voc.add(word)
    return list(voc)

def make_unigram_bigram_models(voc, text, alpha = 1.0):
    uni = {}
    
    for word in voc:
        uni[word] = 0.0
    for word in text:
        uni[word] += 1
    
    bi = {}
    for word_head in voc:
        for word_tail in voc:
            bi[(word_head, word_tail)] = alpha
    for i in range(len(text)):
        if i == 0:
            continue
        bi[(text[i],text[i-1])] += 1
    for (head, tail) in bi:
        bi[(head, tail)] /= uni[tail] + alpha * len(voc)

    for word in voc:
        uni[word] += alpha

    for word in uni:
        uni[word] /= len(text) + alpha * len(voc)
    
    return uni, bi

def count_uni_perplexion(uni_prob, text):
    pp = 0.0
    for word in text:
        pp += math.log2(uni_prob[word])
    return 2 ** (- pp / len(text))

def count_bi_perplexion(bi_prob, text):
    pp = 0.0
    for i in range(len(text)):
        if i == 0:
            continue
        pp += math.log2(bi_prob[(text[i],text[i-1])])
    return 2 ** (- pp / (len(text) - 1))

def tune_hyperparameter(voc, learn_words, test_words):
    alpha = 0.001
    uni_perp, bi_perp, alphas = [], [], []
    for t in range(1, 5_001):
        uni, bi = make_unigram_bigram_models(voc, learn_words, alpha*t)
        alphas.append(alpha*t)
        uni_perp.append(count_uni_perplexion(uni, test_words))
        bi_perp.append(count_bi_perplexion(bi, test_words))
    return uni_perp, bi_perp, alphas


def plot_results(u_plot, b_plot, x_plot):
    plt.plot(x_plot, u_plot, label = "Униграммы") 
    plt.plot(x_plot, b_plot, label = "Биграммы") 
    
    plt.xlabel('alpha') 
    plt.ylabel('Перплексия') 
    
    plt.title('Подбор гипермараметра') 

    plt.legend() 
    
    plt.show() 


def main():
    learn_words = extract_words(learn_text)
    test_words = extract_words(test_text)
    
    voc = make_vocabulary([learn_words, test_words])

    uni_perp, bi_perp, alphas = tune_hyperparameter(voc, learn_words, test_words)

    print(f'Минимальная перплексия для униграмм = {min(uni_perp)} при \\alpha = {alphas[np.argmin(uni_perp, axis=0)]}')
    print(f'Минимальная перплексия для биграмм = {min(bi_perp)} при \\alpha = {alphas[np.argmin(bi_perp, axis=0)]}')

    plot_results(uni_perp, bi_perp, alphas)
        

if __name__ == '__main__':
    main()