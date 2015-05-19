#encoding: utf-8
from .base import ProgressBarBase
import sys


class ProgressBarTerminal(ProgressBarBase):

    def __init__(self,
                 iterable_or_max,
                 title='Progress', key=None, autohide=False, quiet=False,
                 format_str='%(title)s: %(percent)3d%% [%(bar)s] %(current)d/%(max)d [%(elapsed).1f s] [eta %(eta_avg).0f+-%(eta_stddev).0f s]',
                 width=80):
        super(ProgressBarTerminal, self).__init__(iterable_or_max, title, key, autohide, quiet)
        self.format_strs = format_str.split('%(bar)s')
        self.width = width
        self.quiet = quiet
        self.phases = (' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█')

    def p(self, s=None):
        if not self.quiet:
            if s is None:
                print()
            else:
                print(s, end=' ')

    def print_output(self):
        parts = [format % self for format in self.format_strs]
        parts[1:1] = self.bar(self.width - sum(map(len, parts)))
        self.p( '\r' + ''.join(parts))
        sys.stdout.flush()

    def start(self):
        super(ProgressBarTerminal, self).start()
        self.p()
        self.print_output()

    def advance(self):
        super(ProgressBarTerminal, self).advance()
        self.print_output()

    def finish(self):
        super(ProgressBarTerminal, self).finish()
        if not self.autohide:
            self.p()

    def hide(self):
        super(ProgressBarTerminal, self).hide()
        self.p((' ' * self.width) + '\r')
        sys.stdout.flush()

    def bar(self, bar_width):
        completely_filled = self.current * bar_width // self.max
        phase = (self.current * bar_width * len(self.phases) // self.max) % len(self.phases)

        return (self.phases[-1] * completely_filled +
                (self.phases[phase] if completely_filled < bar_width else '') +
                self.phases[0] * (bar_width - completely_filled))

    def set_extra_text(self, text):
        super(ProgressBarTerminal, self).set_extra_text(text)
