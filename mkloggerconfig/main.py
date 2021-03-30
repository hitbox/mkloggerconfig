import argparse
import configparser
import inspect
import logging.config
import logging.handlers
import sys
import textwrap

from . import model

def join(i, joinstr=', '):
    return joinstr.join(map(str, i))

def main(argv=None):
    """
    """
    parser = argparse.ArgumentParser(
        description = main.__doc__,
        prog = 'mkloggerconfig',
    )
    args = parser.parse_args(argv)

    loggingconfig = model.minimalconfig()
    print(loggingconfig.status())


# below is somewhat minimal copy of sliderepl
# it is probably what this will use for interactively creating a logging config file.
import argparse
import code
import inspect
import sys

try:
    import readline
    import rlcompleter
except ImportError:
    readline = None

environ = None

class Repl:
    expose = ('status', 'commands')

    _exec_on_return = False

    def __init__(self):
        self._expose_map = dict(
            (f'!{name}', getattr(self, name)) for name in self.expose)
        self._expose_map['?'] = self.commands

    def commands(self):
        for cmd in self.expose:
            print(cmd)

    def status(self):
        print('** STATUS **')

    @classmethod
    def run(cls):
        instance = cls()

        console = code.InteractiveConsole()
        global environ
        environ = console.locals

        console.raw_input = instance.readfunc
        if readline:
            readline.parse_and_bind('tab: complete')
            readline.set_completer(rlcompleter.Completer(environ).complete)

        console.interact()
        sys.exit(0)

    @property
    def ps1(self):
        return getattr(sys, 'ps1', '>>> ')

    @property
    def ps2(self):
        return getattr(sys, 'ps2', '... ')

    def readfunc(self, prompt=''):
        if self._exec_on_return:
            prompt = '\n[press return to run code]'

        line = input(prompt)

        if self._exec_on_return or prompt == self.ps1:
            tokens = line.split()
            if line == '':
                tokens = ['!status']

            self._exec_on_return = False
            if (
                tokens
                and (tokens[0].startswith('!') or tokens[0] == '?')
                and tokens[0] in self._expose_map
            ):
                fn = self._expose_map[tokens[0]]
                signature = inspect.signature(fn)
                if len(tokens) - 1 != len(signature.parameters):
                    print('usage: %s %s'
                          % (tokens[0], ' '.join(list(signature.parameters)[1:])))
                else:
                    fn(*tokens[1:])
                return ''
        return line


# example of starting the repl
#repl = Repl()
#repl.run()
