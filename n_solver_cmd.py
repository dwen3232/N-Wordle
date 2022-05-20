from solvers.n_solver import NSolver
from utils import base_to_int


def get_guess_code():
    while True:
        try:
            return base_to_int(input(), 3)
        except:
            pass


if __name__ == '__main__':
    N = 4
    solve = NSolver(N, pickle_path='./pickles/table.pickle')
    while True:
        while any(answer for answer in solve.n_answers):
            # pick from list of best queries
            print([len(answers) for answers in solve.n_answers])
            print('Generating queries...')
            best_queries = solve.find_best_queries(5)
            print(best_queries)

            # input result from game
            print('Input used query')
            query = input()
            guess_codes = []
            for i in range(4):
                print(f'Input guess result {i}')
                guess_codes.append(base_to_int(input(), 3))

            print('Updating answers...')
            solve.update_answers(query, guess_codes)
        solve.reset()
