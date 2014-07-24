from ipy_progressbar.terminal_bar import ProgressBarTerminal
from time import sleep

pb = ProgressBarTerminal(80, title='Outer')
for i in pb:
    pb_inner = ProgressBarTerminal(80, title='Inner')
    for j in pb_inner:
        sleep(0.05)
