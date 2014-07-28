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

    def output_change_value(self):
        if self.quiet:
            return
        display_javascript('$("#%(html_id)s > .completed-part").css("width", "%(percent)d%%")' % self, raw=True)
        display_javascript('$("#%(html_id)s > .running-part").css("width", "%(percent_one)d%%")' % self, raw=True)
        display_javascript('$("#%s > .text > .main").text("%s")' % (self.html_id, self.format_str % self), raw=True)

    def start(self):
        super(ProgressBarIPyNb, self).start()
        if not self.quiet:
            display_javascript('$("[data-key=\'%(key)s\']").parent().parent().remove()' % self, raw=True)
            display_html('''
            <style>
                .progress {
                    position: relative;
                }

                .progress > .text {
                    position: absolute;
                    left: 0;
                    width: 100%%;
                    text-align: center;
                }
            </style>

            <h3>%(title)s:</h3>
            <div class="progress progress-striped active" id="%(html_id)s" data-key=%(key)s>
                <div class="bar bar-success completed-part" style="width: 0%%;"></div>
                <div class="bar bar-warning running-part" style="width: 100%%;"></div>
                <div class="text">
                    <span class="main">Starting...</span>
                    <span class="extra"></span>
                </div>
            </div>
            ''' % self, raw=True)
        self.output_change_value()

    def advance(self):
        super(ProgressBarIPyNb, self).advance()
        self.output_change_value()

    def finish(self):
        super(ProgressBarIPyNb, self).finish()
        display_javascript('$("#%s").removeClass("progress-striped active")' % self.html_id, raw=True)

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
