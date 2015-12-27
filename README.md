Introduction
============

ipy-progressbar allows to use the same code for rich progressbars in IPython Notebooks, and for simple fallback ones in terminal sessions.


Example
=======

Code like this:

```python
from ipy_progressbar import ProgressBar

pb = ProgressBar(10, title='Outer')
pb_inner = ProgressBar(5, title='Inner')
for i in pb:)
    for j in pb_inner:
        # inner loop body
```

will work both in IPython Notebook and in plain console. When run in notebook, the output will be rich (Bootstrap progress bars), while console version is mainly thought of as a fallback.

For more examples see `example.py` and `example.ipynb`.

