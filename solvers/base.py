class SolverBase:
    def __init__(self, answers_path, words_path):
        self.answers_path = answers_path
        self.words_path = words_path

    def reset(self):
        raise NotImplementedError

    def update_answers(self, query, guess_code):
        raise NotImplementedError

    def query_entropy(self, query):
        raise NotImplementedError

    def find_best_query(self):
        raise NotImplementedError

    def find_best_queries(self, count):
        raise NotImplementedError

    def pickle_table(self, output_path):
        raise NotImplementedError
