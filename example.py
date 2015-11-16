from ipy_progressbar.terminal_bar import ProgressBarTerminal
from ipy_progressbar import ProgressBar
from time import sleep
from random import random

# both should work:
pb = ProgressBarTerminal(5)
for i in pb:
    sleep(0.5 * random())

pb = ProgressBar(5)
for i in pb:
    sleep(0.5 * random())


# output throttling
for i in ProgressBar(10000):
    sleep(0.0005 * random())


# nested
pb = ProgressBar(5, title='Outer', key='outer')
for i in pb:
    pb_inner = ProgressBar(5, title='Inner', key='inner')
    for j in pb_inner:
        sleep(0.5 * random())
