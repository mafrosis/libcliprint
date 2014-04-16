import datetime
import sys


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

    ERROR = 'ERROR'
    DEBUG = 'DEBUG'
    DEPLOY = 'DEPLOY'
    DNS = 'DNS'
    HIGHSTATE = 'HIGHSTATE'
    REBOOT = 'REBOOT'
    RIAK = 'RIAK'
    SALT = 'SALT'
    SALTCLOUD = 'SALTCLOUD'
    TEST = 'TESTS'
    ELB = 'ELB'
    GRAINS = 'GRAINS'
    EC2 = 'EC2'
    PILLAR = 'PILLAR'

    def __init__(self, start, quiet=False):
        self.start = start
        self.quiet = quiet
        self.progress_running = False

    def _get_colour_and_prefix(self, mode=None, success=None):
        colour = self.WHITE

        if mode == self.ERROR:
            prefix = 'ERROR'
            colour = self.RED
        elif mode == self.DEBUG:
            prefix = 'DEBUG'
            colour = self.GREY
        elif mode is None:
            prefix = 'DEPLOY'
        else:
            prefix = mode

        if success is True:
            colour = self.GREEN
        elif success is False:
            prefix = 'ERROR'
            colour = self.RED

        return colour, prefix

    def p(self, msg, mode=None, notime=False, success=None, extra=None):
        if self.progress_running:
            self.progress_running = False
            sys.stdout.write('\n')

        # setup for print
        colour, prefix = self._get_colour_and_prefix(mode, success=success)

        # default stdout
        out = sys.stdout

        if success is False:
            out = sys.stderr

        if self.quiet is True:
            return

        if notime is True:
            out.write('{}[{: <10}]          {}{}{}\n'.format(
                CliPrinter.YELLOW, prefix, colour, msg, CliPrinter.END
            ))
        else:
            t = self._get_time_elapsed()
            out.write('{}[{: <10}]{} {: >4} {}{}{}\n'.format(
                CliPrinter.YELLOW, prefix, CliPrinter.GREY, t, colour, msg, CliPrinter.END
            ))

        if extra is not None:
            out.write('{}\n'.format(extra))

    def progress(self, amount, mode):
        if self.quiet is True:
            return

        self.progress_running = True
        colour, prefix = self._get_colour_and_prefix(mode)

        t = self._get_time_elapsed()
        sys.stdout.write('\r{}[{: <10}]{} {: >4} {}{}{}'.format(
            CliPrinter.YELLOW, prefix, CliPrinter.GREY, t, colour, (amount * '.'), CliPrinter.END
        ))
        sys.stdout.flush()

    def _get_time_elapsed(self, formatted=True):
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