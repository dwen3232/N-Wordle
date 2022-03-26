from collections import Counter
from scipy.stats import entropy
import pickle5 as pickle
from tqdm import tqdm
from utils import guess

# with pickle: 21.9155, without pickle: 109.7440
class Solver:
    """
        find_best_query -> get_result -> update_answers -> repeat
    """
    def __init__(self, pickle_path=None):
        self.answers = []
        self.words = []
        self.table = None

        with open('./answers.txt') as file:
            data = file.read().split('\n')
            self.answers.extend(data)
            self.words.extend(data)

        with open('./words.txt') as file:
            data = file.read().split('\n')
            self.words.extend(data)

        if pickle_path:
            with open(pickle_path, 'rb') as file:
                print('Loading pickle...')
                self.table = pickle.load(file)

        # print(f'length answers: {len(self.answers)}\nlength words: {len(self.words)}')

    def reset(self):
        self.answers = []
        self.words = []
        with open('./answers.txt') as file:
            data = file.read().split('\n')
            self.answers.extend(data)
            self.words.extend(data)

        with open('./words.txt') as file:
            data = file.read().split('\n')
            self.words.extend(data)

    # guess_code: 3-nary integer representing guess results
    # NOTE: logic might not be correct for querys with repeat letters
    def update_answers(self, query, guess_code):
        def is_word_valid(word):
            counter = Counter(word)
            for q, w in zip(query, word):
                r = guess_code % 3
                if r == 0 and q in word:
                    return False
                elif r == 1:
                    if q == w or (q in counter and counter[q] == 0):
                        return False
                    elif q in counter:
                        counter[q] -= 1
                elif r == 2 and q != w:
                    return False
            return True

        self.answers = [w for w in self.answers if (self.table[f'{w},{query}'] == guess_code if self.table else is_word_valid(w))]
        return len(self.answers)

    # find entropy of given query using current possible answers
    def guess_entropy(self, query):
        c = Counter([self.table[f'{answer},{query}'] if self.table else guess(answer, query) for answer in self.answers])
        s = sum(c.values())
        if s == 0:
            return 0
        return entropy([v / s for v in c.values()], base=2)

    # find best query string
    def find_best_query(self):
        if len(self.answers) == 1:
            return self.answers[0]
        max_entropy, best_word = 0, ''
        for word in tqdm(self.words):
            e = self.guess_entropy(word)
            if e > max_entropy:
                max_entropy = e
                best_word = word
        return best_word

    # returns top count pairs of (entropy, word)
    def best_queries(self, count):
        if len(self.answers) == 1:
            return [(0, self.answers[0])]
        # pairs of (entropy, word)
        pairs = [(self.guess_entropy(word), word) for word in tqdm(self.words)]
        return sorted(pairs, key=lambda x: x[0])[-count:]

    def pickle_table(self, output_path):
        d = {}
        for answer in tqdm(self.answers):
            for word in self.words:
                d[f'{answer},{word}'] = guess(answer, word)
        with open(output_path, 'wb') as file:
            print('Pickling table...')
            pickle.dump(d, file)

