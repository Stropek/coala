import logging

from coalib.core.Bear import Bear as Bear2
from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.output.printers.LogPrinter import LogPrinterMixin
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL_TO_LOGGING_LEVEL

from pyprint.Printer import Printer


class Bear(Bear2, Printer, LogPrinterMixin):
    """
    **This class is deprecated, please use ``coalib.core.Bear`` instead.**

    A bear contains the actual subroutine that is responsible for checking
    source code for certain specifications. However it can actually do
    whatever it wants with the files it gets. If you are missing some Result
    type, feel free to contact us and/or help us extending the coalib.

    This is the base class for every bear. If you want to write an bear, you
    will probably want to look at the GlobalBear and LocalBear classes that
    inherit from this class. In any case you'll want to overwrite at least the
    run method. You can send debug/warning/error messages through the
    debug(), warn(), err() functions. These will send the
    appropriate messages so that they are outputted. Be aware that if you use
    err(), you are expected to also terminate the bear run-through
    immediately.

    If you need some setup or teardown for your bear, feel free to overwrite
    the set_up() and tear_down() functions. They will be invoked
    before/after every run invocation.

    Settings are available at all times through self.section.

    To indicate which languages your bear supports, just give it the
    ``LANGUAGES`` value which should be a set of string(s):

    >>> class SomeBear(Bear):
    ...     LANGUAGES = {'C', 'CPP','C#', 'D'}

    To indicate the requirements of the bear, assign ``REQUIREMENTS`` a set
    with instances of ``PackageRequirements``.

    >>> class SomeBear(Bear):
    ...     REQUIREMENTS = {
    ...         PackageRequirement('pip', 'coala_decorators', '0.2.1')}

    If your bear uses requirements from a manager we have a subclass from,
    you can use the subclass, such as ``PipRequirement``, without specifying
    manager:

    >>> class SomeBear(Bear):
    ...     REQUIREMENTS = {PipRequirement('coala_decorators', '0.2.1')}

    To specify additional attributes to your bear, use the following:

    >>> class SomeBear(Bear):
    ...     AUTHORS = {'Jon Snow'}
    ...     AUTHORS_EMAILS = {'jon_snow@gmail.com'}
    ...     MAINTAINERS = {'Catelyn Stark'}
    ...     MAINTAINERS_EMAILS = {'catelyn_stark@gmail.com'}
    ...     LICENSE = 'AGPL-3.0'
    ...     ASCIINEMA_URL = 'https://asciinema.org/a/80761'

    If the maintainers are the same as the authors, they can be omitted:

    >>> class SomeBear(Bear):
    ...     AUTHORS = {'Jon Snow'}
    ...     AUTHORS_EMAILS = {'jon_snow@gmail.com'}
    >>> SomeBear.maintainers
    {'Jon Snow'}
    >>> SomeBear.maintainers_emails
    {'jon_snow@gmail.com'}

    If your bear needs to include local files, then specify it giving strings
    containing relative file paths to the INCLUDE_LOCAL_FILES set:

    >>> class SomeBear(Bear):
    ...     INCLUDE_LOCAL_FILES = {'checkstyle.jar', 'google_checks.xml'}

    To keep track easier of what a bear can do, simply tell it to the CAN_FIX
    and the CAN_DETECT sets. Possible values:

    >>> CAN_DETECT = {'Syntax', 'Formatting', 'Security', 'Complexity', 'Smell',
    ... 'Unused Code', 'Redundancy', 'Variable Misuse', 'Spelling',
    ... 'Memory Leak', 'Documentation', 'Duplication', 'Commented Code',
    ... 'Grammar', 'Missing Import', 'Unreachable Code', 'Undefined Element',
    ... 'Code Simplification'}
    >>> CAN_FIX = {'Syntax', ...}

    Specifying something to CAN_FIX makes it obvious that it can be detected
    too, so it may be omitted:

    >>> class SomeBear(Bear):
    ...     CAN_DETECT = {'Syntax', 'Security'}
    ...     CAN_FIX = {'Redundancy'}
    >>> list(sorted(SomeBear.can_detect))
    ['Redundancy', 'Security', 'Syntax']

    Every bear has a data directory which is unique to that particular bear:

    >>> class SomeBear(Bear): pass
    >>> class SomeOtherBear(Bear): pass
    >>> SomeBear.data_dir == SomeOtherBear.data_dir
    False

    BEAR_DEPS contains bear classes that are to be executed before this bear
    gets executed. The results of these bears will then be passed to the
    run method as a dict via the dependency_results argument. The dict
    will have the name of the Bear as key and the list of its results as
    results:

    >>> class SomeBear(Bear): pass
    >>> class SomeOtherBear(Bear):
    ...     BEAR_DEPS = {SomeBear}
    >>> SomeOtherBear.BEAR_DEPS
    {<class 'coalib.bears.Bear.SomeBear'>}
    """
    def __init__(self, *args, **kwargs):
        logging.warning('coalib.bears.Bear is deprecated, please use '
                        'coalib.core.Bear instead.')

        Bear2.__init__(self, *args, **kwargs)
        Printer.__init__(self)

    # TODO Pass dependency results to run if defined in function signature!

    # TODO get_metadata needs to be adjusted to grab signature of run like
    # TODO   before.
    def analyze(self, *args, **kwargs):
        self.run(*args, **kwargs)

    def _print(self, output, **kwargs):
        logging.debug(output)

    def log_message(self, log_message, timestamp=None, **kwargs):
        logging.log(LOG_LEVEL_TO_LOGGING_LEVEL(log_message.log_level),
                    log_message.message)

    def run(self, *args, dependency_results=None, **kwargs):
        raise NotImplementedError
