from ipy_progressbar.terminal_bar import ProgressBarTerminal
from time import sleep

pb = ProgressBarTerminal(80)
for i in pb:
    sleep(0.2)
