import pandas as pd
from tqdm import tqdm
from random import sample

from solvers.vanilla_solver import VanillaSolver
from solvers.n_solver import NSolver
from utils import guess


def random_sampler(all_possible_answers, N, count):
    for _ in range(count):
        yield sample(all_possible_answers, N)


# distribution of number of turns: {4: 1298, 3: 894, 2: 22, 5: 99, 6: 2}
if __name__ == '__main__':
    N = 2
    d = {}

    solve = NSolver(N, pickle_path='./pickles/table.pickle')
    all_possible_answers = solve.answers

    # answer is N-tuple of unique answers
    for answers in random_sampler(all_possible_answers, N, len(all_possible_answers)):
        turn = 0
        while any(solve.n_answers):
            # get best query
            best_query = solve.find_best_query() if turn else 'soare' # use 'soare' since its always the best first pick
            # compute resultant guess code
            guess_codes = [guess(answers[i], best_query) for i in range(N)]
            # update answers set
            solve.update_answers(best_query, guess_codes)

            turn += 1

        for i in range(N):
            col = f'answer_{i}'
            d[col] = d.get(col, []) + [answers[i]]
        d['num_turns'] = d.get('num_turns', []) + [turn]
        solve.reset()
        print(f'{answers} finished in {turn} turns')

    df = pd.DataFrame(d)
    df.to_csv(f'./turns-{N}.csv', index=False)

    print(d)






