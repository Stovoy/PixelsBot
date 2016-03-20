import os
import pexpect
import pexpect.popen_spawn
import sys

import ui

_process = None

READY = 'ready> '


def device_click():
    """Makes a click on the device."""
    device_communicate('click')


def device_communicate(message):
    """Communicates with the device via device_interface.py.

    Sends a message over stdin.
    Args:
        message: Message to send to device interface.
    """
    global _process
    if not _process:
        _start_communication()

    print 'Sending command: %s' % message
    _process.sendline(message)
    wait_ready()


def _start_communication():
    """Starts communication via device_interface.py"""
    print 'Make sure your Android phone is connected and given USB debug permissions.'
    working_dir = os.getcwd()
    # TODO: Make this more generic.
    cmd = ['monkeyrunner.bat',  '%s\src\device_interface.py' % working_dir]
    global _process
    _process = pexpect.popen_spawn.PopenSpawn(cmd)
    wait_ready()


def wait_ready():
    global _process
    print 'Waiting for %s...' % READY
    _process.expect(READY)


if __name__ == '__main__':
    # device_click()

    ui.start()
