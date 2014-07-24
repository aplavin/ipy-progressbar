from ipy_progressbar.terminal_bar import ProgressBarTerminal
from ipy_progressbar import ProgressBar
from time import sleep
from random import random

# both should work:

pb = ProgressBarTerminal(5, title='Outer', key='outer')
for i in pb:
    pb_inner = ProgressBarTerminal(5, title='Inner', key='inner')
    for j in pb_inner:
        sleep(0.5 * random())
        # pb.set_extra_text('inner: %d' % j)


pb = ProgressBar(5, title='Outer', key='outer')
for i in pb:
    pb_inner = ProgressBar(5, title='Inner', key='inner')
    for j in pb_inner:
        sleep(0.5 * random())
        # pb.set_extra_text('inner: %d' % j)
