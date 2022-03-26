from time import time
from solver import Solver

def benchmark_solver_pickle_vs_no_pickle1():
    print('~~~PICKLE VS NO PICKLE 1~~~')
    solve1 = Solver(pickle_path='./pickles/table.pickle')
    solve2 = Solver()

    start = time()
    best_queries = solve1.best_queries(5)
    print(len(best_queries), best_queries)
    print(f'time elapsed: {time() - start}')

    start = time()
    best_queries = solve2.best_queries(5)
    print(len(best_queries), best_queries)
    print(f'time elapsed: {time() - start}')

def benchmark_solver_pickle_vs_no_pickle2():
    print('~~~PICKLE VS NO PICKLE 2~~~')
    solve1 = Solver(pickle_path='./pickles/table.pickle')
    solve2 = Solver()

    start = time()
    best_queries = solve1.find_best_query()
    print(best_queries)
    print(f'time elapsed: {time() - start}')

    start = time()
    best_queries = solve2.find_best_query()
    print(best_queries)
    print(f'time elapsed: {time() - start}')

if __name__ == '__main__':
    benchmark_solver_pickle_vs_no_pickle1()
