import datetime
import sys

PROGBAR_LEN = 40


class CliPrinter:
    WHITE = '\033[97m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    GREY = '\033[90m'
    END = '\033[0m'

    DEFAULT = 'MESSAGE'
    ERROR = 'ERROR'
    DEBUG = 'DEBUG'

    def __init__(self, start=None, progressbar_len=PROGBAR_LEN, progressbar_char="#"):
        self.start = start
        self.progressbar_len = progressbar_len
        self.progressbar_char = progressbar_char

        # used internally for tracking state
        self.progress_running = False
        self.line_needs_finishing = False

    def _get_colour_and_prefix(self, mode=None, success=None):
        colour = self.WHITE

        if mode == self.ERROR:
            prefix = 'ERROR'
            colour = self.RED
        elif mode == self.DEBUG:
            prefix = 'DEBUG'
            colour = self.GREY
        elif mode is None:
            prefix = self.DEFAULT
        else:
            prefix = mode

        if success is True:
            colour = self.GREEN
        elif success is False:
            prefix = 'ERROR'
            colour = self.RED

        return colour, prefix

    def p(self, msg, mode=None, notime=False, success=None, extra=None, nonl=False):
        if self.start is None:
            notime = True

        if self.progress_running or self.line_needs_finishing:
            self.progress_running = False
            self.line_needs_finishing = False
            sys.stdout.write('\n')

        # setup for print
        colour, prefix = self._get_colour_and_prefix(mode, success=success)

        # default stdout
        out = sys.stdout

        if success is False:
            out = sys.stderr

        t = self._get_time_elapsed(notime)
        out.write('{}[{: <10}]{} {: >4} {}{}{}'.format(
            CliPrinter.YELLOW, prefix, CliPrinter.GREY, t, colour, msg, CliPrinter.END
        ))

        if extra is not None:
            out.write('{}\n'.format(extra))

        if nonl is True:
            self.line_needs_finishing = True
        else:
            out.write('\n')


    def progressi(self, amount, mode=None):
        self.progress_running = True
        colour, prefix = self._get_colour_and_prefix(mode)

        self.progress_running = True

        t = self._get_time_elapsed()
        sys.stdout.write('\r{}[{: <10}]{} {: >4} {}{}{}'.format(
            CliPrinter.YELLOW, prefix, CliPrinter.GREY, t, colour,
            (amount * self.progressbar_char),
            CliPrinter.END
        ))
        sys.stdout.flush()


    def progressf(self, num_blocks, block_size, total_size):
        self.progress_running = True

        colour, prefix = self._get_colour_and_prefix(None)

        # calculate progress bar size
        progress = float(num_blocks * block_size) / float(total_size)
        progress = progress if progress < 1 else 1

        t = self._get_time_elapsed()
        sys.stdout.write('\r{}[{: <10}]{} {: >4} {}[{}{}] {}%{}'.format(
            CliPrinter.YELLOW, prefix, CliPrinter.GREY, t, colour,
            self.progressbar_char * int(progress * self.progressbar_len),
            ' ' * (self.progressbar_len - int(progress * self.progressbar_len)),
            round(progress * 100, 1),
            CliPrinter.END
        ))
        sys.stdout.flush()


    def _get_time_elapsed(self, notime=False, formatted=True):
        if notime is True or self.start is None:
            return ' ' * 8

        ts = datetime.datetime.now() - self.start
        if formatted is True:
            formatted_ts = '{:02}:{:02}:{:02}'.format(
                ts.seconds // 3600,
                ts.seconds % 3600 // 60,
                ts.seconds % 60
            )
            return formatted_ts
        else:
            return ts


class DummyPrinter:
    def e(self, msg, mode=None, excp=None, notime=False):
        pass

    def p(self, msg, mode=None, notime=False, success=None, extra=None, nonl=False):
        pass

    def progressi(self, amount, mode=None):
        pass

    def progressf(self, num_blocks, block_size, total_size):
        pass
