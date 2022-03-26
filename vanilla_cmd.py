from solvers.vanilla_solver import VanillaSolver
from utils import base_to_int


def get_guess_code():
    while True:
        try:
            return base_to_int(input(), 3)
        except:
            pass


if __name__ == '__main__':
    solve = VanillaSolver(pickle_path='./pickles/table.pickle')
    while True:
        while solve.answers:
            # pick from list of best queries
            print(len(solve.answers))
            print('Generating queries...')
            best_queries = solve.find_best_queries(5)
            print(best_queries)

            # input result from game
            print('Input used query')
            query = input()
            print('Input guess result')
            guess_code = base_to_int(input(), 3)

            print('Updating answers...')
            solve.update_answers(query, guess_code)
        solve.reset()
