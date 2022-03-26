import os
from collections import Counter
from scipy.stats import entropy
import pickle5 as pickle
from tqdm import tqdm

from solvers.base import SolverBase
from utils import guess, is_guess_valid, base_to_int


# with pickle: 21.9155, without pickle: 109.7440
class VanillaSolver(SolverBase):
    """
        find_best_query -> get_result -> update_answers -> repeat
    """

    def __init__(self, pickle_path=None, answers_path='./answers.txt', words_path='./words.txt'):
        super().__init__(answers_path, words_path)
        self.answers = []
        self.words = []
        self.table = None

        with open(self.answers_path) as file:
            data = file.read().split('\n')
            self.answers.extend(data)
            self.words.extend(data)

        with open(self.words_path) as file:
            data = file.read().split('\n')
            self.words.extend(data)

        if pickle_path:
            # pickle table if no pickle exists
            if not os.path.exists(pickle_path):
                self.pickle_table(pickle_path)

            with open(pickle_path, 'rb') as file:
                print('Loading pickle...')
                self.table = pickle.load(file)

        # print(f'length answers: {len(self.answers)}\nlength words: {len(self.words)}')

    # resets the game
    def reset(self):
        self.answers = []
        with open(self.answers_path) as file:
            data = file.read().split('\n')
            self.answers.extend(data)

    # guess_code: 3-nary integer representing guess results
    # NOTE: logic might not be correct for queries with repeat letters
    def update_answers(self, query, guess_code):
        if guess_code == base_to_int('22222', 3):
            self.answers = []
            return

        self.answers = [w for w in self.answers if
                        (self.table[f'{w},{query}'] == guess_code if self.table
                         else is_guess_valid(w, query, guess_code))]
        return len(self.answers)

    # find entropy of given query using current possible answers
    def query_entropy(self, query):
        c = Counter(
            [self.table[f'{answer},{query}'] if self.table else guess(answer, query) for answer in self.answers])
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
            e = self.query_entropy(word)
            if e > max_entropy:
                max_entropy = e
                best_word = word
        return best_word

    # returns top count pairs of (entropy, word)
    def find_best_queries(self, count):
        if len(self.answers) == 1:
            return [(0, self.answers[0])]
        # pairs of (entropy, word)
        pairs = [(self.query_entropy(word), word) for word in tqdm(self.words)]
        # returns (1st, 2nd, 3rd,..., n-th) best words
        return sorted(pairs, key=lambda x: x[0])[-1:-count-1:-1]

    # pickles table
    def pickle_table(self, output_path):
        d = {}
        for answer in tqdm(self.answers):
            for word in self.words:
                d[f'{answer},{word}'] = guess(answer, word)
        with open(output_path, 'wb') as file:
            print('Pickling table...')
            pickle.dump(d, file)
