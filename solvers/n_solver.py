import os
from collections import Counter
from scipy.stats import entropy
import pickle5 as pickle
from tqdm import tqdm

from solvers.base import SolverBase
from utils import guess, is_guess_valid, base_to_int


class NSolver(SolverBase):
    def __init__(self, N=2, pickle_path=None, answers_path='./answers.txt', words_path='./words.txt'):
        super().__init__(answers_path, words_path)
        self.N = N
        self.n_answers = []

        self.answers = []
        self.words = []

        with open(self.answers_path) as file:
            data = file.read().split('\n')
            self.answers.extend(data)
            self.words.extend(data)

        with open(self.words_path) as file:
            data = file.read().split('\n')
            self.words.extend(data)

        self.n_answers = [self.answers.copy() for i in range(N)]

        if pickle_path:
            # pickle table if no pickle exists
            if not os.path.exists(pickle_path):
                self.pickle_table(pickle_path)

            with open(pickle_path, 'rb') as file:
                print('Loading pickle...')
                self.table = pickle.load(file)

    def reset(self):
        self.n_answers = [self.answers.copy() for i in range(N)]

    # update answers using array guess_codes.  Must be that len(guess_codes) == N
    def update_answers(self, query, guess_codes):
        assert len(guess_codes) == self.N
        for i, answers in enumerate(self.n_answers):
            if guess_codes[i] == base_to_int('22222', 3):
                self.n_answers[i] = []
            else:
                self.n_answers[i] = [w for w in self.answers if
                                     (self.table[f'{w},{query}'] == guess_codes[i] if self.table
                                      else is_guess_valid(w, query, guess_codes[i]))]
        return [len(answers) for answers in self.n_answers]

    # returns arr of entropies
    def query_entropy(self, query):
        def single_entropy(answers):
            c = Counter(
                [self.table[f'{a},{query}'] if self.table else guess(a, query) for a in answers])
            s = sum(c.values())
            if s == 0:
                return 0
            return entropy([v / s for v in c.values()], base=2)
        return [single_entropy(answers) for answers in self.n_answers]

    def find_best_query(self):
        # this might not be optimal
        if all(len(answers) == 1 for answers in self.n_answers):
            return [answers[0] for answers in self.n_answers]
        max_entropy, best_word = 0, ''
        for word in tqdm(self.words):
            e = sum(self.query_entropy(word))
            if e > max_entropy:
                max_entropy = e
                best_word = word
        return best_word

    def find_best_queries(self, count):
        if all(len(answers) == 1 for answers in self.n_answers):
            return [(0, answers[0]) for answers in self.n_answers]
        # pairs of (entropy, word)
        pairs = [(sum(self.query_entropy(word)), word) for word in tqdm(self.words)]
        return sorted(pairs, key=lambda x: x[0])[-count:]

    def pickle_table(self, output_path):
        pass
