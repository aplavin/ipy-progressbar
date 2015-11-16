from time import time
from .base import ProgressBarBase
import uuid
from IPython.display import display_html, display_javascript


class ProgressBarIPyNb(ProgressBarBase):

    def __init__(self,
                 iterable_or_max,
                 title='Progress', key=None, autohide=False, quiet=False,
                 format_str='%(current)d/%(max)d (%(percent)d%%) in %(elapsed).1f s, %(last_iter_time).2f s last iter; eta %(eta_avg).0f+-%(eta_stddev).0f s'):
        super(ProgressBarIPyNb, self).__init__(iterable_or_max, title, key, autohide, quiet)
        self.format_str = format_str
        self.key = key
        self.html_id = 'a' + str(uuid.uuid4())

    def output_change_value(self, force=True):
        if force or time() - getattr(self, 'last_print_time', 0) > 0.5:
            self.last_print_time = time()
        else:
            return

        if self.quiet:
            return
        display_javascript('$("#%(html_id)s > .completed-part").css("width", "%(percent)f%%")' % self, raw=True)
        display_javascript('$("#%(html_id)s > .running-part").css("width", "%(percent_one)f%%")' % self, raw=True)
        display_javascript('$("#%s > .text > .main").text("%s")' % (self.html_id, self.format_str % self), raw=True)

    def start(self):
        super(ProgressBarIPyNb, self).start()
        if not self.quiet:
            display_javascript('$("[data-key=\'%(key)s\']").parent().parent().remove()' % self, raw=True)
            display_html('''
            <style>
                .progress {
                    text-align:center;
                }

                .progress > .progress-bar {
                    transition-property: none;
                }

                .progress > .text {
                    position: absolute;
                    right: 0;
                    left: 0;
                }
            </style>

            <h3>%(title)s:</h3>

            <div class="progress" id="%(html_id)s" data-key="%(key)s">
                <div class="progress-bar progress-bar-success completed-part" style="width: 0%%"></div>
                <div class="progress-bar progress-bar-warning running-part" style="width: 100%%"></div>
                <span class="text">
                    <span class="main">Starting...</span>
                    <span class="extra"></span>
                </span>
            </div>
            ''' % self, raw=True)
        self.output_change_value()

    def advance(self):
        super(ProgressBarIPyNb, self).advance()
        self.output_change_value()

    def finish(self):
        super(ProgressBarIPyNb, self).finish()
        self.output_change_value(force=True)

    def hide(self):
        super(ProgressBarIPyNb, self).hide()
        if self.quiet:
            return
        display_javascript('$("#%s").parent().parent().hide()' % self.html_id, raw=True)

    def set_extra_text(self, text):
        super(ProgressBarIPyNb, self).set_extra_text(text)
        if self.quiet:
            return
        display_javascript('$("#%s > .text > .extra").text("|||| %s")' % (self.html_id, text), raw=True)

    @property
    def percent_one(self):
        return 100.0 / self.max
