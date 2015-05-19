from .terminal_bar import ProgressBarTerminal
try:
    from .ipynb_bar import ProgressBarIPyNb
except ImportError:
    pass


def ProgressBar(iterable_or_max,
                title='Progress', key=None, autohide=False, quiet=False,
                format_str_ipynb='%(current)d/%(max)d (%(percent)d%%) in %(elapsed).1f s, %(last_iter_time).2f s last iter; eta %(eta_avg).0f+-%(eta_stddev).0f s',
                format_str_term='%(title)s: %(percent)3d%% [%(bar)s] %(current)d/%(max)d [%(elapsed).1f s] [eta %(eta_avg).0f+-%(eta_stddev).0f s]',
                width_term=80):
    if in_ipynb():
        return ProgressBarIPyNb(iterable_or_max, title, key, autohide, quiet, format_str_ipynb)
    else:
        return ProgressBarTerminal(iterable_or_max, title, key, autohide, quiet, format_str_term, width_term)


def in_ipynb():
    try:
        cfg = get_ipython().config
        # if cfg['IPKernelApp']['parent_appname'] == 'ipython-notebook':
            # return True
        # else:
            # return False
        return True
    except NameError:
        return False
