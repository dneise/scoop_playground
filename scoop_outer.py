#!/usr/bin/env python
from scoop_main import scoop_main
from datetime import datetime
if __name__ == "__main__":
    scoop_main(
        executable='scoop_inner.py',
        args=[1, "Hello", '--haha']
    )
