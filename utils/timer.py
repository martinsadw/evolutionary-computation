import time


class Timer:
    def __init__(self):
        self.init_time()

    def init_time(self):
        self.time_dict = {}
        self.iterations_dict = {}
        self.iterations = 0
        self.last_time = time.process_time()

    def add_time(self, name=None):
        if (name is not None):
            if (name not in self.time_dict):
                self.time_dict[name] = 0
                self.iterations_dict[name] = 0

            self.time_dict[name] += time.process_time() - self.last_time
            self.iterations_dict[name] += 1

        self.last_time = time.process_time()

    def get_time(self):
        result = [name + ": " + str(duration) + "s" for (name, duration) in self.time_dict.items()]

        return result

    def get_iteration_time(self):
        result = [name + ": " + str(duration / self.iterations_dict[name]) + "s" for (name, duration) in self.time_dict.items()]

        return result

    def get_iterations(self):
        result = [name + ": " + str(iterations) for (name, iterations) in self.iterations_dict.items()]

        return result

    # NOTE(andre:2018-07-17): Devido a limitação de precisão do tempo, essa função é muito imprecisa
    def get_total_time(self):
        result = 0
        for time in self.time_dict.values():
            result += time

        return result
