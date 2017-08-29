#!/usr/bin/env python
"""
Usage:
    scoop_inner.py [options] [ARGS ...]

Options:
    --haha   a good laugh
"""
from docopt import docopt
from scoop import futures
import time
from functools import partial
from pprint import pprint

data = range(5)


def func_takes_some_time(*args, **kwargs):
    time.sleep(1)
    return (args, kwargs)

if __name__ == "__main__":
    args = docopt(__doc__)
    func = partial(func_takes_some_time, **args)
    pprint(list(futures.map(func, data)))
