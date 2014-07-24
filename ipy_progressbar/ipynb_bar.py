from .common import ProgressBarBase
import uuid
from IPython.display import display_html, display_javascript


CSS_STYLE = '''
progress {
    position: relative;
    width: 100%%;
    height: 25px;
    -webkit-appearance: none;
    margin-top: 10px;
}
progress::-webkit-progress-bar {
    background: #555;
    -moz-border-radius: 25px;
    -webkit-border-radius: 25px;
    border-radius: 25px;
    padding: 4px;
    -webkit-box-shadow: inset 0 -1px 1px rgba(255,255,255,0.3);
    -moz-box-shadow   : inset 0 -1px 1px rgba(255,255,255,0.3);
    box-shadow        : inset 0 -1px 1px rgba(255,255,255,0.3);
}
progress::-webkit-progress-value {
    border-radius: 20px 8px 8px 20px;
    background-color: rgb(43,194,83);
    background-image: -webkit-gradient(
      linear,
      left bottom,
      left top,
      color-stop(0, rgb(43,194,83)),
      color-stop(1, rgb(84,240,84))
     );
    background-image: -webkit-linear-gradient(
      center bottom,
      rgb(43,194,83) 37%%,
      rgb(84,240,84) 69%%
     );
    -webkit-box-shadow:
      inset 0 2px 9px  rgba(255,255,255,0.3),
      inset 0 -2px 6px rgba(0,0,0,0.4);
    height: 100%%;
    overflow: hidden;
    display: block;
}
progress.completing::-webkit-progress-value {
    border-radius: 20px;
}
progress:before {
    content: attr(data-text) attr(data-ext-text);
    position: absolute;
    left: 0;
    width: 100%%;
    text-align: center;
    line-height: 25px;
    text-shadow: 1px 1px 5px rgba(255, 255, 255, 0.7), 1px -1px 5px rgba(255, 255, 255, 0.7), -1px 1px 5px rgba(255, 255, 255, 0.7), -1px -1px 5px rgba(255, 255, 255, 0.7);
}
'''


class ProgressBarIPyNb(ProgressBarBase):

    html_ids = {}

    display_html('<style>%s</style>' % CSS_STYLE, raw=True)

    def __init__(self,
                 iterable_or_max,
                 title='Progress', key=None, autohide=False, quiet=False,
                 format_str='%(current)d/%(max)d (%(percent)d%%) in %(elapsed).1f s, %(last_iter_time).2f s last iter; eta %(eta_byall).0f s (%(eta_byone).0f s)'):
        super(ProgressBarIPyNb, self).__init__(iterable_or_max, title, key, autohide, quiet)
        self.format_str = format_str

        if key is None:
            self.html_id = 'a' + str(uuid.uuid4())
        else:
            if key not in ProgressBarIPyNb.html_ids:
                ProgressBarIPyNb.html_ids[key] = 'a' + str(uuid.uuid4())
            self.html_id = ProgressBarIPyNb.html_ids[key]

    def output_change_value(self):
        if self.quiet:
            return
        display_javascript('$("progress#%(html_id)s").val("%(current)d")' % self, raw=True)
        display_javascript('$("progress#%s").attr("data-text", "%s")' % (self.html_id, self.format_str % self), raw=True)
        if self.frac > 0.996:
            display_javascript('$("progress#%s").addClass("completing")' % self.html_id, raw=True)
        else:
            display_javascript('$("progress#%s").removeClass("completing")' % self.html_id, raw=True)

    def start(self):
        super(ProgressBarIPyNb, self).start()
        if not self.quiet:
            display_html('''
            <h3>%(title)s:</h3>
            <progress
                value="%(current)d" max="%(max)d"
                id="%(html_id)s"
                data-text="Starting..."
                data-ext-text="">
            </progress>
            ''' % self, raw=True)
            display_javascript('$("progress#%s").parent().parent().slice(0, -1).hide()' % self.html_id, raw=True)
        self.output_change_value()

    def advance(self):
        super(ProgressBarIPyNb, self).advance()
        self.output_change_value()

    def finish(self):
        super(ProgressBarIPyNb, self).finish()

    def hide(self):
        super(ProgressBarIPyNb, self).hide()
        if self.quiet:
            return
        display_javascript('$("progress#%s").parent().parent().hide()' % self.html_id, raw=True)

    def set_extra_text(self, text):
        super(ProgressBarIPyNb, self).set_extra_text(text)
        if self.quiet:
            return
        display_javascript('$("progress#%s").attr("data-ext-text", " |||| %s")' % (self.html_id, text), raw=True)
