from time import time
from collections import deque
from math import sqrt


class ProgressBarBase(object):

    def __init__(self, iterable_or_max, title=None, key=None, autohide=False, quiet=False):
        try:
            # if any iterable given - use it
            self.iterable = iter(iterable_or_max)
            try:
                # if has len - it's the max
                self.max = len(iterable_or_max)
            except TypeError:
                # iterable without len - indeterminate
                self.max = None
        except TypeError:
            # not iterable - assume max is given
            self.iterable = range(iterable_or_max)
            self.max = iterable_or_max

        self.title = title
        self.key = key
        self.autohide = autohide
        self.quiet = quiet

        self.current = None
        self.iter_times = deque(maxlen=100)

    def start(self):
        self.start_time = time()
        self.last_time = time()
        self.current = 0

    def advance(self):
        self.iter_times.append(time() - self.last_time)
        self.last_time = time()
        self.current += 1

    def finish(self):
        if self.autohide:
            self.hide()

    def __iter__(self):
        self.start()
        for elem in self.iterable:
            yield elem
            self.advance()
        self.finish()

    def set_extra_text(self, text):
        self.extra_text = text

    def hide(self):
        pass

    @property
    def frac(self):
        return self.current / self.max

    @property
    def percent(self):
        return self.frac * 100.0

    @property
    def elapsed(self):
        return time() - self.start_time

    @property
    def last_iter_time(self):
        return self.iter_times[-1]

    @property
    def eta_avg(self):
        return (self.max - self.current) * sum(self.iter_times) / len(self.iter_times)

    @property
    def eta_stddev(self):
        mean = sum(self.iter_times) / len(self.iter_times)
        ss = sum((t - mean)**2 for t in self.iter_times)
        return (self.max - self.current) * sqrt(ss / len(self.iter_times))

    def __getitem__(self, key):
        # for % formatting
        try:
            return getattr(self, key)
        except:
            return float('NaN')
