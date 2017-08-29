import os
import sys
import logging
import traceback
from threading import Thread

# Local imports
from scoop import utils
from scoop.launcher import ScoopApp
from scoop.fallbacks import ensureScoopStartedProperly


def is_scoop_started_properly():
    try:
        return ensureScoopStartedProperly(lambda : True)()
    except:
        return False


def scoop_main(**kwargs):

    # Get a list of resources to launch worker(s) on
    hosts = utils.getHosts(
        kwargs.get('hostfile', None),
        kwargs.get('hosts', None)
    )
    num_workers = kwargs.get('num_workers', utils.getWorkerQte(hosts))
    assert num_workers > 0, (
        "Scoop couldn't determine the number of worker to start.\n"
        "Use the 'num_workers=<int>' to set it manually.")

    thisScoopApp = ScoopApp(
        hosts,
        num_workers,
        kwargs.get('num_brokers', 1),
        kwargs.get('verbose', 1),
        kwargs.get('python_interpreter', [sys.executable]),
        kwargs.get('external_hostname', [utils.externalHostname(hosts)])[0],
        kwargs['executable'],
        kwargs.get('args', []),
        kwargs.get('--tunnel', False),
        kwargs.get('path', os.getcwd()),
        kwargs.get('--debug', False),
        kwargs.get('--nice', 0),
        utils.getEnv(),
        kwargs.get('--profile', False),
        kwargs.get('pythonpath', [os.environ.get('PYTHONPATH', '')])[0],
        kwargs.get('prolog', [None])[0],
        kwargs.get('backend', 'ZMQ'),
    )

    rootTaskExitCode = False
    interruptPreventer = Thread(target=thisScoopApp.close)
    try:
        rootTaskExitCode = thisScoopApp.run()
    except Exception as e:
        logging.error('Error while launching SCOOP subprocesses:')
        logging.error(traceback.format_exc())
        rootTaskExitCode = -1
    finally:
        # This should not be interrupted (ie. by a KeyboadInterrupt)
        # The only cross-platform way to do it I found was by using a thread.
        interruptPreventer.start()
        interruptPreventer.join()

    # Exit with the proper exit code
    if rootTaskExitCode:
        sys.exit(rootTaskExitCode)
