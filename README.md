# The normal way:

    time python -m scoop scoop_inner.py --haha 1 Hello

We see it takes ~1..2seconds, so it's running in parallel.

    real    0m1.720s
    user    0m2.160s
    sys 0m0.144s

We see how the args after `scoop_inner.py` are nicely parsed by docopt and
forwarded into each process.

    [((0,), {'--haha': True, 'ARGS': ['1', 'Hello']}),
    ((1,), {'--haha': True, 'ARGS': ['1', 'Hello']}),
    [...]

# The wrong way:

`scoop_inner.py` is executable .. what if we just call it without `python -m scoop`?

    time ./scoop_inner.py --haha 1 Hello

We get the warning message, that we need the `-m scoop` and it takes ~5seconds instead of ~1..2seconds.

But the results are correct.

# With a 2nd script:

Now let's try it with a second script ...

    time ./scoop_outer.py

Aha! This just runs like the first script .. but we did not have to use `python -m scoop`


# Combination

Now we wanna try it using just a single script.

But we need to make a difference. If the script is running the first time,
we actually want to start and setup all the scoop stuff,
but when the script is called on the worker nodes, we do not want to start and setup
the scoop stuff **again** .. this would be an endless loop.

So I implemented a function, that should check if we are running the first time
or not.

    time ./scoop_combi.py


# How does it work?

Well the `scoop.launcher.main()` really wants to parse the command line,
but in order to call it out of python code, we want to provide the parameters,
well as function parameters.
So I broke this main out of `scoop.launcher` and threw out all the command line parsing stuff.
Instead I put in all the `**kwargs` with defaults, which are needed.


