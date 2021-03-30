import inspect
import logging.config
import logging.handlers

from .model import LoggerConf

_empty = object()

def prompt(
        message,
        choices = None,
        default = _empty,
        error_message = None,
        exclude = None,
        required = True,
        type_ = None,
    ):
    if error_message is None:
        error_message = 'Invalid input'
    if required:
        message += f' (required)'
    if default is not _empty:
        message += f' [{default!r}] '
    if not message.endswith(' '):
        message += ' '
    if type_ is None:
        type_ = str
    def print_choices():
        print(f'{list(map(str, choices))!r}')
    while True:
        answer = input(message).strip()
        if answer == '':
            if required and default is _empty:
                print(f'{error_message}: required')
                if choices:
                    print_choices()
                continue
            else:
                answer = default
        if choices and answer not in choices:
            print(f'{error_message}: not in choices')
            print_choices()
        if exclude and answer in exclude:
            print(f'{error_message}: excluded')
        return type_(answer)

def prompt_logger(config):
    loggerconf = LoggerConf()
    print('Add logger')

    loggerconf.name = prompt('Name:', default='logging.handlers.RotatingFileHandler')
    class_ = logging.config._resolve(name)
    sig = inspect.signature(class_)

    loggerconf.level = prompt('Level:', choices=list(logging._nameToLevel))
    loggerconf.level = logging._nameToLevel[loggerconf.level]
    loggerconf.propagate = prompt('Propagate:', choices=[True,False], default=True)

    while not loggerconf.handlers:
        msg = ['Add', 'handler']
        if not loggerconf.handlers:
            msg.insert(1, 'another')
        prompt(' '.join(msg))

    print(sig)
    answers = dict()
    for parameter in sig.parameters.values():
        if parameter.default is inspect._empty:
            default = _empty
            type_ = None
            required = True
        elif parameter.default is not None:
            default = parameter.default
            type_ = type(default)
            required = False
        else:
            default = _empty
            type_ = None
            required = False
        answer = prompt(parameter.name, default=default, required=required, type_=type_)
        answers[parameter.name] = answer
    boundarguments = sig.bind(**answers)

    loggerconf.args = boundarguments.args
    loggerconf.kwargs = boundarguments.kwargs

    return loggerconf


