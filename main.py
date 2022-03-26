from time import time
from solver import Solver
from utils import base_to_int


def get_guess_code():
    while True:
        try:
            return base_to_int(input())
        except:
            pass


if __name__ == '__main__':
    solve = Solver(pickle_path='./pickles/table.pickle')
    while True:
        while len(solve.answers) != 1:
            # pick from list of best queries
            print(len(solve.answers))
            print('Generating queries...')
            best_queries = solve.best_queries(5)
            print(best_queries)

            # input result from game
            print('Input used query')
            query = input()
            print('Input guess result')
            guess_code = base_to_int(input())


            print('Updating answers...')
            solve.update_answers(query, guess_code)
        solve.reset()
