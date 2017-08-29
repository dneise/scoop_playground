#!/usr/bin/env python
"""
Usage:
    scoop_combi.py [options] [ARGS ...]

Options:
    --haha   a good laugh
"""
import time
from docopt import docopt
from functools import partial
from pprint import pprint

from scoop import futures
from scoop_main import scoop_main, is_scoop_started_properly

data = range(5)


def func_takes_some_time(*args, **kwargs):
    time.sleep(1)
    return (args, kwargs)


if __name__ == "__main__":
    if is_scoop_started_properly():
        args = docopt(__doc__)
        func = partial(func_takes_some_time, **args)
        pprint(list(futures.map(func, data)))
    else:
        scoop_main(
            executable=__file__,
            args=[1, "Hello", '--haha']
        )
