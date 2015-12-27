from time import time
from .base import ProgressBarBase
import ipywidgets as iw
from traitlets import directional_link
from IPython.display import display


class ProgressBarIPyNb(ProgressBarBase):
    def __init__(self,
                 iterable_or_max,
                 title='',
                 format_str='%(current)d/%(max)d (%(percent)d%%) in %(elapsed).1f s, %(last_iter_time).2f s last iter; eta %(eta_avg).0f+-%(eta_stddev).0f s'):
        super(ProgressBarIPyNb, self).__init__(iterable_or_max, title)
        self.format_str = format_str

        self.progress_w = iw.FloatProgress(min=0, max=100, value=30, width='100%')
        self.title_w = iw.HTML('<h3 style="display: inline">%(title)s</h3>&nbsp;' % self)
        self.info_w = iw.HTML()

        self.log_check_w = iw.Checkbox(value=False, visible=False, description='Show Log')
        self.log_w = iw.HTML()
        self.log_header_w = iw.HTML('<h2><small>Log messages</small></h2>')
        directional_link((self.log_check_w, 'value'), (self.log_w, 'visible'))
        directional_link((self.log_check_w, 'value'), (self.log_header_w, 'visible'))

        self.container_w = iw.VBox([iw.HBox([self.title_w, self.info_w]),
                                    iw.HBox([self.progress_w, self.log_check_w]),
                                    self.log_header_w, self.log_w,
                                    iw.HBox(height=20)])

        self.displayed = False

    def display_update(self):
        self.progress_w.value = self.percent
        self.info_w.value = '<h3 style="display: inline"><small>%s</small></h3>' % (self.format_str % self)

    def start(self):
        super(ProgressBarIPyNb, self).start()
        if not self.displayed:
            self.displayed = True
            display(self.container_w)
        self.display_update()

    def finish(self):
        super(ProgressBarIPyNb, self).finish()
        self.display_update()

    def log_message(self, text):
        super(ProgressBarIPyNb, self).log_message(text)
        if len(self.log_messages) == 1:
            # first message
            self.log_check_w.visible = True
            self.log_check_w.value = True

        self.log_w.value = '<br/>'.join(self.log_messages)

    set_extra_text = log_message

    @property
    def percent_one(self):
        return 100.0 / self.max
