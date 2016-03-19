import argparse
import os
import pexpect
import sys


parser = argparse.ArgumentParser(description='Run PixelsBot.')

_process = None

OUTPUT_START = '<output start>\r\n'
OUTPUT_DONE = '<output done>\r\n'
READY = 'ready> '


def device_snapshot():
    """Takes a snapshot."""
    data = device_communicate('snapshot')
    prefix = 'array(\'b\', '
    if not data.startswith(prefix):
        print 'Could not parse snapshot data.'
    else:
        print len(data[len(prefix):])


def device_communicate(message):
    """Communicates with the device via device_interface.py.

    Sends a message over stdin.
    Args:
        message: Message to send to device interface.

    Returns: stdout from the device interface.
    """
    global _process
    if not _process:
        _start_communication()

    print 'Sending command: %s' % message
    _process.sendline(message)
    print 'Waiting for %s...' % OUTPUT_START
    _process.expect(OUTPUT_START)
    print 'Waiting for %s...' % OUTPUT_DONE
    _process.expect(OUTPUT_DONE)
    output = _process.before
    print 'Waiting for %s...' % READY
    _process.expect(READY)
    return output


def _start_communication():
    """Starts communication via device_interface.py"""
    working_dir = os.getcwd()
    # TODO: Make this more generic.
    cmd = 'monkeyrunner %s/src/device_interface.py' % working_dir
    global _process
    _process = pexpect.spawn(cmd)
    print 'Waiting for ready...'
    _process.expect(READY)


if __name__ == '__main__':
    args = parser.parse_args()

    device_snapshot()
    device_snapshot()
    device_snapshot()
    device_snapshot()
