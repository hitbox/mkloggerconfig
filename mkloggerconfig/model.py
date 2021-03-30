import logging

class BaseConf:
    """
    """

    def __str__(self):
        return self.name

    @property
    def level_name(self):
        return logging._levelToName[self.level]


class LoggerConf(BaseConf):

    def __init__(
            self,
            name = None,
            level = None,
            handlers = None,
            propagate = True,
    ):
        self.name = name
        self.level = level
        if handlers is None:
            handlers = []
        self.handlers = handlers
        self.propagate = propagate

    def status(self):
        errors = []
        if not self.handlers:
            errors.append(f'{self.name} has no handlers')
        return errors


class HandlerConf(BaseConf):

    def __init__(
            self,
            name,
            class_ = None,
            level = None,
            formatter = None,
            args = None,
            kwargs = None,
    ):
        self.name = name
        self.class_ = class_
        self.level = level
        self.formatter = formatter
        self.args = args
        self.kwargs = kwargs

    def status(self):
        pass


class FormatterConf(BaseConf):
    """
    """

    def __init__(self,
            name,
            format_ = None,
            datefmt = None,
            style = '%',
            validate = True,
    ):
        self.name = name
        self.format_ = format_
        self.datefmt = datefmt
        self.style = style
        self.validate = validate

    def status(self):
        errors = []
        if self.style not in logging._STYLES:
            errors.append('Invalid style')
        return errors


class LoggingConfig:
    """
    """

    def __init__(self, loggers=None, handlers=None, formatters=None):
        if loggers is None:
            loggers = []
        self.loggers = loggers
        if handlers is None:
            handlers = []
        self.handlers = handlers
        if formatters is None:
            formatters = []
        self.formatters = formatters

    def status(self):
        """
        """
        errors = []

        if not self.loggers:
            errors.append('No loggers')
        else:
            for logger in self.loggers:
                if logger.name == 'root':
                    break
            else:
                errors.append('No root logger')

            for logger in self.loggers:
                _errors = logger.status()
                if _errors:
                    errors.extend(_errors)

        if not self.handlers:
            errors.append('No handlers')
        else:
            for handler in self.handlers:
                _errors = handler.status()
                if _errors:
                    errors.extend(_errors)

        if not self.formatters:
            errors.append('No formatters')
        else:
            for formatter in self.formatters:
                _errors = formatter.status()
                if _errors:
                    errors.extend(_errors)

        return errors


def minimalconfig():
    formatter = FormatterConf('basic', format_=logging.BASIC_FORMAT)
    handler = HandlerConf(
        'notset',
        level = logging.NOTSET,
        formatter = formatter
    )
    return LoggingConfig(
        loggers = [
            LoggerConf(
                name = 'root',
                level = logging.NOTSET,
                handlers = [handler],
            )
        ],
        handlers = [handler],
        formatters = [formatter]
    )
