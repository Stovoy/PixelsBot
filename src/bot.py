import argparse
import subprocess
import os
import cStringIO as StringIO

parser = argparse.ArgumentParser(description='Run PixelsBot.')


def device_snapshot():
    data = device_communicate('snapshot')
    print data[:20]


def device_communicate(message):
    """Communicates with the device via device_interface.py.

    Sends a message over stdin.
    Args:
        message: Message to send to device interface.

    Returns: stdout from the device interface.
    """
    working_dir = os.getcwd()
    # TODO: Make this more generic.
    cmd = 'monkeyrunner.bat %s/src/device_interface.py' % working_dir
    process = subprocess.Popen(cmd,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    return process.communicate(message)


if __name__ == '__main__':
    args = parser.parse_args()

    device_snapshot()
